import http from './http'

/**
 * Obtiene el reporte vocacional más reciente del estudiante autenticado.
 */
async function getLatestReport() {
  const { data } = await http.get('/evaluacion/reporte')
  return data
}

/**
 * Obtiene el reporte vocacional por su ID (para orientadores).
 */
async function getReportById(id) {
  const { data } = await http.get(`/evaluacion/reporte/${id}`)
  return data
}

export default { getLatestReport, getReportById }
