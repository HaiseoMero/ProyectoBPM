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
      <section class="profile-zone" aria-labelledby="profile-title">
        <header class="zone-head">
          <p class="zone-eyebrow">Tu perfil en cinco dimensiones</p>
          <h2 id="profile-title" class="zone-title">Cómo te describiste en el cuestionario</h2>
          <p class="zone-sub">Cada dimensión es un continuo entre dos extremos. El marcador indica hacia dónde se ubicaron tus respuestas; ningún punto de la escala es mejor que otro.</p>
        </header>

        <div class="report-grid">
          <aside class="report-visual-card">
            <h3 class="card-inner-title">Mapeo de Perfil de Personalidad</h3>
            <p class="card-inner-sub">Gráfico de los puntajes por dimensión incluidos en el reporte.</p>

            <div class="radar-container-box">
              <div v-for="dim in radarDimensions" :key="dim.letter"
                   class="radar__label-box" :class="'radar__label-box--' + dim.position">
                {{ dim.label }} <strong>{{ dim.score == null ? '—' : dim.score + '%' }}</strong>
              </div>

              <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg"
                   role="img" aria-labelledby="radar-title radar-description">
                <title id="radar-title">Puntajes de las cinco dimensiones BFI-44</title>
                <desc id="radar-description">Cada eje corresponde a una dimensión identificada con su nombre y porcentaje.</desc>
                <polygon v-for="(points, index) in radarGridPoints" :key="index" class="radar__grid" :points="points" />
                <line v-for="(point, index) in radarAxes" :key="index" class="radar__axis"
                      :x1="CENTER" :y1="CENTER" :x2="point.x" :y2="point.y" />
                <polygon v-if="hasRadarScores" class="radar__data" :points="radarPoints" />
                <circle v-for="(pt, i) in radarDots" :key="i" :cx="pt.x" :cy="pt.y" r="4.5" class="radar__dot" />
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

            <div class="reading-guide">
              <h4>Cómo leer tus porcentajes</h4>
              <ul>
                <li>Indican tu posición en la escala del cuestionario, no una nota.</li>
                <li>Un 70 % no significa que superes al 70 % de las personas.</li>
                <li>Mira las cinco dimensiones juntas: ninguna te resume por sí sola.</li>
              </ul>
            </div>
          </aside>

          <div class="report-text-card">
            <h3 class="card-inner-title">Interpretación de Dimensiones</h3>
            <p class="card-inner-sub">Selecciona una dimensión para abrir o cerrar su descripción.</p>

            <ol class="accordion-container">
              <li
                v-for="(dim, index) in dimensionsData"
                :key="dim.letter"
                class="accordion-item"
                :class="{ 'accordion-item--expanded': expandedIndexes.includes(index) }"
                :style="{ '--trait': dim.color }"
              >
                <button :id="`dimension-toggle-${dim.letter}`" type="button" class="accordion-header"
                        :aria-expanded="expandedIndexes.includes(index)"
                        :aria-controls="`dimension-content-${dim.letter}`" @click="toggleAccordion(index)">
                  <span class="accordion-header__left">
                    <span class="accordion-letter" aria-hidden="true">{{ dim.letter }}</span>
                    <span class="accordion-name">{{ dim.name }}</span>
                  </span>
                  <span class="accordion-header__right">
                    <span class="accordion-score-tag">Puntaje: {{ dim.score }}%</span>
                    <span class="accordion-arrow" aria-hidden="true"></span>
                  </span>
                </button>

                <div class="trait-scale" aria-hidden="true">
                  <span class="trait-scale__track">
                    <span class="trait-scale__fill" :style="{ width: (dim.pct ?? dim.score) + '%' }"></span>
                    <span class="trait-scale__marker" :style="{ left: (dim.pct ?? dim.score) + '%' }"></span>
                    <span class="trait-scale__ticks"><i></i><i></i><i></i></span>
                  </span>
                  <span v-if="dim.low" class="trait-scale__pole">{{ dim.low }}</span>
                  <span v-if="dim.high" class="trait-scale__pole trait-scale__pole--high">{{ dim.high }}</span>
                </div>

                <div v-show="expandedIndexes.includes(index)" :id="`dimension-content-${dim.letter}`"
                     class="accordion-content" role="region" :aria-labelledby="`dimension-toggle-${dim.letter}`">
                  <p class="accordion-text-desc">{{ dim.interpretation }}</p>
                  <div class="trait-impact-indicator">
                    <strong>Alcance del puntaje:</strong> {{ dim.vocationalImpact }}
                  </div>
                  <router-link v-if="dim.infoId" :to="`/el-test#${dim.infoId}`" class="trait-more">
                    Qué describe esta dimensión <span aria-hidden="true">→</span>
                  </router-link>
                </div>
              </li>
            </ol>
          </div>
        </div>
      </section>

      <section class="career-recommendations-zone" aria-labelledby="areas-title">
        <header class="zone-head">
          <p class="zone-eyebrow">Para seguir investigando</p>
          <h2 id="areas-title" class="section-title-secondary">Áreas profesionales para explorar</h2>
          <p class="section-sub-secondary">Referencias de las reglas actuales del prototipo; no acreditan afinidad ni aptitud profesional.</p>
        </header>

        <article v-for="(area, areaIndex) in careerAreas" :key="area.title" class="career-area-card">
          <header class="area-head" :class="{ 'area-head--image': area.info?.image }">
            <img v-if="area.info?.image" class="area-head__img" :src="area.info.image.src" alt="" loading="lazy" />
            <div class="area-head__body">
              <p class="area-head__index">Área {{ areaIndex + 1 }} de {{ careerAreas.length }}</p>
              <h3 class="career-card-title">{{ area.title }}</h3>
              <p class="career-card-desc">{{ area.desc }}</p>
            </div>
          </header>

          <div v-if="area.info" class="area-facts">
            <div class="area-fact">
              <h4>Qué se estudia</h4>
              <p>{{ area.info.queSeEstudia }}</p>
            </div>
            <div class="area-fact">
              <h4>Habilidades que se ponen en juego</h4>
              <ul class="area-chips">
                <li v-for="skill in area.info.habilidades" :key="skill">{{ skill }}</li>
              </ul>
            </div>
            <div class="area-fact">
              <h4>Dónde se trabaja</h4>
              <ul class="area-list">
                <li v-for="place in area.info.campoLaboral" :key="place">{{ place }}</li>
              </ul>
            </div>
          </div>

          <div class="career-list-box">
            <h5>Ejemplos de carreras:</h5>
            <ul class="career-grid">
              <li v-for="(carrera, i) in area.carreras" :key="carrera" class="career-item"
                  :class="{ 'career-item--rich': area.details?.[i] }">
                <figure v-if="area.details?.[i]?.image" class="career-item__media">
                  <img :src="area.details[i].image.src" :alt="area.details[i].image.alt" loading="lazy" />
                </figure>
                <div class="career-item__body">
                  <h6 class="career-item__name">{{ carrera.replace(/^[^:]+:\s*/, '') }}</h6>
                  <p v-if="area.details?.[i]?.descripcion" class="career-item__desc">{{ area.details[i].descripcion }}</p>
                  <a v-if="area.details?.[i]?.link" class="career-item__link" :href="area.details[i].link"
                     target="_blank" rel="noopener noreferrer">
                    Dónde se estudia <span class="visually-hidden">{{ carrera.replace(/^[^:]+:\s*/, '') }} (abre en otra pestaña)</span><span aria-hidden="true">↗</span>
                  </a>
                </div>
              </li>
            </ul>
          </div>

          <p v-if="area.credits?.length" class="area-credits">
            Imágenes de Wikimedia Commons:
            <template v-for="(credit, c) in area.credits" :key="credit.source">
              <a :href="credit.source" target="_blank" rel="noopener noreferrer">{{ credit.label }}</a>
              ({{ credit.author }}, <a v-if="credit.licenseUrl" :href="credit.licenseUrl" target="_blank" rel="noopener noreferrer">{{ credit.license }}</a><span v-else>{{ credit.license }}</span>){{ c < area.credits.length - 1 ? ' · ' : '.' }}
            </template>
          </p>
        </article>

        <div class="actionable-tips-card">
          <div class="tips-content">
            <h4>Resumen de resultados</h4>
            <p v-if="careerAreas.length">
              Áreas incluidas en este reporte: {{ careerAreas.map(area => area.title).join(', ') }}.
              Los puntajes y las interpretaciones por dimensión se presentan arriba.
            </p>
            <p v-else>Las reglas actuales no permiten sugerir un área para esta combinación. Los puntajes OCEAN siguen disponibles.</p>
            <p class="tips-note">Antes de decidir, conversa estas referencias con tu orientador y contrástalas con tus intereses, habilidades y experiencias.</p>
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
import { enrichCareerArea } from '../data/areasEstudio'

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
    dimensionsData.value = orderDimensions(report.dimensions)
    expandedIndexes.value = defaultExpanded(dimensionsData.value)
    careerAreas.value = (report.careerAreas || []).map(enrichCareerArea)
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

