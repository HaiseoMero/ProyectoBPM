<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div class="sidebar__brand">
        <span class="sidebar__logo-icon">◈</span>
        <span class="sidebar__logo-text">Vócalis</span>
      </div>
      
      <nav class="sidebar__nav">
        <a href="#" class="sidebar__link sidebar__link--active">
          Panel de Alumnos
        </a>
        <a href="#" @click.prevent="showFeatureAlert" class="sidebar__link">
          Estadísticas Globales
        </a>
        <a href="#" @click.prevent="showFeatureAlert" class="sidebar__link">
          Mi Unidad (BPM)
        </a>
      </nav>

      <div class="sidebar__footer">
        <div class="user-avatar-zone">
          <div class="avatar avatar--admin">LC</div>
          <div class="user-info">
            <span class="user-name">Prof. Lismary C.</span>
            <span class="user-role">Orientadora Escolar</span>
          </div>
        </div>
        <a href="#" @click.prevent="logout" class="logout-btn">
          Cerrar Sesión
        </a>
      </div>
    </aside>

    <main class="main-content">
      
      <section class="panel-header-zone">
        <div class="panel-title-container">
          <span class="panel-eyebrow">Unidad de Convivencia y Orientación Escolar</span>
          <h1 class="panel-title">Panel de Gestión y Monitoreo</h1>
          <p class="panel-sub">Auditoría en tiempo real de los procesos psicométricos y flujos de negocio Camunda 8.</p>
        </div>
      </section>

      <section class="metrics-grid">
        <div class="metric-card">
          <div class="metric-card__data">
            <span class="metric-num">142</span>
            <span class="metric-label">Alumnos Asignados</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-card__data">
            <span class="metric-num">38</span>
            <span class="metric-label">Flujos en Evaluación</span>
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-card__data">
            <span class="metric-num" style="color: #10B981;">104</span>
            <span class="metric-label">Reportes Listos</span>
          </div>
        </div>
      </section>

      <section class="filters-card">
        <div class="filters-grid">
          <div class="filter-group">
            <label>Buscar estudiante</label>
            <input 
              v-model="filters.search" 
              type="text" 
              placeholder="Ej: José Miguel Piña..." 
              class="filter-input"
            />
          </div>
          <div class="filter-group">
            <label>Curso</label>
            <select v-model="filters.course" class="filter-select">
              <option value="">Todos los cursos</option>
              <option value="4° Medio A">4° Medio A</option>
              <option value="4° Medio B">4° Medio B</option>
              <option value="4° Medio C">4° Medio C</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Estado del Flujo Camunda</label>
            <select v-model="filters.status" class="filter-select">
              <option value="">Todos los estados</option>
              <option value="Registro">Registro</option>
              <option value="Evaluación">Evaluación</option>
              <option value="Procesamiento">Procesamiento</option>
              <option value="Reporte Listo">Reporte Listo</option>
            </select>
          </div>
        </div>
      </section>

      <section class="table-section">
        <p v-if="loadingStudents" class="loading-text">Cargando estudiantes…</p>
        <template v-else>
        <div class="table-container">
          <table class="students-table">
            <thead>
              <tr>
                <th>Estudiante</th>
                <th>Curso</th>
                <th>Última Actualización</th>
                <th>Estado Flujo BPM</th>
                <th style="text-align: center;">Acciones de Ingeniería</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id" class="table-row">
                <td>
                  <div class="student-profile-cell">
                    <div class="student-initials">{{ student.name.split(' ').map(n => n[0]).join('').substring(0,2) }}</div>
                    <div class="student-meta">
                      <strong class="student-name">{{ student.name }}</strong>
                      <span class="student-email">{{ student.email }}</span>
                    </div>
                  </div>
                </td>
                <td><span class="course-tag">{{ student.course }}</span></td>
                <td><span class="date-text">{{ student.lastUpdate }}</span></td>
                <td>
                  <span class="bpm-tag" :class="'bpm-tag--' + student.statusClass">
                    {{ student.bpmStatus }}
                  </span>
                </td>
                <td>
                  <div class="actions-cell-buttons">
                    <button @click="auditAnswers(student.name)" class="btn-table btn-table--ghost">
                      Auditar
                    </button>
                    <button 
                      @click="viewReport(student)" 
                      class="btn-table btn-table--primary"
                      :disabled="student.bpmStatus !== 'Reporte Listo'"
                    >
                      Ver Reporte
                    </button>
                  </div>
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
          <span class="pagination-info">Mostrando <strong>{{ filteredStudents.length }}</strong> de <strong>{{ studentsPool.length }}</strong> alumnos registrados</span>
          <div class="pagination-buttons">
            <button class="btn-page" disabled>Anterior</button>
            <button class="btn-page btn-page--active">1</button>
            <button class="btn-page" disabled>Siguiente</button>
          </div>
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

