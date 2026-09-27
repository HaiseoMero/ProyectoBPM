import importlib.util
from pathlib import Path

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def migration_db(monkeypatch):
    path = Path(__file__).parents[1] / 'alembic/versions/20260922_registro_contexto.py'
    spec = importlib.util.spec_from_file_location('registro_migration', path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    engine = create_engine('sqlite:///:memory:')
    with engine.begin() as connection:
        for sql in [
            'CREATE TABLE orientador (id INTEGER PRIMARY KEY, nombre_completo VARCHAR(255))',
            'CREATE TABLE curso (id INTEGER PRIMARY KEY, nombre VARCHAR(100) NOT NULL, establecimiento VARCHAR(255) NOT NULL, orientador_id INTEGER REFERENCES orientador(id))',
            'CREATE TABLE estudiante (id INTEGER PRIMARY KEY, edad INTEGER NOT NULL, curso_id INTEGER REFERENCES curso(id))',
            "INSERT INTO orientador VALUES (1, 'Orientador antiguo')",
            "INSERT INTO curso VALUES (1, '4° Medio A', 'Liceo Uno', 1)",
            'INSERT INTO estudiante VALUES (1, 17, 1)',
        ]:
            connection.execute(text(sql))
        monkeypatch.setattr(migration, 'op', Operations(MigrationContext.configure(connection)))
        yield migration, connection
    engine.dispose()


def test_migration_preserves_legacy_data_and_enforces_course_unique(migration_db):
    migration, connection = migration_db
    migration.upgrade()
    migration.upgrade()  # También compatible con tablas creadas desde el modelo actualizado.
    assert connection.execute(text('SELECT edad, curso_id, fecha_nacimiento FROM estudiante')).all() == [(17, 1, None)]
    assert connection.execute(text('SELECT nombre_completo, establecimiento FROM orientador')).all() == [('Orientador antiguo', None)]
    assert connection.execute(text('SELECT orientador_id FROM curso WHERE id=1')).scalar() == 1
    with pytest.raises(IntegrityError):
        connection.execute(text("INSERT INTO curso VALUES (2, '4° Medio A', 'Liceo Uno', NULL)"))
    connection.execute(text("INSERT INTO curso VALUES (3, '4° Medio A', 'Otro Liceo', NULL)"))


def test_duplicate_courses_abort_before_any_schema_changes(migration_db):
    migration, connection = migration_db
    connection.execute(text("INSERT INTO curso VALUES (2, '4° Medio A', 'Liceo Uno', NULL)"))
    with pytest.raises(RuntimeError, match='duplicados'):
        migration.upgrade()
    assert len(inspect(connection).get_columns('estudiante')) == 3
    assert len(inspect(connection).get_columns('orientador')) == 2
    assert connection.execute(text('SELECT COUNT(*) FROM curso')).scalar() == 2
