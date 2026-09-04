<template>
  <div class="landing">

    <nav class="nav">
      <div class="nav__logo">
        <span class="nav__logo-icon">◈</span>
        <span class="nav__logo-text">Vócalis</span>
      </div>
      <div class="nav__links">
        <a href="#como-funciona">Cómo funciona</a>
        <a href="#dimensiones">El test</a>
        <router-link to="/auth" class="nav__cta">Comenzar gratis</router-link>
      </div>
    </nav>

    <section class="hero">
      <div class="hero__bg-glow hero__bg-glow--1"></div>
      <div class="hero__bg-glow hero__bg-glow--2"></div>

      <div class="hero__content">
        <div class="hero__badge">
          <span class="badge__dot"></span>
          Test científico · Modelo Big Five OCEAN
        </div>

        <h1 class="hero__title">
          Descubre quién<br />
          <em>realmente</em> eres.
        </h1>

        <p class="hero__sub">
          Un test de personalidad validado científicamente que conecta tu perfil
          con las carreras donde puedes brillar de verdad.
        </p>

        <div class="hero__actions">
          <a href="#register" class="btn btn--primary">
            Descubrir mi perfil
            <span class="btn__arrow">→</span>
          </a>
          <a href="#como-funciona" class="btn btn--ghost">Ver cómo funciona</a>
        </div>

        <div class="hero__stats">
          <div class="stat">
            <span class="stat__num">44</span>
            <span class="stat__label">preguntas</span>
          </div>
          <div class="stat__divider"></div>
          <div class="stat">
            <span class="stat__num">5</span>
            <span class="stat__label">dimensiones</span>
          </div>
          <div class="stat__divider"></div>
          <div class="stat">
            <span class="stat__num">~8</span>
            <span class="stat__label">minutos</span>
          </div>
        </div>
      </div>

      <div class="hero__radar-wrap">
        <div class="radar__label radar__label--top">Apertura</div>
        <div class="radar__label radar__label--tr">Responsabilidad</div>
        <div class="radar__label radar__label--br">Extraversión</div>
        <div class="radar__label radar__label--bl">Amabilidad</div>
        <div class="radar__label radar__label--tl">Neuroticismo</div>
        <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg">
          <polygon class="radar__grid" points="160,40 268,100 268,220 160,280 52,220 52,100" />
          <polygon class="radar__grid" points="160,72 244,116 244,204 160,248 76,204 76,116" />
          <polygon class="radar__grid" points="160,104 220,132 220,188 160,216 100,188 100,132" />
          <polygon class="radar__grid" points="160,136 196,148 196,172 160,184 124,172 124,148" />
          <line class="radar__axis" x1="160" y1="160" x2="160" y2="40" />
          <line class="radar__axis" x1="160" y1="160" x2="268" y2="100" />
          <line class="radar__axis" x1="160" y1="160" x2="268" y2="220" />
          <line class="radar__axis" x1="160" y1="160" x2="160" y2="280" />
          <line class="radar__axis" x1="160" y1="160" x2="52" y2="220" />
          <line class="radar__axis" x1="160" y1="160" x2="52" y2="100" />
          <polygon class="radar__data" ref="radarData" :points="radarPoints" />
          <circle
            v-for="(pt, i) in radarDots"
            :key="i"
            :cx="pt.x"
            :cy="pt.y"
            r="5"
            class="radar__dot"
          />
        </svg>
      </div>
    </section>

    <section class="steps" id="como-funciona">
      <div class="section__eyebrow">El proceso</div>
      <h2 class="section__title">Tres pasos, una respuesta.</h2>

      <div class="steps__grid">
        <div class="step-card" v-for="step in steps" :key="step.n">
          <div class="step-card__num">{{ step.n }}</div>
          <h3 class="step-card__title">{{ step.title }}</h3>
          <p class="step-card__desc">{{ step.desc }}</p>
        </div>
      </div>
    </section>

    <section class="ocean" id="dimensiones">
      <div class="ocean__left">
        <div class="section__eyebrow">El modelo científico</div>
        <h2 class="section__title">El Big Five<br />OCEAN.</h2>
        <p class="ocean__intro">
          El modelo de personalidad más respaldado por la psicología moderna,
          con décadas de investigación y validación en más de 50 países.
        </p>
      </div>
      <div class="ocean__cards">
        <div
          class="ocean-card"
          v-for="dim in dimensions"
          :key="dim.letter"
          :style="{ '--accent': dim.color }"
        >
          <span class="ocean-card__letter">{{ dim.letter }}</span>
          <div>
            <h4 class="ocean-card__name">{{ dim.name }}</h4>
            <p class="ocean-card__desc">{{ dim.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="report-preview">
      <div class="section__eyebrow">Tu reporte</div>
      <h2 class="section__title">No solo un número.<br />Una hoja de ruta.</h2>
      <div class="report-preview__grid">
        <div class="report-card" v-for="card in reportFeatures" :key="card.title">
          <h4 class="report-card__title">{{ card.title }}</h4>
          <p class="report-card__desc">{{ card.desc }}</p>
        </div>
      </div>
    </section>

    <section class="register" id="register">
      <div class="register__glow"></div>
      <div class="register__box">
        <div class="section__eyebrow">Empieza hoy</div>
        <h2 class="register__title">Tu perfil te está esperando.</h2>
        <p class="register__sub">
          Gratis, sin tarjeta de crédito. Solo tú y 44 preguntas que pueden cambiar tu rumbo.
        </p>
        <form class="register__form" @submit.prevent="handleRegister">
          <input
            v-model="form.name"
            class="register__input"
            type="text"
            placeholder="Tu nombre"
            required
          />
          <input
            v-model="form.email"
            class="register__input"
            type="email"
            placeholder="tu@correo.cl"
            required
          />
          <button type="submit" class="btn btn--primary btn--full">
            Crear mi cuenta gratis
            <span class="btn__arrow">→</span>
          </button>
        </form>
        <p class="register__login">
          ¿Ya tienes cuenta?
          <router-link to="/auth">Inicia sesión aquí</router-link>
        </p>
      </div>
    </section>

    <footer class="footer">
      <div class="footer__logo">
        <span class="nav__logo-icon">◈</span>
        <span>Vócalis</span>
      </div>
      <p class="footer__copy">
        Proyecto de Título · Ingeniería en Informática · 2026
      </p>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

// ── Radar animation ──────────────────────────────────────────────────────────
const AXES = [
  { angle: -90 },   // top (Apertura)
  { angle: -18 },   // top-right (Responsabilidad)
  { angle: 54  },   // bottom-right (Extraversión)
  { angle: 126 },   // bottom-left (Amabilidad)
  { angle: 198 },   // top-left (Neuroticismo)
]
const CENTER = 160
const MAX_R  = 120

const targetValues  = ref([0.85, 0.70, 0.60, 0.80, 0.45])
const currentValues = ref([0.0,  0.0,  0.0,  0.0,  0.0 ])
let animFrame = null
let phaseTick = 0

function lerp(a, b, t) { return a + (b - a) * t }

function polarToXY(angleDeg, r) {
  const rad = (angleDeg * Math.PI) / 180
  return {
    x: CENTER + r * Math.cos(rad),
    y: CENTER + r * Math.sin(rad),
  }
}

function tick() {
  phaseTick++
  // Slowly morph target every ~180 frames
  if (phaseTick % 180 === 0) {
    targetValues.value = targetValues.value.map(() => 0.35 + Math.random() * 0.60)
  }
  currentValues.value = currentValues.value.map((v, i) =>
    lerp(v, targetValues.value[i], 0.02)
  )
  animFrame = requestAnimationFrame(tick)
}

onMounted(() => { animFrame = requestAnimationFrame(tick) })
onUnmounted(() => { if (animFrame) cancelAnimationFrame(animFrame) })

const radarDots = computed(() =>
  AXES.map((ax, i) => polarToXY(ax.angle, currentValues.value[i] * MAX_R))
)

const radarPoints = computed(() =>
  radarDots.value.map(p => `${p.x},${p.y}`).join(' ')
)

// ── Content data ─────────────────────────────────────────────────────────────
const router = useRouter()

const steps = [
  { n: '01', title: 'Responde el test', desc: 'Contesta 44 afirmaciones simples sobre cómo piensas, sientes y actúas. Sin respuestas incorrectas.' },
  { n: '02', title: 'Conoce tu perfil', desc: 'El sistema calcula tus puntuaciones en las 5 dimensiones OCEAN y genera tu radar de personalidad.' },
  { n: '03', title: 'Descubre tu ruta', desc: 'Recibe recomendaciones de áreas profesionales y familias de carreras alineadas con tus fortalezas.' },
]

const dimensions = [
  { letter: 'O', name: 'Apertura', desc: 'Creatividad, curiosidad intelectual y gusto por las nuevas experiencias.', color: '#4F46E5' },
  { letter: 'C', name: 'Responsabilidad', desc: 'Organización, disciplina y orientación al logro de metas.', color: '#10B981' },
  { letter: 'E', name: 'Extraversión', desc: 'Sociabilidad, energía y comodidad en entornos grupales.', color: '#F59E0B' },
  { letter: 'A', name: 'Amabilidad', desc: 'Empatía, cooperación y disposición a ayudar a los demás.', color: '#EC4899' },
  { letter: 'N', name: 'Neuroticismo', desc: 'Respuesta emocional y gestión del estrés y la ansiedad.', color: '#EF4444' },
]

const reportFeatures = [
  { title: 'Gráfico radar OCEAN', desc: 'Visualiza tus cinco dimensiones de un vistazo en un gráfico interactivo.' },
  { title: 'Texto interpretativo', desc: 'Explicación personalizada de qué significa cada puntaje en tu caso particular.' },
  { title: 'Áreas profesionales', desc: 'Sugerencias concretas de rubros laborales donde tu perfil tiene mayor afinidad.' },
  { title: 'Familias de carreras', desc: 'Grupos de carreras ordenados por compatibilidad con tus fortalezas detectadas.' },
]

// ── Form ──────────────────────────────────────────────────────────────────────
// Este formulario solo captura el nombre y correo como puerta de entrada;
// el registro completo (contraseña, rol) se termina en /auth para no
// duplicar la lógica de creación de cuenta en dos lugares distintos.
const form = ref({ name: '', email: '' })
function handleRegister() {
  router.push({
    path: '/auth',
    query: { mode: 'register', name: form.value.name, email: form.value.email },
  })
}
</script>

<style scoped>
/* ── Reset & tokens ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@600;700;800&display=swap');

*,
*::before,
*::after { box-sizing: border-box; margin: 0; padding: 0; }

.landing {
  /* MODO CLARO - Paleta limpia y profesional */
  --c-bg:       #F8FAFC; /* Slate 50 - Fondo general */
  --c-surface:  #FFFFFF; /* Blanco puro para tarjetas */
  --c-primary:  #4F46E5; /* Índigo moderno */
  --c-accent1:  #0EA5E9; /* Sky blue */
  --c-accent2:  #10B981; /* Esmeralda */
  --c-text:     #0F172A; /* Slate 900 - Texto principal oscuro */
  --c-muted:    #64748B; /* Slate 500 - Texto secundario */
  --c-border:   #E2E8F0; /* Slate 200 - Bordes sutiles */
  --r-card:     16px;

  font-family: 'Inter', sans-serif;
  background: var(--c-bg);
  color: var(--c-text);
  overflow-x: hidden;
}

/* ── Nav ─────────────────────────────────────────────────────────────────── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 48px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--c-border);
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.nav__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.25rem;
  letter-spacing: -0.01em;
  color: var(--c-text);
}

.nav__logo-icon {
  color: var(--c-primary);
  font-size: 1.4rem;
}

.nav__links {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav__links a {
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s;
}

.nav__links a:hover { color: var(--c-primary); }

.nav__cta {
  background: var(--c-primary) !important;
  color: #FFFFFF !important;
  padding: 8px 20px;
  border-radius: 100px;
  font-size: 0.875rem !important;
  font-weight: 600;
  box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
}

.nav__cta:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3); }

/* ── Hero ────────────────────────────────────────────────────────────────── */
.hero {
  min-height: 100vh;
  padding: 120px 48px 80px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 64px;
  position: relative;
  overflow: hidden;
}

.hero__bg-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  z-index: 0;
}

