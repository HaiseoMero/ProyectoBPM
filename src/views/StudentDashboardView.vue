<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div class="sidebar__brand">
        <span class="sidebar__logo-icon">◈</span>
        <span class="sidebar__logo-text">Vócalis</span>
      </div>
      
      <nav class="sidebar__nav">
        <a href="#" 
           class="sidebar__link" 
           :class="{ 'sidebar__link--active': currentTab === 'dashboard' }"
           @click.prevent="currentTab = 'dashboard'">
          Dashboard
        </a>
        <a href="#" 
           class="sidebar__link" 
           :class="{ 'sidebar__link--active': currentTab === 'history' }"
           @click.prevent="currentTab = 'history'">
          Bitácora de Proceso
        </a>
      </nav>

      <div class="sidebar__footer">
        <div class="user-avatar-zone">
          <div class="avatar">{{ studentInitials }}</div>
          <div class="user-info">
            <span class="user-name">{{ studentName || 'Estudiante' }}</span>
            <span class="user-role">Estudiante</span>
          </div>
        </div>
        <a href="#" @click.prevent="logout" class="logout-btn">
          Cerrar Sesión
        </a>
      </div>
    </aside>

    <main class="main-content">
      <nav class="mobile-nav" aria-label="Navegación del estudiante">
        <button type="button" @click="currentTab = 'dashboard'">Dashboard</button>
        <button type="button" @click="currentTab = 'history'">Bitácora</button>
        <button type="button" @click="logout">Cerrar Sesión</button>
      </nav>
      
      <header class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Estado BPM registrado</span>
          <span class="bpm-status-text">Estado actual: <strong>{{ currentBpmStageText }}</strong></span>
        </div>
        
        <div class="bpm-steps">
          <div 
            v-for="(step, index) in bpmStages" 
            :key="index" 
            class="bpm-step"
            :class="{ 
              'bpm-step--completed': index < currentBpmStageIndex, 
              'bpm-step--active': index === currentBpmStageIndex 
            }"
          >
            <div class="bpm-step__node">
              <span v-if="index < currentBpmStageIndex">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="bpm-step__label">{{ step.label }}</span>
            <div v-if="index < bpmStages.length - 1" class="bpm-step__line"></div>
          </div>
        </div>
      </header>

      <section class="welcome-section">
        <h1 class="welcome-title">¡Hola de nuevo, {{ studentName || 'Estudiante' }}!</h1>
        <p class="welcome-sub">Estudiante · Plataforma Vócalis</p>
        <p v-if="orientadorName" class="welcome-orientador">Tu orientador/a: <strong>{{ orientadorName }}</strong></p>
      </section>

      <p v-if="!loading && loadError" class="action-card__desc" role="alert">{{ loadError }}</p>

      <div v-show="currentTab === 'dashboard'" class="dashboard-grid">
        
        <div v-if="loading" class="action-card">
          <div class="action-card__info">
            <p class="action-card__desc" role="status">Cargando tus datos…</p>
          </div>
        </div>

        <div v-else-if="!report && !hasPreviousTest && !loadError" class="action-card action-card--start">
          <div class="action-card__info">
            <span class="action-card__badge">Disponible ahora</span>
            <h2 class="action-card__title">El cuestionario BFI-44 está disponible</h2>
            <p class="action-card__desc">Aún no hay un reporte disponible.</p>
            <p class="action-card__desc">
              Responde 44 afirmaciones sobre cómo te describes habitualmente. Los resultados muestran dimensiones de personalidad para apoyar tu reflexión.
            </p>
            <p class="action-card__warning">
              ⚡ 44 afirmaciones · sin límite de tiempo · un envío final
            </p>
            <button @click="startTest" class="btn btn--primary">
              Iniciar cuestionario BFI-44
            </button>
          </div>
          <div class="action-card__visual">
            <div class="visual-circle">◈</div>
          </div>
        </div>

        <div v-else-if="report" class="action-card action-card--report">
          <div class="action-card__info">
            <span class="action-card__badge action-card__badge--success">Reporte disponible</span>
            <h2 class="action-card__title">Reporte generado</h2>
            <p v-if="report.careerAreas.length" class="action-card__desc">
              Áreas para explorar incluidas en tu reporte:
              <strong>{{ report.careerAreas.map(area => area.title).join(', ') }}</strong>.
            </p>
            <p v-if="report.careerAreas.length" class="action-card__warning" role="note">
              Estas áreas son referencias exploratorias del prototipo; los resultados BFI-44 no evalúan tus aptitudes ni determinan una carrera.
            </p>
            <p v-else class="action-card__desc">El reporte no incluye áreas profesionales.</p>
            <div class="report-quick-stats">
              <div v-for="dimension in report.dimensions" :key="dimension.letter" class="q-stat">
                <span>{{ dimension.letter }}</span> {{ dimension.name }}: {{ dimension.score }}%
              </div>
            </div>
            <button @click="viewLatestReport" class="btn btn--primary">
              Ver Reporte Completo
            </button>
          </div>
        </div>

        <div v-else-if="!loadError" class="action-card action-card--report">
          <div class="action-card__info">
            <h2 class="action-card__title">Reporte no disponible</h2>
            <p class="action-card__desc">Tu cuestionario está completado, pero aún no hay un reporte disponible.</p>
          </div>
        </div>

        <div class="info-sidebar">
          <div class="info-mini-card">
            <div>
              <h4 class="mini-card__title">Antes de responder</h4>
              <p class="mini-card__desc">Responde con sinceridad. No hay respuestas correctas ni perfiles mejores que otros.</p>
            </div>
          </div>

          <div class="info-mini-card">
            <div>
              <h4 class="mini-card__title">Modelo Psicométrico</h4>
              <p class="mini-card__desc">
                El BFI-44 describe cinco dimensiones de personalidad. Sus puntajes no determinan aptitud, éxito académico ni una carrera adecuada.
              </p>
            </div>
          </div>
        </div>

      </div>

      <section v-show="currentTab === 'history'" class="history-section" id="history-section">
        <h3 class="history-title">Bitácora de mi Proceso</h3>
        
        <div class="timeline-container">
          <div v-if="timeline.registro" class="timeline-item">
            <div class="timeline-dot timeline-dot--completed"></div>
            <div class="timeline-content">
              <h4>Registro en plataforma</h4>
              <p>Te registraste el {{ formatDate(timeline.registro) }}</p>
            </div>
          </div>
          
          <div v-if="timeline.evaluacion" class="timeline-item">
            <div class="timeline-dot timeline-dot--completed"></div>
            <div class="timeline-content">
              <h4>Cuestionario finalizado</h4>
              <p>Completaste el cuestionario el {{ formatDate(timeline.evaluacion) }}</p>
            </div>
          </div>
          
          <div v-if="timeline.reporte" class="timeline-item">
            <div class="timeline-dot timeline-dot--completed"></div>
            <div class="timeline-content">
              <h4>Reporte generado</h4>
              <p>Tu reporte fue generado el {{ formatDate(timeline.reporte) }}</p>
            </div>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authService from '../services/authService'
