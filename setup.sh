#!/usr/bin/env bash
# Prepara una base MySQL nueva para un laboratorio Vócalis. No borra contenedores ni volúmenes.
set -euo pipefail
umask 077

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" != "--isolated" || $# -ne 1 ]]; then
  echo 'Uso: VOCALIS_SETUP_MYSQL_ADMIN_URL=<URL privada> ./setup.sh --isolated' >&2
  exit 2
fi
if [[ -z "${VOCALIS_SETUP_MYSQL_ADMIN_URL:-}" ]]; then
  echo 'Falta VOCALIS_SETUP_MYSQL_ADMIN_URL (MySQL con permiso CREATE DATABASE).' >&2
  exit 2
fi
PYTHON_BIN="${VOCALIS_SETUP_PYTHON:-$ROOT_DIR/backend/venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  echo 'No se encontró el Python del backend; define VOCALIS_SETUP_PYTHON.' >&2
  exit 2
fi
STATE_DIR="$(mktemp -d /tmp/vocalis-setup.XXXXXXXX)"
export VOCALIS_SETUP_STATE_DIR="$STATE_DIR"
"$PYTHON_BIN" -B - <<'PY'
import asyncio
import os
import secrets
import shlex
from pathlib import Path
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

folder = Path(os.environ['VOCALIS_SETUP_STATE_DIR'])
admin_url = make_url(os.environ['VOCALIS_SETUP_MYSQL_ADMIN_URL'])
if admin_url.drivername != 'mysql+aiomysql':
    raise SystemExit('La URL administrativa debe usar mysql+aiomysql.')
name = 'vocalis_setup_' + uuid4().hex

async def create_database():
    engine = create_async_engine(admin_url, isolation_level='AUTOCOMMIT')
    try:
        async with engine.connect() as connection:
            await connection.execute(text(f'CREATE DATABASE `{name}` CHARACTER SET utf8mb4'))
    finally:
        await engine.dispose()

asyncio.run(create_database())
app_url = admin_url.set(database=name).render_as_string(hide_password=False)
(folder / 'database_name').write_text(name + '\n')
(folder / 'runtime.env').write_text('\n'.join(
    f'{key}={shlex.quote(value)}' for key, value in {
        'DATABASE_URL': app_url,
        'ZEEBE_GATEWAY': '127.0.0.1:26500',
        'JWT_SECRET': secrets.token_urlsafe(48),
        'ORIENTADOR_REGISTRATION_CODE': secrets.token_urlsafe(24),
    }.items()
) + '\n')
PY

# Alembic comienza sobre el esquema creado por los modelos: no existe una migración inicial completa.
set -a
# shellcheck disable=SC1090
source "$STATE_DIR/runtime.env"
set +a
cd "$ROOT_DIR/backend"
"$PYTHON_BIN" -B - <<'PY'
import asyncio
from app.database import Base, engine
from app import models  # noqa: F401 - registrar todas las tablas en Base.metadata

async def create_schema():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()

asyncio.run(create_schema())
PY
"$PYTHON_BIN" -B -m alembic upgrade head
"$PYTHON_BIN" -B -m app.seed
printf 'Base aislada preparada: %s\n' "$(cat "$STATE_DIR/database_name")"
printf 'Configuración privada (0600) para API local: %s/runtime.env\n' "$STATE_DIR"
printf 'Para ejecutar API sin recarga: cd backend && set -a && source %q/runtime.env && set +a && venv/bin/python -B -m uvicorn app.main:app --host 127.0.0.1 --port 8000\n' "$STATE_DIR"
printf 'Frontend local: npm run dev -- --host 127.0.0.1\n'
