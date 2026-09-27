import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.models import Estudiante, Evaluacion, Pregunta, ReporteVocacional, Respuesta, Usuario
from app.routers.evaluacion import router
from app.seed import PREGUNTAS
from app.utils.security import create_access_token


def auth(user_id):
    token = create_access_token({"sub": f"user{user_id}@example.test"})
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def api():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with sessions() as db:
        db.add_all([
            Usuario(id=i, email=f"user{i}@example.test", hashed_password="unused",
                    rol="orientador" if i == 4 else "estudiante")
            for i in range(1, 5)
        ])
        await db.flush()
        db.add_all([
            Estudiante(id=i, usuario_id=i, nombre_completo=f"Alumno {i}", edad=17)
            for i in range(1, 4)
        ])
        db.add_all([
            Pregunta(id=i, texto=texto, dimension=dimension, es_invertida=invertida, orden=i)
            for i, texto, dimension, invertida in PREGUNTAS
        ])
        await db.flush()
        db.add_all([Evaluacion(id=i, estudiante_id=i, estado="en_progreso") for i in (1, 2)])
        await db.flush()
        db.add_all([Respuesta(evaluacion_id=i, pregunta_id=1, valor=i + 1) for i in (1, 2)])
        await db.commit()

    async def test_db():
        async with sessions() as db:
            yield db

    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.dependency_overrides[get_db] = test_db
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client, sessions
    finally:
        await engine.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [1, 2])
async def test_returns_only_authenticated_students_answers(api, user_id):
    client, _ = api
    # Un parámetro ajeno no cambia la evaluación seleccionada por identidad.
    response = await client.get("/api/evaluacion/respuestas?estudiante_id=99", headers=auth(user_id))
    assert response.status_code == 200
    assert response.json() == [{"preguntaId": 1, "valor": user_id + 1, "saved": True}]


@pytest.mark.asyncio
async def test_no_evaluation_returns_empty_without_creating_one(api):
    client, sessions = api
    response = await client.get("/api/evaluacion/respuestas", headers=auth(3))
    assert response.status_code == 200
    assert response.json() == []
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Evaluacion)) == 2


@pytest.mark.asyncio
async def test_requires_authentication_and_student_role(api):
    client, _ = api
    assert (await client.get("/api/evaluacion/respuestas")).status_code in (401, 403)
    assert (await client.get("/api/evaluacion/respuestas", headers=auth(4))).status_code == 403


@pytest.mark.asyncio
async def test_resume_updates_existing_evaluation_and_answer(api):
    client, sessions = api
    response = await client.post("/api/evaluacion/respuesta", headers=auth(1),
                                 json={"preguntaId": 1, "valor": 5})
    assert response.status_code == 200
    response = await client.get("/api/evaluacion/respuestas", headers=auth(1))
    assert response.json() == [{"preguntaId": 1, "valor": 5, "saved": True}]
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Evaluacion)) == 2
        assert await db.scalar(select(func.count()).select_from(Respuesta)) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize('missing_id', [44, 999])
async def test_partial_answer_requires_existing_question(api, missing_id):
    client, sessions = api
    if missing_id == 44:
        async with sessions() as db:
            await db.delete(await db.get(Pregunta, missing_id))
            await db.commit()
    response = await client.post('/api/evaluacion/respuesta', headers=auth(3),
                                 json={'preguntaId': missing_id, 'valor': 3})
    assert response.status_code == 422
    assert response.json() == {'detail': 'La pregunta no existe'}
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Evaluacion)) == 2
        assert await db.scalar(select(func.count()).select_from(Respuesta)) == 2


@pytest.mark.asyncio
async def test_partial_answer_accepts_question_id_from_database(api, monkeypatch):
    client, sessions = api
    monkeypatch.setattr('app.services.bpm_service.finish_cuestionario', AsyncMock())
    async with sessions() as db:
        question = await db.get(Pregunta, 44)
        question.id = 80
        await db.commit()
    response = await client.post('/api/evaluacion/respuesta', headers=auth(1),
                                 json={'preguntaId': 80, 'valor': 3})
    assert response.status_code == 200
    assert response.json()['preguntaId'] == 80
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Respuesta).where(Respuesta.pregunta_id == 80)) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("estado", ["completada", "procesada"])
async def test_finished_evaluation_cannot_be_edited_or_submitted_again(api, estado):
    client, sessions = api
    async with sessions() as db:
        evaluation = await db.get(Evaluacion, 1)
        evaluation.estado = estado
        await db.commit()
    response = await client.post("/api/evaluacion/respuesta", headers=auth(1),
                                 json={"preguntaId": 1, "valor": 5})
    assert response.status_code == 400
    response = await client.post("/api/evaluacion/enviar", headers=auth(1),
                                 json={"respuestas": [{"preguntaId": i, "valor": 5} for i in range(1, 45)]})
    assert response.status_code == 400
    response = await client.get("/api/evaluacion/respuestas", headers=auth(1))
    assert response.json() == [{"preguntaId": 1, "valor": 2, "saved": True}]