import evaluacionService from '../services/evaluacionService'
import reporteService from '../services/reporteService'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()
const route = useRoute()

// Pestaña actual de la interfaz
const currentTab = ref('dashboard')
watch(() => route.hash, hash => {
  currentTab.value = hash === '#history-section' ? 'history' : 'dashboard'
}, { immediate: true })

// Estado de la evaluación desde backend
const hasPreviousTest = ref(false)
const bpmState = ref(null)
const orientadorName = ref(null)
const studentName = ref('')
const studentInitials = computed(() => studentName.value.split(/\s+/).filter(Boolean)
  .slice(0, 2).map(part => Array.from(part)[0]).join('').toUpperCase() || '—')
const report = ref(null)
const loading = ref(true)
const loadError = ref('')
const timeline = ref({
  registro: null,
  evaluacion: null,
  reporte: null
})

onMounted(async () => {
  const [profileResult, estadoResult, reportResult] = await Promise.allSettled([
    authService.getProfile(),
    evaluacionService.getEstado(),
    reporteService.getLatestReport()
  ])
  if (profileResult.status === 'fulfilled') {
    studentName.value = profileResult.value?.name?.trim() || ''
  }

  if (estadoResult.status === 'fulfilled') {
    const estado = estadoResult.value
    bpmState.value = estado.bpm_estado ?? null
    hasPreviousTest.value = estado.tiene_evaluacion && ['completada', 'procesada'].includes(estado.estado)
    orientadorName.value = estado.orientador_nombre
    
    timeline.value.registro = estado.registro_fecha
    timeline.value.evaluacion = estado.evaluacion_fecha
    timeline.value.reporte = estado.reporte_fecha
  } else {
    loadError.value = 'No se pudo cargar el estado de tu evaluación. Intenta recargar la página.'
  }

  if (reportResult.status === 'fulfilled') {
    report.value = reportResult.value
  } else if (reportResult.reason.response?.status !== 404) {
    loadError.value = [loadError.value, 'No se pudo consultar tu reporte. Intenta recargar la página.'].filter(Boolean).join(' ')
  }
  loading.value = false
})

