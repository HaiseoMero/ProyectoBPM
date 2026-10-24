<template>
  <div class="dashboard-layout">
    
    <DashboardNavigation
      :items="navigationItems"
      :user-name="displayedStudentName"
      :user-role="isOrientador ? 'Estudiante evaluado' : 'Mi reporte'"
      label="Navegación del reporte"
      @logout="logout"
    />

    <main class="main-content">
      <p v-if="isOrientador" class="report-student">Consulta del reporte de {{ displayedStudentName }}</p>
      
      <header v-if="!errorMessage" class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Resultados BFI-44</span>
          <span class="bpm-status-text" role="status">{{ loading ? 'Consultando estado del proceso…' : 'Estado del proceso: ' + getBpmStatus(bpmState).label }}</span>
        </div>
      </header>

      <section class="report-header-zone">
        <div class="report-title-container">
          <span class="report-eyebrow">Resultados del cuestionario</span>
          <h1 class="report-title">{{ isOrientador ? 'Resultados BFI-44 del estudiante' : 'Tus resultados BFI-44' }}</h1>
          <p class="report-sub">Reporte generado el {{ evaluatedAt }}.</p>
        </div>
      </section>

      <p v-if="loading" class="loading-text" role="status">Cargando tu reporte…</p>
      <p v-else-if="errorMessage" role="alert">{{ errorMessage }}</p>

      <template v-else>
      <div class="report-grid">
        
        <div class="report-visual-card">
          <h3 class="card-inner-title">Mapeo de Perfil de Personalidad</h3>
          <p class="card-inner-sub">Gráfico de los puntajes por dimensión incluidos en el reporte.</p>
          
          <div class="radar-container-box">
            <div v-for="dim in radarDimensions" :key="dim.letter"
                 class="radar__label-box" :class="'radar__label-box--' + dim.position">
              {{ dim.label }} ({{ dim.score == null ? '—' : dim.score + '%' }})
            </div>

            <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg"
                 role="img" aria-labelledby="radar-title radar-description">
              <title id="radar-title">Puntajes de las cinco dimensiones BFI-44</title>
              <desc id="radar-description">Cada eje corresponde a una dimensión identificada con su nombre y porcentaje.</desc>
              <polygon v-for="(points, index) in radarGridPoints" :key="index" class="radar__grid" :points="points" />
              <line v-for="(point, index) in radarAxes" :key="index" class="radar__axis"
                    :x1="CENTER" :y1="CENTER" :x2="point.x" :y2="point.y" />
              <polygon v-if="hasRadarScores" class="radar__data" :points="radarPoints" />
              <circle v-for="(pt, i) in radarDots" :key="i" :cx="pt.x" :cy="pt.y" r="5" class="radar__dot" />
              <text v-for="axis in radarLabelPoints" :key="axis.letter" :x="axis.x" :y="axis.y"
                    class="radar__axis-letter" text-anchor="middle" dominant-baseline="middle" aria-hidden="true">{{ axis.letter }}</text>
            </svg>
          </div>
          <dl class="radar-legend" aria-label="Puntajes por dimensión">
            <div v-for="dim in radarDimensions" :key="dim.letter" class="radar-legend__item">
              <dt><span class="radar-legend__letter">{{ dim.letter }}</span> {{ dim.label }}</dt>
              <dd>{{ dim.score == null ? 'Sin puntaje' : dim.score + '%' }}</dd>
            </div>
          </dl>

          <div class="dominant-profile-badge">
            <div class="badge-info">
              <span class="badge-label">Dimensión con mayor puntaje:</span>
              <span class="badge-value">{{ dominantTraitLabel }}</span>
            </div>
          </div>
        </div>

        <div class="report-text-card">
          <h3 class="card-inner-title">Interpretación de Dimensiones</h3>
          <p class="card-inner-sub">Selecciona una dimensión para abrir o cerrar su descripción.</p>

          <div class="accordion-container">
            <div 
              v-for="(dim, index) in dimensionsData" 
              :key="dim.letter" 
              class="accordion-item"
              :class="{ 'accordion-item--expanded': expandedIndexes.includes(index) }"
            >
              <button :id="`dimension-toggle-${dim.letter}`" type="button" class="accordion-header"
                      :aria-expanded="expandedIndexes.includes(index)"
                      :aria-controls="`dimension-content-${dim.letter}`" @click="toggleAccordion(index)">
                <span class="accordion-header__left">
                  <span class="accordion-letter" :style="{ color: dim.color }">{{ dim.letter }}</span>
                  <span class="accordion-name">{{ dim.name }}</span>
                </span>
                <span class="accordion-header__right">
                  <span class="accordion-score-tag">Puntaje: {{ dim.score }}%</span>
                  <span class="accordion-arrow" aria-hidden="true">{{ expandedIndexes.includes(index) ? '▼' : '▶' }}</span>
                </span>
              </button>
              <div v-show="expandedIndexes.includes(index)" :id="`dimension-content-${dim.letter}`"
                   class="accordion-content" role="region" :aria-labelledby="`dimension-toggle-${dim.letter}`">
                <p class="accordion-text-desc">{{ dim.interpretation }}</p>
                <div class="trait-impact-indicator">
                  <strong>Alcance del puntaje:</strong> {{ dim.vocationalImpact }}
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <section class="career-recommendations-zone">
        <h2 class="section-title-secondary">Áreas profesionales para explorar</h2>
        <p class="section-sub-secondary">Referencias de las reglas actuales del prototipo; no acreditan afinidad ni aptitud profesional.</p>

        <div class="career-cards-grid">
          <div v-for="area in careerAreas" :key="area.title" class="career-area-card">
            <div class="career-card-header">
              <h4 class="career-card-title">{{ area.title }}</h4>
            </div>
            <p class="career-card-desc">{{ area.desc }}</p>
            <div class="career-list-box">
              <h5>Ejemplos de carreras:</h5>
              <ul>
                <li v-for="carrera in area.carreras" :key="carrera">{{ carrera }}</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="actionable-tips-card">
          <div class="tips-content">
            <h4>Resumen de resultados</h4>
            <p v-if="careerAreas.length">
              Áreas incluidas en este reporte: {{ careerAreas.map(area => area.title).join(', ') }}.
              Los puntajes y las interpretaciones por dimensión se presentan arriba.
            </p>
            <p v-else>Las reglas actuales no permiten sugerir un área para esta combinación. Los puntajes OCEAN siguen disponibles.</p>
          </div>
        </div>
      </section>
      </template>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import reporteService from '../services/reporteService'
