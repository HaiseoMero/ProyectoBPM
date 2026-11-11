<template>
  <div class="dashboard-layout">
    
    <DashboardNavigation
      :items="[{ label: 'Panel de alumnos', to: '/orientador/dashboard', active: true }]"
      :user-name="userName"
      user-role="Orientador(a) escolar"
      label="Navegación del orientador"
      @logout="logout"
    />

    <main class="main-content">
      <section class="panel-header-zone">
        <div class="panel-title-container">
          <span class="panel-eyebrow">Unidad de Convivencia y Orientación Escolar</span>
          <h1 class="panel-title">Panel de Gestión y Monitoreo</h1>
          <p class="panel-sub">Consulta de los estados registrados de los procesos psicométricos y flujos BPM.</p>
        </div>
      </section>

      <section class="metrics-grid">
        <div class="metric-card metric-card--total">
          <div class="metric-card__data">
            <span class="metric-num">{{ totalAlumnos }}</span>
            <span class="metric-label">Alumnos Asignados</span>
          </div>
        </div>
        <div class="metric-card metric-card--progress">
          <div class="metric-card__data">
            <span class="metric-num">{{ flujosEnCurso }}</span>
            <span class="metric-label">Flujos en procesamiento</span>
          </div>
        </div>
        <div class="metric-card metric-card--ready">
          <div class="metric-card__data">
            <span class="metric-num metric-num--success">{{ reportesListos }}</span>
            <span class="metric-label">Reportes Listos</span>
          </div>
        </div>
      </section>

      <section class="course-assignment" aria-labelledby="course-assignment-title">
        <div class="course-assignment__header">
          <h2 id="course-assignment-title">Cursos sin orientador asignado</h2>
          <button type="button" class="btn-table btn-table--primary" :disabled="loadingCourses || assigningCourseId !== null" @click="loadCourses">Actualizar cursos</button>
        </div>
        <p>Si compartes colegio con otros orientadores, coordina qué cursos atenderá cada uno. Al tomar un curso a cargo, sus estudiantes actuales y los que se registren después aparecerán en tu panel. Se conservan los cursos que ya tienen responsable.</p>
        <p v-if="courseMessage" role="status">{{ courseMessage }}</p>
        <p v-if="assignmentError" role="alert">{{ assignmentError }}</p>
        <p v-if="loadingCourses" role="status">Consultando cursos de tu establecimiento…</p>
        <p v-else-if="coursesError" role="alert">{{ coursesError }} Usa «Actualizar cursos» para reintentar.</p>
        <p v-else-if="unassignedCourses.length === 0">No hay cursos sin asignar en tu establecimiento.</p>
        <ul v-else class="unassigned-courses">
          <li v-for="course in unassignedCourses" :key="course.id">
            <span><strong>{{ course.nombre }}</strong> · {{ course.total_estudiantes }} estudiantes</span>
            <button type="button" class="btn-table btn-table--primary" :disabled="assigningCourseId !== null" :aria-label="`Tomar a cargo ${course.nombre}`" @click="assignCourse(course)">
              {{ assigningCourseId === course.id ? 'Asignando…' : 'Tomar a cargo' }}
            </button>
          </li>
        </ul>
      </section>

      <section class="filters-card">
        <div class="filters-grid">
          <div class="filter-group">
            <label for="student-search">Buscar estudiante</label>
            <input 
              id="student-search"
              v-model="filters.search" 
              type="search"
              placeholder="Ej: José Miguel Piña..." 
              class="filter-input"
            />
          </div>
          <div class="filter-group">
            <label for="student-course">Curso</label>
            <select id="student-course" v-model="filters.course" class="filter-select">
              <option value="">Todos los cursos</option>
              <option v-for="course in availableCourses" :key="course" :value="course">{{ course }}</option>
            </select>
          </div>
          <div class="filter-group">
            <label for="student-status">Estado del Flujo Camunda</label>
            <select id="student-status" v-model="filters.status" class="filter-select">
              <option value="">Todos los estados</option>
              <option v-for="step in bpmStages" :key="step.state" :value="step.state">{{ step.label }}</option>
              <option value="unavailable">Estado no disponible</option>
            </select>
          </div>
        </div>
      </section>

      <section class="table-section">
        <p v-if="loadingStudents" class="loading-text" role="status">Cargando estudiantes…</p>
        <div v-else-if="studentsError" class="loading-text" role="alert">
          <p>{{ studentsError }}</p>
          <button class="btn-table btn-table--primary" @click="loadStudents">Reintentar</button>
        </div>
        <p v-else-if="studentsPool.length === 0" class="loading-text">Todavía no tienes estudiantes asignados.</p>
        <template v-else>
        <div class="table-container">
          <table class="students-table">
            <caption class="table-caption">Estudiantes asignados y estado de su proceso</caption>
            <thead>
              <tr>
                <th scope="col">Estudiante</th>
                <th scope="col">Curso</th>
                <th scope="col">Inicio de evaluación</th>
                <th scope="col">Estado Flujo BPM</th>
                <th scope="col" style="text-align: center;">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id" class="table-row">
                <td>
                  <div class="student-profile-cell">
                    <div class="student-initials" aria-hidden="true">{{ student.name.split(' ').map(n => n[0]).join('').substring(0,2) }}</div>
                    <div class="student-meta">
                      <strong class="student-name">{{ student.name }}</strong>
                      <span class="student-email">{{ student.email }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="cell-label" aria-hidden="true">Curso</span>
                  <span class="course-tag">{{ student.course }}</span>
                </td>
                <td>
                  <span class="cell-label" aria-hidden="true">Inicio de evaluación</span>
                  <span class="date-text">{{ student.lastUpdate }}</span>
                </td>
                <td>
                  <span class="cell-label" aria-hidden="true">Estado Flujo BPM</span>
                  <span class="bpm-tag" :class="'bpm-tag--' + getBpmStatus(student.bpm_estado).statusClass">
                    {{ getBpmStatus(student.bpm_estado).label }}
                  </span>
                  <span
                    v-if="student.estado_evaluacion === 'en_progreso' && !student.hasReport"
                    class="report-unavailable"
                  >Evaluación pendiente</span>
                </td>
                <td>
                  <div class="actions-cell-buttons">
                    <button 
                      @click="viewReport(student)" 
                      class="btn-table btn-table--primary"
                      :disabled="!student.hasReport"
                      :aria-label="`Ver reporte de ${student.name}`"
                    >
                      Ver Reporte
                    </button>
                  </div>
                  <span v-if="!student.hasReport" class="report-unavailable">Reporte no disponible</span>
                </td>
              </tr>
              <tr v-if="filteredStudents.length === 0">
                <td colspan="5" class="empty-table-msg">
                  No se encontraron estudiantes que coincidan con los criterios de búsqueda establecidos.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="table-pagination-footer">
          <span class="pagination-info" role="status" aria-live="polite" aria-atomic="true">Mostrando <strong>{{ filteredStudents.length }}</strong> de <strong>{{ studentsPool.length }}</strong> alumnos registrados</span>
        </footer>
        </template>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import orientadorService from '../services/orientadorService'
import authService from '../services/authService'
import DashboardNavigation from '../components/DashboardNavigation.vue'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()

const filters = ref({
  search: '',
  course: '',
  status: ''
})

const studentsPool = ref([])
const loadingStudents = ref(true)
const studentsError = ref('')
const userName = ref('Orientador')
const unassignedCourses = ref([])
const loadingCourses = ref(true)
const coursesError = ref('')
const assigningCourseId = ref(null)
const assignmentError = ref('')
const courseMessage = ref('')

async function loadCourses() {
  loadingCourses.value = true
  coursesError.value = ''
  try {
    unassignedCourses.value = await orientadorService.getUnassignedCourses()
  } catch {
    coursesError.value = 'No se pudieron consultar los cursos.'
  } finally {
    loadingCourses.value = false
  }
}

async function assignCourse(course) {
  if (assigningCourseId.value !== null) return
  assigningCourseId.value = course.id
  assignmentError.value = ''
  courseMessage.value = ''
  try {
    await orientadorService.assignCourse(course.id)
    courseMessage.value = `Ahora tienes a cargo el curso ${course.nombre}.`
    await Promise.all([loadCourses(), loadStudents()])
  } catch (error) {
    const messages = {
      401: 'Tu sesión no es válida. Vuelve a iniciar sesión.',
      403: 'No tienes permiso para asignar cursos.',
      404: 'El curso ya no está disponible en tu establecimiento.',
      409: 'Otro orientador ya tomó este curso a cargo. La lista se ha actualizado.',
    }
    assignmentError.value = messages[error.response?.status] || 'No se pudo confirmar la asignación. Actualiza los cursos e intenta nuevamente.'
    if ([404, 409].includes(error.response?.status)) await loadCourses()
  } finally {
    assigningCourseId.value = null
  }
}

// Métricas calculadas dinámicamente desde los datos reales
const totalAlumnos = computed(() => studentsPool.value.length)

const flujosEnCurso = computed(() => {
  return studentsPool.value.filter(s => 
    s.bpm_estado === 'calculando_ocean' || s.bpm_estado === 'generando_reporte'
  ).length
})

const reportesListos = computed(() => {
  return studentsPool.value.filter(s => s.hasReport).length
})

// Cursos disponibles extraídos dinámicamente de los estudiantes
const availableCourses = computed(() => {
  const courses = new Set(studentsPool.value.map(s => s.course))
  return [...courses].sort()
})

async function loadStudents() {
  loadingStudents.value = true
  studentsError.value = ''
  try {
    studentsPool.value = await orientadorService.getStudents()
  } catch {
    studentsError.value = 'No se pudieron cargar los estudiantes. Intenta nuevamente.'
  } finally {
    loadingStudents.value = false
  }
}

onMounted(() => {
  authService.getProfile().then(profile => {
    if (profile) userName.value = profile.name
  })
  loadStudents()
  loadCourses()
})

const filteredStudents = computed(() => {
  return studentsPool.value.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(filters.value.search.toLowerCase()) || 
                          student.email.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesCourse = filters.value.course === '' || student.course === filters.value.course
    const state = getBpmStatus(student.bpm_estado).state
    const matchesStatus = filters.value.status === '' ||
      (filters.value.status === 'unavailable' ? state === null : state === filters.value.status)
    
    return matchesSearch && matchesCourse && matchesStatus
  })
})