function formatDate(dateString) {
  if (!dateString) return ''
  const d = new Date(dateString)
  return d.toLocaleDateString('es-CL', {
    day: 'numeric', month: 'long', year: 'numeric',
    hour: '2-digit', minute:'2-digit'
  })
}

const currentBpmStageIndex = computed(() => {
  return bpmStages.findIndex(step => step.state === bpmState.value)
})

const currentBpmStageText = computed(() => {
  return getBpmStatus(bpmState.value).label
})

// Redirección hacia próximos mockups
function startTest() {
  router.push('/estudiante/evaluacion') // Redirección exacta
}

function viewLatestReport() {
  router.push('/estudiante/reporte')
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
/* ── Infraestructura del layout en rejilla del Dashboard ────────────────── */
.dashboard-layout {
  --sidebar-w:  260px;
  --c-bg:       #F8FAFC;
  --c-surface:  #FFFFFF;
  --c-primary:  #4F46E5;
  --c-accent-completed: #10B981;
  --c-text:     #0F172A;
  --c-muted:    #64748B;
  --c-border:   #E2E8F0;
  --r-card:     16px;

  min-height: 100vh;
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  display: flex;
}

/* ── Panel de Navegación Lateral (Sidebar) ───────────────────────────────── */
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

.sidebar__nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}
.sidebar__link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  color: var(--c-muted);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.sidebar__link:hover, .sidebar__link--active {
  background: #EEF2FF;
  color: var(--c-primary);
}
.sidebar__icon { font-size: 1.1rem; }

.sidebar__footer {
  border-top: 1px solid var(--c-border);
  padding-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.user-avatar-zone {
  display: flex;
  align-items: center;
  gap: 12px;
}
.avatar {
  width: 40px; height: 40px;
  background: #C7D2FE;
  color: var(--c-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}
.user-info { display: flex; flex-direction: column; text-align: left; }
.user-name { font-weight: 600; font-size: 0.88rem; }
.user-role { font-size: 0.75rem; color: var(--c-muted); }

.logout-btn {
  color: #EF4444;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 8px;
  transition: background 0.2s;
}
.logout-btn:hover { background: #FEF2F2; }

/* ── Área de Contenido Principal ────────────────────────────────────────── */
.main-content {
  flex: 1;
  margin-left: calc(var(--sidebar-w) + 32px); 
  padding: 40px 48px;
  max-width: 1100px;
}

/* ── Barra de Progreso Superior del Proceso de Negocio (BPM) ─────────────── */
.bpm-progress-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.01);
}
.bpm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.bpm-badge {
  font-size: 0.72rem;
  background: #F1F5F9;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 700;
  color: var(--c-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.bpm-status-text { font-size: 0.85rem; color: var(--c-muted); }
.bpm-status-text strong { color: var(--c-primary); }

.bpm-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}
.bpm-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}
.bpm-step__node {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 2px solid var(--c-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  color: var(--c-muted);
  z-index: 2;
  transition: all 0.3s;
}
.bpm-step__label {
  margin-top: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-muted);
}
.bpm-step__line {
  position: absolute;
  top: 16px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--c-border);
  z-index: 1;
}

/* Modificadores de estado dinámicos de Camunda */
.bpm-step--completed .bpm-step__node {
  background: var(--c-accent-completed);
  border-color: var(--c-accent-completed);
  color: #FFFFFF;
}
.bpm-step--completed .bpm-step__line { background: var(--c-accent-completed); }
.bpm-step--completed .bpm-step__label { color: var(--c-text); }

