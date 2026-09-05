import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base, async_session_maker
from app.models import Curso, Orientador, Usuario, Estudiante, Pregunta
from app.utils.security import hash_password

PREGUNTAS = [
    (1, 'Es sociable, conversador y expresivo.', 'E', False),
    (2, 'Tiende a ser crítico con los demás.', 'A', True),
    (3, 'Hace un trabajo minucioso y detallado.', 'C', False),
    (4, 'Es deprimido, triste o melancólico con frecuencia.', 'N', False),
    (5, 'Es original, se le ocurren ideas nuevas continuamente.', 'O', False),
    (6, 'Es reservado, prefiere guardar las distancias.', 'E', True),
    (7, 'Es servicial, cooperador y no busca conflictos.', 'A', False),
    (8, 'Puede ser algo descuidado o desorganizado.', 'C', True),
    (9, 'Es calmado, maneja bien las situaciones de estrés.', 'N', True),
    (10, 'Tiene mucha curiosidad por temas y áreas distintas.', 'O', False),
    (11, 'Lleno de energía, es una persona muy activa.', 'E', False),
    (12, 'Inicia disputas o discusiones con facilidad.', 'A', True),
    (13, 'Es un trabajador confiable y cumple sus promesas.', 'C', False),
    (14, 'Se pone tenso o ansioso con facilidad.', 'N', False),
    (15, 'Es ingenioso, un pensador profundo.', 'O', False),
    (16, 'Genera mucho entusiasmo en los grupos.', 'E', False),
    (17, 'Tiene un corazón blando, es propenso a perdonar.', 'A', False),
    (18, 'Tiende a ser desorganizado en sus tareas escolares.', 'C', True),
    (19, 'Se preocupa mucho por cosas sin importancia.', 'N', False),
    (20, 'Tiene una imaginación muy activa y viva.', 'O', False),
    (21, 'Suele ser callado o tímido ante desconocidos.', 'E', True),
    (22, 'Tiende a confiar plenamente en las personas.', 'A', False),
    (23, 'Tiende a ser flojo o postergar los deberes.', 'C', True),
    (24, 'Es emocionalmente estable, difícil de alterar.', 'N', True),
    (25, 'Es creativo, inventa soluciones diferentes.', 'O', False),
    (26, 'Tiene una personalidad asertiva y dominante.', 'E', False),
    (27, 'Puede ser frío o distante con sus pares.', 'A', True),
    (28, 'Persevera hasta terminar los planes que empieza.', 'C', False),
    (29, 'Es temperamental, cambia de humor con rapidez.', 'N', False),
    (30, 'Valora las experiencias artísticas y estéticas.', 'O', False),
    (31, 'A veces es tímido o le cuesta tomar la iniciativa.', 'E', True),
    (32, 'Es considerado y amable con casi todo el mundo.', 'A', False),
    (33, 'Hace las cosas de manera eficiente y rápida.', 'C', False),
    (34, 'Se mantiene calmado en situaciones de alta presión.', 'N', True),
    (35, 'Prefiere trabajos rutinarios y predecibles.', 'O', True),
    (36, 'Es extrovertido, le agrada hacer amigos.', 'E', False),
    (37, 'A veces es rudo o poco empático con el resto.', 'A', True),
    (38, 'Establece planes y metas claras para su futuro.', 'C', False),
    (39, 'Se siente nervioso o inseguro de sí mismo.', 'N', False),
    (40, 'Le gusta reflexionar y jugar con ideas abstractas.', 'O', False),
    (41, 'Tiene pocos intereses artísticos o científicos.', 'O', True),
    (42, 'Le gusta cooperar en tareas comunitarias.', 'A', False),
    (43, 'Se distrae fácilmente de sus responsabilidades.', 'C', True),
    (44, 'Tiene sofisticación y buen gusto artístico.', 'O', False),
]

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session_maker() as db:
        # Preguntas
        for orden, texto, dim, inv in PREGUNTAS:
            db.add(Pregunta(orden=orden, texto=texto, dimension=dim, es_invertida=inv))
            
        # Orientador
        user_ori = Usuario(email='orientador@vocalis.cl', hashed_password=hash_password('vocalis123'), rol='orientador')
        db.add(user_ori)
        await db.flush()
        
        orientador = Orientador(usuario_id=user_ori.id, nombre_completo='Prof. María González', departamento='Orientación')
        db.add(orientador)
        await db.flush()
        
        # Cursos
        curso_a = Curso(nombre='4° Medio A', establecimiento='Liceo Demo Vócalis', orientador_id=orientador.id)
        curso_b = Curso(nombre='4° Medio B', establecimiento='Liceo Demo Vócalis', orientador_id=orientador.id)
        curso_c = Curso(nombre='4° Medio C', establecimiento='Liceo Demo Vócalis', orientador_id=orientador.id)
        db.add_all([curso_a, curso_b, curso_c])
        await db.flush()
        
        # Estudiante
        user_est = Usuario(email='estudiante@vocalis.cl', hashed_password=hash_password('vocalis123'), rol='estudiante')
        db.add(user_est)
        await db.flush()
        
        estudiante = Estudiante(usuario_id=user_est.id, nombre_completo='José Miguel Piña', edad=17, curso_id=curso_a.id)
        db.add(estudiante)
        
        await db.commit()
        print("Base de datos inicializada con éxito")

async def main():
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
