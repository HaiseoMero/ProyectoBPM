from datetime import datetime
import pytest
from app.models import Evaluacion, ProcesoBPM
from tests.test_reportes import report_api, headers


@pytest.mark.asyncio
@pytest.mark.parametrize('state', [None, 'registro', 'calculando_ocean', 'generando_reporte', 'reporte_listo', 'desconocido'])
async def test_student_list_preserves_raw_bpm_state_and_start_date(report_api, state):
    client, sessions = report_api
    async with sessions() as db:
        (await db.get(Evaluacion, 1)).created_at = datetime(2026, 1, 15, 10, 0)
        if state is not None:
            db.add(ProcesoBPM(evaluacion_id=1, estado_actual=state, updated_at=datetime(2026, 2, 20)))
        await db.commit()
    response = await client.get('/api/orientador/estudiantes', headers=headers(10))
    assert response.status_code == 200
    students = {student['id']: student for student in response.json()}
    assert students[1]['bpm_estado'] == state
    assert students[1]['hasReport'] is True
    assert students[4]['hasReport'] is False
    assert students[5]['hasReport'] is False
    assert students[1]['lastUpdate'] == '15 de Ene, 2026'
    assert students[4]['lastUpdate'] == 'Desconocido'  # Estudiante aún sin evaluación.
    assert set(students[1]) == {'id', 'name', 'email', 'course', 'lastUpdate', 'bpm_estado', 'hasReport'}


@pytest.mark.asyncio
@pytest.mark.parametrize('state', [None, 'registro'])
async def test_saved_report_is_accessible_before_zeebe_finishes(report_api, state):
    client, sessions = report_api
    if state:
        async with sessions() as db:
            db.add(ProcesoBPM(evaluacion_id=1, estado_actual=state))
            await db.commit()
    students = (await client.get('/api/orientador/estudiantes', headers=headers(10))).json()
    assert {row['id'] for row in students} == {1, 4, 5}
    assert next(row for row in students if row['id'] == 1)['hasReport'] is True
    assert next(row for row in students if row['id'] == 1)['bpm_estado'] == state
    assert (await client.get('/api/orientador/estudiante/1/reporte', headers=headers(10))).status_code == 200
    assert (await client.get('/api/orientador/estudiante/1/reporte', headers=headers(11))).status_code == 403