.hero__bg-glow--1 {
  width: 480px; height: 480px;
  background: rgba(79, 70, 229, 0.12); /* Brillo índigo suave */
  top: -80px; left: -100px;
}

.hero__bg-glow--2 {
  width: 360px; height: 360px;
  background: rgba(16, 185, 129, 0.12); /* Brillo esmeralda suave */
  bottom: 0; right: 15%;
}

.hero__content {
  position: relative;
  z-index: 1;
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #EEF2FF;
  border: 1px solid #C7D2FE;
  color: var(--c-primary);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 100px;
  margin-bottom: 28px;
}

.badge__dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--c-primary);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%        { opacity: 0.5; transform: scale(0.8); }
}

.hero__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2.8rem, 5vw, 4.2rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 20px;
  color: var(--c-text);
}

.hero__title em {
  font-style: normal;
  background: linear-gradient(135deg, var(--c-primary), var(--c-accent1));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero__sub {
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--c-muted);
  max-width: 440px;
  margin-bottom: 36px;
}

.hero__actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 48px;
}

.hero__stats {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat__num {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.6rem;
  color: var(--c-primary);
  line-height: 1;
}

.stat__label {
  font-size: 0.75rem;
  color: var(--c-muted);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 600;
}

.stat__divider {
  width: 1px;
  height: 36px;
  background: var(--c-border);
}

/* ── Radar ───────────────────────────────────────────────────────────────── */
.hero__radar-wrap {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radar__svg {
  width: min(420px, 90vw);
  height: auto;
  filter: drop-shadow(0 10px 25px rgba(79, 70, 229, 0.15));
}

.radar__grid {
  fill: none;
  stroke: #CBD5E1; /* Gris medio para el grid */
  stroke-width: 1;
}

.radar__axis {
  stroke: #CBD5E1;
  stroke-width: 1;
}

.radar__data {
  fill: rgba(79, 70, 229, 0.15); /* Relleno índigo semitransparente */
  stroke: var(--c-primary);
  stroke-width: 2.5;
  stroke-linejoin: round;
  transition: points 0.05s linear;
}

.radar__dot {
  fill: var(--c-accent1);
  filter: drop-shadow(0 0 4px rgba(14, 165, 233, 0.5));
}

.radar__label {
  position: absolute;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--c-text);
  white-space: nowrap;
}

.radar__label--top { top: 2%; left: 50%; transform: translateX(-50%); }
.radar__label--tr  { top: 22%; right: 2%; }
.radar__label--br  { bottom: 22%; right: 2%; }
.radar__label--bl  { bottom: 22%; left: 2%; }
.radar__label--tl  { top: 22%; left: 2%; }

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn--primary {
  background: var(--c-primary);
  color: #fff;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3);
}

.btn--primary:hover {
  transform: translateY(-2px);
  background: #4338CA;
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}

.btn--ghost {
  background: #FFFFFF;
  color: var(--c-text);
  border: 1px solid var(--c-border);
}

.btn--ghost:hover {
  border-color: var(--c-primary);
  color: var(--c-primary);
}

.btn--full { width: 100%; justify-content: center; }

.btn__arrow {
  font-size: 1rem;
  transition: transform 0.2s;
}

.btn:hover .btn__arrow { transform: translateX(3px); }

/* ── Section shared ──────────────────────────────────────────────────────── */
.section__eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 12px;
}

