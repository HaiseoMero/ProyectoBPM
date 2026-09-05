import http from './http'

/**
 * Obtiene los 44 ítems del cuestionario.
 */
async function getQuestions() {
  const { data } = await http.get('/evaluacion/preguntas')
  return data
}

/**
 * Guarda el progreso parcial de una respuesta individual.
 */
async function saveAnswer(preguntaId, valor) {
  const { data } = await http.post('/evaluacion/respuesta', { preguntaId, valor })
  return data
}

/**
 * Envía el cuestionario completo y dispara el proceso BPM en Camunda.
 */
async function submitEvaluation(answers) {
  // Convert map {1: 5, 2: 3} to array of {preguntaId, valor}
  const respuestasArray = Object.entries(answers).map(([preguntaId, valor]) => ({
    preguntaId: parseInt(preguntaId),
    valor: parseInt(valor)
  }))
  
  const { data } = await http.post('/evaluacion/enviar', { respuestas: respuestasArray })
  return data
}

export default { getQuestions, saveAnswer, submitEvaluation }
