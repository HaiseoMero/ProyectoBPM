"""Autorización HTTP real (JWT y BD), sin sustituir las dependencias de identidad."""
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.database import Base, get_db
from app.models import Curso, Estudiante, Evaluacion, Orientador, ReporteVocacional, Usuario
from app.routers.reporte import router as reporte_router
from app.routers.orientador import router as orientador_router
from app.schemas.reporte import ReporteOut
from app.utils.security import create_access_token

SCORES = {'N': 0.125, 'A': 0.375, 'E': 0.5, 'C': 0.75, 'O': 0.875}
REPORT_DATE = datetime(2026, 1, 15, 12, 0)
ENDPOINTS = [('/api/evaluacion/reporte', 1),
             ('/api/evaluacion/reporte/101', 1),
             ('/api/orientador/estudiante/1/reporte', 10)]


def headers(user_id, **claims):
    token = create_access_token({'sub': f'report{user_id}@example.com', **claims})
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def report_api():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with sessions() as db:
        db.add_all([Usuario(id=i, email=f'report{i}@example.com', hashed_password='unused',
                            rol='estudiante' if i < 10 else 'orientador')
                    for i in [1, 2, 3, 4, 5, 6, 10, 11, 12]])
        await db.flush()
        db.add_all([Orientador(id=i, usuario_id=i, nombre_completo=f'Orientador {i}',
                               establecimiento='Liceo A' if i < 12 else 'Liceo B')
                    for i in [10, 11, 12]])
        await db.flush()
        db.add_all([
            Curso(id=1, nombre='4° Medio A', establecimiento='Liceo A', orientador_id=10),
            Curso(id=2, nombre='4° Medio B', establecimiento='Liceo A', orientador_id=11),
            Curso(id=3, nombre='4° Medio C', establecimiento='Liceo A'),
            Curso(id=4, nombre='4° Medio A', establecimiento='Liceo B', orientador_id=12),
        ])
        await db.flush()
        courses = {1: 1, 2: 2, 3: 3, 4: 1, 5: 1, 6: 4}
        db.add_all([Estudiante(id=i, usuario_id=i, nombre_completo=f'Estudiante {i}',
                               edad=17, curso_id=course) for i, course in courses.items()])
        await db.flush()
        db.add_all([Evaluacion(id=i, estudiante_id=i, estado='completada') for i in [1, 2, 3, 5, 6]])
        await db.flush()
        db.add_all([ReporteVocacional(id=100+i, evaluacion_id=i, scores_json=SCORES,
                                      created_at=REPORT_DATE) for i in [1, 2, 3, 6]])
        await db.commit()

    async def db_dependency():
        async with sessions() as db:
            yield db

    app = FastAPI()
    app.include_router(reporte_router, prefix='/api')
    app.include_router(orientador_router, prefix='/api')
    app.dependency_overrides[get_db] = db_dependency
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            yield client, sessions
    finally:
        await engine.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize('path', ['/api/evaluacion/reporte', '/api/evaluacion/reporte/101'])
async def test_student_reads_own_report(report_api, path):
    client, _ = report_api
    response = await client.get(path, headers=headers(1))
    assert response.status_code == 200
    assert response.json()['studentName'] == 'Estudiante 1'
    assert response.json()['scores'] == SCORES


@pytest.mark.asyncio
@pytest.mark.parametrize('report_id', [102, 103, 106])
async def test_student_cannot_read_others_reports(report_api, report_id):
    client, _ = report_api
    # Incluso un claim de rol distinto no sustituye el rol registrado en MySQL.
    response = await client.get(f'/api/evaluacion/reporte/{report_id}', headers=headers(1, role='orientador'))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Reporte no encontrado'}


@pytest.mark.asyncio
async def test_my_report_ignores_foreign_identifiers_in_query(report_api):
    client, _ = report_api
    response = await client.get('/api/evaluacion/reporte?estudiante_id=2&reporte_id=102', headers=headers(1))
    assert response.status_code == 200
    assert response.json()['studentName'] == 'Estudiante 1'


