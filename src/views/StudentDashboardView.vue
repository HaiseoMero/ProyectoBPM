<template>
  <div class="dashboard-layout">
    
    <DashboardNavigation
      :items="navigationItems"
      :user-name="studentName || 'Estudiante'"
      user-role="Estudiante"
      label="Navegación del estudiante"
      @logout="logout"
    />

    <main class="main-content">
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
            :aria-current="index === currentBpmStageIndex ? 'step' : undefined"
          >
            <div class="bpm-step__node">
              <span v-if="index < currentBpmStageIndex">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="bpm-step__label">{{ step.label }}</span>
            <div v-if="index < bpmStages.length - 1" class="bpm-step__line" aria-hidden="true"></div>
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
            <span class="action-card__badge">{{ hasPendingTest ? 'Cuestionario pendiente' : 'Disponible ahora' }}</span>
            <h2 class="action-card__title">{{ hasPendingTest ? 'Tienes un cuestionario BFI-44 pendiente' : 'El cuestionario BFI-44 está disponible' }}</h2>
            <p v-if="hasPendingTest" class="action-card__desc">
              Dejaste tu cuestionario sin finalizar. Tus respuestas guardadas se conservan para que puedas retomarlo desde donde quedaste.
            </p>
            <p v-else class="action-card__desc">Aún no hay un reporte disponible.</p>
            <p v-if="!hasPendingTest" class="action-card__desc">
              Responde 44 afirmaciones sobre cómo te describes habitualmente. Los resultados muestran dimensiones de personalidad para apoyar tu reflexión.
            </p>
            <p class="action-card__warning">
              44 afirmaciones · sin límite de tiempo · un envío final
            </p>
            <button @click="startTest" class="btn btn--primary">
              {{ hasPendingTest ? 'Continuar cuestionario BFI-44' : 'Iniciar cuestionario BFI-44' }}
            </button>
          </div>
          <div class="action-card__visual" aria-hidden="true">
            <svg class="visual-radar" viewBox="0 0 120 120">
              <polygon points="60,10 107.6,44.5 89.4,100.5 30.6,100.5 12.4,44.5" />
              <polygon points="60,32.5 86.2,51.5 76.2,82.3 43.8,82.3 33.8,51.5" />
              <polygon class="visual-radar__data" points="60,18 98,47 80,90 38,86 26,49" />
            </svg>
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
        <p v-if="loading" role="status">Cargando tu bitácora…</p>
        <p v-else-if="!loadError && !Object.values(timeline).some(Boolean)" class="action-card__desc">
          Aún no hay fechas registradas en tu bitácora.
        </p>
        
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
import DashboardNavigation from '../components/DashboardNavigation.vue'
import evaluacionService from '../services/evaluacionService'
import reporteService from '../services/reporteService'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()
const route = useRoute()

// Pestaña actual de la interfaz
const currentTab = ref('dashboard')
const navigationItems = computed(() => [
  { label: 'Panel principal', to: '/estudiante/dashboard', active: currentTab.value === 'dashboard' },
  { label: 'Bitácora', to: '/estudiante/dashboard#history-section', active: currentTab.value === 'history' },
])
watch(() => route.hash, hash => {
  currentTab.value = hash === '#history-section' ? 'history' : 'dashboard'
}, { immediate: true })

// Estado de la evaluación desde backend
const hasPreviousTest = ref(false)
const hasPendingTest = ref(false)
const bpmState = ref(null)
const orientadorName = ref(null)
const studentName = ref('')

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
    hasPendingTest.value = estado.tiene_evaluacion && estado.estado === 'en_progreso'
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
/* ── Progreso del proceso (BPM) ─────────────────────────────────────────── */
.bpm-progress-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 24px 28px;
  margin-bottom: 36px;
  box-shadow: var(--shadow-card);
}
.bpm-header {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.bpm-badge {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--c-primary);
}
.bpm-status-text { font-size: 0.85rem; color: var(--c-muted); }
.bpm-status-text strong { color: var(--c-text); }

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
  min-width: 0;
}
.bpm-step__node {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: var(--c-surface);
  border: 1px solid var(--c-border-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.8rem;
  color: var(--c-muted);
  z-index: 2;
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}
.bpm-step__label {
  margin-top: 10px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-muted);
  text-align: center;
  overflow-wrap: anywhere;
}
.bpm-step__line {
  position: absolute;
  top: 17px;
  left: calc(50% + 22px);
  width: calc(100% - 44px);
  height: 1px;
  background: repeating-linear-gradient(90deg, var(--c-border-strong) 0 6px, transparent 6px 12px);
  z-index: 1;
}