def final_payload():
    return {"respuestas": [{"preguntaId": i, "valor": 3} for i in range(1, 45)]}


@pytest.mark.asyncio
@pytest.mark.parametrize("case", [
    "missing_field", "null_list", "empty", "missing_answer", "extra_answer",
    "duplicate", "unknown_id", "zero_id", "string_id", "boolean_id",
    "below_range", "above_range", "fraction", "boolean_value", "string_value",
    "missing_value", "null_answer",
])
async def test_invalid_final_payload_is_controlled_and_does_not_change_data(api, monkeypatch, case):
    client, sessions = api
    notify = AsyncMock()
    monkeypatch.setattr("app.services.bpm_service.finish_cuestionario", notify)
    payload = final_payload()
    answers = payload["respuestas"]
    if case == "missing_field":
        payload = {}
    elif case == "null_list":
        payload["respuestas"] = None
    elif case == "empty":
        answers.clear()
    elif case == "missing_answer":
        answers.pop()
    elif case == "extra_answer":
        answers.append({"preguntaId": 45, "valor": 3})
    elif case == "duplicate":
        answers[-1]["preguntaId"] = 1
    elif case in ("unknown_id", "zero_id", "string_id", "boolean_id"):
        answers[-1]["preguntaId"] = {"unknown_id": 999, "zero_id": 0, "string_id": "44", "boolean_id": True}[case]
    elif case == "missing_value":
        del answers[0]["valor"]
    elif case == "null_answer":
        answers[0] = None
    else:
        answers[0]["valor"] = {"below_range": 0, "above_range": 6, "fraction": 2.5,
                               "boolean_value": True, "string_value": "3"}[case]

    response = await client.post("/api/evaluacion/enviar", headers=auth(1), json=payload)
    assert response.status_code == 422
    notify.assert_not_awaited()
    notify.assert_not_awaited()
    async with sessions() as db:
        evaluation = await db.get(Evaluacion, 1)
        assert evaluation.estado == "en_progreso"
        assert evaluation.completed_at is None
        assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 0
    response = await client.get("/api/evaluacion/respuestas", headers=auth(1))
    assert response.json() == [{"preguntaId": 1, "valor": 2, "saved": True}]


@pytest.mark.asyncio
async def test_malformed_json_returns_validation_error(api):
    client, _ = api
    response = await client.post("/api/evaluacion/enviar", headers={**auth(1), "Content-Type": "application/json"},
                                 content='{"respuestas":')
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_final_ids_must_exist_in_database(api):
    client, sessions = api
    async with sessions() as db:
        await db.delete(await db.get(Pregunta, 44))
        await db.commit()
    response = await client.post("/api/evaluacion/enviar", headers=auth(1), json=final_payload())
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_final_submission_uses_question_order_for_scoring_and_ids_for_storage(api, monkeypatch):
    client, sessions = api
    monkeypatch.setattr("app.services.bpm_service.finish_cuestionario", AsyncMock())
    async with sessions() as db:
        await db.execute(delete(Respuesta))
        await db.execute(delete(Pregunta))
        db.add_all([
            Pregunta(id=49 + orden, texto=texto, dimension=dimension,
                     es_invertida=invertida, orden=orden)
            for orden, texto, dimension, invertida in PREGUNTAS
        ])
        await db.commit()

    payload = {"respuestas": [
        {"preguntaId": 49 + orden, "valor": 5 if orden == 1 else 3}
        for orden in range(1, 45)
    ]}
    response = await client.post("/api/evaluacion/enviar", headers=auth(1), json=payload)
    assert response.status_code == 200
    async with sessions() as db:
        report = await db.get(ReporteVocacional, response.json()["reportId"])
        assert report.scores_json == {"O": 0.5, "C": 0.5, "E": 0.5625, "A": 0.5, "N": 0.5}
        saved = (await db.scalars(select(Respuesta).where(Respuesta.evaluacion_id == 1))).all()
        assert {r.pregunta_id: r.valor for r in saved} == {
            answer["preguntaId"]: answer["valor"] for answer in payload["respuestas"]
        }
        assert await db.scalar(select(func.count()).select_from(Evaluacion).where(Evaluacion.estudiante_id == 1)) == 1


