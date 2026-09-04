<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div class="sidebar__brand">
        <span class="sidebar__logo-icon">◈</span>
        <span class="sidebar__logo-text">Vócalis</span>
      </div>
      
      <nav class="sidebar__nav">
        <a href="#" class="sidebar__link sidebar__link--active" @click.prevent>
          Dashboard
        </a>
        <a href="#" @click.prevent="startTest" class="sidebar__link">
          Realizar Test
        </a>
        <a href="#" @click.prevent="scrollToHistory" class="sidebar__link">
          Mi Historial
        </a>
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
            <span class="bpm-step__label">{{ step }}</span>
            <div v-if="index < bpmStages.length - 1" class="bpm-step__line"></div>
          </div>
        </div>
      </header>

      <section class="welcome-section">
        <h1 class="welcome-title">¡Hola de nuevo, José Miguel!</h1>
        <p class="welcome-sub">Estudiante de 4° Medio · Centro Educativo Técnico Profesional</p>
      </section>

      <div class="dashboard-grid">
        
        <div v-if="!hasPreviousTest" class="action-card action-card--start">
          <div class="action-card__info">
            <span class="action-card__badge">Disponible ahora</span>
            <h2 class="action-card__title">Tu evaluación vocacional está lista</h2>
            <p class="action-card__desc">
              Descubre tus fortalezas conductuales mediante el inventario científico BFI-44 de 44 ítems. 
              Te tomará aproximadamente 8 minutos completarlo de forma secuencial.
            </p>
            <button @click="startTest" class="btn btn--primary">
              Iniciar Evaluación Vocacional
            </button>
          </div>
          <div class="action-card__visual">
            <div class="visual-circle">◈</div>
          </div>
        </div>

        <div v-else class="action-card action-card--report">
          <div class="action-card__info">
            <span class="action-card__badge action-card__badge--success">Evaluación Completada</span>
            <h2 class="action-card__title">Último Reporte Generado</h2>
            <p class="action-card__desc">
              Tu perfil dominante actual muestra una alta afinidad con el área de 
              <strong>Tecnología e Ingeniería</strong> debido a tus altos índices de Apertura y Responsabilidad.
            </p>
            <div class="report-quick-stats">
              <div class="q-stat"><span>O</span> Apertura: 85%</div>
              <div class="q-stat"><span>C</span> Responsabilidad: 72%</div>
            </div>
            <button @click="viewLatestReport" class="btn btn--primary">
              Ver Reporte Completo
            </button>
          </div>
        </div>

        <div class="info-sidebar">
          <div class="info-mini-card">
            <div>
              <h4 class="mini-card__title">Consejo Vocacional</h4>
              <p class="mini-card__desc">Responde el cuestionario con total honestidad. No existen perfiles buenos ni malos, solo rutas distintas.</p>
            </div>
          </div>

          <div class="info-mini-card">
            <div>
              <h4 class="mini-card__title">Modelo Psicométrico</h4>
              <p class="mini-card__desc">Basado en el Big Five Inventory (BFI-44), garantizando precisión y validez científica.</p>
            </div>
          </div>

          <div class="simulator-switch">
            <p>Modo desarrollo — Simular estado del alumno:</p>
            <button @click="toggleTestState" class="sim-btn">
              Cambiar a: {{ hasPreviousTest ? 'Primer Ingreso' : 'Con Test Hecho' }}
            </button>
          </div>
        </div>

      </div>

      <section class="history-section" id="history-section">
        <h3 class="history-title">Historial de Perfiles Guardados</h3>
        
        <div class="history-table-container">
          <table class="history-table">
            <thead>
              <tr>
                <th>Fecha de Aplicación</th>
                <th>Instrumento</th>
                <th>Dimensión Dominante</th>
                <th>Estado del Flujo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, index) in historyRecords" :key="index">
                <td><strong>{{ record.date }}</strong></td>
                <td><span class="inst-tag">BFI-44</span></td>
                <td>{{ record.dominant }}</td>
                <td><span class="status-tag" :class="'status-tag--' + record.statusClass">{{ record.status }}</span></td>
                <td>
                  <button @click="viewLatestReport" class="table-action-btn">Ver Reporte</button>
                </td>
              </tr>
              <tr v-if="historyRecords.length === 0">
                <td colspan="5" class="empty-table-text">No registras perfiles guardados en períodos anteriores.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado simulado del estudiante: true si ya rindió un test, false si es nuevo
