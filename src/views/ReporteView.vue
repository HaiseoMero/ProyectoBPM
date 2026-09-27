<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div class="sidebar__brand">
        <span class="sidebar__logo-icon">◈</span>
        <span class="sidebar__logo-text">Vócalis</span>
      </div>
      
      <nav class="sidebar__nav">
        <router-link :to="isOrientador ? '/orientador/dashboard' : '/estudiante/dashboard'" class="sidebar__link">
          Dashboard
        </router-link>
        <router-link v-if="!isOrientador" to="/estudiante/dashboard#history-section" class="sidebar__link">
          Mi Historial
        </router-link>
      </nav>

      <div class="sidebar__footer">
        <div class="user-avatar-zone">
          <div class="avatar">{{ studentInitials }}</div>
          <div class="user-info">
            <span class="user-name">{{ displayedStudentName }}</span>
            <span class="user-role">{{ isOrientador ? 'Estudiante evaluado' : 'Mi reporte' }}</span>
          </div>
        </div>
        <a href="#" @click.prevent="logout" class="logout-btn">
          Cerrar Sesión
        </a>
      </div>
    </aside>

    <main class="main-content">
      <p v-if="isOrientador">Consulta del reporte de {{ displayedStudentName }}</p>
      
      <header class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Reporte vocacional</span>
          <span class="bpm-status-text">Estado del proceso no disponible.</span>
        </div>
      </header>

      <section class="report-header-zone">
        <div class="report-title-container">
          <span class="report-eyebrow">Resultados del cuestionario</span>
          <h1 class="report-title">{{ isOrientador ? 'Reporte Vocacional del Estudiante' : 'Tu Reporte Vocacional' }}</h1>
          <p class="report-sub">Reporte generado el {{ evaluatedAt }}.</p>
        </div>
        <div class="report-actions">
          <button @click="simulatePDFExport" class="btn btn--ghost">
            Exportar PDF (Mejora Futura)
          </button>
        </div>
      </section>

      <p v-if="loading" class="loading-text">Cargando tu reporte…</p>
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

            <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg">
              <polygon v-for="(points, index) in radarGridPoints" :key="index" class="radar__grid" :points="points" />
              <line v-for="(point, index) in radarAxes" :key="index" class="radar__axis"
                    :x1="CENTER" :y1="CENTER" :x2="point.x" :y2="point.y" />
              <polygon v-if="hasRadarScores" class="radar__data" :points="radarPoints" />
              <circle v-for="(pt, i) in radarDots" :key="i" :cx="pt.x" :cy="pt.y" r="5" class="radar__dot" />
            </svg>
          </div>

          <div class="dominant-profile-badge">
            <div class="badge-info">
              <span class="badge-label">Rasgo Dominante Detectado:</span>
              <span class="badge-value">{{ dominantTraitLabel }}</span>
            </div>
          </div>
        </div>

        <div class="report-text-card">
          <h3 class="card-inner-title">Interpretación de Dimensiones</h3>
          <p class="card-inner-sub">Haz clic sobre cualquier dimensión para colapsar o expandir su análisis psicológico.</p>

          <div class="accordion-container">
            <div 
              v-for="(dim, index) in dimensionsData" 
              :key="dim.letter" 
              class="accordion-item"
              :class="{ 'accordion-item--expanded': expandedIndexes.includes(index) }"
            >
              <header class="accordion-header" @click="toggleAccordion(index)">
                <div class="accordion-header__left">
                  <span class="accordion-letter" :style="{ color: dim.color }">{{ dim.letter }}</span>
                  <span class="accordion-name">{{ dim.name }}</span>
                </div>
                <div class="accordion-header__right">
                  <span class="accordion-score-tag">Puntaje: {{ dim.score }}%</span>
                  <span class="accordion-arrow">{{ expandedIndexes.includes(index) ? '▼' : '▶' }}</span>
                </div>
              </header>
              <div v-show="expandedIndexes.includes(index)" class="accordion-content">
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

const loading = ref(true)
const errorMessage = ref('')
const route = useRoute()
const isOrientador = computed(() => route.meta.role === 'orientador')
const studentName = ref('')
const displayedStudentName = computed(() => studentName.value || 'Nombre no disponible')
const studentInitials = computed(() => studentName.value
  ? studentName.value.split(/\s+/).slice(0, 2).map(part => Array.from(part)[0]).join('').toUpperCase()
  : '—')
const evaluatedAt = ref('')
const dimensionsData = ref([])
const careerAreas = ref([])