.bpm-step--completed .bpm-step__node {
  background: var(--c-tint);
  border-color: var(--c-tint-border);
  color: var(--c-primary);
}
.bpm-step--completed .bpm-step__line { background: var(--c-tint-border); }
.bpm-step--completed .bpm-step__label { color: var(--c-text); }

.bpm-step--active .bpm-step__node {
  background: var(--c-primary);
  border-color: var(--c-primary);
  color: #FFFFFF;
  box-shadow: 0 0 0 5px var(--c-tint);
}
.bpm-step--active .bpm-step__label { color: var(--c-primary); font-weight: 700; }

/* ── Bienvenida ─────────────────────────────────────────────────────────── */
.welcome-section { text-align: left; margin-bottom: 32px; }
.welcome-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(1.6rem, 3vw, 2.1rem);
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 6px;
}
.welcome-sub { font-size: 0.9rem; color: var(--c-muted); margin-bottom: 12px; }
.welcome-orientador {
  display: inline-block;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--c-text-soft);
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  padding: 6px 14px;
  border-radius: 14px;
  overflow-wrap: anywhere;
}
.welcome-orientador::before {
  content: '';
  display: inline-block;
  vertical-align: middle;
  margin: -2px 8px 0 0;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-primary);
}
.welcome-orientador strong { color: var(--c-text); }

/* ── Tarjetas principales ───────────────────────────────────────────────── */
.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
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
  gap: 24px;
  text-align: left;
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}
.action-card__info { flex: 1; min-width: 0; z-index: 2; overflow-wrap: anywhere; }
.action-card__badge {
  display: inline-block;
  font-size: 0.72rem;
  background: var(--c-tint);
  border: 1px solid var(--c-tint-border);
  color: var(--c-primary);
  padding: 4px 10px;
  border-radius: 100px;
  font-weight: 700;
  margin-bottom: 16px;
}
.action-card__badge--success {
  background: var(--c-tint);
  border-color: var(--c-tint-border);
  color: var(--c-primary-strong);
}
.action-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.55rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-bottom: 12px;
}
.action-card__desc { font-size: 0.95rem; line-height: 1.65; color: var(--c-muted); margin-bottom: 12px; }
.action-card__warning {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.5;
  color: var(--c-warning);
  background: var(--c-warning-bg);
  border: 1px solid var(--c-warning-border);
  padding: 8px 12px;
  border-radius: 10px;
  margin-bottom: 24px;
}

