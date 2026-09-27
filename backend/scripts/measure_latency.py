"""Carga HTTP de 30 usuarios sintéticos; sólo en una demo aislada.

No mide renderizado, tiempo humano ni finalización BPM. No reutiliza evaluaciones.
Genera muestras JSON sin contraseñas/tokens y percentiles por operación.
"""
import argparse
import asyncio
from collections import Counter
import json
import math
from pathlib import Path
import secrets
import time
from urllib.parse import urlparse
import uuid

import httpx


def percentile(values, fraction):
    ordered = sorted(values)
    return round(ordered[max(0, math.ceil(len(ordered) * fraction) - 1)], 2) if ordered else None


async def run(args):
    if urlparse(args.base_url).hostname not in ('localhost', '127.0.0.1'):
        raise ValueError('Sólo se permite una API de demo local')
    if not args.isolated_demo:
        raise ValueError('Confirma --isolated-demo: se crearán usuarios y evaluaciones sintéticas')
    run_id = uuid.uuid4().hex
    samples = []
    barrier = asyncio.Barrier(args.users)
    started = time.perf_counter()

    async def user(index):
        async with httpx.AsyncClient(base_url=args.base_url.rstrip('/') + '/api/', timeout=args.timeout) as client:
            # Calentamiento sin datos: excluido de las muestras.
            for _ in range(3):
                (await client.get('evaluacion/preguntas')).raise_for_status()
            await barrier.wait()

            async def measured(operation, method, path, payload=None):
                before = time.perf_counter()
                status, error = None, None
                response = None
                try:
                    response = await client.request(method, path, json=payload)
                    status = response.status_code
                    if status != 200:
                        error = f'HTTP {status}'
                except httpx.HTTPError as exc:
                    error = type(exc).__name__
                samples.append(dict(user=index, operation=operation,
                    started_s=round(before - started, 6),
                    ms=round((time.perf_counter() - before) * 1000, 3), status=status, error=error))
                if error:
                    return None
                return response.json()

            email = f'load-{run_id}-{index}@example.com'
            password = secrets.token_urlsafe(18)
            registered = await measured('registro', 'POST', 'auth/register', dict(
                email=email, password=password, nombre_completo=f'Carga {index}',
                role='estudiante', establecimiento=f'Carga {run_id}',
                nivel='4° Medio', letra='A', fecha_nacimiento='2009-01-15'))
            if registered is None:
                return False
            login = await measured('login', 'POST', 'auth/login', dict(email=email, password=password))
            if login is None:
                return False
            client.headers['Authorization'] = 'Bearer ' + login['access_token']
            answers = [dict(preguntaId=i, valor=3) for i in range(1, 45)]
            for i, answer in enumerate(answers, 1):
                if await measured('guardar', 'POST', 'evaluacion/respuesta', answer) is None:
                    return False
                if i == 20:
                    saved = await measured('reanudar', 'GET', 'evaluacion/respuestas')
                    if saved is None or len(saved) != 20:
                        return False
                if args.think_seconds:
                    await asyncio.sleep(args.think_seconds)
            result = await measured('enviar', 'POST', 'evaluacion/enviar', {'respuestas': answers})
            if result is None:
                return False
            report = await measured('reporte', 'GET', 'evaluacion/reporte')
            state = await measured('estado', 'GET', 'evaluacion/estado')
            return bool(report and report.get('scores') == {d: .5 for d in 'OCEAN'}
                        and state and state.get('estado') == 'completada')

    # Un fallo de preparación cancela la barrera; no dejar a otros usuarios colgados.
    tasks = [asyncio.create_task(user(i)) for i in range(args.users)]
    try:
        completed = await asyncio.wait_for(asyncio.gather(*tasks), args.deadline)
    except Exception:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
    operations = {}
    for operation in sorted({s['operation'] for s in samples}):
        group = [s for s in samples if s['operation'] == operation]
        success = [s['ms'] for s in group if not s['error']]
        operations[operation] = dict(requests=len(group), successful=len(success),
            errors=len(group) - len(success), p50_ms=percentile(success, .5),
            p95_ms=percentile(success, .95), p99_ms=percentile(success, .99),
            max_ms=max(success) if success else None,
            statuses=dict(Counter(str(s['status']) for s in group)))
    first = min(s['started_s'] for s in samples)
    last = max(s['started_s'] + s['ms'] / 1000 for s in samples)
    report = dict(run_id=run_id, users=args.users, workload='one closed-loop BFI-44 journey per user',
        think_seconds=args.think_seconds, completed_journeys=sum(completed),
        measured_seconds=round(last - first, 3), throughput_rps=round(len(samples) / (last - first), 3),
        percentile_method='nearest-rank, successful HTTP requests only',
        operations=operations, samples=samples)
    Path(args.output).write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != 'samples'}, indent=2))
    return 0 if all(completed) and all(s['error'] is None for s in samples) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True, help='Ejemplo: http://127.0.0.1:8000')
    parser.add_argument('--isolated-demo', action='store_true')
    parser.add_argument('--users', type=int, choices=range(1, 101), default=30)
    parser.add_argument('--think-seconds', type=float, default=0)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--deadline', type=float, default=900)
    parser.add_argument('--output', default='latency.json')
    raise SystemExit(asyncio.run(run(parser.parse_args())))