import orientadorService from '../services/orientadorService'
import authService from '../services/authService'
import DashboardNavigation from '../components/DashboardNavigation.vue'
import { getBpmStatus } from '../utils/bpmStatus'

const loading = ref(true)
const errorMessage = ref('')
const route = useRoute()
const isOrientador = computed(() => route.meta.role === 'orientador')
const navigationItems = computed(() => isOrientador.value
  ? [{ label: 'Panel de alumnos', to: '/orientador/dashboard', active: false }]
  : [
      { label: 'Panel principal', to: '/estudiante/dashboard', active: false },
      { label: 'Bitácora', to: '/estudiante/dashboard#history-section', active: false },
    ])
const studentName = ref('')
const displayedStudentName = computed(() => studentName.value || 'Nombre no disponible')

const evaluatedAt = ref('')
const dimensionsData = ref([])
const careerAreas = ref([])
const bpmState = ref(null)

watch([isOrientador, () => route.params.studentId], async ([orientador, studentId], _, onCleanup) => {
  let cancelled = false
  onCleanup(() => { cancelled = true })
  loading.value = true
  errorMessage.value = ''
  studentName.value = ''
  evaluatedAt.value = ''
  dimensionsData.value = []
  careerAreas.value = []
  bpmState.value = null
  try {
    if (orientador && (!/^\d+$/.test(studentId || '') || Number(studentId) < 1)) {
      errorMessage.value = 'Identificador de estudiante inválido.'
      return
    }
    const report = orientador
      ? await orientadorService.getStudentReport(studentId)
      : await reporteService.getLatestReport()
    if (cancelled) return
    studentName.value = typeof report.studentName === 'string' ? report.studentName.trim() : ''
    evaluatedAt.value = report.evaluatedAt
    dimensionsData.value = report.dimensions
    careerAreas.value = report.careerAreas
    bpmState.value = report.bpm_estado ?? null
  } catch (error) {
    if (cancelled) return
    const messages = {
      401: 'Tu sesión no es válida. Vuelve a iniciar sesión.',
      403: 'No tienes permiso para consultar el reporte de este estudiante.',
      404: 'No hay un reporte disponible.',
    }
    errorMessage.value = messages[error.response?.status] || 'No se pudo cargar el reporte. Intenta nuevamente.'
  } finally {
    if (!cancelled) loading.value = false
  }
}, { immediate: true })