@pytest.mark.asyncio
@pytest.mark.parametrize('counselor,student', [(10, 1), (11, 2), (12, 6)])
@pytest.mark.parametrize('route', ['by_id', 'counselor'])
async def test_counselor_reads_only_assigned_course(report_api, counselor, student, route):
    client, _ = report_api
    path = f'/api/evaluacion/reporte/{100+student}' if route == 'by_id' else f'/api/orientador/estudiante/{student}/reporte'
    response = await client.get(path, headers=headers(counselor))
    assert response.status_code == 200
    assert response.json()['studentName'] == f'Estudiante {student}'


@pytest.mark.asyncio
@pytest.mark.parametrize('student', [2, 3, 6])
@pytest.mark.parametrize('route,status_code', [('by_id', 404), ('counselor', 403)])
async def test_counselor_cannot_read_other_or_unassigned_courses(report_api, student, route, status_code):
    client, _ = report_api
    # Incluye otro orientador del MISMO establecimiento y curso sin asignación.
    path = f'/api/evaluacion/reporte/{100+student}' if route == 'by_id' else f'/api/orientador/estudiante/{student}/reporte'
    response = await client.get(path, headers=headers(10))
    assert response.status_code == status_code
    assert set(response.json()) == {'detail'}


@pytest.mark.asyncio
@pytest.mark.parametrize('user', [1, 10])
async def test_nonexistent_report_id_is_404(report_api, user):
    client, _ = report_api
    response = await client.get('/api/evaluacion/reporte/99999', headers=headers(user))
    assert response.status_code == 404
    assert response.json() == {'detail': 'Reporte no encontrado'}


@pytest.mark.asyncio
@pytest.mark.parametrize('student', [4, 5])
async def test_no_evaluation_or_no_report_is_404_for_authorized_users(report_api, student):
    client, _ = report_api
    own = await client.get('/api/evaluacion/reporte', headers=headers(student))
    counselor = await client.get(f'/api/orientador/estudiante/{student}/reporte', headers=headers(10))
    assert own.status_code == counselor.status_code == 404


@pytest.mark.asyncio
async def test_nonexistent_student_in_counselor_route_preserves_current_403(report_api):
    client, _ = report_api
    response = await client.get('/api/orientador/estudiante/99999/reporte', headers=headers(10))
    assert response.status_code == 403  # No se acredita pertenencia al curso.


@pytest.mark.asyncio
@pytest.mark.parametrize('path,user', [('/api/evaluacion/reporte', 10),
                                       ('/api/orientador/estudiante/1/reporte', 1)])
async def test_role_specific_routes_reject_wrong_role(report_api, path, user):
    client, _ = report_api
    assert (await client.get(path, headers=headers(user))).status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize('path,user', ENDPOINTS)