.section__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(1.8rem, 3vw, 2.8rem);
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-bottom: 20px;
  color: var(--c-text);
}

/* ── Steps ───────────────────────────────────────────────────────────────── */
.steps {
  padding: 96px 48px;
  text-align: center;
  position: relative;
  background: var(--c-surface); /* Blanco para separar del hero */
}

.steps__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 48px;
}

.step-card {
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 36px 28px;
  text-align: left;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}

.step-card:hover {
  border-color: #C7D2FE;
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.step-card__num {
  font-family: 'Poppins', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--c-primary);
  margin-bottom: 16px;
}

.step-card__icon {
  font-size: 2rem;
  margin-bottom: 16px;
  line-height: 1;
}

.step-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.step-card__desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--c-muted);
}

/* ── Ocean ───────────────────────────────────────────────────────────────── */
.ocean {
  padding: 96px 48px;
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 64px;
  align-items: start;
}

.ocean__intro {
  font-size: 0.95rem;
  line-height: 1.65;
  color: var(--c-muted);
  max-width: 360px;
}

.ocean__cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ocean-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-left: 4px solid var(--accent);
  border-radius: var(--r-card);
  padding: 20px 24px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.ocean-card:hover {
  transform: translateX(6px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.06);
}

.ocean-card__letter {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 2rem;
  color: var(--accent);
  line-height: 1;
  min-width: 40px;
}

