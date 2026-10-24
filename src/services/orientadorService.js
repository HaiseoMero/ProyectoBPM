import http from './http'

/**
 * Lista los estudiantes asignados al orientador autenticado.
 */
async function getStudents() {
  const { data } = await http.get('/orientador/estudiantes')
  return data
}

async function getStudentReport(studentId) {
  const { data } = await http.get(`/orientador/estudiante/${encodeURIComponent(studentId)}/reporte`)
  return data
}

async function getUnassignedCourses() {
  const { data } = await http.get('/orientador/cursos/sin-asignar')
  return data
}

async function assignCourse(courseId) {
  const { data } = await http.post(`/orientador/cursos/${encodeURIComponent(courseId)}/asignar`)
  return data
}

export default { getStudents, getStudentReport, getUnassignedCourses, assignCourse }