function viewReport(student) {
  if (student.hasReport) {
    router.push({ name: 'orientador-reporte', params: { studentId: student.id } })
  }
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
.course-assignment { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px 28px; margin-bottom: 24px; text-align: left; box-shadow: var(--shadow-card); }
.course-assignment__header { display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; align-items: center; }
.course-assignment h2 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.1rem; letter-spacing: -0.01em; }
.course-assignment p { color: var(--c-muted); font-size: 0.86rem; line-height: 1.6; margin-top: 12px; }
.course-assignment .btn-table { min-height: 44px; }
.unassigned-courses { list-style: none; padding: 0; margin-top: 16px; display: grid; gap: 12px; }
.unassigned-courses li { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; padding: 14px 16px; background: var(--c-bg); border: 1px solid var(--c-border); border-radius: 12px; font-size: 0.88rem; }
/* ── Encabezado ── */
.panel-header-zone { margin-bottom: 32px; text-align: left; }
.panel-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 10px; display: block; }
.panel-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.6rem, 3vw, 2.1rem); line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 6px; }
.panel-sub { font-size: 0.9rem; color: var(--c-muted); }

/* ── Tarjetas de Métricas ── */
.metrics-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin-bottom: 32px; }
.metric-card { position: relative; background: var(--c-surface); border: 1px solid var(--c-border); padding: 24px 24px 24px 28px; border-radius: var(--r-card); display: flex; align-items: center; box-shadow: var(--shadow-card); overflow: hidden; }
/* Franja de color que distingue cada métrica */
.metric-card::before { content: ''; position: absolute; left: 0; top: 18px; bottom: 18px; width: 3px; border-radius: 0 3px 3px 0; background: var(--c-border-strong); }
.metric-card--progress::before { background: #F59E0B; }
.metric-card--ready::before { background: var(--c-primary); }
.metric-card__data { display: flex; flex-direction: column; text-align: left; }
.metric-num { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 2rem; letter-spacing: -0.02em; color: var(--c-text); line-height: 1.05; }
.metric-num--success { color: var(--c-primary); }
.metric-label { font-size: 0.82rem; font-weight: 500; color: var(--c-muted); margin-top: 6px; }

/* ── Filtros ── */
.filters-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px 28px; margin-bottom: 24px; box-shadow: var(--shadow-card); }
.filters-grid { display: grid; grid-template-columns: minmax(0, 2fr) repeat(2, minmax(0, 1fr)); gap: 20px; }
.filter-group { display: flex; flex-direction: column; min-width: 0; text-align: left; gap: 6px; }
.filter-group label { font-size: 0.82rem; font-weight: 600; color: var(--c-text); }
.filter-input, .filter-select { width: 100%; min-height: 48px; background: var(--c-surface); border: 1px solid var(--c-border-strong); border-radius: 12px; padding: 12px 14px; font-size: 0.9rem; color: var(--c-text); outline: none; font-family: 'Inter', sans-serif; transition: border-color 0.2s, box-shadow 0.2s; }
.filter-input::placeholder { color: #94A3B8; }
.filter-input:focus, .filter-select:focus { border-color: var(--c-primary); box-shadow: var(--ring); }

/* ── Tabla (Bug Solucionado agregando padding exacto a las celdas td) ── */
.table-section { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); overflow: hidden; box-shadow: var(--shadow-card); }
.table-container { overflow-x: auto; }
.loading-text { padding: 40px 20px; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.loading-text .btn-table { margin-top: 16px; }
.table-caption { position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
.cell-label { display: none; }
.report-unavailable { display: block; margin-top: 6px; color: var(--c-muted); font-size: 0.78rem; }
.students-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left; }

.students-table th { 
  background: var(--c-bg); 
  padding: 14px 20px; 
  font-weight: 700; 
  color: var(--c-muted); 
  border-bottom: 1px solid var(--c-border); 
  font-size: 0.72rem; 
  text-transform: uppercase; 
  letter-spacing: 0.08em; 
}

/* El arreglo crítico de espacio se aplica aquí */
.students-table td { 
  padding: 16px 20px; 
  vertical-align: middle;
}

.table-row { border-bottom: 1px solid var(--c-border); transition: background 0.15s; }
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: var(--c-bg); }

