import { mockDelay } from './mockDelay'
import { BFI44_QUESTIONS } from './bfi44Questions'
// import http from './http' // Descomentar cuando exista el backend FastAPI

/**
 * Obtiene los 44 ítems del cuestionario.
 * TODO backend: reemplazar por `const { data } = await http.get('/evaluacion/preguntas')`
 */
async function getQuestions() {
  await mockDelay(200)
  return BFI44_QUESTIONS
}

/**
 * Guarda el progreso parcial de una respuesta individual.
 * TODO backend: `await http.post('/evaluacion/respuesta', { preguntaId, valor })`
 */
async function saveAnswer(preguntaId, valor) {
  await mockDelay(80)
  return { preguntaId, valor, saved: true }
}

/**
 * Envía el cuestionario completo y dispara el proceso BPM en Camunda.
 * TODO backend: `const { data } = await http.post('/evaluacion/enviar', { respuestas })`
 * El backend debe: guardar respuestas, publicar el mensaje que avanza el
 * proceso BPMN, calcular las dimensiones OCEAN y devolver el id del reporte.
 */
async function submitEvaluation(answers) {
  await mockDelay(600)
  return { reportId: 'mock-report-id', status: 'PROCESADO' }
}

export default { getQuestions, saveAnswer, submitEvaluation }