@pytest.mark.asyncio
async def test_valid_final_snapshot_replaces_partial_answers_and_preserves_one_evaluation(api, monkeypatch):
    client, sessions = api
    notify = AsyncMock()
    monkeypatch.setattr("app.services.bpm_service.finish_cuestionario", notify)
    payload = final_payload()
    payload["respuestas"][0]["valor"] = 5
    # El orden del payload no cambia la correspondencia entre preguntas y valores.
    payload["respuestas"].reverse()
    response = await client.post("/api/evaluacion/enviar", headers=auth(1), json=payload)
    assert response.status_code == 200
    notify.assert_awaited_once()
    async with sessions() as db:
        evaluation = await db.get(Evaluacion, 1)
        assert evaluation.estado == "completada"
        assert evaluation.completed_at is not None
        assert await db.scalar(select(func.count()).select_from(Evaluacion).where(Evaluacion.estudiante_id == 1)) == 1
        report = await db.get(ReporteVocacional, response.json()["reportId"])
        assert report.scores_json == {"O": 0.5, "C": 0.5, "E": 0.5625, "A": 0.5, "N": 0.5}
    response = await client.get("/api/evaluacion/respuestas", headers=auth(1))
    assert {r["preguntaId"]: r["valor"] for r in response.json()} == {r["preguntaId"]: r["valor"] for r in payload["respuestas"]}
    assert len(response.json()) == 44
    other = await client.get("/api/evaluacion/respuestas", headers=auth(2))
    assert other.json() == [{"preguntaId": 1, "valor": 3, "saved": True}]
    assert (await client.post("/api/evaluacion/enviar", headers=auth(1), json=payload)).status_code == 400
    assert (await client.post("/api/evaluacion/respuesta", headers=auth(1), json={"preguntaId": 1, "valor": 1})).status_code == 400
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 1
    assert notify.await_count == 1


@pytest.mark.asyncio
async def test_final_submission_does_not_create_a_second_evaluation(api):
    client, sessions = api
    response = await client.post("/api/evaluacion/enviar", headers=auth(3), json=final_payload())
    assert response.status_code == 400
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Evaluacion)) == 2


@pytest.mark.asyncio
async def test_failed_commit_rolls_back_final_answers_and_report(api, monkeypatch):
    client, sessions = api
    notify = AsyncMock()
    monkeypatch.setattr("app.services.bpm_service.finish_cuestionario", notify)

    async def fail_commit(db):
        # Simular un fallo después de enviar las escrituras a la BD, antes de confirmar.
        await db.flush()
        raise RuntimeError("Fallo de commit simulado")

    monkeypatch.setattr(AsyncSession, "commit", fail_commit)
    with pytest.raises(RuntimeError, match="Fallo de commit simulado"):
        await client.post("/api/evaluacion/enviar", headers=auth(1), json=final_payload())
    notify.assert_not_awaited()
    async with sessions() as db:
        evaluation = await db.get(Evaluacion, 1)
        assert evaluation.estado == "en_progreso"
        assert evaluation.completed_at is None
        assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 0
        assert await db.scalar(select(func.count()).select_from(Respuesta)) == 2
    response = await client.get("/api/evaluacion/respuestas", headers=auth(1))
    assert response.json() == [{"preguntaId": 1, "valor": 2, "saved": True}]


@pytest.mark.asyncio
async def test_partial_answer_retries_mysql_deadlock_without_duplicate_evaluation(api, monkeypatch):
    from sqlalchemy.exc import OperationalError
    client, sessions = api
    monkeypatch.setattr('app.services.bpm_service.finish_cuestionario', AsyncMock())
    original_flush = AsyncSession.flush
    attempts = 0

    async def deadlock_once(db, *args, **kwargs):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise OperationalError('insert', {}, Exception(1213, 'deadlock'))
        return await original_flush(db, *args, **kwargs)

    monkeypatch.setattr(AsyncSession, 'flush', deadlock_once)
    response = await client.post('/api/evaluacion/respuesta', headers=auth(3),
                                 json={'preguntaId': 1, 'valor': 3})
    assert response.status_code == 200
    assert attempts >= 2
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Evaluacion).where(Evaluacion.estudiante_id == 3)) == 1
        assert await db.scalar(select(func.count()).select_from(Respuesta)) == 3


@pytest.mark.asyncio
async def test_partial_answer_exhausted_deadlock_returns_503(api, monkeypatch):
    from sqlalchemy.exc import OperationalError
    client, sessions = api

    async def deadlock(db, *args, **kwargs):
        raise OperationalError('insert', {}, Exception(1213, 'deadlock'))

    monkeypatch.setattr(AsyncSession, 'flush', deadlock)
    response = await client.post('/api/evaluacion/respuesta', headers=auth(3),
                                 json={'preguntaId': 1, 'valor': 3})
    assert response.status_code == 503
    assert response.json() == {'detail': 'No se pudo guardar la respuesta. Intenta nuevamente'}
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Evaluacion)) == 2
