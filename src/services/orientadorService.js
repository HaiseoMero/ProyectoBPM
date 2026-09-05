import http from './http'

/**
 * Lista los estudiantes asignados al orientador autenticado.
 */
async function getStudents() {
  const { data } = await http.get('/orientador/estudiantes')
  return data
}

export default { getStudents }
