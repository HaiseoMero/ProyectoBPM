from datetime import date, timedelta
from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.database import Base, get_db
from app.models import Curso, Estudiante, Orientador, Usuario
from app.models.estudiante import calcular_edad
from app.routers.auth import router as auth_router
from app.routers.orientador import router as orientador_router
from app.utils.security import create_access_token

CODE = 'test-only-private-code'


def student(email='student@example.com', school='Liceo Uno', **changes):
    return dict(email=email, password='password123', nombre_completo='Alumno Prueba',
                role='estudiante', establecimiento=school, nivel='4° Medio', letra='A',
                fecha_nacimiento='2009-05-10') | changes


def counselor(email='counselor@example.com', school='Liceo Uno', **changes):
    return dict(email=email, password='password123', nombre_completo='Orientador Prueba',
                role='orientador', establecimiento=school, departamento='Orientación',
                codigo_verificacion=CODE) | changes


@pytest_asyncio.fixture
async def api(monkeypatch):
    monkeypatch.setattr(settings, 'ORIENTADOR_REGISTRATION_CODE', SecretStr(CODE))
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async def test_db():
        async with sessions() as db:
            yield db

    app = FastAPI()
    app.include_router(auth_router, prefix='/api')
    app.include_router(orientador_router, prefix='/api')
    app.dependency_overrides[get_db] = test_db
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            yield client, sessions
    finally:
        await engine.dispose()


async def register(client, payload):
    response = await client.post('/api/auth/register', json=payload)
    assert response.status_code == 200, response.text
    assert response.json()['ok'] is True
    return response


def test_age_changes_only_on_birthday_and_legacy_age_survives():
    dob = date(2009, 9, 22)
    assert calcular_edad(dob, date(2026, 9, 21)) == 16
    assert calcular_edad(dob, date(2026, 9, 22)) == 17
    assert calcular_edad(dob, date(2026, 9, 23)) == 17
    assert calcular_edad(date(2008, 2, 29), date(2025, 2, 28)) == 16
    assert calcular_edad(date(2008, 2, 29), date(2025, 3, 1)) == 17
    legacy = Estudiante(edad=42)
    assert legacy.fecha_nacimiento is None and legacy.edad == 42
    legacy.fecha_nacimiento = dob
    assert legacy.edad == calcular_edad(dob)  # Nunca se presenta la edad histórica contradictoria.


@pytest.mark.asyncio
async def test_student_registration_birthdate_login_and_profile(api):
    client, sessions = api
    await register(client, student())
    async with sessions() as db:
        est = await db.scalar(select(Estudiante))
        assert est.fecha_nacimiento == date(2009, 5, 10)
        assert est.edad == calcular_edad(est.fecha_nacimiento)
        assert est._edad_historica == est.edad
        course = await db.get(Curso, est.curso_id)
        assert course.establecimiento == 'Liceo Uno'
        assert course.orientador_id is None
    login = await client.post('/api/auth/login', json={'email': student()['email'], 'password': 'password123'})
    assert login.status_code == 200
    assert login.json()['role'] == 'estudiante'
    headers = {'Authorization': f"Bearer {login.json()['access_token']}"}
    profile = await client.get('/api/auth/me', headers=headers)
    assert profile.status_code == 200 and profile.json()['name'] == 'Alumno Prueba'
    assert 'fecha_nacimiento' not in profile.json()
    async with sessions() as db:
        user = await db.scalar(select(Usuario))
        user.is_active = False
        await db.commit()
    assert (await client.get('/api/auth/me', headers=headers)).status_code == 401
    assert (await client.post('/api/auth/login', json={'email': student()['email'], 'password': 'password123'})).status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize('dob', ['2026-02-30', 'not-a-date', '1900-01-01', None, 12345,
    '2009-05-10T00:00:00', date.today().isoformat(), (date.today() + timedelta(days=1)).isoformat()])
async def test_invalid_birthdate_leaves_no_user_or_course(api, dob):
    client, sessions = api
    response = await client.post('/api/auth/register', json=student(fecha_nacimiento=dob))
    assert response.status_code == 422
    assert 'password123' not in response.text
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Usuario)) == 0
        assert await db.scalar(select(func.count()).select_from(Curso)) == 0


@pytest.mark.asyncio
async def test_counselor_code_valid_and_not_returned(api):
    client, sessions = api
    response = await register(client, counselor())
    assert CODE not in response.text
    async with sessions() as db:
        ori = await db.scalar(select(Orientador))
        assert ori.establecimiento == 'Liceo Uno'
        assert not hasattr(ori, 'codigo_verificacion')
    response = await client.post('/api/auth/login', json={'email': counselor()['email'], 'password': 'password123'})
    assert response.status_code == 200 and response.json()['role'] == 'orientador'


@pytest.mark.asyncio
@pytest.mark.parametrize('code', ['wrong-private-code', None, '', 'código-incorrecto'])
async def test_invalid_or_missing_counselor_code(api, code):
    client, sessions = api
    response = await client.post('/api/auth/register', json=counselor(codigo_verificacion=code))
    assert response.status_code == 403
    assert CODE not in response.text
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Usuario)) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize('configured', [None, SecretStr(''), SecretStr('  ')])
async def test_unconfigured_code_disables_registration(api, monkeypatch, configured):
    client, _ = api
    monkeypatch.setattr(settings, 'ORIENTADOR_REGISTRATION_CODE', configured)
    response = await client.post('/api/auth/register', json=counselor())
    assert response.status_code == 403
    assert 'deshabilitado' in response.json()['detail']