// Se abre por defecto la dimensión con mayor puntaje; el resto queda a un toque.
const expandedIndexes = ref([])

// Extremos de cada continuo y ancla en la página «El test».
const TRAIT_SCALE = {
  O: { low: 'Prefiere lo conocido', high: 'Busca lo nuevo', infoId: 'apertura' },
  C: { low: 'Flexible y espontáneo', high: 'Organizado y metódico', infoId: 'responsabilidad' },
  E: { low: 'Reservado', high: 'Sociable', infoId: 'extraversion' },
  A: { low: 'Directo y crítico', high: 'Cooperativo y empático', infoId: 'amabilidad' },
  N: { low: 'Emocionalmente estable', high: 'Más sensible al estrés', infoId: 'neuroticismo' },
}
const OCEAN_ORDER = ['O', 'C', 'E', 'A', 'N']

// Presenta las dimensiones siempre en orden OCEAN, sin depender del orden del JSON.
function orderDimensions(dimensions = []) {
  return [...dimensions]
    .sort((a, b) => OCEAN_ORDER.indexOf(a.letter) - OCEAN_ORDER.indexOf(b.letter))
    .map(dim => ({
      ...TRAIT_SCALE[dim.letter],
      ...dim,
      pct: Math.max(0, Math.min(100, Number(dim.score) || 0)),
    }))
}