const router = useRouter()

const filters = ref({
  search: '',
  course: '',
  status: ''
})

const studentsPool = ref([])
const loadingStudents = ref(true)

onMounted(async () => {
  studentsPool.value = await orientadorService.getStudents()
  loadingStudents.value = false
})

const filteredStudents = computed(() => {
  return studentsPool.value.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(filters.value.search.toLowerCase()) || 
                          student.email.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesCourse = filters.value.course === '' || student.course === filters.value.course
    const matchesStatus = filters.value.status === '' || student.bpmStatus === filters.value.status
    
    return matchesSearch && matchesCourse && matchesStatus
  })
})

function auditAnswers(studentName) {
  alert(`Abriendo visor de auditoría histórica para: ${studentName}.`)
}

function viewReport(student) {
  if (student.bpmStatus === 'Reporte Listo') {
    router.push({ path: '/estudiante/reporte', query: { studentId: student.id } })
  }
}

function showFeatureAlert() {
  alert('Esta sección corresponde al panel extendido del Administrador, proyectada como una mejora futura.')
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
/* ── Variables de Entorno y Colores ── */
.dashboard-layout {
  --sidebar-w:  260px;
  --c-bg:       #F8FAFC;
  --c-surface:  #FFFFFF;
  --c-primary:  #4F46E5;
  --c-border:   #E2E8F0;
  --c-text:     #0F172A;
  --c-muted:    #64748B;
  --r-card:     16px;

  min-height: 100vh;
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  display: flex;
}

/* ── Sidebar ── */
.sidebar {
  width: var(--sidebar-w);
  background: var(--c-surface);
  border-right: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; bottom: 0; left: 0;
  padding: 32px 24px;
  z-index: 50;
}
.sidebar__brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  margin-bottom: 40px;
}
.sidebar__logo-icon { color: var(--c-primary); }
.sidebar__nav { display: flex; flex-direction: column; gap: 8px; flex: 1; }
.sidebar__link { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; color: var(--c-muted); text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }
.sidebar__link:hover, .sidebar__link--active { background: #EEF2FF; color: var(--c-primary); }
.sidebar__footer { border-top: 1px solid var(--c-border); padding-top: 20px; display: flex; flex-direction: column; gap: 16px; }
.user-avatar-zone { display: flex; align-items: center; gap: 12px; }
.avatar { width: 40px; height: 40px; background: #C7D2FE; color: var(--c-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; }
.avatar--admin { background: #FEE2E2; color: #EF4444; }
.user-info { display: flex; flex-direction: column; text-align: left; }
.user-name { font-weight: 600; font-size: 0.88rem; }
.user-role { font-size: 0.75rem; color: var(--c-muted); }
.logout-btn { color: #EF4444; text-decoration: none; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; padding: 8px; border-radius: 8px; text-align: left; }
.logout-btn:hover { background: #FEF2F2; }

/* ── Margen del Contenido con Separación Corregida ── */
.main-content {
  flex: 1;
  margin-left: calc(var(--sidebar-w) + 32px);
  padding: 40px 48px;
  max-width: 1150px;
}

/* ── Encabezado ── */
.panel-header-zone { margin-bottom: 32px; text-align: left; }
.panel-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 4px; display: block; }
.panel-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.8rem; margin-bottom: 4px; }
.panel-sub { font-size: 0.9rem; color: var(--c-muted); }

/* ── Tarjetas de Métricas ── */
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 32px; }
.metric-card { background: var(--c-surface); border: 1px solid var(--c-border); padding: 24px; border-radius: var(--r-card); display: flex; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.01); }
.metric-card__data { display: flex; flex-direction: column; text-align: left; }
.metric-num { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.7rem; color: var(--c-text); line-height: 1.1; }
.metric-label { font-size: 0.8rem; font-weight: 600; color: var(--c-muted); margin-top: 2px; }

/* ── Filtros ── */
.filters-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px; margin-bottom: 24px; }
.filters-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 20px; }
.filter-group { display: flex; flex-direction: column; text-align: left; gap: 6px; }
.filter-group label { font-size: 0.78rem; font-weight: 700; color: var(--c-muted); text-transform: uppercase; letter-spacing: 0.02em; }
.filter-input, .filter-select { background: #F8FAFC; border: 1px solid var(--c-border); border-radius: 10px; padding: 12px 14px; font-size: 0.88rem; color: var(--c-text); outline: none; font-family: 'Inter', sans-serif; }
.filter-input:focus, .filter-select:focus { border-color: var(--c-primary); background: #FFFFFF; box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1); }

/* ── Tabla (Bug Solucionado agregando padding exacto a las celdas td) ── */
.table-section { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.01); }
.table-container { overflow-x: auto; }
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.students-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left; }

