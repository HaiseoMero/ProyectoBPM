import importlib.util
from pathlib import Path

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def migration_db(monkeypatch):
    path = Path(__file__).parents[1] / "alembic/versions/20260922_unique_evaluacion_estudiante.py"
    spec = importlib.util.spec_from_file_location("evaluacion_unique_migration", path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text(
            "CREATE TABLE evaluacion (id INTEGER PRIMARY KEY, estudiante_id INTEGER NOT NULL)"
        ))
        monkeypatch.setattr(migration, "op", Operations(MigrationContext.configure(connection)))
        yield migration, connection
    engine.dispose()


def test_upgrade_preserves_data_and_rejects_second_evaluation(migration_db):
    migration, connection = migration_db
    connection.execute(text("INSERT INTO evaluacion VALUES (1, 10), (2, 20)"))
    migration.upgrade()
    assert connection.execute(text("SELECT * FROM evaluacion ORDER BY id")).all() == [(1, 10), (2, 20)]
    with pytest.raises(IntegrityError):
        connection.execute(text("INSERT INTO evaluacion VALUES (3, 10)"))
    connection.execute(text("INSERT INTO evaluacion VALUES (4, 30)"))
    migration.downgrade()
    connection.execute(text("INSERT INTO evaluacion VALUES (5, 10)"))


def test_upgrade_aborts_without_changing_duplicate_data(migration_db):
    migration, connection = migration_db
    connection.execute(text("INSERT INTO evaluacion VALUES (1, 10), (2, 10)"))
    with pytest.raises(RuntimeError, match="varias evaluaciones"):
        migration.upgrade()
    assert connection.execute(text("SELECT * FROM evaluacion ORDER BY id")).all() == [(1, 10), (2, 10)]
    assert inspect(connection).get_unique_constraints("evaluacion") == []


def test_upgrade_does_not_duplicate_existing_constraint(migration_db):
    migration, connection = migration_db
    migration.upgrade()
    migration.upgrade()
    assert len(inspect(connection).get_unique_constraints("evaluacion")) == 1
