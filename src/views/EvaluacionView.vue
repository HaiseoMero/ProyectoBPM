<template>
  <div class="test-layout">
    <main class="main-content">
      
      <div class="top-navigation">
        <router-link to="/estudiante/dashboard" class="back-btn">
          <span class="btn__arrow">←</span> Volver al Dashboard
        </router-link>
        <div class="brand">
          <span class="brand-icon">◈</span>
          <span class="brand-text">Vócalis</span>
        </div>
      </div>
      
      <header class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Estado BPM registrado</span>
          <span class="bpm-status-text">Estado actual: <strong>{{ getBpmStatus(bpmState).label }}</strong></span>
        </div>
        
        <div class="bpm-steps">
          <div v-for="(step, index) in bpmStages" :key="step.state" class="bpm-step"
               :class="{ 'bpm-step--completed': index < bpmStageIndex, 'bpm-step--active': index === bpmStageIndex }">
            <div class="bpm-step__node">{{ index < bpmStageIndex ? '✓' : index + 1 }}</div>
            <span class="bpm-step__label">{{ step.label }}</span>
            <div v-if="index < bpmStages.length - 1" class="bpm-step__line"></div>
          </div>
        </div>
      </header>

      <section class="test-header-zone">
        <div class="test-title-container">
          <h1 class="test-title">Inventario Big Five (BFI-44)</h1>
          <div class="test-instructions-box">
            <span class="instructions-icon">✨</span>
            <p>
              Vas a responder 44 afirmaciones sobre cómo eres normalmente. No hay respuestas correctas o incorrectas. Responde con tu primera impresión — no lo pienses demasiado, ni te compares con lo que crees que "deberías" ser. <strong>Podrás enviar el cuestionario completo una sola vez</strong>; tus respuestas parciales se guardan para que puedas continuar después. Los resultados describen dimensiones de personalidad y no determinan una carrera.
            </p>
          </div>
        </div>
        
        <div class="progress-stats-box">
          <div class="progress-text">
            Bloque <strong>{{ currentPage + 1 }}</strong> de <strong>{{ totalPages }}</strong> 
            <span class="progress-count">({{ answeredCount }} de 44 respondidas)</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: percentProgress + '%' }"></div>
          </div>
        </div>
      </section>

      <section class="test-card-container">
        <p v-if="loadingQuestions" class="loading-text">Cargando cuestionario…</p>
        <div v-else-if="loadError" role="alert">
          <p>{{ loadError }}</p>
          <button class="btn btn--primary" @click="loadQuestionnaire">Reintentar carga</button>
        </div>
        <div v-else-if="isCompleted" role="status">
          <p>Esta evaluación ya está completada y no se puede editar.</p>
          <router-link to="/estudiante/reporte" class="btn btn--primary">Ver reporte</router-link>
        </div>
        <template v-else>
        <div role="status">
          <p>{{ savingCount ? 'Guardando respuestas…' : (hasUnsavedAnswers ? 'Hay respuestas sin guardar. Tus selecciones se conservan en esta página.' : 'Todas las respuestas seleccionadas están guardadas.') }}</p>
          <button v-if="hasUnsavedAnswers && !savingCount" class="btn btn--ghost" @click="retrySaving">Reintentar guardado</button>
        </div>
        <div class="likert-table-wrapper">
          <table class="likert-table">
            <thead>
              <tr>
                <th class="col-question">Afirmación: "Me considero una persona que..."</th>
                <th class="col-option">Totalmente en Desacuerdo</th>
                <th class="col-option">En Desacuerdo</th>
                <th class="col-option">Neutro</th>
                <th class="col-option">De Acuerdo</th>
                <th class="col-option">Totalmente de Acuerdo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in paginatedQuestions" :key="q.id" class="likert-row">
                <td class="question-text">
                  <span class="question-number">{{ q.id }}.</span> {{ q.text }}
                </td>
                <td v-for="val in 5" :key="val" class="option-cell" @click="selectAnswer(q.id, val)">
                  <label class="radio-container">
                    <input 
                      type="radio" 
                      :name="'q-' + q.id" 
                      :value="val" 
                      :checked="answers[q.id] === val"
                      :disabled="submitting"
                      @change="selectAnswer(q.id, val)"
                    />
                    <span class="custom-radio">
                      <span class="custom-radio__inner">{{ val }}</span>
                    </span>
                  </label>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="test-navigation-footer">
          <button 
            @click="prevPage" 
            class="btn btn--ghost" 
            :disabled="currentPage === 0"
          >
            ← Bloque Anterior
          </button>
          
          <div v-if="validationMessage" class="validation-warning">
            {{ validationMessage }}
          </div>

          <button 
            @click="nextPage" 
            class="btn btn--primary"
            :disabled="submitting"
          >
            {{ isLastPage ? (submitting ? 'Calculando perfil…' : 'Finalizar y Calcular Perfil') : 'Siguiente Bloque →' }}
          </button>
        </footer>
        </template>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import evaluacionService from '../services/evaluacionService'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()

