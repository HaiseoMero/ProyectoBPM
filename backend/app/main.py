from fastapi import FastAPI
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    worker_task = asyncio.create_task(start_worker())
    yield
    worker_task.cancel()

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
    return {"status": "ok", "service": "vocalis-api"}
