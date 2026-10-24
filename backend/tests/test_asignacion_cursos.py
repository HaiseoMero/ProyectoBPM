"""Asignación explícita con identidad real y BD aislada; no modifica MySQL local."""
import pytest
from app.models import Curso, Estudiante, Usuario
from tests.test_reportes import report_api, headers
from tests.test_auth_registro import api, register, counselor, student
from app.utils.security import create_access_token


@pytest.mark.asyncio
async def test_only_unassigned_own_school_courses_and_counts_are_listed(report_api):
    client, sessions = report_api
    async with sessions() as db:
        db.add_all([Curso(id=5, nombre='1° Medio A', establecimiento='Liceo B'),
                    Curso(id=6, nombre='2° Medio A', establecimiento='Liceo A')])
        await db.commit()
    response = await client.get('/api/orientador/cursos/sin-asignar', headers=headers(10))
    assert response.status_code == 200
    assert response.json() == [
        {'id': 6, 'nombre': '2° Medio A', 'total_estudiantes': 0},
        {'id': 3, 'nombre': '4° Medio C', 'total_estudiantes': 1},
    ]
    assert (await client.get('/api/orientador/cursos/sin-asignar', headers=headers(12))).json() == [
        {'id': 5, 'nombre': '1° Medio A', 'total_estudiantes': 0}]


@pytest.mark.asyncio
async def test_claim_grants_only_course_owner_access_and_is_idempotent(report_api):
    client, sessions = report_api
    path = '/api/orientador/cursos/3/asignar'
    assert (await client.get('/api/orientador/estudiante/3/reporte', headers=headers(10))).status_code == 403
    # Ambos orientadores vieron el curso disponible; una solicitud atrasada no lo reasigna.
    for user in [10, 11]:
        assert len((await client.get('/api/orientador/cursos/sin-asignar', headers=headers(user))).json()) == 1
    for _ in range(2):
        response = await client.post(path, headers=headers(10), json={'orientador_id': 11})
        assert response.status_code == 200
        assert response.json() == {'id': 3, 'orientador_id': 10}  # El cuerpo no puede elegir otra identidad.
    assert (await client.post(path, headers=headers(11))).status_code == 409
    async with sessions() as db:
        assert (await db.get(Curso, 3)).orientador_id == 10
        # Los futuros estudiantes del curso heredan el responsable, sin reasignación individual.
        db.add(Usuario(id=7, email='report7@example.com', hashed_password='unused', rol='estudiante'))
        await db.flush()
        db.add(Estudiante(id=7, usuario_id=7, nombre_completo='Nuevo estudiante', edad=17, curso_id=3))
        await db.commit()
    assert (await client.get('/api/orientador/cursos/sin-asignar', headers=headers(10))).json() == []
    own = (await client.get('/api/orientador/estudiantes', headers=headers(10))).json()
    other = (await client.get('/api/orientador/estudiantes', headers=headers(11))).json()
    assert {s['id'] for s in own} == {1, 3, 4, 5, 7}
    assert {s['id'] for s in other} == {2}
    assert (await client.get('/api/orientador/estudiante/3/reporte', headers=headers(10))).status_code == 200
    assert (await client.get('/api/orientador/estudiante/3/reporte', headers=headers(11))).status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize('course_id,status', [(2, 409), (4, 404), (9999, 404), (0, 422)])
async def test_cannot_replace_other_counselor_or_claim_foreign_course(report_api, course_id, status):
    client, sessions = report_api
    response = await client.post(f'/api/orientador/cursos/{course_id}/asignar', headers=headers(10))
    assert response.status_code == status
    async with sessions() as db:
        assert (await db.get(Curso, 2)).orientador_id == 11
        assert (await db.get(Curso, 4)).orientador_id == 12


@pytest.mark.asyncio
@pytest.mark.parametrize('method,path', [('get', '/api/orientador/cursos/sin-asignar'),
                                      ('post', '/api/orientador/cursos/3/asignar')])
async def test_assignment_requires_active_counselor_identity(report_api, method, path):
    client, sessions = report_api
    call = getattr(client, method)
    assert (await call(path)).status_code in (401, 403)
    assert (await call(path, headers=headers(1, role='orientador'))).status_code == 403
    async with sessions() as db:
        (await db.get(Usuario, 10)).is_active = False
        await db.commit()
    assert (await call(path, headers=headers(10))).status_code == 401


@pytest.mark.asyncio
async def test_new_course_with_two_registered_counselors_can_be_claimed(api):
    client, _ = api
    await register(client, counselor('first@example.com'))
    await register(client, counselor('second@example.com'))
    await register(client, student())
    def authorization(email):
        return {'Authorization': 'Bearer ' + create_access_token({'sub': email})}
    first, second = authorization('first@example.com'), authorization('second@example.com')
    assert (await client.get('/api/orientador/estudiantes', headers=first)).json() == []
    pending = (await client.get('/api/orientador/cursos/sin-asignar', headers=second)).json()
    assert len(pending) == 1 and pending[0]['total_estudiantes'] == 1
    course_id = pending[0]['id']
    assert (await client.post(f'/api/orientador/cursos/{course_id}/asignar', headers=second)).status_code == 200
    await register(client, student('another@example.com'))
    assert len((await client.get('/api/orientador/estudiantes', headers=second)).json()) == 2
    assert (await client.get('/api/orientador/estudiantes', headers=first)).json() == []
