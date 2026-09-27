from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.config import settings

from app.routers.auth import router as auth_router
from app.routers.evaluacion import router as evaluacion_router
from app.routers.reporte import router as reporte_router
from app.routers.orientador import router as orientador_router

import asyncio
from app.worker import start_worker
from app.services.bpm_service import retry_pending_events, close_zeebe_client, log_event

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.background_errors = {}

    def observe(name, task):
        if task.cancelled():
            return
        exc = task.exception()
        error = type(exc).__name__ if exc else 'UnexpectedStop'
        app.state.background_errors[name] = error
        log_event('bpm_background_task_stopped', task=name, error=error)

    worker_task = asyncio.create_task(start_worker(), name='zeebe-worker')
    retry_task = asyncio.create_task(retry_pending_events(), name='bpm-retry')
    worker_task.add_done_callback(lambda task: observe('zeebe-worker', task))
    retry_task.add_done_callback(lambda task: observe('bpm-retry', task))
    try:
        yield
    finally:
        worker_task.cancel()
        retry_task.cancel()
        await asyncio.gather(worker_task, retry_task, return_exceptions=True)
        await close_zeebe_client()

app = FastAPI(
    title="Vócalis API",
    description="API del sistema de orientación vocacional",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(evaluacion_router, prefix="/api")
app.include_router(reporte_router, prefix="/api")
app.include_router(orientador_router, prefix="/api")

@app.get("/")
async def health_check():
    if getattr(app.state, 'background_errors', {}):
        raise HTTPException(status_code=503, detail='Proceso BPM no disponible')
    return {"status": "ok", "service": "vocalis-api"}