const questions = ref([])
const loadingQuestions = ref(true)
const loadError = ref('')
const bpmState = ref(null)
const isCompleted = ref(false)
const bpmStageIndex = computed(() => bpmStages.findIndex(step => step.state === bpmState.value))

function applyEstado(estado) {
  bpmState.value = estado.bpm_estado ?? null
  isCompleted.value = ['completada', 'procesada'].includes(estado.estado)
}

async function refreshEstado() {
  try {
    applyEstado(await evaluacionService.getEstado())
  } catch {
    bpmState.value = null
  }
}

async function loadQuestionnaire() {
  loadingQuestions.value = true
  loadError.value = ''
  try {
    const [items, saved, estado] = await Promise.all([
      evaluacionService.getQuestions(),
      evaluacionService.getAnswers(),
      evaluacionService.getEstado()
    ])
    questions.value = items
    answers.value = Object.fromEntries(saved.map(answer => [answer.preguntaId, answer.valor]))
    savedAnswers.value = { ...answers.value }
    applyEstado(estado)
    const firstUnanswered = items.findIndex(q => !answers.value[q.id])
    currentPage.value = firstUnanswered < 0 ? Math.max(0, totalPages.value - 1) : Math.floor(firstUnanswered / itemsPerPage)
  } catch {
    bpmState.value = null
    loadError.value = 'No se pudo recuperar el cuestionario y su progreso. Reintenta antes de responder.'
  } finally {
    loadingQuestions.value = false
  }
}

onMounted(() => {
  window.addEventListener('beforeunload', warnUnsaved)
  loadQuestionnaire()
})
onUnmounted(() => window.removeEventListener('beforeunload', warnUnsaved))

// Paginación
const currentPage = ref(0)
const itemsPerPage = 10
const validationMessage = ref('')
const submitting = ref(false)

// Estado de respuestas: clave es ID de pregunta, valor es puntaje Likert (1 a 5)
const answers = ref({})
const savedAnswers = ref({})
const savingCount = ref(0)
let saveQueue = Promise.resolve()
const hasUnsavedAnswers = computed(() => Object.entries(answers.value)
  .some(([id, value]) => savedAnswers.value[id] !== value))

function warnUnsaved(event) {
  if (savingCount.value || hasUnsavedAnswers.value) {
    event.preventDefault()
    event.returnValue = ''
  }
}

onBeforeRouteLeave(async () => {
  if (submitting.value) return false
  while (savingCount.value) await saveQueue
  return !hasUnsavedAnswers.value || window.confirm('Hay respuestas sin guardar. Si sales, perderás esos cambios. ¿Salir de todos modos?')
})

const totalPages = computed(() => Math.ceil(questions.value.length / itemsPerPage))
const isLastPage = computed(() => currentPage.value === totalPages.value - 1)

// Segmentar las 10 preguntas correspondientes al bloque actual
const paginatedQuestions = computed(() => {
  const start = currentPage.value * itemsPerPage
  return questions.value.slice(start, start + itemsPerPage)
})

// Contadores de progreso analítico
const answeredCount = computed(() => Object.keys(answers.value).length)
const percentProgress = computed(() =>
  questions.value.length ? Math.round((answeredCount.value / questions.value.length) * 100) : 0
)

function queueSave(qId, val) {
  savingCount.value++
  // Guardado individual en orden: evita crear dos evaluaciones o sobrescribir
  // una selección reciente con una petición anterior que termine más tarde.
  saveQueue = saveQueue.then(async () => {
    try {
      if (isCompleted.value) return
      await evaluacionService.saveAnswer(qId, val)
      savedAnswers.value[qId] = val
      if (bpmState.value === null) await refreshEstado()
    } catch (error) {
      // La selección local permanece pendiente hasta un reintento exitoso.
      delete savedAnswers.value[qId]
      if (error.response?.status === 400) await refreshEstado()
    } finally {
      savingCount.value--
    }
  })
}