const hasPreviousTest = ref(false)

// Configuración de las etapas del proceso Camunda 8 BPMN
const bpmStages = ['Registro', 'Evaluación', 'Procesamiento', 'Reporte Listo']

// Índice actual del progreso BPM basado en el estado simulado del alumno
const currentBpmStageIndex = computed(() => {
  return hasPreviousTest.value ? 3 : 1 // Etapa 'Reporte Listo' (3) o 'Evaluación' (1)
})

const currentBpmStageText = computed(() => {
  return bpmStages[currentBpmStageIndex.value]
})

// Registros de historial simulados dinámicamente según el switcher
const historyRecords = computed(() => {
  if (!hasPreviousTest.value) return []
  return [
    { date: '19 de Junio, 2026', dominant: 'Apertura a la Experiencia (O)', status: 'Finalizado', statusClass: 'success' },
    { date: '14 de Abril, 2026', dominant: 'Amabilidad / Cooperación (A)', status: 'Archivado', statusClass: 'muted' }
  ]
})

// Funciones de simulación y redirección hacia próximos mockups
function toggleTestState() {
  hasPreviousTest.value = !hasPreviousTest.value
}

function startTest() {
  router.push('/estudiante/evaluacion') // Redirección exacta
}

function viewLatestReport() {
  router.push('/estudiante/reporte')
}

function scrollToHistory() {
  const el = document.getElementById('history-section')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
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
.welcome-sub { font-size: 0.9rem; color: var(--c-muted); }

/* ── Tarjetas Informativas y Dashboard Grid ─────────────────────────────── */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  margin-bottom: 40px;
  align-items: start;
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
.action-card__desc { font-size: 0.92rem; line-height: 1.6; color: var(--c-muted); margin-bottom: 24px; }

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
.info-sidebar { display: flex; flex-direction: column; gap: 16px; }
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

/* Switch de Desarrollo */
.simulator-switch {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: var(--r-card);
  padding: 16px;
  text-align: left;
}
.simulator-switch p { font-size: 0.78rem; font-weight: 700; color: #92400E; margin-bottom: 8px; }
.sim-btn {
  width: 100%;
  padding: 8px;
  background: #F59E0B;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
}

/* ── Sección de Historial de Trazabilidad ────────────────────────────────── */
.history-section { text-align: left; margin-top: 16px; }
.history-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.2rem; margin-bottom: 16px; }

.history-table-container {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.01);
}
.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
}
.history-table th {
  background: #F8FAFC;
  padding: 14px 20px;
  font-weight: 600;
  color: var(--c-muted);
  border-bottom: 1px solid var(--c-border);
}
.history-table td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--c-border);
}
.inst-tag {
  background: #F1F5F9;
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.78rem;
}
.status-tag {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
}
.status-tag--success { background: #D1FAE5; color: #065F46; }
.status-tag--muted { background: #E2E8F0; color: #475569; }

.table-action-btn {
  background: none;
  border: 1px solid var(--c-primary);
  color: var(--c-primary);
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}
.table-action-btn:hover { background: var(--c-primary); color: #FFFFFF; }
.empty-table-text { text-align: center; color: var(--c-muted); padding: 32px !important; font-style: italic; }

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
@media (max-width: 900px) {
  .sidebar { display: none; }
  .main-content { margin-left: 0; padding: 24px; }
  .dashboard-grid { grid-template-columns: 1fr; }
  .bpm-step__label { display: none; }
}
</style>