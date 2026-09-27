"""Pruebas opcionales MySQL 8: crean y eliminan exclusivamente una BD temporal propia.

Configurar VOCALIS_TEST_MYSQL_ADMIN_URL con permiso CREATE DATABASE para ejecutarlas.
Nunca se crean ni eliminan tablas en la BD indicada por la URL administrativa.
"""
import asyncio
import importlib.util
import os
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from alembic.migration import MigrationContext
from alembic.operations import Operations
from pydantic import SecretStr
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.database import Base
from app.schemas.auth import RegisterRequest
from app.services.auth_service import create_user


@pytest_asyncio.fixture
async def mysql_db(monkeypatch):
    url = os.environ.get('VOCALIS_TEST_MYSQL_ADMIN_URL')
    if not url:
        pytest.skip('MySQL aislado requiere VOCALIS_TEST_MYSQL_ADMIN_URL')
    name = 'vocalis_test_registro_' + uuid4().hex
    admin = create_async_engine(url)
    engine = create_async_engine(make_url(url).set(database=name))
    async with admin.begin() as conn:
        await conn.execute(text(f'CREATE DATABASE `{name}` CHARACTER SET utf8mb4'))
    try:
        monkeypatch.setattr(settings, 'ORIENTADOR_REGISTRATION_CODE', SecretStr('test-code'))
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        await engine.dispose()
        async with admin.begin() as conn:
            await conn.execute(text(f'DROP DATABASE `{name}`'))
        await admin.dispose()


def payload(i, role='estudiante'):
    fields = (dict(nivel='4° Medio', letra='A', fecha_nacimiento='2009-05-10')
              if role == 'estudiante' else dict(codigo_verificacion='test-code'))
    return RegisterRequest(email=f'user{i}@example.com', password='password123',
                           nombre_completo=f'Usuario {i}', role=role,
                           establecimiento='Liceo Concurrente', **fields)


@pytest.mark.asyncio
async def test_mysql_simultaneous_students_reuse_one_course(mysql_db):
    sessions = async_sessionmaker(mysql_db, expire_on_commit=False)
    async def register(i):
        async with sessions() as db:
            await create_user(db, payload(i))
    await asyncio.gather(*(register(i) for i in range(3)))
    async with mysql_db.connect() as conn:
        assert await conn.scalar(text('SELECT COUNT(*) FROM curso')) == 1
        assert await conn.scalar(text('SELECT COUNT(*) FROM estudiante')) == 3
        assert await conn.scalar(text('SELECT COUNT(*) FROM usuario')) == 3


@pytest.mark.asyncio
async def test_mysql_concurrent_student_counselor_leaves_assigned_course(mysql_db):
    sessions = async_sessionmaker(mysql_db, expire_on_commit=False)
    async def register(i, role):
        async with sessions() as db:
            await create_user(db, payload(i, role))
    await asyncio.gather(register(1, 'orientador'), register(2, 'estudiante'))
    async with mysql_db.connect() as conn:
        assert await conn.scalar(text('SELECT COUNT(*) FROM curso WHERE orientador_id IS NOT NULL')) == 1
        assert await conn.scalar(text('SELECT COUNT(*) FROM estudiante')) == 1


@pytest.mark.asyncio
async def test_mysql_migration_preserves_legacy_rows_and_unique(mysql_db, monkeypatch):
    path = Path(__file__).parents[1] / 'alembic/versions/20260922_registro_contexto.py'
    spec = importlib.util.spec_from_file_location('registro_mysql_migration', path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    # Recrear únicamente el esquema previo en esta BD temporal recién creada.
    async with mysql_db.begin() as conn:
        for sql in [
            'ALTER TABLE curso DROP INDEX uq_curso_establecimiento_nombre',
            'ALTER TABLE orientador DROP COLUMN establecimiento',
            'ALTER TABLE estudiante DROP COLUMN fecha_nacimiento',
            "INSERT INTO usuario (id,email,hashed_password,rol,is_active) VALUES (1,'ori@example.com','unused','orientador',1),(2,'est@example.com','unused','estudiante',1)",
            "INSERT INTO orientador (id,usuario_id,nombre_completo) VALUES (1,1,'Orientador antiguo')",
            "INSERT INTO curso (id,nombre,establecimiento,orientador_id) VALUES (1,'4° Medio A','Liceo',1)",
            "INSERT INTO estudiante (id,usuario_id,nombre_completo,edad,curso_id) VALUES (1,2,'Estudiante antiguo',17,1)",
        ]:
            await conn.execute(text(sql))
    def upgrade(conn):
        monkeypatch.setattr(migration, 'op', Operations(MigrationContext.configure(conn)))
        migration.upgrade()
    async with mysql_db.begin() as conn:
        await conn.run_sync(upgrade)
        assert (await conn.execute(text('SELECT edad,fecha_nacimiento,curso_id FROM estudiante'))).one() == (17, None, 1)
        assert await conn.scalar(text('SELECT establecimiento FROM orientador')) is None
        assert await conn.scalar(text('SELECT orientador_id FROM curso')) == 1
        from sqlalchemy.exc import IntegrityError
        with pytest.raises(IntegrityError):
            await conn.execute(text("INSERT INTO curso (nombre,establecimiento) VALUES ('4° Medio A','Liceo')"))
        await conn.execute(text("INSERT INTO curso (nombre,establecimiento) VALUES ('4° Medio A','Otro Liceo')"))


@pytest.mark.asyncio
async def test_seed_is_compatible_in_disposable_mysql_only(mysql_db, monkeypatch):
    from app import seed
    # Ambos recursos se sustituyen: nunca ejecutar seed sobre el motor de desarrollo.
    monkeypatch.setattr(seed, 'engine', mysql_db)
    monkeypatch.setattr(seed, 'async_session_maker', async_sessionmaker(mysql_db))
    await seed.seed_data()
    async with mysql_db.connect() as conn:
        assert await conn.scalar(text('SELECT COUNT(*) FROM pregunta')) == 44
        assert await conn.scalar(text('SELECT COUNT(*) FROM curso c JOIN orientador o ON c.orientador_id=o.id WHERE c.establecimiento=o.establecimiento')) == 3
        assert (await conn.execute(text('SELECT edad,fecha_nacimiento FROM estudiante'))).one() == (17, None)


@pytest.mark.asyncio
async def test_mysql_twelve_simultaneous_students_reuse_course(mysql_db):
    sessions = async_sessionmaker(mysql_db, expire_on_commit=False)
    async def register(i):
        async with sessions() as db:
            await create_user(db, payload(i))
    await asyncio.gather(*(register(i) for i in range(12)))
    async with mysql_db.connect() as conn:
        assert await conn.scalar(text('SELECT COUNT(*) FROM curso')) == 1
        assert await conn.scalar(text('SELECT COUNT(*) FROM estudiante')) == 12
        assert await conn.scalar(text('SELECT COUNT(*) FROM usuario')) == 12
