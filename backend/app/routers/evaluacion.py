from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.schemas.evaluacion import PreguntaOut, RespuestaIn, RespuestaOut, SubmitEvaluationRequest, SubmitEvaluationResponse, EstadoEvaluacion
from app.models import Pregunta, Evaluacion, Respuesta, ReporteVocacional, Estudiante
from app.utils.dependencies import require_estudiante
from app.services.ocean_scorer import calculate_ocean_scores, get_dominant_dimensions
from app.services.bpm_service import start_process, queue_cuestionario
from app.services import bpm_service

router = APIRouter(prefix="/evaluacion", tags=["Evaluación BFI-44"])

@router.get("/preguntas", response_model=list[PreguntaOut])
async def get_preguntas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pregunta).order_by(Pregunta.orden))
    preguntas = result.scalars().all()
    # Map 'texto' to 'text'
    return [PreguntaOut(id=p.id, text=p.texto, dimension=p.dimension) for p in preguntas]

@router.get("/respuestas", response_model=list[RespuestaOut])
async def get_respuestas(estudiante: Estudiante = Depends(require_estudiante), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Respuesta)
        .join(Evaluacion, Respuesta.evaluacion_id == Evaluacion.id)
        .where(Evaluacion.estudiante_id == estudiante.id)
        .order_by(Respuesta.pregunta_id)
    )
    return [RespuestaOut(preguntaId=r.pregunta_id, valor=r.valor) for r in result.scalars().all()]

@router.post("/respuesta", response_model=RespuestaOut)
async def save_respuesta(respuesta: RespuestaIn, estudiante: Estudiante = Depends(require_estudiante), db: AsyncSession = Depends(get_db)):
    # Serializar también la creación inicial cuando aún no existe evaluación.
    await db.execute(select(Estudiante.id).where(Estudiante.id == estudiante.id).with_for_update())
    # Check if evaluacion exists
    result = await db.execute(select(Evaluacion).where(Evaluacion.estudiante_id == estudiante.id).with_for_update())
    evaluacion = result.scalar_one_or_none()
    
    if evaluacion and evaluacion.estado in ("completada", "procesada"):
        raise HTTPException(status_code=400, detail="El estudiante ya completó una evaluación")
        
    if not evaluacion:
        evaluacion = Evaluacion(estudiante_id=estudiante.id, estado="en_progreso")
        db.add(evaluacion)
        await db.flush()
        await start_process(db, evaluacion.id)
        
    # Upsert respuesta
    res_query = await db.execute(
        select(Respuesta).where(
            Respuesta.evaluacion_id == evaluacion.id,
            Respuesta.pregunta_id == respuesta.preguntaId
        )
    )
    existing_resp = res_query.scalar_one_or_none()
    if existing_resp:
        existing_resp.valor = respuesta.valor
    else:
        new_resp = Respuesta(evaluacion_id=evaluacion.id, pregunta_id=respuesta.preguntaId, valor=respuesta.valor)
        db.add(new_resp)
        
    eval_id = evaluacion.id
    await db.commit()
    await bpm_service.finish_cuestionario(db, eval_id)
    return RespuestaOut(preguntaId=respuesta.preguntaId, valor=respuesta.valor, saved=True)

@router.post("/enviar", response_model=SubmitEvaluationResponse)
async def submit_evaluation(request: SubmitEvaluationRequest, estudiante: Estudiante = Depends(require_estudiante), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Evaluacion).where(Evaluacion.estudiante_id == estudiante.id).with_for_update())
    evaluacion = result.scalar_one_or_none()
    
    if not evaluacion:
        raise HTTPException(status_code=400, detail="No hay evaluación en progreso")
    if evaluacion.estado in ("completada", "procesada"):
        raise HTTPException(status_code=400, detail="Evaluación ya completada")
        
    answers = {r.preguntaId: r.valor for r in request.respuestas}
    if len(answers) != len(request.respuestas):
        raise HTTPException(status_code=422, detail="No se permiten preguntas duplicadas")

    preg_result = await db.execute(select(Pregunta.id))
    if set(answers) != set(preg_result.scalars().all()):
        raise HTTPException(status_code=422, detail="Debes responder exactamente las preguntas existentes del BFI-44")

    try:
        scores = calculate_ocean_scores(answers)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    # El envío final validado es la fuente de verdad. Persistir ese mismo
    # conjunto y su reporte en una única transacción, sustituyendo el borrador.
    saved_result = await db.execute(select(Respuesta).where(Respuesta.evaluacion_id == evaluacion.id))
    saved = {r.pregunta_id: r for r in saved_result.scalars().all()}
    for pregunta_id, valor in answers.items():
        if pregunta_id in saved:
            saved[pregunta_id].valor = valor
        else:
            db.add(Respuesta(evaluacion_id=evaluacion.id, pregunta_id=pregunta_id, valor=valor))
    
    # Create Reporte
    reporte = ReporteVocacional(
        evaluacion_id=evaluacion.id,
        scores_json=scores
    )
    db.add(reporte)
    evaluacion.estado = "completada"
    evaluacion.completed_at = func.now()
    
    # Reporte y evento pendiente se confirman juntos. Ningún RPC precede al commit.
    await queue_cuestionario(db, evaluacion.id)
    await db.flush()
    report_id, eval_id = reporte.id, evaluacion.id
    await db.commit()
    await bpm_service.finish_cuestionario(db, eval_id)

    return SubmitEvaluationResponse(reportId=report_id, status="success")

@router.get("/estado", response_model=EstadoEvaluacion)
async def get_estado(estudiante: Estudiante = Depends(require_estudiante), db: AsyncSession = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    from app.models.curso import Curso
    
    result_est = await db.execute(
        select(Estudiante)
        .options(selectinload(Estudiante.usuario), selectinload(Estudiante.curso).selectinload(Curso.orientador))
        .where(Estudiante.id == estudiante.id)
    )
    est = result_est.scalar_one()
    
    orientador_nombre = None
    if est.curso and est.curso.orientador:
        orientador_nombre = est.curso.orientador.nombre_completo

    result = await db.execute(
        select(Evaluacion)
        .options(selectinload(Evaluacion.reporte))
        .where(Evaluacion.estudiante_id == estudiante.id)
    )
    evaluacion = result.scalar_one_or_none()
    
    registro_fecha = est.usuario.created_at
    
    if not evaluacion:
        return EstadoEvaluacion(
            tiene_evaluacion=False,
            registro_fecha=registro_fecha,
            orientador_nombre=orientador_nombre
        )
        
    from app.models.proceso_bpm import ProcesoBPM
    proc_result = await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == evaluacion.id))
    proceso = proc_result.scalar_one_or_none()
    bpm_estado = proceso.estado_actual if proceso else None
    
    
    reporte_fecha = None
    if evaluacion.reporte:
        reporte_fecha = evaluacion.reporte.created_at
        
    return EstadoEvaluacion(
        tiene_evaluacion=True,
        estado=evaluacion.estado,
        bpm_estado=bpm_estado,
        registro_fecha=registro_fecha,
        evaluacion_fecha=evaluacion.completed_at,
        reporte_fecha=reporte_fecha,
        orientador_nombre=orientador_nombre
    )