watch([isOrientador, () => route.params.studentId], async ([orientador, studentId], _, onCleanup) => {
  let cancelled = false
  onCleanup(() => { cancelled = true })
  loading.value = true
  errorMessage.value = ''
  studentName.value = ''
  evaluatedAt.value = ''
  dimensionsData.value = []
  careerAreas.value = []
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

// Control de secciones colapsables (Se expanden las dos primeras dimensiones dominantes por defecto)
const expandedIndexes = ref([0, 1])

function toggleAccordion(index) {
  if (expandedIndexes.value.includes(index)) {
    expandedIndexes.value = expandedIndexes.value.filter(i => i !== index)
  } else {
    expandedIndexes.value.push(index)
  }
}

function simulatePDFExport() {
  alert('La exportación PDF está fuera del alcance del MVP y se contempla como una mejora futura.')
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
/* ── Infraestructura y Rejilla General ──────────────────────────────────── */
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

/* ── Sidebar (Consistente al 100%) ───────────────────────────────────────── */
.sidebar {
  width: var(--sidebar-w); background: var(--c-surface); border-right: 1px solid var(--c-border);
  display: flex; flex-direction: column; position: fixed; top: 0; bottom: 0; left: 0; padding: 32px 24px; z-index: 50;
}
.sidebar__brand { display: flex; align-items: center; gap: 8px; font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.3rem; margin-bottom: 40px; }
.sidebar__logo-icon { color: var(--c-primary); }
.sidebar__nav { display: flex; flex-direction: column; gap: 8px; flex: 1; }
.sidebar__link { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; color: var(--c-muted); text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }
.sidebar__link:hover, .sidebar__link--active { background: #EEF2FF; color: var(--c-primary); }
.sidebar__icon { font-size: 1.1rem; }
.sidebar__footer { border-top: 1px solid var(--c-border); padding-top: 20px; display: flex; flex-direction: column; gap: 16px; }
.user-avatar-zone { display: flex; align-items: center; gap: 12px; }
.avatar { width: 40px; height: 40px; background: #C7D2FE; color: var(--c-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; }
.user-info { display: flex; flex-direction: column; text-align: left; }
.user-name { font-weight: 600; font-size: 0.88rem; }
.user-role { font-size: 0.75rem; color: var(--c-muted); }
.logout-btn { color: #EF4444; text-decoration: none; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 8px; padding: 8px; border-radius: 8px; }
.logout-btn:hover { background: #FEF2F2; }

/* ── Margen de contenido principal con la separación extra aplicada ─────── */
.main-content {
  flex: 1;
  margin-left: calc(var(--sidebar-w) + 32px);
  padding: 40px 48px;
  max-width: 1100px;
}

/* ── Barra de Progreso Superior (BPM Finalizada) ────────────────────────── */
.bpm-progress-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px; margin-bottom: 32px; }
.bpm-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
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

/* ── Rejilla del Reporte: Gráfico vs Acordeón ───────────────────────────── */
.report-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 24px; margin-bottom: 32px; align-items: start; }
.report-visual-card, .report-text-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 24px; padding: 32px; box-shadow: 0 10px 25px rgba(15, 23, 42, 0.01); text-align: left; }

.card-inner-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.15rem; margin-bottom: 4px; }
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.card-inner-sub { font-size: 0.82rem; color: var(--c-muted); margin-bottom: 24px; }

/* Posicionamiento de Etiquetas del Radar */
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

.dominant-profile-badge { display: flex; align-items: center; gap: 12px; background: #EEF2FF; border: 1px solid #C7D2FE; padding: 14px; border-radius: 12px; margin-top: 28px; }
.badge-icon { font-size: 1.5rem; }
.badge-info { display: flex; flex-direction: column; }
.badge-label { font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: var(--c-primary); }
.badge-value { font-size: 0.88rem; font-weight: 700; color: var(--c-text); }

/* ── Secciones Colapsables (Acordeón) ───────────────────────────────────── */
.accordion-container { display: flex; flex-direction: column; gap: 12px; }
.accordion-item { border: 1px solid var(--c-border); border-radius: 12px; overflow: hidden; transition: all 0.2s; }
.accordion-item--expanded { border-color: #C7D2FE; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.03); }
.accordion-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #FFFFFF; cursor: pointer; transition: background 0.15s; user-select: none; }
.accordion-header:hover { background: #F8FAFC; }

.accordion-header__left { display: flex; align-items: center; gap: 12px; }
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

.career-cards-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin-bottom: 32px; }
.career-area-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 28px; box-shadow: 0 4px 12px rgba(0,0,0,0.01); }
.career-card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.career-card-icon { font-size: 1.6rem; }
.career-card-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: var(--c-text); }
.career-card-desc { font-size: 0.88rem; line-height: 1.5; color: var(--c-muted); margin-bottom: 20px; }

.career-list-box { background: var(--c-bg); border: 1px solid var(--c-border); padding: 16px; border-radius: 12px; }
.career-list-box h5 { font-size: 0.8rem; text-transform: uppercase; font-weight: 700; color: var(--c-muted); margin-bottom: 10px; }
.career-list-box ul { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.career-list-box li { font-size: 0.85rem; font-weight: 600; color: var(--c-text); }

/* Caja de sugerencias de ingeniería final */
.actionable-tips-card { display: flex; gap: 20px; background: #FFFBEB; border: 1px solid #FDE68A; border-radius: var(--r-card); padding: 28px; align-items: flex-start; }
.tips-icon { font-size: 2rem; line-height: 1; }
.tips-content h4 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: #92400E; margin-bottom: 6px; }
.tips-content p { font-size: 0.9rem; line-height: 1.6; color: #B45309; }

/* Botones estándar del proyecto */
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 100px; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.88rem; text-decoration: none; cursor: pointer; transition: all 0.2s; border: none; }
.btn--ghost { background: #FFFFFF; color: var(--c-text); border: 1px solid var(--c-border); }
.btn--ghost:hover { border-color: var(--c-primary); color: var(--c-primary); }

@media (max-width: 900px) {
  .sidebar { display: none; }
  .main-content { margin-left: 0; padding: 20px; }
  .report-grid, .career-cards-grid { grid-template-columns: 1fr; }
  .radar-container-box { width: 100%; max-width: 320px; margin: 0 auto 20px; }
  .report-header-zone { flex-direction: column; align-items: flex-start; gap: 16px; }
}
</style>