// Lógica matemática nativa para construir el Gráfico de Radar SVG
const AXES = [
  { letter: 'O', label: 'Apertura', angle: -90, position: 'top' },
  { letter: 'C', label: 'Responsabilidad', angle: -18, position: 'tr' },
  { letter: 'E', label: 'Extraversión', angle: 54, position: 'br' },
  { letter: 'A', label: 'Amabilidad', angle: 126, position: 'bl' },
  { letter: 'N', label: 'Neuroticismo', angle: 198, position: 'tl' }
]
const CENTER = 160
const MAX_R = 120

function polarToXY(angleDeg, r) {
  const rad = (angleDeg * Math.PI) / 180
  return {
    x: CENTER + r * Math.cos(rad),
    y: CENTER + r * Math.sin(rad),
  }
}

// La identidad del eje depende de la letra, nunca del orden del JSON.
const radarDimensions = computed(() => AXES.map(axis => ({
  ...axis,
  score: dimensionsData.value.find(dim => dim.letter === axis.letter)?.score ?? null
})))
const hasRadarScores = computed(() => radarDimensions.value.every(dim => dim.score !== null))
const radarAxes = AXES.map(axis => polarToXY(axis.angle, MAX_R))
const radarLabelPoints = AXES.map(axis => ({ letter: axis.letter, ...polarToXY(axis.angle, MAX_R + 22) }))
const radarGridPoints = [1, 0.75, 0.5, 0.25].map(scale =>
  AXES.map(axis => {
    const point = polarToXY(axis.angle, MAX_R * scale)
    return `${point.x},${point.y}`
  }).join(' ')
)
const radarDots = computed(() => hasRadarScores.value
  ? radarDimensions.value.map(dim => polarToXY(dim.angle, dim.score / 100 * MAX_R))
  : []
)

const radarPoints = computed(() =>
  radarDots.value.map(p => `${p.x},${p.y}`).join(' ')
)

// El rasgo dominante se calcula a partir del puntaje más alto real,
// en vez de un texto fijo desconectado de los datos.
const dominantTraitLabel = computed(() => {
  if (!dimensionsData.value.length) return ''
  const top = dimensionsData.value.reduce((max, d) => (d.score > max.score ? d : max))
  return `${top.name} (${top.score}%)`
})

// Se abren las dos primeras dimensiones del reporte por defecto.
const expandedIndexes = ref([0, 1])