.students-table th { 
  background: #F8FAFC; 
  padding: 16px 20px; 
  font-weight: 700; 
  color: var(--c-muted); 
  border-bottom: 1px solid var(--c-border); 
  font-size: 0.8rem; 
  text-transform: uppercase; 
  letter-spacing: 0.04em; 
}

/* El arreglo crítico de espacio se aplica aquí */
.students-table td { 
  padding: 16px 20px; 
  vertical-align: middle;
}

.table-row { border-bottom: 1px solid var(--c-border); transition: background 0.15s; }
.table-row:hover { background: #F8FAFC; }

/* Celda interna de perfil de estudiante */
.student-profile-cell { display: flex; align-items: center; gap: 14px; }
.student-initials { width: 38px; height: 38px; background: #EEF2FF; color: var(--c-primary); font-weight: 700; font-size: 0.8rem; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.student-meta { display: flex; flex-direction: column; text-align: left; }
.student-name { font-size: 0.92rem; color: var(--c-text); }
.student-email { font-size: 0.78rem; color: var(--c-muted); }

.course-tag { background: #F1F5F9; color: #475569; padding: 4px 10px; border-radius: 8px; font-weight: 600; font-size: 0.8rem; }
.date-text { color: var(--c-muted); font-size: 0.85rem; }

/* Estados del flujo */
.bpm-tag { font-size: 0.78rem; font-weight: 700; padding: 6px 12px; border-radius: 8px; display: inline-flex; align-items: center; }
.bpm-tag--success { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
.bpm-tag--warning { background: #FFFBEB; color: #92400E; border: 1px solid #FDE68A; }
.bpm-tag--info { background: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; }
.bpm-tag--danger { background: #FFF1F2; color: #9F1239; border: 1px solid #FECDD3; }

/* Botones de acción */
.actions-cell-buttons { display: flex; gap: 8px; }
.btn-table { padding: 8px 14px; border-radius: 8px; font-weight: 600; font-size: 0.8rem; cursor: pointer; border: none; transition: all 0.2s; font-family: 'Inter', sans-serif; }
.btn-table--ghost { background: #FFFFFF; color: var(--c-muted); border: 1px solid var(--c-border); }
.btn-table--ghost:hover { border-color: var(--c-primary); color: var(--c-primary); background: #EEF2FF; }
.btn-table--primary { background: var(--c-primary); color: #FFFFFF; }
.btn-table--primary:hover:not(:disabled) { background: #4338CA; transform: translateY(-1px); }
.btn-table--primary:disabled { background: #F1F5F9; color: #CBD5E1; cursor: not-allowed; }

/* Paginación de pie de tabla */
.table-pagination-footer { padding: 16px 20px; display: flex; justify-content: space-between; align-items: center; background: #FFFFFF; border-top: 1px solid var(--c-border); }
.pagination-info { font-size: 0.82rem; color: var(--c-muted); }
.pagination-buttons { display: flex; gap: 6px; }
.btn-page { background: #FFFFFF; border: 1px solid var(--c-border); color: var(--c-muted); padding: 6px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; cursor: pointer; }
.btn-page--active { background: var(--c-primary); color: #FFFFFF; border-color: var(--c-primary); }

.empty-table-msg { text-align: center; color: var(--c-muted); font-style: italic; padding: 40px !important; }

@media (max-width: 900px) {
  .sidebar { display: none; }
  .main-content { margin-left: 0; padding: 20px; }
  .metrics-grid, .filters-grid { grid-template-columns: 1fr; }
  .actions-cell-buttons { flex-direction: column; }
}
</style>