@pytest.mark.parametrize('invalid_kind', ['malformed', 'bad_signature', 'expired', 'no_sub', 'unknown_user'])
async def test_invalid_jwt_rejected_on_all_report_endpoints(report_api, path, user, invalid_kind):
    client, _ = report_api
    claims = {'sub': f'report{user}@example.com'}
    if invalid_kind == 'malformed':
        token = 'not.a.valid-jwt'
    elif invalid_kind == 'bad_signature':
        token = jwt.encode(claims, settings.JWT_SECRET + '-wrong', algorithm='HS256')
    elif invalid_kind == 'expired':
        token = create_access_token(claims, expires_delta=timedelta(seconds=-60))
    elif invalid_kind == 'no_sub':
        token = create_access_token({'role': 'estudiante'})
    else:
        token = create_access_token({'sub': 'missing@example.com'})
    response = await client.get(path, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401
    assert set(response.json()) == {'detail'}


@pytest.mark.asyncio
@pytest.mark.parametrize('path,user', ENDPOINTS)
async def test_report_endpoints_require_bearer_token(report_api, path, user):
    client, _ = report_api
    assert (await client.get(path)).status_code in (401, 403)  # HTTPBearer según versión FastAPI.


@pytest.mark.asyncio
@pytest.mark.parametrize('path,user', ENDPOINTS + [('/api/evaluacion/reporte/101', 10)])
async def test_disabling_user_invalidates_existing_token(report_api, path, user):
    client, sessions = report_api
    authorization = headers(user)
    assert (await client.get(path, headers=authorization)).status_code == 200
    async with sessions() as db:
        (await db.get(Usuario, user)).is_active = False
        await db.commit()
    response = await client.get(path, headers=authorization)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Usuario inactivo'}


@pytest.mark.asyncio
async def test_all_three_endpoints_share_exact_report_contract(report_api):
    client, _ = report_api
    bodies = []
    for path, user in ENDPOINTS + [('/api/evaluacion/reporte/101', 10)]:
        response = await client.get(path, headers=headers(user))
        assert response.status_code == 200
        body = response.json()
        assert set(body) == {'studentName', 'evaluatedAt', 'scores', 'dimensions', 'careerAreas'}
        assert ReporteOut.model_validate(body).model_dump() == body
        bodies.append(body)
    assert all(body == bodies[0] for body in bodies)
    body = bodies[0]
    assert body['studentName'] == 'Estudiante 1'
    assert body['evaluatedAt'] == REPORT_DATE.strftime('%d de %b, %Y')
    assert body['scores'] == SCORES
    assert len(body['dimensions']) == 5
    assert {d['letter']: d['score'] for d in body['dimensions']} == {'O': 87, 'C': 75, 'E': 50, 'A': 37, 'N': 12}
    for dimension in body['dimensions']:
        assert set(dimension) == {'letter', 'name', 'score', 'color', 'interpretation', 'vocationalImpact'}
        assert dimension['vocationalImpact'] == 'Este puntaje por sí solo no permite inferir aptitud ni recomendar una profesión.'
    assert len(body['careerAreas']) == 1
    assert body['careerAreas'][0]['title'] == 'Tecnología, Ciencias Básicas y Agropecuaria'
    assert set(body['careerAreas'][0]) == {'title', 'desc', 'carreras'}
    assert 'Referencia exploratoria' in body['careerAreas'][0]['desc']
    assert body['careerAreas'][0]['carreras'] == [
        'A modo exploratorio: Ingeniería Informática', 'Biología', 'Agronomía', 'Astronomía',
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize('scores,title', [
    ({'O': 0.9, 'A': 0.8, 'E': 0.3, 'C': 0.2, 'N': 0.1}, 'Ciencias Sociales y Humanidades'),
    ({'N': 0.95, 'O': 0.9, 'C': 0.8, 'A': 0.2, 'E': 0.1}, 'Tecnología, Ciencias Básicas y Agropecuaria'),
    (dict.fromkeys('OCEAN', 0.5), 'Tecnología, Ciencias Básicas y Agropecuaria'),
])
async def test_exploratory_area_preserves_scores_and_contract_on_all_endpoints(report_api, scores, title):
    client, sessions = report_api
    async with sessions() as db:
        (await db.get(ReporteVocacional, 101)).scores_json = scores
        await db.commit()
    bodies = []
    for path, user in ENDPOINTS:
        response = await client.get(path, headers=headers(user))
        assert response.status_code == 200
        body = response.json()
        assert len(body['careerAreas']) == 1
        assert body['careerAreas'][0]['title'] == title
        assert body['scores'] == scores
        assert len(body['dimensions']) == 5
        assert ReporteOut.model_validate(body).model_dump() == body
        bodies.append(body)
    assert bodies[0] == bodies[1] == bodies[2]


def test_spanish_interpretations_change_with_score_and_keep_scope():
    from app.routers.reporte import build_reporte_out, get_dimension_interpretation
    for value in [0, 0.5, 1]:
        result = build_reporte_out(ReporteVocacional(scores_json=dict.fromkeys('OCEAN', value)), 'Alumno')
        assert {d.letter: d.interpretation for d in result.dimensions} == {
            letter: get_dimension_interpretation(letter, int(value * 100)) for letter in 'OCEAN'
        }
        assert all(d.vocationalImpact == 'Este puntaje por sí solo no permite inferir aptitud ni recomendar una profesión.' for d in result.dimensions)
        assert all(d.score == int(value * 100) for d in result.dimensions)
    assert get_dimension_interpretation('O', 0).startswith('Tus respuestas indican una preferencia')
    assert get_dimension_interpretation('N', 100).startswith('Pareces tener una mayor reactividad')


@pytest.mark.asyncio
async def test_reading_historical_report_does_not_invent_persisted_interpretations(report_api):
    client, sessions = report_api
    for path, user in ENDPOINTS:
        assert (await client.get(path, headers=headers(user))).status_code == 200
    async with sessions() as db:
        report = await db.get(ReporteVocacional, 101)
        assert report.carreras_json is None and report.interpretaciones_json is None
        assert report.scores_json == SCORES