function toggleAccordion(index) {
  if (expandedIndexes.value.includes(index)) {
    expandedIndexes.value = expandedIndexes.value.filter(i => i !== index)
  } else {
    expandedIndexes.value.push(index)
  }
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
/* ── Barra de Progreso Superior (BPM Finalizada) ────────────────────────── */
.bpm-progress-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px; margin-bottom: 32px; }
.bpm-header { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; }
.bpm-badge { font-size: 0.72rem; background: #F1F5F9; padding: 4px 10px; border-radius: 6px; font-weight: 700; color: var(--c-muted); text-transform: uppercase; }
.bpm-badge--success { background: #E1F5FE; color: #0288D1; }
.bpm-status-text { font-size: 0.85rem; color: var(--c-muted); }
.text-success { color: #10B981 !important; }
.bpm-steps { display: flex; justify-content: space-between; align-items: center; position: relative; }
.bpm-step { display: flex; flex-direction: column; align-items: center; position: relative; flex: 1; }
.bpm-step__node { width: 32px; height: 32px; border-radius: 50%; background: #FFFFFF; border: 2px solid var(--c-border); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; color: var(--c-muted); z-index: 2; }
.bpm-step__label { margin-top: 8px; font-size: 0.8rem; font-weight: 600; color: var(--c-muted); }
.bpm-step__line { position: absolute; top: 16px; left: 50%; width: 100%; height: 2px; background: var(--c-border); z-index: 1; }
.bpm-step--completed .bpm-step__node { background: #10B981; border-color: #10B981; color: #FFFFFF; }
.bpm-step--completed .bpm-step__line { background: #10B981; }
.bpm-step--active-final .bpm-step__node { background: var(--c-primary) !important; border-color: var(--c-primary) !important; color: #FFFFFF !important; box-shadow: 0 0 0 4px #EEF2FF; }

/* ── Encabezado del Reporte ─────────────────────────────────────────────── */
.report-header-zone { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px; gap: 24px; }
.report-title-container { text-align: left; }
.report-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 4px; display: block; }
.report-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.8rem; margin-bottom: 4px; }
.report-sub { font-size: 0.9rem; color: var(--c-muted); }
.report-student { margin-bottom: 16px; overflow-wrap: anywhere; }
.report-title-container { min-width: 0; }

/* ── Rejilla del Reporte: Gráfico vs Acordeón ───────────────────────────── */
.report-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr); gap: 24px; margin-bottom: 32px; align-items: start; }
.report-visual-card, .report-text-card { min-width: 0; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 24px; padding: 32px; box-shadow: 0 10px 25px rgba(15, 23, 42, 0.01); text-align: left; overflow-wrap: anywhere; }

.card-inner-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.15rem; margin-bottom: 4px; }
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.card-inner-sub { font-size: 0.82rem; color: var(--c-muted); margin-bottom: 24px; }

/* Ejes identificados por letra; leyenda legible fuera del gráfico. */
.radar-container-box { position: relative; display: flex; align-items: center; justify-content: center; height: 320px; margin-bottom: 20px; }
.radar__svg { width: 260px; height: auto; filter: drop-shadow(0 8px 20px rgba(79, 70, 229, 0.08)); }
.radar__grid, .radar__axis { stroke: #CBD5E1; stroke-width: 1; fill: none; }
.radar__data { fill: rgba(79, 70, 229, 0.12); stroke: var(--c-primary); stroke-width: 2.5; stroke-linejoin: round; }
.radar__dot { fill: #0EA5E9; }

.radar__label-box { position: absolute; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--c-text); background: #F8FAFC; border: 1px solid var(--c-border); padding: 4px 8px; border-radius: 6px; }
.radar__label-box--top { top: -2%; left: 50%; transform: translateX(-50%); }
.radar__label-box--tr  { top: 22%; right: -5%; }
.radar__label-box--br  { bottom: 18%; right: -5%; }
.radar__label-box--bl  { bottom: 18%; left: -5%; }
.radar__label-box--tl  { top: 22%; left: -5%; }


.radar__axis-letter { display: none; font-size: 16px; font-weight: 700; fill: var(--c-text); }
.radar-legend { display: none; gap: 8px; margin: 0; }
.radar-legend__item { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: 8px 12px; background: #F8FAFC; border: 1px solid var(--c-border); border-radius: 8px; font-size: 0.85rem; }
.radar-legend dt { min-width: 0; }
.radar-legend dd { margin: 0; flex-shrink: 0; font-weight: 700; }
.radar-legend__letter { color: var(--c-primary); font-weight: 800; }

.dominant-profile-badge { display: flex; align-items: center; gap: 12px; background: #EEF2FF; border: 1px solid #C7D2FE; padding: 14px; border-radius: 12px; margin-top: 28px; }
.badge-icon { font-size: 1.5rem; }
.badge-info { display: flex; flex-direction: column; }
.badge-label { font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: var(--c-primary); }
.badge-value { font-size: 0.88rem; font-weight: 700; color: var(--c-text); }

/* ── Secciones Colapsables (Acordeón) ───────────────────────────────────── */
.accordion-container { display: flex; flex-direction: column; gap: 12px; }
.accordion-item { border: 1px solid var(--c-border); border-radius: 12px; overflow: hidden; transition: all 0.2s; }
.accordion-item--expanded { border-color: #C7D2FE; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.03); }
.accordion-header { width: 100%; min-height: 56px; display: flex; flex-wrap: wrap; gap: 8px 12px; justify-content: space-between; align-items: center; padding: 16px 20px; color: var(--c-text); text-align: left; border: none; background: #FFFFFF; cursor: pointer; transition: background 0.15s; }
.accordion-header:hover { background: #F8FAFC; }
.accordion-header:focus-visible { outline-offset: -4px; }

.accordion-header__left { display: flex; min-width: 0; align-items: center; gap: 12px; }
.accordion-letter { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.2rem; }
.accordion-name { font-weight: 600; font-size: 0.9rem; }
.accordion-header__right { display: flex; align-items: center; gap: 14px; }
.accordion-score-tag { font-size: 0.78rem; background: #F1F5F9; color: var(--c-muted); padding: 4px 8px; border-radius: 6px; font-weight: 600; }
.accordion-arrow { font-size: 0.7rem; color: var(--c-muted); }

.accordion-content { padding: 18px 20px; background: #F8FAFC; border-top: 1px solid var(--c-border); text-align: left; }
.accordion-text-desc { font-size: 0.85rem; line-height: 1.6; color: var(--c-muted); margin-bottom: 12px; }
.trait-impact-indicator { font-size: 0.82rem; color: var(--c-text); background: #FFFFFF; border: 1px solid var(--c-border); padding: 8px 12px; border-radius: 8px; }

/* ── Recomendaciones de Carreras y Bloque Final ────────────────────────── */
.career-recommendations-zone { text-align: left; margin-top: 40px; border-top: 1px solid var(--c-border); padding-top: 40px; }
.section-title-secondary { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.3rem; margin-bottom: 4px; }
.section-sub-secondary { font-size: 0.9rem; color: var(--c-muted); margin-bottom: 28px; }

.career-cards-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; margin-bottom: 32px; }
.career-area-card { min-width: 0; overflow-wrap: anywhere; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 28px; box-shadow: 0 4px 12px rgba(0,0,0,0.01); }
.career-card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.career-card-icon { font-size: 1.6rem; }
.career-card-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: var(--c-text); }
.career-card-desc { font-size: 0.88rem; line-height: 1.5; color: var(--c-muted); margin-bottom: 20px; }

.career-list-box { background: var(--c-bg); border: 1px solid var(--c-border); padding: 16px; border-radius: 12px; }
.career-list-box h5 { font-size: 0.8rem; text-transform: uppercase; font-weight: 700; color: var(--c-muted); margin-bottom: 10px; }
.career-list-box ul { padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px; }
.career-list-box li { font-size: 0.85rem; font-weight: 600; color: var(--c-text); }

/* Caja de sugerencias de ingeniería final */
.actionable-tips-card { display: flex; gap: 20px; background: #FFFBEB; border: 1px solid #FDE68A; border-radius: var(--r-card); padding: 28px; align-items: flex-start; }
.tips-icon { font-size: 2rem; line-height: 1; }
.tips-content h4 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: #92400E; margin-bottom: 6px; }
.tips-content p { font-size: 0.9rem; line-height: 1.6; color: #B45309; }
.tips-content { min-width: 0; overflow-wrap: anywhere; }

/* Botones estándar del proyecto */
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 100px; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.88rem; text-decoration: none; cursor: pointer; transition: all 0.2s; border: none; }

@media (max-width: 1200px) {
  .report-grid, .career-cards-grid { grid-template-columns: 1fr; }
  .report-header-zone { flex-direction: column; align-items: flex-start; gap: 16px; }
}
@media (max-width: 600px) {
  .radar-container-box { height: auto; margin-bottom: 16px; }
  .radar__svg { width: 100%; max-width: 320px; }
  .radar__label-box { display: none; }
  .radar__axis-letter { display: block; }
  .radar-legend { display: grid; }
  .bpm-progress-card, .report-visual-card, .report-text-card, .career-area-card, .actionable-tips-card { padding: 20px; border-radius: var(--r-card); }
  .report-title { font-size: 1.5rem; }
  .report-grid, .career-cards-grid { gap: 16px; }
  .accordion-header { padding: 14px; }
  .accordion-header__left { gap: 8px; }
  .accordion-header__right { width: 100%; justify-content: space-between; }
  .accordion-content { padding: 16px 14px; }
  .career-recommendations-zone { margin-top: 24px; padding-top: 24px; }
}
@media (prefers-reduced-motion: reduce) {
  .accordion-item, .accordion-header { transition: none; }
}
</style>