@pytest.mark.asyncio
async def test_validation_errors_never_echo_code_or_password(api):
    client, _ = api
    for payload in [counselor(fecha_nacimiento='2009-05-10'), counselor(establecimiento=' '),
                    counselor(codigo_verificacion={'secret': CODE})]:
        response = await client.post('/api/auth/register', json=payload)
        assert response.status_code == 422
        assert CODE not in response.text and 'password123' not in response.text


@pytest.mark.asyncio
async def test_same_name_other_school_and_course_reuse(api):
    client, sessions = api
    await register(client, student())
    await register(client, student('second@example.com'))
    await register(client, student('third@example.com', 'Otro Liceo'))
    async with sessions() as db:
        students = (await db.scalars(select(Estudiante).order_by(Estudiante.id))).all()
        assert students[0].curso_id == students[1].curso_id
        assert students[0].curso_id != students[2].curso_id
        assert await db.scalar(select(func.count()).select_from(Curso)) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize('count', [0, 1, 2])
async def test_student_assignment_zero_one_many_counselors(api, count):
    client, sessions = api
    for i in range(count):
        await register(client, counselor(f'ori{i}@example.com'))
    await register(client, student())
    async with sessions() as db:
        course = await db.scalar(select(Curso))
        assert (course.orientador_id is not None) == (count == 1)


@pytest.mark.asyncio
async def test_first_counselor_assigns_waiting_courses_only_in_same_school(api):
    client, sessions = api
    await register(client, student())
    await register(client, student('other@example.com', 'Otro Liceo'))
    await register(client, counselor())
    async with sessions() as db:
        courses = (await db.scalars(select(Curso).order_by(Curso.id))).all()
        assert courses[0].orientador_id is not None
        assert courses[1].orientador_id is None


@pytest.mark.asyncio
async def test_second_counselor_preserves_association_and_ambiguous_courses(api):
    client, sessions = api
    await register(client, counselor())
    await register(client, student())
    async with sessions() as db:
        assigned = await db.scalar(select(Curso))
        first_id = assigned.orientador_id
        db.add(Curso(nombre='3° Medio B', establecimiento='Liceo Uno'))
        await db.commit()
    await register(client, counselor('second@example.com'))
    await register(client, student('secondstudent@example.com'))
    async with sessions() as db:
        courses = (await db.scalars(select(Curso).order_by(Curso.id))).all()
        assert courses[0].orientador_id == first_id
        assert courses[1].orientador_id is None
        assert await db.scalar(select(func.count()).select_from(Curso)) == 2


@pytest.mark.asyncio
async def test_existing_legacy_association_is_never_replaced(api):
    client, sessions = api
    await register(client, counselor('legacy@example.com'))
    await register(client, student())
    async with sessions() as db:
        ori = await db.scalar(select(Orientador))
        ori.establecimiento = None
        legacy_id = ori.id
        await db.commit()
    await register(client, counselor('new@example.com'))
    await register(client, student('newstudent@example.com'))
    async with sessions() as db:
        course = await db.scalar(select(Curso))
        assert course.orientador_id == legacy_id


@pytest.mark.asyncio
async def test_authorization_depends_on_assigned_course_not_school(api):
    client, sessions = api
    await register(client, counselor())
    await register(client, student())
    await register(client, counselor('second@example.com'))
    async with sessions() as db:
        est = await db.scalar(select(Estudiante))
        student_id = est.id
    for email, own in [(counselor()['email'], True), ('second@example.com', False)]:
        headers = {'Authorization': 'Bearer ' + create_access_token({'sub': email})}
        response = await client.get('/api/orientador/estudiantes', headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == (1 if own else 0)
        response = await client.get(f'/api/orientador/estudiante/{student_id}/reporte', headers=headers)
        assert response.status_code == (404 if own else 403)


@pytest.mark.asyncio
async def test_duplicate_email_does_not_leave_partial_data(api):
    client, sessions = api
    await register(client, student())
    response = await client.post('/api/auth/register', json=student(school='Other School'))
    assert response.status_code == 409
    async with sessions() as db:
        for model in (Usuario, Estudiante, Curso):
            assert await db.scalar(select(func.count()).select_from(model)) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('changes', [
    {'email': 'invalid'}, {'password': 'short'}, {'role': 'admin'},
    {'establecimiento': '  '}, {'nivel': None}, {'letra': None},
    {'departamento': 'No corresponde'}, {'codigo_verificacion': CODE},
])
async def test_registration_preserves_validation_and_role_specific_fields(api, changes):
    client, sessions = api
    response = await client.post('/api/auth/register', json=student(**changes))
    assert response.status_code == 422
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Usuario)) == 0


@pytest.mark.asyncio
async def test_failed_commit_rolls_back_user_profile_and_course(api):
    client, sessions = api
    # Simula fallo al confirmar una transacción ya preparada, sin tocar la BD de desarrollo.
    from sqlalchemy.exc import OperationalError
    with patch('sqlalchemy.ext.asyncio.AsyncSession.commit', side_effect=OperationalError('commit', {}, Exception('unavailable'))):
        response = await client.post('/api/auth/register', json=student())
    assert response.status_code == 503
    async with sessions() as db:
        for model in (Usuario, Estudiante, Curso):
            assert await db.scalar(select(func.count()).select_from(model)) == 0