function defaultExpanded(dimensions) {
  if (!dimensions.length) return []
  const top = dimensions.reduce((best, dim, i) => (dim.score > dimensions[best].score ? i : best), 0)
  return [top]
}

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
/* ── Estado del proceso ─────────────────────────────────────────────────── */
.bpm-progress-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 18px 24px; margin-bottom: 32px; box-shadow: var(--shadow-card); }
.bpm-header { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; }
.bpm-badge { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--c-primary); }
.bpm-status-text { display: inline-flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--c-text-soft); }
.bpm-status-text::before { content: ''; flex: 0 0 8px; width: 8px; height: 8px; border-radius: 50%; background: var(--c-primary); box-shadow: 0 0 0 4px var(--c-tint); }

/* ── Encabezado ─────────────────────────────────────────────────────────── */
.report-header-zone { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; gap: 24px; }
.report-title-container { text-align: left; min-width: 0; }
.report-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 10px; display: block; }
.report-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.7rem, 3.2vw, 2.4rem); line-height: 1.1; letter-spacing: -0.035em; margin-bottom: 8px; }
.report-sub { font-size: 0.9rem; color: var(--c-muted); }
.report-student {
  display: inline-flex; align-items: center; gap: 8px;
  margin-bottom: 16px; padding: 6px 14px;
  border: 1px solid var(--c-tint-border); border-radius: 100px;
  background: var(--c-tint); color: var(--c-primary-strong);
  font-size: 0.85rem; font-weight: 600; overflow-wrap: anywhere;
}
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }

/* Encabezado común de cada zona */
.zone-head { max-width: 720px; margin-bottom: 28px; text-align: left; }
.zone-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 10px; }
.zone-title, .section-title-secondary { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.4rem, 2.6vw, 1.85rem); line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 10px; }
.zone-sub, .section-sub-secondary { font-size: 0.95rem; line-height: 1.65; color: var(--c-muted); }

/* ── Perfil: resumen fijo + escalas ─────────────────────────────────────── */
.report-grid { display: grid; grid-template-columns: minmax(300px, 0.8fr) minmax(0, 1.2fr); gap: 24px; align-items: start; }
.report-visual-card, .report-text-card { min-width: 0; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 24px; padding: 28px; text-align: left; overflow-wrap: anywhere; }
.report-visual-card { position: sticky; top: 24px; box-shadow: var(--shadow-raised); }
.report-text-card { padding: 28px 28px 12px; box-shadow: var(--shadow-card); }

.card-inner-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em; margin-bottom: 4px; }
.card-inner-sub { font-size: 0.85rem; color: var(--c-muted); margin-bottom: 8px; }

