"""Demo HTTP/MySQL/Zeebe aislada, sin mocks ni seed destructivo.

Ejecutar desde backend; instrucciones en docs/validacion_mvp.md.
La URL administrativa se lee de VOCALIS_TEST_MYSQL_ADMIN_URL, nunca se imprime.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import uuid

import httpx
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))


async def run(args):
    admin_url = make_url(os.environ['VOCALIS_TEST_MYSQL_ADMIN_URL'])
    if admin_url.get_backend_name() != 'mysql':
        raise ValueError('Esta validación requiere MySQL real')
    # Nunca aceptar el nombre de una BD existente como destino.
    database = 'vocalis_demo_' + uuid.uuid4().hex
    output = Path(tempfile.mkdtemp(prefix='vocalis-demo-'))
    os.chmod(output, 0o700)
    checks = []

    def check(name, condition, evidence=None):
        entry = {'check': name, 'passed': bool(condition), 'evidence': evidence}
        checks.append(entry)
        (output / 'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2))
        print(json.dumps(entry, ensure_ascii=False), flush=True)

    # Cortar únicamente el broker rotulado y publicado en el puerto indicado.
    if args.zeebe_container:
        info = json.loads(subprocess.check_output(['docker', 'inspect', args.zeebe_container]))[0]
        assert info['Config']['Labels'].get('vocalis.validation') == 'true'
        ports = info['NetworkSettings']['Ports']['26500/tcp']
        assert args.gateway in [f"127.0.0.1:{p['HostPort']}" for p in ports]

    admin = create_async_engine(admin_url)
    engine = None
    process = None
    channel = None
    stopped = False
    created = False
    try:
        async with admin.begin() as conn:
            version = await conn.scalar(text('SELECT VERSION()'))
            check('MySQL 8', version.startswith('8.0.'), version)
            await conn.execute(text(f'CREATE DATABASE `{database}` CHARACTER SET utf8mb4'))
            created = True
        environment = {
            'DATABASE_URL': admin_url.set(database=database).render_as_string(hide_password=False),
            'ZEEBE_GATEWAY': args.gateway,
            'JWT_SECRET': secrets.token_urlsafe(48),
            'ORIENTADOR_REGISTRATION_CODE': secrets.token_urlsafe(24),
            'PYTHONDONTWRITEBYTECODE': '1',
        }
        os.environ.update(environment)
        # Sólo contiene secretos de esta demo; nunca añadir al repositorio.
        (output / 'environment.json').write_text(json.dumps(environment, indent=2))
        os.chmod(output / 'environment.json', 0o600)
        from app.database import Base, engine as app_engine, async_session_maker
        from app.models import Pregunta
        from app.seed import PREGUNTAS
        from pyzeebe import ZeebeClient, create_insecure_channel
        engine = app_engine
        # Las revisiones existentes no son una migración inicial completa.
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        migration = await asyncio.to_thread(subprocess.run,
            [sys.executable, '-B', '-m', 'alembic', 'upgrade', 'head'],
            cwd=BACKEND, capture_output=True, text=True)
        (output / 'migrations.log').write_text(migration.stdout + migration.stderr)
        check('Migraciones aplicadas en BD vacía inicializada', migration.returncode == 0)
        if migration.returncode:
            raise RuntimeError('No se pudo migrar la BD de demo')
        async with async_session_maker() as db:
            db.add_all(Pregunta(id=i, orden=i, texto=t, dimension=d, es_invertida=r)
                       for i, t, d, r in PREGUNTAS)
            await db.commit()
            revision = await db.scalar(text('SELECT version_num FROM alembic_version'))
            check('Revisión actual', revision == '20260924_bpm_outbox', revision)

        channel = create_insecure_channel(grpc_address=args.gateway)
        client = ZeebeClient(channel)
        deadline = time.monotonic() + 90
        while True:
            try:
                topology = await asyncio.wait_for(client.topology(), 5)
                break
            except Exception:
                if time.monotonic() >= deadline:
                    raise RuntimeError('Zeebe no disponible en 90 segundos') from None
                await asyncio.sleep(2)
        (output / 'topology.txt').write_text(str(topology))
        deployment = await asyncio.wait_for(client.deploy_resource(
            BACKEND.parent / 'bpmn/evaluacion-vocacional.bpmn'), 20)
        (output / 'deployment.txt').write_text(str(deployment))
        check('BPMN original desplegado en Zeebe real', True)

        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        base = f'http://127.0.0.1:{port}'
        (output / 'runtime.json').write_text(json.dumps({'database': database, 'base_url': base}))
        app_module = 'app.main:app'
        extra = []
        if args.diagnose_worker:
            # Registrar y relanzar, sin alterar el comportamiento del worker.
            (output / 'diagnostic_app.py').write_text(
                'import logging\nfrom app import main\napp = main.app\n'
                'original = main.start_worker\n'
                'async def observed():\n'
                '    try:\n        await original()\n'
                '    except Exception:\n'
                '        logging.exception("validation_worker_failed")\n        raise\n'
                'main.start_worker = observed\n')
            app_module = 'diagnostic_app:app'
            extra = ['--app-dir', str(output)]
        if args.reload:
            extra += ['--reload', '--reload-dir', str(BACKEND / 'app')]
        with (output / 'backend.log').open('w') as log:
            process = subprocess.Popen([sys.executable, '-B', '-m', 'uvicorn', app_module,
                                        '--host', '127.0.0.1', '--port', str(port), '--loop', args.loop, *extra],
                                       cwd=BACKEND, stdout=log, stderr=log)
        async with httpx.AsyncClient(base_url=base, timeout=30) as http:
            for _ in range(60):
                try:
                    if (await http.get('/')).status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                if process.poll() is not None:
                    raise RuntimeError('FastAPI no arrancó; revisar backend.log')
                await asyncio.sleep(1)
            else:
                raise RuntimeError('Timeout al iniciar FastAPI')

            async def request(method, path, token=None, payload=None, status=200):
                response = await http.request(method, '/api' + path,
                    headers={'Authorization': f'Bearer {token}'} if token else {}, json=payload)
                if response.status_code != status:
                    # No registrar bodies de login ni tokens.
                    raise AssertionError(f'{method} {path}: {response.status_code}, esperado {status}')
                return response.json()

            password = secrets.token_urlsafe(20)
            async def account(name, role, school):
                email = f'{name}@example.com'
                body = dict(email=email, password=password, nombre_completo=name,
                            role=role, establecimiento=school)
                if role == 'orientador':
                    body['codigo_verificacion'] = environment['ORIENTADOR_REGISTRATION_CODE']
                else:
                    body.update(nivel='4° Medio', letra='A', fecha_nacimiento='2009-01-15')
                await request('POST', '/auth/register', payload=body)
                result = await request('POST', '/auth/login', payload={'email': email, 'password': password})
                return result['access_token']

            ori = await account('Orientador', 'orientador', 'Demo')
            other_ori = await account('OrientadorAjeno', 'orientador', 'Otro')
            student = await account('Estudiante', 'estudiante', 'Demo')
            other = await account('EstudianteAjeno', 'estudiante', 'Otro')
            check('Registro y login de ambos roles', True)
            rows = await request('GET', '/orientador/estudiantes', ori)
            student_id = rows[0]['id']
            check('Curso asociado únicamente al orientador correcto',
                  len(rows) == 1 and rows[0]['name'] == 'Estudiante' and rows[0]['course'] == '4° Medio A')
            check('Sin evaluación al registrarse', not (await request('GET', '/evaluacion/estado', student))['tiene_evaluacion'])
            questions = await request('GET', '/evaluacion/preguntas')
            check('Banco BFI-44', [q['id'] for q in questions] == list(range(1, 45)))
            answers = [{'preguntaId': i, 'valor': 3} for i in range(1, 45)]
            for answer in answers[:20]:
                await request('POST', '/evaluacion/respuesta', student, answer)
            # Nuevo login; recuperar el borrador desde MySQL, sin usar estado de una vista.
            student = (await request('POST', '/auth/login', payload={
                'email': 'Estudiante@example.com', 'password': password}))['access_token']
            saved = await request('GET', '/evaluacion/respuestas', student)
            check('Reanudación parcial desde MySQL', [(r['preguntaId'], r['valor']) for r in saved] == [(i, 3) for i in range(1, 21)])
            for answer in answers[20:]:
                await request('POST', '/evaluacion/respuesta', student, answer)
            check('Recuperación de las 44 respuestas', len(await request('GET', '/evaluacion/respuestas', student)) == 44)
            async with engine.connect() as conn:
                key = await conn.scalar(text('SELECT process_instance_key FROM proceso_bpm WHERE evaluacion_id=1'))
                check('Instancia real persistida antes del envío', bool(key), key)
            check('Estado inicial del estudiante', (await request('GET', '/evaluacion/estado', student))['bpm_estado'] == 'registro')
            result = await request('POST', '/evaluacion/enviar', student, {'respuestas': answers})
            report_id = result['reportId']
            report = await request('GET', '/evaluacion/reporte', student)
            by_id = await request('GET', f'/evaluacion/reporte/{report_id}', student)
            counselor_report = await request('GET', f'/orientador/estudiante/{student_id}/reporte', ori)
            check('Contrato idéntico en tres endpoints autorizados', report == by_id == counselor_report)
            check('OCEAN neutral calculado desde 44 respuestas', report['scores'] == {d: .5 for d in 'OCEAN'})
            check('Cinco dimensiones sin área inventada', len(report['dimensions']) == 5 and report['careerAreas'] == [])
            await request('GET', f'/evaluacion/reporte/{report_id}', other, status=404)
            await request('GET', f'/orientador/estudiante/{student_id}/reporte', other_ori, status=403)
            check('Reportes ajenos bloqueados para ambos roles', True)
            await request('POST', '/evaluacion/enviar', student, {'respuestas': answers}, status=400)
            await request('POST', '/evaluacion/respuesta', student, answers[0], status=400)
            check('Reenvío y edición completada bloqueados', True)

            async def wait_bpm(token, label):
                observed = []
                deadline = time.monotonic() + args.wait_seconds
                while time.monotonic() < deadline:
                    state = (await request('GET', '/evaluacion/estado', token))['bpm_estado']
                    if not observed or state != observed[-1]:
                        observed.append(state)
                    if state == 'reporte_listo':
                        break
                    await asyncio.sleep(.25)
                check(label, observed[-1] == 'reporte_listo', observed)

            await wait_bpm(student, 'Avance real Zeebe hasta reporte_listo')
            rows = await request('GET', '/orientador/estudiantes', ori)
            check('Endpoint del panel orientador refleja reporte_listo', rows[0]['bpm_estado'] == 'reporte_listo', rows[0]['bpm_estado'])
            state = await request('GET', '/evaluacion/estado', student)
            check('Fechas reales de cierre y reporte', bool(state['evaluacion_fecha'] and state['reporte_fecha']))

            if args.zeebe_container:
                recovery = await account('Recuperacion', 'estudiante', 'Demo')
                # Iniciar la instancia con broker disponible; después caer antes de publicar.
                await request('POST', '/evaluacion/respuesta', recovery, answers[0])
                await asyncio.to_thread(subprocess.run, ['docker', 'stop', '-t', '10', args.zeebe_container], check=True, capture_output=True)
                stopped = True
                await request('POST', '/evaluacion/enviar', recovery, {'respuestas': answers})
                check('Reporte consultable con Zeebe caído', (await request('GET', '/evaluacion/reporte', recovery))['scores'] == report['scores'])
                async with engine.connect() as conn:
                    pending = (await conn.execute(text("SELECT estado, ultimo_error FROM bpm_evento WHERE evaluacion_id=2 AND tipo='completar'"))).mappings().one()
                    check('Fallo real de broker deja evento recuperable', pending['estado'] == 'pendiente', dict(pending))
                await asyncio.to_thread(subprocess.run, ['docker', 'start', args.zeebe_container], check=True, capture_output=True)
                stopped = False
                await wait_bpm(recovery, 'Reintento automático tras recuperar Zeebe')
                async with engine.connect() as conn:
                    event_state = await conn.scalar(text("SELECT estado FROM bpm_evento WHERE evaluacion_id=2 AND tipo='completar'"))
                    check('Publicación recuperada después de la caída', event_state in ('enviado', 'consumido'), event_state)
            else:
                checks.append({'check': 'Caída real de Zeebe', 'skipped': True, 'reason': 'Sin contenedor exclusivo autorizado'})

            async with engine.connect() as conn:
                evaluations = (await conn.execute(text('SELECT estudiante_id, COUNT(*) n FROM evaluacion GROUP BY estudiante_id'))).mappings().all()
                check('Una evaluación por estudiante tras reanudar y reenviar', all(r['n'] == 1 for r in evaluations), [dict(r) for r in evaluations])
                events = (await conn.execute(text('SELECT evaluacion_id,tipo,estado,intentos,ultimo_error FROM bpm_evento ORDER BY id'))).mappings().all()
                (output / 'events.json').write_text(json.dumps([dict(r) for r in events], indent=2))
            # Credenciales sintéticas para continuar manualmente sólo con --keep-db.
            (output / 'accounts.json').write_text(json.dumps({'password': password, 'emails': ['Estudiante@example.com', 'Orientador@example.com']}, indent=2))
    except Exception as exc:
        check('Ejecución integral', False, f'{type(exc).__name__}: {exc}')
        raise
    finally:
        if stopped:
            await asyncio.to_thread(subprocess.run, ['docker', 'start', args.zeebe_container], check=True, capture_output=True)
        if process:
            process.terminate()
            await asyncio.to_thread(process.wait, timeout=20)
        if channel:
            await channel.close()
        if engine:
            await engine.dispose()
        if created and not args.keep_db:
            async with admin.begin() as conn:
                await conn.execute(text(f'DROP DATABASE `{database}`'))
        await admin.dispose()
        (output / 'checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2))
        print(f'ARTIFACTS {output}; DB {database}; retained={args.keep_db}', flush=True)
    return 1 if any(c.get('passed') is False for c in checks) else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reload', action='store_true', help='Arranque de desarrollo usado por Docker Compose')
    parser.add_argument('--loop', choices=['auto', 'asyncio', 'uvloop'], default='auto')
    parser.add_argument('--gateway', default='127.0.0.1:27650')
    parser.add_argument('--zeebe-container', help='Debe tener label vocalis.validation=true')
    parser.add_argument('--wait-seconds', type=int, default=90)
    parser.add_argument('--keep-db', action='store_true', help='Conservar únicamente la BD nueva de esta ejecución para demo manual')
    parser.add_argument('--diagnose-worker', action='store_true', help='Registrar y relanzar excepciones del worker')
    raise SystemExit(asyncio.run(run(parser.parse_args())))
