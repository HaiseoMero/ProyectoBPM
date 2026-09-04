import { mockDelay } from './mockDelay'
// import http from './http' // Descomentar cuando exista el backend FastAPI

// TODO backend: este arreglo se reemplaza por GET /api/orientador/estudiantes
const STUDENTS_SEED = [
  { id: 1, name: 'José Miguel Piña', email: 'jose.pina@vocalis.cl', course: '4° Medio A', lastUpdate: 'Hoy, 08:15 AM', bpmStatus: 'Reporte Listo', statusClass: 'success' },
  { id: 2, name: 'Valentina Silva', email: 'v.silva@alumno.cl', course: '4° Medio A', lastUpdate: 'Ayer, 16:40 PM', bpmStatus: 'Evaluación', statusClass: 'warning' },
  { id: 3, name: 'Benjamín Morales', email: 'b.morales@alumno.cl', course: '4° Medio B', lastUpdate: '17 de Jun, 2026', bpmStatus: 'Reporte Listo', statusClass: 'success' },
  { id: 4, name: 'Javiera Paz Toledo', email: 'javi.toledo@alumno.cl', course: '4° Medio C', lastUpdate: '15 de Jun, 2026', bpmStatus: 'Registro', statusClass: 'info' },
  { id: 5, name: 'Bastián Contreras', email: 'bastian.c@alumno.cl', course: '4° Medio B', lastUpdate: '11 de Jun, 2026', bpmStatus: 'Procesamiento', statusClass: 'danger' },
]

/**
 * Lista los estudiantes asignados al orientador autenticado.
 * TODO backend: `const { data } = await http.get('/orientador/estudiantes')`
 */
async function getStudents() {
  await mockDelay()
  return STUDENTS_SEED
}

export default { getStudents }