.radar-container-box { position: relative; display: flex; align-items: center; justify-content: center; height: 300px; margin: 8px 0 12px; }
.radar__svg { width: 220px; height: auto; overflow: visible; }
.radar__grid, .radar__axis { stroke: var(--c-border); stroke-width: 1; fill: none; }
.radar__grid:first-of-type { stroke: var(--c-border-strong); }
.radar__data { fill: rgba(4, 120, 87, 0.14); stroke: var(--c-primary); stroke-width: 2; stroke-linejoin: round; }
.radar__dot { fill: var(--c-surface); stroke: var(--c-primary); stroke-width: 2; }

.radar__label-box { position: absolute; display: flex; flex-direction: column; align-items: center; gap: 0; font-size: 0.7rem; font-weight: 500; line-height: 1.25; color: var(--c-muted); text-align: center; white-space: nowrap; }
.radar__label-box strong { font-family: 'Poppins', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--c-text); }
.radar__label-box--top { top: 0; left: 50%; transform: translateX(-50%); }
.radar__label-box--tr  { top: 30%; right: 0; }
.radar__label-box--br  { bottom: 4%; right: 10%; }
.radar__label-box--bl  { bottom: 4%; left: 10%; }
.radar__label-box--tl  { top: 30%; left: 0; }

.radar__axis-letter { display: none; font-family: 'Poppins', sans-serif; font-size: 16px; font-weight: 700; fill: var(--c-text); }
.radar-legend { display: none; gap: 8px; margin: 0; }
.radar-legend__item { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 8px 12px; background: var(--c-bg); border: 1px solid var(--c-border); border-radius: 10px; font-size: 0.85rem; }
.radar-legend dt { min-width: 0; display: flex; align-items: center; gap: 8px; }
.radar-legend dd { margin: 0; flex-shrink: 0; font-weight: 700; }
.radar-legend__letter { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 7px; background: var(--c-tint); color: var(--c-primary); font-family: 'Poppins', sans-serif; font-weight: 700; }

.dominant-profile-badge { display: flex; align-items: center; gap: 12px; background: var(--c-tint); border: 1px solid var(--c-tint-border); border-left: 4px solid var(--c-accent2); padding: 14px 16px; border-radius: 12px; margin-top: 8px; }
.badge-info { display: flex; flex-direction: column; gap: 2px; }
.badge-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; color: var(--c-primary); }
.badge-value { font-size: 0.95rem; font-weight: 700; color: var(--c-text); }

.reading-guide { margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--c-border); }
.reading-guide h4 { font-family: 'Poppins', sans-serif; font-size: 0.85rem; font-weight: 700; margin-bottom: 10px; }
.reading-guide ul { list-style: none; padding: 0; display: grid; gap: 8px; }
.reading-guide li { position: relative; padding-left: 16px; font-size: 0.82rem; line-height: 1.5; color: var(--c-text-soft); }
.reading-guide li::before { content: ''; position: absolute; left: 0; top: 0.55em; width: 6px; height: 6px; border-radius: 50%; background: var(--c-border-strong); }

/* Lista de dimensiones: cada una con su escala bipolar siempre visible */
.accordion-container { list-style: none; padding: 0; margin: 12px 0 0; display: flex; flex-direction: column; }
.accordion-item { --trait: var(--c-primary); border-top: 1px solid var(--c-border); padding: 4px 0 18px; }
.accordion-header { width: 100%; min-height: 56px; display: flex; flex-wrap: wrap; gap: 8px 12px; justify-content: space-between; align-items: center; padding: 12px 4px 8px; color: var(--c-text); text-align: left; border: none; border-radius: 10px; background: transparent; cursor: pointer; }
.accordion-header:hover .accordion-name { color: var(--c-primary); }
.accordion-header:focus-visible { outline-offset: 2px; }

