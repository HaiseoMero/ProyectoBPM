"""MySQL real para commits/bloqueos. Zeebe simulado: no acredita E2E."""
import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database import get_db
from app.models import BPMEvento, Usuario, Estudiante, Evaluacion, Pregunta, ProcesoBPM, ReporteVocacional
from app.routers.evaluacion import router
from app.seed import PREGUNTAS
from app.services import bpm_service as bpm
from tests.test_registro_mysql import mysql_db
from tests.test_evaluacion_respuestas import auth, final_payload


async def populate(engine):
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with sessions() as db:
        db.add(Usuario(id=1, email='user1@example.test', hashed_password='unused', rol='estudiante'))
        await db.flush()
        db.add(Estudiante(id=1, usuario_id=1, nombre_completo='Test', edad=17))
        await db.flush()
        db.add(Evaluacion(id=1, estudiante_id=1, estado='en_progreso'))
        await db.flush()
        db.add(ProcesoBPM(evaluacion_id=1, estado_actual='registro', process_instance_key='123'))
        db.add_all([Pregunta(id=i, texto=t, dimension=d, es_invertida=inv, orden=i) for i,t,d,inv in PREGUNTAS])
        await db.commit()
    return sessions


@pytest.mark.asyncio
async def test_mysql_two_submissions_one_report_one_publication(mysql_db, monkeypatch):
    sessions = await populate(mysql_db)
    async def publish(**kwargs):
        async with sessions() as db:
            assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 1
            assert (await db.get(Evaluacion, 1)).estado == 'completada'
        await asyncio.sleep(0.05)
    zeebe = SimpleNamespace(topology=AsyncMock(), publish_message=AsyncMock(side_effect=publish))
    monkeypatch.setattr(bpm, 'get_zeebe_client', lambda: zeebe)
    async def dependency():
        async with sessions() as db:
            yield db
    app = FastAPI()
    app.include_router(router, prefix='/api')
    app.dependency_overrides[get_db] = dependency
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        responses = await asyncio.gather(*[client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload()) for _ in range(2)])
    assert sorted(r.status_code for r in responses) == [200, 400]
    zeebe.publish_message.assert_awaited_once()
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 1
        assert await db.scalar(select(func.count()).select_from(BPMEvento)) == 1


@pytest.mark.asyncio
async def test_mysql_dispatchers_skip_locked_event(mysql_db, monkeypatch):
    sessions = await populate(mysql_db)
    async with sessions() as db:
        (await db.get(Evaluacion, 1)).estado = 'completada'
        db.add(ReporteVocacional(evaluacion_id=1, scores_json={}))
        db.add(BPMEvento(evaluacion_id=1, tipo='completar'))
        await db.commit()
        event_id = await db.scalar(select(BPMEvento.id))
    entered, release = asyncio.Event(), asyncio.Event()
    async def publish(**kwargs):
        entered.set()
        await release.wait()
    zeebe = SimpleNamespace(topology=AsyncMock(), publish_message=AsyncMock(side_effect=publish))
    monkeypatch.setattr(bpm, 'get_zeebe_client', lambda: zeebe)
    async def dispatch():
        async with sessions() as db:
            await bpm.dispatch_event(db, event_id)
    first = asyncio.create_task(dispatch())
    try:
        await asyncio.wait_for(entered.wait(), 3)
        await asyncio.wait_for(dispatch(), 3)
    finally:
        release.set()
        await first
    await dispatch()
    zeebe.publish_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_mysql_migration_does_not_republish_legacy_data(mysql_db, monkeypatch):
    await populate(mysql_db)
    path = Path(__file__).parents[1] / 'alembic/versions/20260924_bpm_outbox.py'
    spec = importlib.util.spec_from_file_location('bpm_outbox_migration', path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    def upgrade(conn):
        monkeypatch.setattr(migration, 'op', Operations(MigrationContext.configure(conn)))
        migration.upgrade()
        migration.upgrade()
    async with mysql_db.begin() as conn:
        await conn.execute(text('DROP TABLE bpm_evento'))  # Exclusivamente BD temporal de la fixture.
        await conn.run_sync(upgrade)
        assert await conn.scalar(text('SELECT COUNT(*) FROM bpm_evento')) == 0
        assert await conn.scalar(text('SELECT COUNT(*) FROM evaluacion')) == 1
        assert await conn.scalar(text('SELECT process_instance_key FROM proceso_bpm')) == '123'
        await conn.execute(text("INSERT INTO bpm_evento (evaluacion_id,tipo,message_id,estado,intentos) VALUES (1,'completar','one','pendiente',0)"))
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            await conn.execute(text("INSERT INTO bpm_evento (evaluacion_id,tipo,message_id,estado,intentos) VALUES (1,'completar','two','pendiente',0)"))


@pytest.mark.asyncio
async def test_mysql_unknown_partial_question_returns_422_before_foreign_key(mysql_db):
    sessions = await populate(mysql_db)
    async def dependency():
        async with sessions() as db:
            yield db
    app = FastAPI()
    app.include_router(router, prefix='/api')
    app.dependency_overrides[get_db] = dependency
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post('/api/evaluacion/respuesta', headers=auth(1),
                                     json={'preguntaId': 999, 'valor': 3})
    assert response.status_code == 422
    assert response.json() == {'detail': 'La pregunta no existe'}
    async with sessions() as db:
        from app.models import Respuesta
        assert await db.scalar(select(func.count()).select_from(Respuesta)) == 0
        assert await db.scalar(select(func.count()).select_from(Evaluacion)) == 1