.bpm-step--active .bpm-step__node {
  border-color: var(--c-primary);
  color: var(--c-primary);
  box-shadow: 0 0 0 4px #EEF2FF;
}
.bpm-step--active .bpm-step__label { color: var(--c-primary); font-weight: 700; }

/* ── Encabezado de Bienvenida ───────────────────────────────────────────── */
.welcome-section { text-align: left; margin-bottom: 32px; }
.welcome-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.8rem; margin-bottom: 4px; }
.welcome-sub { font-size: 0.9rem; color: var(--c-muted); margin-bottom: 8px; }
.welcome-orientador { font-size: 0.85rem; color: var(--c-primary); background: #EEF2FF; display: inline-block; padding: 4px 12px; border-radius: 100px; font-weight: 500; }

/* ── Tarjetas Informativas y Dashboard Grid ─────────────────────────────── */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  margin-bottom: 40px;
  align-items: stretch;
}

.action-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 40px;
  display: flex;
  text-align: left;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.02);
  position: relative;
  overflow: hidden;
}
.action-card__info { flex: 1; z-index: 2; }
.action-card__badge {
  display: inline-block;
  font-size: 0.72rem;
  background: #EEF2FF;
  border: 1px solid #C7D2FE;
  color: var(--c-primary);
  padding: 4px 10px;
  border-radius: 100px;
  font-weight: 700;
  margin-bottom: 16px;
}
.action-card__badge--success {
  background: #ECFDF5;
  border-color: #A7F3D0;
  color: #065F46;
}
.action-card__title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.5rem; margin-bottom: 12px; }
.action-card__desc { font-size: 0.92rem; line-height: 1.6; color: var(--c-muted); margin-bottom: 12px; }
.action-card__warning { font-size: 0.85rem; font-weight: 600; color: #D97706; background: #FFFBEB; padding: 8px 12px; border-radius: 8px; margin-bottom: 24px; display: inline-block; }

.action-card__visual {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 20px;
}
.visual-circle {
  width: 90px; height: 90px;
  border-radius: 50%;
  background: #EEF2FF;
  color: var(--c-primary);
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.report-quick-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}
.q-stat {
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
}
.q-stat span { color: var(--c-primary); font-weight: 700; margin-right: 4px; }

/* Barra lateral informativa */
.info-sidebar { display: flex; flex-direction: column; gap: 16px; justify-content: space-between; height: 100%; }
.info-mini-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 20px;
  display: flex;
  gap: 16px;
  text-align: left;
}
.mini-card__icon { font-size: 1.5rem; line-height: 1; }
.mini-card__title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.9rem; margin-bottom: 4px; }
.mini-card__desc { font-size: 0.8rem; line-height: 1.4; color: var(--c-muted); }

/* ── Bitácora / Línea de Tiempo ───────────────────────────────────────── */
.history-section { text-align: left; margin-top: 16px; }
.history-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.2rem; margin-bottom: 24px; }

.timeline-container {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.timeline-item {
  display: flex;
  gap: 20px;
  position: relative;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 24px;
  bottom: -32px;
  width: 2px;
  background: var(--c-border);
}

.timeline-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--c-border);
  margin-top: 4px;
  position: relative;
  z-index: 2;
}
.timeline-dot--completed {
  background: var(--c-primary);
  box-shadow: 0 0 0 4px #EEF2FF;
}

.timeline-content h4 {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: var(--c-text);
  margin-bottom: 4px;
}

.timeline-content p {
  font-size: 0.85rem;
  color: var(--c-muted);
}

/* Botón reutilizado del Home */
.btn {
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}
.btn--primary {
  background: var(--c-primary);
  color: #fff;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.2);
}
.btn--primary:hover {
  transform: translateY(-1px);
  background: #4338CA;
}

/* Responsivo */
.mobile-nav { display: none; }
.mobile-nav button, .mobile-nav a {
  border: 1px solid var(--c-border);
  border-radius: 8px;
  background: var(--c-surface);
  color: var(--c-primary);
  font: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 8px 10px;
  text-decoration: none;
  cursor: pointer;
}

@media (max-width: 900px) {
  .mobile-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
  .sidebar { display: none; }
  .main-content { margin-left: 0; padding: 24px; }
  .dashboard-grid { grid-template-columns: 1fr; }
  .bpm-step__label { display: none; }
}
</style>
