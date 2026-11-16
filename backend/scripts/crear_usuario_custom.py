import asyncio
from sqlalchemy import select, func
from app.database import async_session_maker
from app.models.usuario import Usuario, RolEnum
from app.models.estudiante import Estudiante
from app.models.curso import Curso
from app.models.evaluacion import Evaluacion, EstadoEvaluacion
from app.models.respuesta import Respuesta
from app.models.reporte import ReporteVocacional
from app.models.pregunta import Pregunta
from app.services.auth_service import hash_password
from app.services.ocean_scorer import (
    calculate_ocean_scores,
    calcular_porcentajes_bfi44,
    evaluar_perfil_vocacional,
)

respuestas_raw = [
    3, 4, 4, 4, 4,
    3, 5, 4, 3, 5,
    3, 4, 4, 5, 5,
    3, 2, 3, 5, 4,
    5, 3, 3, 3, 4,
    3, 3, 4, 4, 5,
    4, 3, 3, 3, 4,
    3, 3, 5, 5, 5,
    5, 4, 5, 5
]

async def crear_cuenta():
    async with async_session_maker() as db:
        stmt = select(Curso).where(Curso.nombre == '4° Medio A')
        curso = (await db.execute(stmt)).scalars().first()
        if not curso:
            stmt = select(Curso)
            curso = (await db.execute(stmt)).scalars().first()
        
        email = 'estudiante.bfi44@prueba.cl'
        stmt_u = select(Usuario).where(Usuario.email == email)
        u_existente = (await db.execute(stmt_u)).scalars().first()
        if u_existente:
            email = 'estudiante.bfi44_nuevo@prueba.cl'

        usuario = Usuario(
            email=email,
            hashed_password=hash_password('prueba123'),
            rol=RolEnum.estudiante
        )
        db.add(usuario)
        await db.flush()

        estudiante = Estudiante(
            usuario_id=usuario.id,
            nombre_completo='Estudiante Vocacional',
            edad=17,
            curso_id=curso.id if curso else None
        )
        db.add(estudiante)
        await db.flush()

        evaluacion = Evaluacion(
            estudiante_id=estudiante.id,
            estado=EstadoEvaluacion.completada,
            completed_at=func.now()
        )
        db.add(evaluacion)
        await db.flush()

        preguntas_res = (await db.execute(select(Pregunta).order_by(Pregunta.orden))).scalars().all()
        
        respuestas_por_orden = {}
        for idx, valor in enumerate(respuestas_raw, start=1):
            respuestas_por_orden[idx] = valor
            p = next((pr for pr in preguntas_res if pr.orden == idx), None)
            if p:
                r = Respuesta(
                    evaluacion_id=evaluacion.id,
                    pregunta_id=p.id,
                    valor=valor
                )
                db.add(r)

        scores = calculate_ocean_scores(respuestas_por_orden)
        porcentajes = calcular_porcentajes_bfi44(respuestas_por_orden)
        perfil = evaluar_perfil_vocacional(porcentajes)
        div = perfil["divisiones"]

        reporte = ReporteVocacional(
            evaluacion_id=evaluacion.id,
            scores_json=scores,
            div_o=div["O"],
            div_c=div["C"],
            div_e=div["E"],
            div_a=div["A"],
            div_n=div["N"],
            combinacion_id=perfil["combinacion_id"],
        )
        db.add(reporte)
        await db.commit()

        print("=== CUENTA CREADA EXITOSAMENTE ===")
        print(f"Email: {email}")
        print("Password: prueba123")
        print(f"Combinacion ID: #{perfil['combinacion_id']} de 1,024 (Codigo Base 4: {perfil['combinacion_codigo']})")
        print("Puntajes OCEAN (Porcentajes 0-100%):")
        for dim, info in scores.items():
            pct = info.get("porcentaje", info.get("score"))
            lbl = info.get("division_label", "")
            print(f"  - {dim}: {pct}% ({lbl})")
        
        ranking = perfil.get("ranking_areas", [])
        if ranking:
            print("Top 3 Areas Recomendadas:")
            for a in ranking[:3]:
                print(f"  * {a['nombre']} ({a['similitud']}%)")

if __name__ == "__main__":
    asyncio.run(crear_cuenta())
