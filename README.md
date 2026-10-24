# Vócalis — Plataforma Web de Orientación Vocacional Basada en Procesos (BPM)

**Vócalis** es una aplicación web diseñada para apoyar la gestión, continuidad y trazabilidad del proceso de orientación vocacional y autoconocimiento en estudiantes de enseñanza media en Chile. Integra la aplicación digital del cuestionario **Big Five Inventory de 44 ítems (BFI-44)** como instrumento exploratorio no determinista, centralizando resultados y estados de avance para el seguimiento de los orientadores escolares mediante orquestación real en **Camunda 8 (Zeebe)**.

---

## Arquitectura y Tecnologías

- **Frontend (`src/`):** Vue 3 (Composition API) + Vue Router 5 + Axios + Vite 8, con diseño responsivo para escritorio (`1440×900`) y dispositivos móviles (`390×844`).
- **Backend (`backend/`):** Python + FastAPI asíncrono + SQLAlchemy 2.0 (`aiomysql`) + migraciones incrementales con Alembic + autenticación JWT y Bcrypt.
- **Base de datos:** MySQL 8.0 (10 tablas normalizadas con control transaccional ACID y tabla `bpm_evento` bajo patrón *Transactional Outbox*).
- **Orquestación BPM (`bpmn/`):** Modelo BPMN 2.0 (`evaluacion-vocacional.bpmn`) ejecutado sobre **Camunda 8 / Zeebe** mediante `pyzeebe` (*job workers* integrados en el ciclo de vida de FastAPI).

---

## Estructura del Repositorio

- `src/` — Vistas, componentes reutilizables, rutas protegidas por rol, servicios HTTP y hojas de estilo responsivas.
- `backend/app/` — Modelos SQLAlchemy, esquemas Pydantic, routers REST (`auth`, `evaluacion`, `reporte`, `orientador`), motor `ocean_scorer.py`, integración `bpm_service.py` y `worker.py`.
- `backend/alembic/` — Migraciones versionadas del esquema relacional.
- `backend/tests/` — Suite automatizada de pruebas unitarias, de integración y concurrencia con `pytest`.
- `bpmn/` — Definición ejecutable del proceso BPMN 2.0 para Camunda 8.
- `tests/` — Pruebas de frontend (`tests/frontend/`, neutralidad vocacional y suites responsivas con Playwright) y validación de scripts en Windows (`tests/windows/`).
- `docs/` — Documentación del proyecto, memoria de título (`Piña_J_Proyecto_Final_2026_22-10-26.docx` y `.md`) y reporte técnico de validación (`validacion_mvp.md`).

---

## Puesta en Marcha

### Opción 1: Ejecución rápida en Windows y Red Local Wi-Fi (Camunda 8 Run)

Consulta la guía detallada en **[Vócalis en el teléfono (`MOVIL_WINDOWS.md`)](MOVIL_WINDOWS.md)**:

1. **Modo local (`http://localhost:5173/`):** ejecuta `INICIAR_PROYECTO.cmd`.
2. **Modo red local Wi-Fi (acceso desde teléfonos físicos en la misma red):** ejecuta `INICIAR_PROYECTO_WIFI.cmd` y abre la dirección `http://<IP-LAN>:5173/` mostrada en consola.
3. **Detener todos los servicios de forma segura:** ejecuta `DETENER_PROYECTO.cmd`.

### Opción 2: Entorno contenedorizado (Docker Compose + Desarrollo manual)

1. Copiar las plantillas de variables de entorno:
   ```sh
   cp .env.example .env
   cp backend/.env.example backend/.env
   ```
2. Levantar MySQL 8.0 y Camunda 8 (Zeebe / Operate):
   ```sh
   docker compose up -d
   ```
3. Instalar dependencias e iniciar el backend en `backend/`:
   ```sh
   cd backend
   python -m venv venv
   # En Linux/macOS: source venv/bin/activate | En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
4. Instalar paquetes e iniciar el frontend desde la raíz:
   ```sh
   npm ci
   npm run dev
   ```

---

## Pruebas Automatizadas y Calidad

- **Backend (`pytest`):**
  ```sh
  cd backend
  pytest tests -q
  ```
- **Frontend (neutralidad del reporte, compilación y linter):**
  ```sh
  npm test
  npm run lint
  npm run build
  ```
- **Pruebas responsivas en navegador (requiere Playwright + Chromium y servidor Vite en puerto de prueba):**
  ```sh
  npm run test:responsive
  ```
- **Pruebas del orquestador de arranque en Windows:**
  ```sh
  npm run test:windows
  ```

Para revisar el protocolo reproducible de laboratorio aislado, cobertura, tolerancia a fallos de Zeebe y prueba de carga con 30 usuarios concurrentes, consulta [`docs/validacion_mvp.md`](docs/validacion_mvp.md).