function selectAnswer(qId, val) {
  if (loadingQuestions.value || loadError.value || isCompleted.value || submitting.value) return
  if (answers.value[qId] === val) return
  answers.value[qId] = val
  validationMessage.value = ''
  queueSave(qId, val)
}

function retrySaving() {
  if (isCompleted.value || submitting.value || savingCount.value) return
  for (const [id, value] of Object.entries(answers.value)) {
    if (savedAnswers.value[id] !== value) queueSave(Number(id), value)
  }
}

function prevPage() {
  if (currentPage.value > 0) {
    currentPage.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

async function nextPage() {
  if (loadingQuestions.value || loadError.value || isCompleted.value || submitting.value) return
  // Validar si todas las preguntas del bloque actual fueron respondidas
  const unansweredQuestions = paginatedQuestions.value.filter(q => !answers.value[q.id])

  if (unansweredQuestions.length > 0) {
    validationMessage.value = 'Debes contestar todas las afirmaciones de este bloque antes de continuar.'
    return
  }

  if (!isLastPage.value) {
    currentPage.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  if (questions.value.some(q => !answers.value[q.id])) {
    validationMessage.value = 'Aún quedan preguntas sin responder.'
    return
  }

  submitting.value = true
  try {
    await saveQueue
    if (isCompleted.value) return
    if (hasUnsavedAnswers.value) {
      validationMessage.value = 'Reintenta el guardado de las respuestas pendientes antes de finalizar.'
      return
    }
    await evaluacionService.submitEvaluation(answers.value)
    isCompleted.value = true
    submitting.value = false
    await router.push('/estudiante/reporte')
  } catch {
    validationMessage.value = 'No se pudo finalizar la evaluación. Tus respuestas se conservan; puedes reintentar.'
    await refreshEstado()
  } finally {
    submitting.value = false
  }
}

</script>

<style scoped>
/* ── Infraestructura y Rejilla General ──────────────────────────────────── */
.test-layout {
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
  justify-content: center;
}

/* ── Navegación Superior Simplificada ───────────────────────────────────── */
.top-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.back-btn {
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
}
.back-btn:hover { color: var(--c-primary); }
.brand { display: flex; align-items: center; gap: 8px; font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.2rem; }
.brand-icon { color: var(--c-primary); }

/* ── Margen de contenido principal centrado ─────────────────────────────── */
.main-content {
  flex: 1;
  padding: 32px 24px;
  max-width: 1000px;
  width: 100%;
}

/* ── Barra de Progreso Superior (BPM) ───────────────────────────────────── */
.bpm-progress-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 24px;
  margin-bottom: 32px;
}
.bpm-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.bpm-badge { font-size: 0.72rem; background: #F1F5F9; padding: 4px 10px; border-radius: 6px; font-weight: 700; color: var(--c-muted); text-transform: uppercase; }
.bpm-status-text { font-size: 0.85rem; color: var(--c-muted); }
.bpm-status-text strong { color: var(--c-primary); }
.bpm-steps { display: flex; justify-content: space-between; align-items: center; position: relative; }
.bpm-step { display: flex; flex-direction: column; align-items: center; position: relative; flex: 1; }
.bpm-step__node {
  width: 32px; height: 32px; border-radius: 50%; background: #FFFFFF; border: 2px solid var(--c-border);
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; color: var(--c-muted); z-index: 2;
}
.bpm-step__label { margin-top: 8px; font-size: 0.8rem; font-weight: 600; color: var(--c-muted); }
.bpm-step__line { position: absolute; top: 16px; left: 50%; width: 100%; height: 2px; background: var(--c-border); z-index: 1; }

.bpm-step--completed .bpm-step__node { background: #10B981; border-color: #10B981; color: #FFFFFF; }
.bpm-step--completed .bpm-step__line { background: #10B981; }
.bpm-step--active .bpm-step__node { border-color: var(--c-primary); color: var(--c-primary); box-shadow: 0 0 0 4px #EEF2FF; }
.bpm-step--active .bpm-step__label { color: var(--c-primary); font-weight: 700; }

/* ── Zona del Encabezado del Test e Indicador de Progreso ────────────────── */
.test-header-zone {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 24px;
  gap: 24px;
}
.test-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.8rem; margin-bottom: 12px; text-align: left;}
.test-instructions-box {
  display: flex;
  gap: 16px;
  background: #EEF2FF;
  border-left: 4px solid var(--c-primary);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  font-size: 0.92rem;
  color: var(--c-text);
  line-height: 1.6;
  max-width: 600px;
  text-align: left;
}
.test-instructions-box p { margin: 0; }
.test-instructions-box strong { color: var(--c-primary); }
.instructions-icon { font-size: 1.4rem; }

.progress-stats-box {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  padding: 16px 20px;
  border-radius: 12px;
  width: 340px;
  text-align: left;
}
.progress-text { font-size: 0.82rem; color: var(--c-text); margin-bottom: 8px; font-weight: 500; }
.progress-count { color: var(--c-muted); float: right; font-size: 0.8rem; }
.progress-bar-bg { width: 100%; height: 6px; background: #E2E8F0; border-radius: 100px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: linear-gradient(90deg, var(--c-primary), #0EA5E9); transition: width 0.4s ease; }

/* ── Matriz Likert (Tabla Estilizada) ────────────────────────────────────── */
.test-card-container {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.01);
}
.likert-table-wrapper { overflow-x: auto; }
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.likert-table { width: 100%; border-collapse: collapse; text-align: left; }

.likert-table th {
  padding: 16px;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-muted);
  border-bottom: 2px solid var(--c-border);
  background: #F8FAFC;
}
.col-question { width: 45%; }
.col-option { width: 11%; text-align: center; }

.likert-row { border-bottom: 1px solid var(--c-border); transition: background 0.15s; }
.likert-row:hover { background: #F8FAFC; }

.question-text { padding: 20px 16px; font-size: 0.95rem; font-weight: 500; color: var(--c-text); }
.question-number { color: var(--c-primary); font-weight: 700; margin-right: 6px; }

.option-cell { text-align: center; cursor: pointer; padding: 16px; }

/* Custom Radio Buttons redondos e interactivos */
.radio-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}
.radio-container input { position: absolute; opacity: 0; cursor: pointer; }

.custom-radio {
  width: 34px; height: 34px;
  border: 2px solid #CBD5E1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  background: #FFFFFF;
}
.custom-radio__inner { font-size: 0.85rem; font-weight: 700; color: #64748B; }

/* Estados dinámicos de selección de la escala Likert */
.radio-container input:checked ~ .custom-radio {
  border-color: var(--c-primary);
  background: var(--c-primary);
}
.radio-container input:checked ~ .custom-radio .custom-radio__inner { color: #FFFFFF; }
.likert-row:hover .custom-radio { border-color: #94A3B8; }

/* ── Footer de Navegación ───────────────────────────────────────────────── */
.test-navigation-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 32px;
  border-top: 1px solid var(--c-border);
  padding-top: 24px;
}
.validation-warning { font-size: 0.85rem; color: #EF4444; font-weight: 600; background: #FEF2F2; padding: 8px 16px; border-radius: 8px; border: 1px solid #FCA5A5; }

/* Botones estructurados del Home */
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 28px; border-radius: 100px; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.92rem; text-decoration: none; cursor: pointer; transition: all 0.2s; border: none; }
.btn--primary { background: var(--c-primary); color: #fff; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.2); }
.btn--primary:hover { transform: translateY(-1px); background: #4338CA; box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3); }
.btn--ghost { background: #FFFFFF; color: var(--c-text); border: 1px solid var(--c-border); }
.btn--ghost:hover:not(:disabled) { border-color: var(--c-primary); color: var(--c-primary); }
.btn--ghost:disabled { color: #CBD5E1; border-color: #E2E8F0; cursor: not-allowed; }

@media (max-width: 900px) {
  .main-content { padding: 20px; box-sizing: border-box; min-width: 0; }
  .test-card-container, .test-header-zone { min-width: 0; }
  .likert-table-wrapper { max-width: 100%; }
  .test-header-zone { flex-direction: column; align-items: flex-start; }
  .progress-stats-box { width: 100%; box-sizing: border-box; }
  .likert-table th:not(.col-question), .option-cell { padding: 8px 4px; }
  .custom-radio { width: 28px; height: 28px; }
}
</style>