.ocean-card__name {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 4px;
}

.ocean-card__desc {
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--c-muted);
}

/* ── Report preview ──────────────────────────────────────────────────────── */
.report-preview {
  padding: 96px 48px;
  text-align: center;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
  border-bottom: 1px solid var(--c-border);
}

.report-preview__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-top: 48px;
}

.report-card {
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 28px 22px;
  text-align: left;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.report-card:hover { 
  border-color: var(--c-primary); 
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.08);
}

.report-card__icon {
  font-size: 1.8rem;
  margin-bottom: 14px;
  line-height: 1;
}

.report-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 8px;
  color: var(--c-text);
}

.report-card__desc {
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--c-muted);
}

/* ── Register ────────────────────────────────────────────────────────────── */
.register {
  padding: 96px 48px;
  display: flex;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.register__glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, rgba(79, 70, 229, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.register__box {
  position: relative;
  z-index: 1;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 56px 48px;
  width: 100%;
  max-width: 480px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0,0,0,0.04);
}

.register__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  letter-spacing: -0.02em;
  margin-bottom: 12px;
}

.register__sub {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--c-muted);
  margin-bottom: 36px;
}

.register__form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.register__input {
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  border-radius: 12px;
  padding: 14px 18px;
  font-size: 0.95rem;
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  width: 100%;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.register__input::placeholder { color: #94A3B8; }

.register__input:focus {
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
  background: #FFFFFF;
}

.register__login {
  margin-top: 20px;
  font-size: 0.85rem;
  color: var(--c-muted);
}

.register__login a {
  color: var(--c-primary);
  text-decoration: none;
  font-weight: 600;
}

/* ── Footer ──────────────────────────────────────────────────────────────── */
.footer {
  padding: 32px 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--c-border);
  background: var(--c-surface);
}

.footer__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
}

.footer__copy {
  font-size: 0.85rem;
  color: var(--c-muted);
  font-weight: 500;
}

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
    padding: 100px 24px 60px;
    gap: 48px;
    text-align: center;
  }

  .hero__sub,
  .hero__badge { margin-left: auto; margin-right: auto; }

  .hero__actions { justify-content: center; }
  .hero__stats   { justify-content: center; }

  .hero__radar-wrap {
    order: -1;
  }

  .steps,
  .ocean,
  .report-preview,
  .register { padding: 64px 24px; }

  .steps__grid        { grid-template-columns: 1fr; }
  .ocean              { grid-template-columns: 1fr; gap: 40px; }
  .report-preview__grid { grid-template-columns: repeat(2, 1fr); }

  .nav { padding: 16px 24px; }
  .nav__links a:not(.nav__cta) { display: none; }

  .register__box { padding: 36px 24px; }
  .footer { flex-direction: column; gap: 12px; text-align: center; }
}

@media (max-width: 480px) {
  .report-preview__grid { grid-template-columns: 1fr; }
}

/* ── Reduced motion ──────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .badge__dot       { animation: none; }
  .btn              { transition: none; }
  .step-card,
  .ocean-card,
  .report-card      { transition: none; }
}
</style>