/* Celda interna de perfil de estudiante */
.student-profile-cell { display: flex; align-items: center; gap: 14px; }
.student-initials { width: 38px; height: 38px; background: var(--c-tint); border: 1px solid var(--c-tint-border); color: var(--c-primary); font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.78rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.student-meta { display: flex; flex-direction: column; min-width: 0; text-align: left; overflow-wrap: anywhere; }
.student-name { font-size: 0.92rem; color: var(--c-text); }
.student-email { font-size: 0.78rem; color: var(--c-muted); }

.course-tag { display: inline-block; background: var(--c-bg); border: 1px solid var(--c-border); color: var(--c-text-soft); padding: 4px 10px; border-radius: 8px; font-weight: 600; font-size: 0.8rem; }
.date-text { color: var(--c-muted); font-size: 0.85rem; }

/* Estados del flujo */
/* Estado con punto de color: legible sin depender solo del fondo */
.bpm-tag { font-size: 0.78rem; font-weight: 600; padding: 5px 12px 5px 10px; border-radius: 100px; display: inline-flex; align-items: center; gap: 8px; overflow-wrap: anywhere; border: 1px solid; }
.bpm-tag::before { content: ''; flex: 0 0 7px; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.bpm-tag--success { background: var(--c-tint); color: var(--c-primary-strong); border-color: var(--c-tint-border); }
.bpm-tag--warning { background: var(--c-warning-bg); color: var(--c-warning); border-color: var(--c-warning-border); }
.bpm-tag--info { background: var(--c-info-bg); color: var(--c-info); border-color: var(--c-info-border); }
.bpm-tag--danger { background: var(--c-danger-bg); color: var(--c-danger); border-color: var(--c-danger-border); }

/* Botones de acción */
.actions-cell-buttons { display: flex; gap: 8px; }
.btn-table { padding: 8px 16px; border-radius: 100px; font-weight: 600; font-size: 0.82rem; cursor: pointer; border: 1px solid transparent; transition: background-color 0.2s; font-family: 'Inter', sans-serif; }
.btn-table--primary { background: var(--c-primary); color: #FFFFFF; }
.btn-table--primary:hover:not(:disabled) { background: var(--c-primary-strong); }
.btn-table--primary:disabled { background: #F1F5F9; border-color: var(--c-border); color: #94A3B8; cursor: not-allowed; }

/* Paginación de pie de tabla */
.table-pagination-footer { padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; background: var(--c-bg); border-top: 1px solid var(--c-border); }
.pagination-info { font-size: 0.82rem; color: var(--c-muted); }

.empty-table-msg { text-align: center; color: var(--c-muted); font-style: italic; padding: 40px !important; }

@media (max-width: 1200px) {
  .filters-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .filter-group:first-child { grid-column: 1 / -1; }
}
@media (max-width: 1100px) {
  .table-container { overflow: visible; padding: 16px; }
  .students-table { display: block; }
  .students-table thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
  .students-table tbody { display: grid; gap: 16px; }
  .students-table tr { display: block; min-width: 0; }
  .table-row, .table-row:last-child { padding: 16px; border: 1px solid var(--c-border); border-radius: 14px; }
  .students-table td { display: block; padding: 0; }
  .students-table td + td { margin-top: 12px; }
  .cell-label { display: block; margin-bottom: 4px; font-size: 0.75rem; font-weight: 700; color: var(--c-muted); }
  .actions-cell-buttons .btn-table { width: 100%; min-height: 48px; }
  .empty-table-msg { padding: 16px !important; }
}
@media (max-width: 900px) {
  .filter-input, .filter-select { font-size: 16px; }
}
@media (max-width: 600px) {
  .panel-title { font-size: 1.5rem; }
  .metrics-grid, .filters-grid { grid-template-columns: 1fr; gap: 12px; }
  .metric-card { padding: 16px 20px; }
  .metric-card__data { width: 100%; flex-direction: row; align-items: center; gap: 16px; }
  .metric-num { min-width: 2ch; }
  .metric-label { margin-top: 0; }
  .filters-card { padding: 20px; }
  .table-container, .table-pagination-footer { padding: 12px; }
  .table-pagination-footer { text-align: left; }
}
@media (prefers-reduced-motion: reduce) {
  .table-row, .btn-table, .filter-input, .filter-select { transition: none; }
}
</style>