/* Tarjeta para comenzar: bloque verde profundo, igual que el cierre de la portada */
.action-card--start {
  background: var(--c-deep);
  border-color: var(--c-deep);
  color: #ECFDF5;
}
.action-card--start::before {
  content: '';
  position: absolute;
  width: 560px; height: 560px;
  right: -240px; bottom: -300px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 47px, rgba(167, 243, 208, 0.08) 47px 48px);
  pointer-events: none;
}
.action-card--start .action-card__badge { background: rgba(190, 242, 100, 0.12); border-color: rgba(190, 242, 100, 0.35); color: #BEF264; }
.action-card--start .action-card__title { color: #FFFFFF; }
.action-card--start .action-card__desc { color: #A7F3D0; }
.action-card--start .action-card__warning { color: #ECFDF5; background: rgba(255, 255, 255, 0.06); border-color: rgba(167, 243, 208, 0.25); }
.action-card--start .btn--primary { background: #FFFFFF; color: var(--c-deep); }
.action-card--start .btn--primary:hover { background: var(--c-tint); }

.action-card__visual {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 12px;
  z-index: 1;
}
.visual-radar { width: 150px; height: 150px; overflow: visible; }
.visual-radar polygon { fill: none; stroke: rgba(167, 243, 208, 0.3); stroke-width: 1; }
.visual-radar .visual-radar__data { fill: rgba(132, 204, 22, 0.22); stroke: var(--c-accent2); stroke-width: 2; stroke-linejoin: round; }

.report-quick-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}
.q-stat {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  padding: 6px 12px 6px 6px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--c-text-soft);
}
.q-stat span {
  display: inline-grid;
  place-items: center;
  width: 26px; height: 26px;
  border-radius: 7px;
  background: var(--c-tint);
  color: var(--c-primary);
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
}

/* ── Columna informativa ────────────────────────────────────────────────── */
.info-sidebar { display: flex; flex-direction: column; gap: 16px; height: 100%; }
.info-mini-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 22px;
  display: flex;
  gap: 16px;
  text-align: left;
}
.info-mini-card:first-child { background: var(--c-tint); border-color: var(--c-tint-border); }
.mini-card__icon { font-size: 1.5rem; line-height: 1; }
.mini-card__title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px; }
.mini-card__desc { font-size: 0.85rem; line-height: 1.55; color: var(--c-muted); }
.info-mini-card:first-child .mini-card__desc { color: var(--c-text-soft); }

/* ── Bitácora ───────────────────────────────────────────────────────────── */
.history-section { text-align: left; margin-top: 16px; }
.history-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.35rem;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
}

.timeline-container {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  box-shadow: var(--shadow-card);
}

.timeline-item { display: flex; gap: 20px; position: relative; }
.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 26px;
  bottom: -30px;
  width: 1px;
  background: repeating-linear-gradient(180deg, var(--c-tint-border) 0 6px, transparent 6px 12px);
}

.timeline-dot {
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--c-border);
  margin-top: 3px;
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}
.timeline-content { min-width: 0; overflow-wrap: anywhere; }
.timeline-dot--completed {
  background: var(--c-primary);
  box-shadow: 0 0 0 4px var(--c-tint);
}

.timeline-content h4 {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: var(--c-text);
  margin-bottom: 4px;
}
.timeline-content p { font-size: 0.875rem; color: var(--c-muted); }

/* ── Botón ──────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding: 12px 24px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  border: none;
}
.btn--primary { background: var(--c-primary); color: #fff; }
.btn--primary:hover { background: var(--c-primary-strong); }

/* ── Responsive ─────────────────────────────────────────────────────────── */
@media (max-width: 1200px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .info-sidebar { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); height: auto; }
}
@media (max-width: 600px) {
  .report-quick-stats { display: grid; grid-template-columns: 1fr; gap: 8px; }
  .bpm-progress-card, .action-card, .timeline-container { padding: 20px; }
  .bpm-progress-card, .welcome-section { margin-bottom: 24px; }
  .bpm-steps { flex-direction: column; align-items: stretch; gap: 16px; }
  .bpm-step { flex-direction: row; gap: 12px; }
  .bpm-step__node { flex-shrink: 0; }
  .bpm-step__label { margin-top: 0; text-align: left; }
  .bpm-step__line { left: 16px; top: 38px; width: 1px; height: calc(100% - 22px); background: repeating-linear-gradient(180deg, var(--c-border-strong) 0 6px, transparent 6px 12px); }
  .bpm-step--completed .bpm-step__line { background: var(--c-tint-border); }
  .action-card { flex-direction: column; border-radius: 20px; }
  .action-card__visual { display: none; }
  .action-card__title { font-size: 1.3rem; }
  .action-card .btn { width: 100%; justify-content: center; }
  .info-sidebar { grid-template-columns: 1fr; }
  .timeline-item { gap: 16px; }
}
@media (prefers-reduced-motion: reduce) {
  .bpm-step__node, .btn { transition: none; }
}
</style>
