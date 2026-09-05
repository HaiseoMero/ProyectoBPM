<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div class="sidebar__brand">
        <span class="sidebar__logo-icon">◈</span>
        <span class="sidebar__logo-text">Vócalis</span>
      </div>
      
      <nav class="sidebar__nav">
        <router-link to="/estudiante/dashboard" class="sidebar__link">
          Dashboard
        </router-link>
        <a href="#" class="sidebar__link sidebar__link--active">
          Realizar Test
        </a>
        <router-link to="/estudiante/dashboard#history-section" class="sidebar__link">
          Mi Historial
        </router-link>
      </nav>

      <div class="sidebar__footer">
        <div class="user-avatar-zone">
          <div class="avatar">JM</div>
          <div class="user-info">
            <span class="user-name">José Miguel</span>
            <span class="user-role">Estudiante</span>
          </div>
        </div>
        <router-link to="/auth" class="logout-btn">
          Cerrar Sesión
        </router-link>
      </div>
    </aside>

    <main class="main-content">
      
      <header class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Flujo Activo Camunda 8</span>
          <span class="bpm-status-text">Estado actual: <strong>Rindiendo Cuestionario Psicométrico</strong></span>
        </div>
        
        <div class="bpm-steps">
          <div class="bpm-step bpm-step--completed">
            <div class="bpm-step__node">✓</div>
            <span class="bpm-step__label">Registro</span>
            <div class="bpm-step__line"></div>
          </div>
          <div class="bpm-step bpm-step--active">
            <div class="bpm-step__node">2</div>
            <span class="bpm-step__label">Evaluación</span>
            <div class="bpm-step__line"></div>
          </div>
          <div class="bpm-step">
            <div class="bpm-step__node">3</div>
            <span class="bpm-step__label">Procesamiento</span>
            <div class="bpm-step__line"></div>
          </div>
          <div class="bpm-step">
            <div class="bpm-step__node">4</div>
            <span class="bpm-step__label">Reporte Listo</span>
          </div>
        </div>
      </header>

      <section class="test-header-zone">
        <div class="test-title-container">
          <h1 class="test-title">Inventario Big Five (BFI-44)</h1>
          <div class="test-instructions-box">
            <span class="instructions-icon">✨</span>
            <p>
              Vas a responder 44 afirmaciones sobre cómo eres normalmente. No hay respuestas correctas o incorrectas. Responde con tu primera impresión — no lo pienses demasiado, ni te compares con lo que crees que "deberías" ser. <strong>Solo podrás realizar este test una vez</strong>, así que tómate un momento para estar tranquilo/a antes de comenzar.
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
        <template v-else>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import evaluacionService from '../services/evaluacionService'

const router = useRouter()

// El banco de ítems se carga desde el servicio (hoy mock, mañana la tabla
// `pregunta` en MySQL vía FastAPI).
const questions = ref([])
const loadingQuestions = ref(true)

onMounted(async () => {
  questions.value = await evaluacionService.getQuestions()
  loadingQuestions.value = false
})

// Paginación
const currentPage = ref(0)
const itemsPerPage = 10
const validationMessage = ref('')
const submitting = ref(false)

// Estado de respuestas: clave es ID de pregunta, valor es puntaje Likert (1 a 5)
const answers = ref({})

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

function selectAnswer(qId, val) {
  answers.value[qId] = val
  validationMessage.value = ''
  evaluacionService.saveAnswer(qId, val)
}

function prevPage() {
  if (currentPage.value > 0) {
    currentPage.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

async function nextPage() {
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

  // Última página: enviamos el cuestionario completo y el motor BPM procesa
  // el cálculo de las dimensiones OCEAN. El reporte generado se muestra
  // directamente, sin diálogos bloqueantes.
  submitting.value = true
  try {
    await evaluacionService.submitEvaluation(answers.value)
    router.push('/estudiante/reporte')
  } finally {
    submitting.value = false
  }
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
.sidebar__link:hover, .sidebar__link--active { background: #EEF2FF; color: var(--c-primary); }
.sidebar__icon { font-size: 1.1rem; }
.sidebar__footer { border-top: 1px solid var(--c-border); padding-top: 20px; display: flex; flex-direction: column; gap: 16px; }
.user-avatar-zone { display: flex; align-items: center; gap: 12px; }
.avatar {
  width: 40px; height: 40px;
  background: #C7D2FE; color: var(--c-primary);
  border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;
}
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
  .sidebar { display: none; }
  .main-content { margin-left: 0; padding: 20px; }
  .test-header-zone { flex-direction: column; align-items: flex-start; }
  .progress-stats-box { width: 100%; }
  .likert-table th:not(.col-question), .option-cell { padding: 8px 4px; }
  .custom-radio { width: 28px; height: 28px; }
}
</style>