.accordion-header__left { display: flex; min-width: 0; align-items: center; gap: 12px; }
.accordion-letter { display: inline-grid; place-items: center; width: 34px; height: 34px; flex-shrink: 0; border-radius: 10px; color: var(--trait); background: color-mix(in srgb, var(--trait) 10%, #FFFFFF); font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1rem; }
.accordion-name { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; letter-spacing: -0.01em; transition: color 0.15s; }
.accordion-header__right { display: flex; align-items: center; gap: 14px; }
.accordion-score-tag { font-size: 0.82rem; color: var(--c-text-soft); font-weight: 600; font-variant-numeric: tabular-nums; }
.accordion-arrow { width: 8px; height: 8px; border-right: 2px solid var(--c-muted); border-bottom: 2px solid var(--c-muted); transform: rotate(45deg) translateY(-2px); transition: transform 0.2s; margin-right: 6px; }
.accordion-item--expanded .accordion-arrow { transform: rotate(-135deg) translateY(-2px); border-color: var(--c-primary); }

.trait-scale { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-areas: "track track" "low high"; row-gap: 8px; column-gap: 12px; padding: 0 4px 0 50px; }
.trait-scale__track { grid-area: track; position: relative; height: 8px; border-radius: 8px; background: #F1F5F9; }
.trait-scale__fill { position: absolute; inset: 0 auto 0 0; border-radius: 8px; background: color-mix(in srgb, var(--trait) 28%, #FFFFFF); }
.trait-scale__marker { position: absolute; top: 50%; width: 16px; height: 16px; border-radius: 50%; transform: translate(-50%, -50%); background: var(--c-surface); border: 3px solid var(--trait); box-shadow: 0 1px 3px rgba(15, 23, 42, 0.18); z-index: 1; }
.trait-scale__ticks { position: absolute; inset: 0; display: flex; justify-content: space-evenly; pointer-events: none; }
.trait-scale__ticks i { width: 1px; height: 100%; background: rgba(255, 255, 255, 0.9); }
.trait-scale__pole { grid-area: low; font-size: 0.75rem; color: var(--c-muted); }
.trait-scale__pole--high { grid-area: high; text-align: right; }

.accordion-content { margin: 16px 4px 0 50px; padding: 16px 18px; background: var(--c-bg); border-radius: 12px; text-align: left; }
.accordion-text-desc { font-size: 0.92rem; line-height: 1.65; color: var(--c-text-soft); margin-bottom: 12px; }
.trait-impact-indicator { font-size: 0.84rem; line-height: 1.55; color: var(--c-text); background: #FFFFFF; border: 1px solid var(--c-border); border-left: 3px solid var(--c-accent1); padding: 10px 14px; border-radius: 10px; }
.trait-more { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; margin-top: 4px; font-size: 0.85rem; font-weight: 600; color: var(--c-primary); text-decoration: none; }
.trait-more:hover { text-decoration: underline; text-underline-offset: 4px; }

/* ── Áreas para explorar ────────────────────────────────────────────────── */
.career-recommendations-zone { text-align: left; margin-top: 56px; border-top: 1px solid var(--c-border); padding-top: 48px; }

.career-area-card { min-width: 0; overflow: hidden; overflow-wrap: anywhere; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 24px; margin-bottom: 24px; box-shadow: var(--shadow-card); }

.area-head { position: relative; padding: 32px; background: var(--c-deep); color: #ECFDF5; }
.area-head--image { min-height: 240px; display: flex; align-items: flex-end; }
.area-head__img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
/* Velo para leer el texto sobre la fotografía */
.area-head--image::after { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(6, 78, 59, 0.15) 0%, rgba(6, 78, 59, 0.92) 78%); }
.area-head__body { position: relative; z-index: 1; max-width: 760px; }
.area-head__index { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #BEF264; margin-bottom: 8px; }
.career-card-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.25rem, 2.4vw, 1.6rem); line-height: 1.2; letter-spacing: -0.02em; color: #FFFFFF; margin-bottom: 10px; }
.career-card-desc { font-size: 0.92rem; line-height: 1.6; color: #D1FAE5; }

.area-facts { display: grid; grid-template-columns: 1.2fr 1fr 1fr; border-bottom: 1px solid var(--c-border); }
.area-fact { padding: 24px 28px; min-width: 0; }
.area-fact + .area-fact { border-left: 1px solid var(--c-border); }
.area-fact h4 { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 12px; }
.area-fact p { font-size: 0.9rem; line-height: 1.6; color: var(--c-text-soft); }
.area-chips { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
.area-chips li { font-size: 0.8rem; font-weight: 500; color: var(--c-text-soft); background: var(--c-bg); border: 1px solid var(--c-border); padding: 4px 10px; border-radius: 100px; }
.area-list { list-style: none; padding: 0; display: grid; gap: 8px; }
.area-list li { position: relative; padding-left: 16px; font-size: 0.88rem; line-height: 1.45; color: var(--c-text-soft); }
.area-list li::before { content: ''; position: absolute; left: 0; top: 0.5em; width: 6px; height: 6px; border-radius: 50%; background: var(--c-primary); }

.career-list-box { padding: 24px 28px 28px; }
.career-list-box h5 { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; color: var(--c-muted); margin-bottom: 14px; }
.career-grid { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.career-item { min-width: 0; display: flex; flex-direction: column; border: 1px solid var(--c-border); border-radius: 16px; overflow: hidden; background: var(--c-surface); }
.career-item:not(.career-item--rich) { flex-direction: row; align-items: center; padding: 12px 16px; border-radius: 100px; background: var(--c-bg); }
.career-item__media { margin: 0; aspect-ratio: 4 / 3; background: #F1F5F9; overflow: hidden; }
.career-item__media img { width: 100%; height: 100%; object-fit: cover; display: block; }
.career-item__body { padding: 14px 16px 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; min-width: 0; }
.career-item:not(.career-item--rich) .career-item__body { padding: 0; }
.career-item__name { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.95rem; line-height: 1.3; color: var(--c-text); margin: 0; }
.career-item__desc { font-size: 0.84rem; line-height: 1.5; color: var(--c-muted); }
.career-item__link { margin-top: auto; display: inline-flex; align-items: center; gap: 6px; min-height: 44px; font-size: 0.82rem; font-weight: 600; color: var(--c-primary); text-decoration: none; }
.career-item__link:hover { text-decoration: underline; text-underline-offset: 4px; }

.area-credits { padding: 0 28px 20px; font-size: 0.7rem; line-height: 1.6; color: var(--c-muted); }
.area-credits a { color: inherit; }

.actionable-tips-card { display: flex; gap: 20px; background: var(--c-warning-bg); border: 1px solid var(--c-warning-border); border-left: 4px solid #F59E0B; border-radius: var(--r-card); padding: 24px 28px; align-items: flex-start; }
.tips-content h4 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: var(--c-warning); margin-bottom: 6px; }
.tips-content p { font-size: 0.9rem; line-height: 1.6; color: #78350F; }
.tips-content .tips-note { margin-top: 8px; font-size: 0.85rem; }
.tips-content { min-width: 0; overflow-wrap: anywhere; }

@media (max-width: 1200px) {
  .report-grid { grid-template-columns: 1fr; }
  .report-visual-card { position: static; }
  .report-header-zone { flex-direction: column; align-items: flex-start; gap: 16px; }
  .area-facts { grid-template-columns: 1fr 1fr; }
  .area-fact:first-child { grid-column: 1 / -1; border-bottom: 1px solid var(--c-border); }
  .area-fact:nth-child(2) { border-left: none; }
}
@media (max-width: 600px) {
  .radar-container-box { height: auto; margin-bottom: 16px; }
  .radar__svg { width: 100%; max-width: 300px; }
  .radar__label-box { display: none; }
  .radar__axis-letter { display: block; }
  .radar-legend { display: grid; }
  .bpm-progress-card, .report-visual-card, .actionable-tips-card { padding: 20px; border-radius: var(--r-card); }
  .report-text-card { padding: 20px 16px 8px; border-radius: var(--r-card); }
  .accordion-header { padding: 12px 0 8px; }
  .accordion-header__left { gap: 10px; }
  .trait-scale { padding: 0; }
  .accordion-content { margin: 14px 0 0; padding: 14px; }
  .career-recommendations-zone { margin-top: 32px; padding-top: 32px; }
  .career-area-card { border-radius: 20px; }
  .area-head { padding: 24px 20px; }
  .area-head--image { min-height: 220px; }
  .area-facts { grid-template-columns: 1fr; }
  .area-fact { padding: 20px; }
  .area-fact + .area-fact { border-left: none; border-top: 1px solid var(--c-border); }
  .area-fact:first-child { border-bottom: none; }
  .career-list-box { padding: 20px; }
  .career-grid { grid-template-columns: 1fr; gap: 12px; }
  /* Fila compacta: miniatura a la izquierda para acortar la página */
  .career-item--rich { display: grid; grid-template-columns: 88px minmax(0, 1fr); align-items: start; }
  .career-item--rich .career-item__media { aspect-ratio: auto; height: 100%; min-height: 120px; }
  .career-item--rich .career-item__body { padding: 12px 14px; gap: 6px; }
  .career-item__desc { font-size: 0.82rem; }
  .area-credits { padding: 0 20px 16px; }
}
@media (prefers-reduced-motion: reduce) {
  .accordion-arrow, .accordion-name { transition: none; }
}
</style>
