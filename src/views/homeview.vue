<template>
  <div class="landing">

    <nav class="nav" aria-label="Navegación de inicio">
      <div class="nav__logo">
        <span class="nav__logo-icon" aria-hidden="true">◈</span>
        <span class="nav__logo-text">Vócalis</span>
      </div>
      <div class="nav__links">
        <router-link to="/como-funciona">Cómo funciona</router-link>
        <router-link to="/el-test">El test</router-link>
        <router-link to="/auth" class="nav__cta">Comenzar gratis</router-link>
      </div>
    </nav>

    <main>
    <!-- ── Hero ─────────────────────────────────────────────────────────── -->
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__bg-glow" aria-hidden="true"></div>

      <div class="hero__inner wrap">
        <div class="hero__content">
          <p class="hero__eyebrow">Cuestionario BFI-44 · Modelo de los cinco grandes</p>

          <h1 id="hero-title" class="hero__title">
            Conoce más<br />
            <em>sobre</em> ti.
          </h1>

          <p class="hero__sub">
            Explora tus rasgos de personalidad con el BFI-44 y comparte tus resultados
            con tu orientador. Un apoyo para reflexionar sobre tu futuro, junto con tus intereses y experiencias.
          </p>

          <div class="hero__actions">
            <a href="#register" class="btn btn--primary">
              Descubrir mi perfil
              <span class="btn__arrow" aria-hidden="true">→</span>
            </a>
            <router-link to="/como-funciona" class="btn btn--ghost">Ver cómo funciona</router-link>
          </div>

          <div class="hero__stats">
            <div class="stat">
              <span class="stat__num">44</span>
              <span class="stat__label">afirmaciones</span>
            </div>
            <div class="stat__divider" aria-hidden="true"></div>
            <div class="stat">
              <span class="stat__num">5</span>
              <span class="stat__label">dimensiones</span>
            </div>
            <div class="stat__divider" aria-hidden="true"></div>
            <div class="stat">
              <span class="stat__num">~8</span>
              <span class="stat__label">minutos</span>
            </div>
          </div>
        </div>

        <div class="hero__visual">
          <div class="hero__visual-head">
            <span class="hero__visual-title">Perfil de ejemplo</span>
            <span class="hero__visual-tag">Datos ficticios</span>
          </div>

          <div ref="radarContainer" class="hero__radar-wrap">
            <div class="radar__label radar__label--top">Apertura</div>
            <div class="radar__label radar__label--tr">Responsabilidad</div>
            <div class="radar__label radar__label--br">Extraversión</div>
            <div class="radar__label radar__label--bl">Amabilidad</div>
            <div class="radar__label radar__label--tl">Neuroticismo</div>
            <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="landing-radar-title">
              <title id="landing-radar-title">Ejemplo de las cinco dimensiones OCEAN</title>
              <polygon v-for="(points, index) in radarGridPoints" :key="index"
                       class="radar__grid" :points="points" />
              <line v-for="(point, index) in radarAxes" :key="index" class="radar__axis"
                    :x1="CENTER" :y1="CENTER" :x2="point.x" :y2="point.y" />
              <polygon class="radar__data" :points="radarPoints" />
              <circle
                v-for="(pt, i) in radarDots"
                :key="i"
                :cx="pt.x"
                :cy="pt.y"
                r="4.5"
                class="radar__dot"
              />
            </svg>
          </div>

          <p class="hero__visual-note">
            Cada dimensión es un continuo. No hay perfiles mejores ni peores, solo formas distintas de ser.
          </p>
        </div>
      </div>
    </section>

    <!-- ── Para quién ───────────────────────────────────────────────────── -->
    <section class="audience" id="para-quien" aria-labelledby="audience-title">
      <div class="wrap">
        <header class="section__head">
          <p class="section__eyebrow">Para quién es</p>
          <h2 id="audience-title" class="section__title">Una herramienta,<br />dos miradas.</h2>
          <p class="section__lead">
            Vócalis conecta lo que cada estudiante descubre de sí mismo con el acompañamiento
            que ya ocurre en la orientación escolar.
          </p>
        </header>

        <div class="audience__grid">
          <article v-for="group in audiences" :key="group.title" class="audience-card" :class="`audience-card--${group.tone}`">
            <div class="audience-card__head">
              <span class="audience-card__icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path :d="group.icon" />
                </svg>
              </span>
              <div>
                <p class="audience-card__kicker">{{ group.kicker }}</p>
                <h3 class="audience-card__title">{{ group.title }}</h3>
              </div>
            </div>
            <ul class="audience-card__list">
              <li v-for="item in group.items" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <!-- ── Proceso ──────────────────────────────────────────────────────── -->
    <section class="steps" id="como-funciona" aria-labelledby="steps-title">
      <div class="wrap">
        <header class="section__head section__head--row">
          <div>
            <p class="section__eyebrow">El proceso</p>
            <h2 id="steps-title" class="section__title">Tres pasos para<br />conocerte mejor.</h2>
          </div>
          <router-link to="/como-funciona" class="text-link">
            Ver el recorrido completo <span aria-hidden="true">→</span>
          </router-link>
        </header>

        <ol class="steps__list">
          <li class="step-card" v-for="step in steps" :key="step.n">
            <span class="step-card__num" aria-hidden="true">{{ step.n }}</span>
            <h3 class="step-card__title">{{ step.title }}</h3>
            <p class="step-card__desc">{{ step.desc }}</p>
          </li>
        </ol>
      </div>
    </section>

    <!-- ── Dimensiones ──────────────────────────────────────────────────── -->
    <section class="ocean" id="dimensiones" aria-labelledby="ocean-title">
      <div class="ocean__inner wrap">
        <div class="ocean__left">
          <p class="section__eyebrow">Las dimensiones de personalidad</p>
          <h2 id="ocean-title" class="section__title">El Big Five<br />OCEAN.</h2>
          <p class="ocean__intro">
            El modelo Big Five describe cinco dimensiones de personalidad. En Vócalis,
            estos resultados aportan una perspectiva para conversar sobre cómo te describes y lo que te interesa.
          </p>
          <p class="ocean__hint">
            Cada rasgo va de un extremo a otro. Tu resultado indica hacia dónde tiendes,
            no si está bien o mal.
          </p>
          <router-link to="/el-test" class="text-link">
            Conocer cada dimensión en detalle <span aria-hidden="true">→</span>
          </router-link>
        </div>

        <ul class="ocean__cards">
          <li
            class="ocean-card"
            v-for="dim in dimensions"
            :key="dim.letter"
            :style="{ '--accent': dim.color }"
          >
            <span class="ocean-card__letter" aria-hidden="true">{{ dim.letter }}</span>
            <div class="ocean-card__body">
              <h3 class="ocean-card__name">{{ dim.name }}</h3>
              <p class="ocean-card__desc">{{ dim.desc }}</p>
              <p class="ocean-card__scale">
                <span class="visually-hidden">Va desde </span>
                <span class="ocean-card__pole">{{ dim.low }}</span>
                <span class="visually-hidden"> hasta </span>
                <span class="ocean-card__track" aria-hidden="true"></span>
                <span class="ocean-card__pole ocean-card__pole--high">{{ dim.high }}</span>
              </p>
            </div>
          </li>
        </ul>
      </div>
    </section>

    <!-- ── Reporte ──────────────────────────────────────────────────────── -->
    <section class="report-preview" aria-labelledby="report-title">
      <div class="report-preview__inner wrap">
        <header class="section__head">
          <p class="section__eyebrow">Tu reporte</p>
          <h2 id="report-title" class="section__title">Tus resultados.<br />Un punto de partida.</h2>
          <p class="section__lead">
            Al terminar el cuestionario recibes un reporte que puedes consultar desde tu cuenta
            y revisar junto a tu orientador.
          </p>
        </header>

        <div class="report-preview__grid">
          <article class="report-card" v-for="card in reportFeatures" :key="card.title">
            <span class="report-card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path :d="card.icon" />
              </svg>
            </span>
            <h3 class="report-card__title">{{ card.title }}</h3>
            <p class="report-card__desc">{{ card.desc }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ── Expectativas ─────────────────────────────────────────────────── -->
    <section class="scope" aria-labelledby="scope-title">
      <div class="wrap">
        <header class="section__head">
          <p class="section__eyebrow">Antes de empezar</p>
          <h2 id="scope-title" class="section__title">Qué es Vócalis,<br />y qué no es.</h2>
        </header>

        <div class="scope__grid">
          <div class="scope__col scope__col--is">
            <h3 class="scope__heading">Es</h3>
            <ul class="scope__list">
              <li v-for="item in scopeIs" :key="item">
                <svg class="scope__mark" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 10.5l3.2 3.2L15 6.8" /></svg>
                <span>{{ item }}</span>
              </li>
            </ul>
          </div>
          <div class="scope__col scope__col--not">
            <h3 class="scope__heading">No es</h3>
            <ul class="scope__list">
              <li v-for="item in scopeNot" :key="item">
                <svg class="scope__mark" viewBox="0 0 20 20" aria-hidden="true"><path d="M6 10h8" /></svg>
                <span>{{ item }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Registro ─────────────────────────────────────────────────────── -->
    <section class="register" id="register" aria-labelledby="register-title">
      <div class="register__inner wrap">
        <div class="register__copy">
          <p class="section__eyebrow section__eyebrow--on-dark">Empieza hoy</p>
          <h2 id="register-title" class="register__title">Tu perfil te está esperando.</h2>
          <p class="register__sub">
            Crea tu cuenta y responde 44 afirmaciones para empezar a reflexionar. Vócalis complementa el acompañamiento de tu orientador.
          </p>
          <ul class="register__facts">
            <li>Sin costo para estudiantes</li>
            <li>Desde tu computador o teléfono</li>
            <li>Tus respuestas se guardan mientras avanzas</li>
          </ul>
        </div>

        <div class="register__box">
          <form class="register__form" @submit.prevent="handleRegister">
            <div class="field">
              <label for="landing-name">Tu nombre</label>
              <input
                id="landing-name"
                name="nombre"
                autocomplete="name"
                v-model="form.name"
                class="register__input"
                type="text"
                placeholder="Ej.: Camila Rojas"
                required
              />
            </div>
            <div class="field">
              <label for="landing-email">Correo electrónico</label>
              <input
                id="landing-email"
                name="email"
                autocomplete="email"
                inputmode="email"
                autocapitalize="none"
                :spellcheck="false"
                v-model="form.email"
                class="register__input"
                type="email"
                placeholder="tu@correo.cl"
                required
              />
            </div>
            <button type="submit" class="btn btn--primary btn--full">
              Crear mi cuenta gratis
              <span class="btn__arrow" aria-hidden="true">→</span>
            </button>
            <p class="register__hint">En el siguiente paso eliges tu rol y completas tus datos.</p>
          </form>
          <p class="register__login">
            ¿Ya tienes cuenta?
            <router-link to="/auth">Inicia sesión aquí</router-link>
          </p>
        </div>
      </div>
    </section>
    </main>

    <footer class="footer">
      <div class="footer__inner wrap">
        <div class="footer__brand">
          <div class="footer__logo">
            <span class="nav__logo-icon" aria-hidden="true">◈</span>
            <span>Vócalis</span>
          </div>
          <p class="footer__copy">
            Proyecto de Título · Ingeniería en Informática · 2026
          </p>
        </div>
        <div class="footer__links">
          <router-link to="/como-funciona">Cómo funciona</router-link>
          <router-link to="/el-test">El test</router-link>
          <router-link to="/auth">Iniciar sesión</router-link>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

defineOptions({ name: 'HomeView' })

// ── Radar animation ──────────────────────────────────────────────────────────
const AXES = [
  { letter: 'O', angle: -90 },
  { letter: 'C', angle: -18 },
  { letter: 'E', angle: 54 },
  { letter: 'A', angle: 126 },
  { letter: 'N', angle: 198 },
]
const CENTER = 160
const MAX_R  = 120

const exampleValues = [0.85, 0.70, 0.60, 0.80, 0.45]
const targetValues = ref([...exampleValues])
const currentValues = ref(exampleValues.map(() => 0))
const radarContainer = ref(null)
let animFrame = null
let lastTimestamp = null
let targetElapsed = 0
let radarVisible = false
let observer

function polarToXY(angleDeg, r) {
  const rad = (angleDeg * Math.PI) / 180
  return {
    x: CENTER + r * Math.cos(rad),
    y: CENTER + r * Math.sin(rad),
  }
}

const radarAxes = AXES.map(axis => polarToXY(axis.angle, MAX_R))
const radarGridPoints = [1, 0.75, 0.5, 0.25].map(scale =>
  AXES.map(axis => {
    const point = polarToXY(axis.angle, MAX_R * scale)
    return `${point.x},${point.y}`
  }).join(' ')
)

function stopRadar() {
  if (animFrame !== null) cancelAnimationFrame(animFrame)
  animFrame = null
  lastTimestamp = null
}

function canAnimate() {
  return radarVisible && !document.hidden
}

// Conserva el movimiento continuo original y su velocidad en distintas pantallas.
function animateRadar(timestamp) {
  animFrame = null
  if (!canAnimate()) { stopRadar(); return }
  const elapsed = lastTimestamp === null ? 1000 / 60 : Math.min(timestamp - lastTimestamp, 100)
  lastTimestamp = timestamp
  targetElapsed += elapsed
  if (targetElapsed >= 3000) {
    targetElapsed %= 3000
    targetValues.value = targetValues.value.map(() => 0.35 + Math.random() * 0.60)
  }
  const blend = 1 - Math.pow(0.98, elapsed / (1000 / 60))
  currentValues.value = currentValues.value.map((value, index) =>
    value + (targetValues.value[index] - value) * blend
  )
  animFrame = requestAnimationFrame(animateRadar)
}

function syncRadar() {
  if (!canAnimate()) {
    stopRadar()
    return
  }
  if (animFrame === null) animFrame = requestAnimationFrame(animateRadar)
}

onMounted(() => {
  document.addEventListener('visibilitychange', syncRadar)
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(([entry]) => {
      radarVisible = entry.isIntersecting
      syncRadar()
    }, { threshold: 0.15 })
    observer.observe(radarContainer.value)
  } else {
    radarVisible = true
    syncRadar()
  }
})
onUnmounted(() => {
  stopRadar()
  observer?.disconnect()
  document.removeEventListener('visibilitychange', syncRadar)
})

const radarDots = computed(() =>
  AXES.map((ax, i) => polarToXY(ax.angle, currentValues.value[i] * MAX_R))
)

const radarPoints = computed(() =>
  radarDots.value.map(p => `${p.x},${p.y}`).join(' ')
)

// ── Content data ─────────────────────────────────────────────────────────────
const router = useRouter()

const audiences = [
  {
    tone: 'student',
    kicker: 'Si eres estudiante',
    title: 'Un espacio para mirarte con calma',
    icon: 'M12 12a4 4 0 1 0 0-8a4 4 0 1 0 0 8z M4.5 20.5c0-4 3.4-6.5 7.5-6.5s7.5 2.5 7.5 6.5',
    items: [
      'Respondes 44 afirmaciones a tu ritmo, desde tu computador o teléfono.',
      'Puedes pausar y continuar después: tus respuestas quedan guardadas.',
      'Recibes un reporte con tu perfil en las cinco dimensiones.',
    ],
  },
  {
    tone: 'counselor',
    kicker: 'Si eres orientador u orientadora',
    title: 'Contexto para cada conversación',
    icon: 'M9 11a3.5 3.5 0 1 0 0-7a3.5 3.5 0 1 0 0 7z M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6 M16 4.3a3.5 3.5 0 0 1 0 6.4 M18 14.4c2.1.7 3.5 2.7 3.5 5.6',
    items: [
      'Asignas los cursos que acompañas y ves a sus estudiantes en un solo panel.',
      'Sigues en qué etapa está cada estudiante: registro, cuestionario o reporte listo.',
      'Consultas los reportes para preparar entrevistas de orientación.',
    ],
  },
]

const steps = [
  { n: '01', title: 'Responde el test', desc: 'Contesta 44 afirmaciones simples sobre cómo piensas, sientes y actúas. Sin respuestas incorrectas.' },
  { n: '02', title: 'Conoce tu perfil', desc: 'El sistema calcula tus puntuaciones en las 5 dimensiones OCEAN y genera tu radar de personalidad.' },
  { n: '03', title: 'Reflexiona con tu orientador', desc: 'Revisa tus resultados y explora tus intereses junto con tu orientador. Elegir tu camino requiere también conocer tus habilidades, experiencias y opciones.' },
]

const dimensions = [
  { letter: 'O', name: 'Apertura', desc: 'Creatividad, curiosidad intelectual y gusto por las nuevas experiencias.', color: '#4F46E5', low: 'Prefiere lo conocido', high: 'Busca lo nuevo' },
  { letter: 'C', name: 'Responsabilidad', desc: 'Organización, disciplina y orientación al logro de metas.', color: '#10B981', low: 'Flexible y espontáneo', high: 'Organizado y metódico' },
  { letter: 'E', name: 'Extraversión', desc: 'Sociabilidad, energía y comodidad en entornos grupales.', color: '#F59E0B', low: 'Reservado', high: 'Sociable' },
  { letter: 'A', name: 'Amabilidad', desc: 'Empatía, cooperación y disposición a ayudar a los demás.', color: '#EC4899', low: 'Directo y crítico', high: 'Cooperativo y empático' },
  { letter: 'N', name: 'Neuroticismo', desc: 'Respuesta emocional y gestión del estrés y la ansiedad.', color: '#EF4444', low: 'Emocionalmente estable', high: 'Más sensible al estrés' },
]

const reportFeatures = [
  { title: 'Gráfico radar OCEAN', desc: 'Consulta tus puntajes en las cinco dimensiones de personalidad en un mismo gráfico.', icon: 'M12 3l8.5 6.2-3.2 10H6.7L3.5 9.2z M12 3v9 M20.5 9.2L12 12 M17.3 19.2L12 12 M6.7 19.2L12 12 M3.5 9.2L12 12' },
  { title: 'Texto interpretativo', desc: 'Lee descripciones de las tendencias que reflejan tus respuestas para apoyar tu reflexión.', icon: 'M4 6h16 M4 10h16 M4 14h11 M4 18h7' },
  { title: 'Áreas para explorar', desc: 'Referencias exploratorias del prototipo para investigar y conversar. No son una medida de afinidad profesional.', icon: 'M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M15.5 8.5l-2 5-5 2 2-5z' },
  { title: 'Acompañamiento del orientador', desc: 'Tu orientador asignado puede consultar tu avance y tus resultados para apoyar el seguimiento.', icon: 'M9 11a3.5 3.5 0 1 0 0-7a3.5 3.5 0 1 0 0 7z M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6 M16 4.3a3.5 3.5 0 0 1 0 6.4 M18 14.4c2.1.7 3.5 2.7 3.5 5.6' },
]

const scopeIs = [
  'Un cuestionario de autoconocimiento basado en el modelo de los cinco grandes rasgos.',
  'Una descripción de tendencias en tu forma habitual de pensar, sentir y actuar.',
  'Un punto de partida para conversar con tu orientador sobre tus intereses.',
]

const scopeNot = [
  'Un test que te diga qué carrera estudiar.',
  'Una evaluación con nota, puntaje ideal o respuestas correctas.',
  'Un diagnóstico psicológico ni clínico.',
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
/* ── Tokens de la portada ───────────────────────────────────────────────── */

.landing {
  --c-bg:             #F8FAFC; /* Slate 50 - Fondo general */
  --c-surface:        #FFFFFF; /* Blanco para tarjetas */
  --c-primary:        #047857; /* Verde esmeralda oscuro (Emerald 700) */
  --c-primary-strong: #065F46; /* Emerald 800 - Hover */
  --c-deep:           #064E3B; /* Emerald 900 - Bloque de registro */
  --c-accent1:        #0D9488; /* Teal 600 */
  --c-accent2:        #84CC16; /* Lima (Lime 500) */
  --c-tint:           #ECFDF5; /* Emerald 50 - Fondos suaves */
  --c-tint-border:    #A7F3D0; /* Emerald 200 - Bordes suaves */
  --c-text:           #0F172A; /* Slate 900 - Texto principal */
  --c-muted:          #64748B; /* Slate 500 - Texto secundario */
  --c-border:         #E2E8F0; /* Slate 200 - Bordes sutiles */
  --r-card:           16px;
  --wrap-pad:         48px;

  font-family: 'Inter', sans-serif;
  background: var(--c-bg);
  color: var(--c-text);
}
.landing section[id] { scroll-margin-top: 100px; }

.wrap {
  max-width: 1180px;
  margin: 0 auto;
  padding-left: var(--wrap-pad);
  padding-right: var(--wrap-pad);
}

.visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

/* ── Nav ─────────────────────────────────────────────────────────────────── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 48px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--c-border);
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
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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
  transition: background-color 0.2s;
}

.nav__cta:hover { background: var(--c-primary-strong) !important; }

/* ── Hero ────────────────────────────────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  padding: 136px 0 96px;
  background: linear-gradient(180deg, #F1F8F4 0%, var(--c-bg) 100%);
  border-bottom: 1px solid var(--c-border);
}

/* Trama de puntos que se desvanece detrás del gráfico */
.hero__bg-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: radial-gradient(rgba(4, 120, 87, 0.16) 1px, transparent 1.2px);
  background-size: 22px 22px;
  -webkit-mask-image: radial-gradient(ellipse 45% 60% at 76% 50%, #000 0%, transparent 75%);
  mask-image: radial-gradient(ellipse 45% 60% at 76% 50%, #000 0%, transparent 75%);
}

.hero__inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
  align-items: center;
  gap: 64px;
}

.hero__content { min-width: 0; }

.hero__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--c-primary);
  margin-bottom: 24px;
}

.hero__eyebrow::before {
  content: '';
  width: 24px;
  height: 2px;
  border-radius: 2px;
  background: var(--c-primary);
}

.hero__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2.8rem, 5.4vw, 4.6rem);
  line-height: 1.04;
  letter-spacing: -0.035em;
  margin-bottom: 24px;
  color: var(--c-text);
}

/* Subrayado tipo marcador en lugar de texto degradado */
.hero__title em {
  font-style: normal;
  color: var(--c-primary);
  background: linear-gradient(transparent 64%, rgba(132, 204, 22, 0.38) 64%, rgba(132, 204, 22, 0.38) 92%, transparent 92%);
  padding: 0 0.04em;
}

.hero__sub {
  font-size: 1.075rem;
  line-height: 1.7;
  color: #475569; /* Slate 600: más contraste para el párrafo principal */
  max-width: 470px;
  margin-bottom: 36px;
}

.hero__actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 44px;
}

.hero__stats {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-top: 28px;
  border-top: 1px solid var(--c-border);
  max-width: 470px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.stat__num {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.75rem;
  color: var(--c-text);
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat__label {
  font-size: 0.8rem;
  color: var(--c-muted);
  font-weight: 500;
}

.stat__divider {
  width: 1px;
  height: 36px;
  background: var(--c-border);
}

/* ── Tarjeta del radar ───────────────────────────────────────────────────── */
.hero__visual {
  position: relative;
  min-width: 0;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 22px 24px 24px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 24px 48px -24px rgba(6, 78, 59, 0.22);
}

.hero__visual-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--c-border);
}

.hero__visual-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
}

.hero__visual-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-muted);
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  padding: 4px 10px;
  border-radius: 100px;
  white-space: nowrap;
}

.hero__visual-note {
  margin-top: 4px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--c-muted);
}

/* ── Radar ───────────────────────────────────────────────────────────────── */
/* El contenedor mide exactamente lo mismo que el SVG para que los
   rótulos se anclen a cada vértice con porcentajes del viewBox. */
.hero__radar-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: min(340px, 100%);
  margin: 44px auto 40px;
}

.radar__svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

.radar__grid {
  fill: none;
  stroke: #E2E8F0;
  stroke-width: 1;
}

.radar__grid:first-of-type { stroke: #CBD5E1; }

.radar__axis {
  stroke: #E2E8F0;
  stroke-width: 1;
}

.radar__data {
  fill: rgba(4, 120, 87, 0.14);
  stroke: var(--c-primary);
  stroke-width: 2;
  stroke-linejoin: round;
}

.radar__dot {
  fill: var(--c-surface);
  stroke: var(--c-primary);
  stroke-width: 2;
}

.radar__label {
  position: absolute;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-text);
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.9);
  padding: 2px 6px;
  border-radius: 6px;
}

/* Vértices en el viewBox 320×320: O(50%,12.5%) C(85.6%,38.4%)
   E(72%,80.3%) A(28%,80.3%) N(14.4%,38.4%) */
.radar__label--top { left: 50%;   top: calc(12.5% - 10px); transform: translate(-50%, -100%); }
.radar__label--tr  { left: 85.6%; top: calc(38.4% - 10px); transform: translate(-50%, -100%); }
.radar__label--br  { left: 72%;   top: calc(80.3% + 10px); transform: translateX(-50%); }
.radar__label--bl  { left: 28%;   top: calc(80.3% + 10px); transform: translateX(-50%); }
.radar__label--tl  { left: 14.4%; top: calc(38.4% - 10px); transform: translate(-50%, -100%); }

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 13px 26px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
  border: 1px solid transparent;
}

.btn--primary {
  background: var(--c-primary);
  color: #fff;
}

.btn--primary:hover { background: var(--c-primary-strong); }

.btn--ghost {
  background: var(--c-surface);
  color: var(--c-text);
  border-color: var(--c-border);
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

.text-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 44px;
  color: var(--c-primary);
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  white-space: nowrap;
}

.text-link span { transition: transform 0.2s; }
.text-link:hover { text-decoration: underline; text-underline-offset: 4px; }
.text-link:hover span { transform: translateX(3px); }

/* ── Section shared ──────────────────────────────────────────────────────── */
.section__head {
  max-width: 640px;
  margin-bottom: 48px;
}

.section__head--row {
  max-width: none;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.section__eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 14px;
}

.section__eyebrow--on-dark { color: #BEF264; } /* Lime 300 sobre verde profundo */

.section__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(1.9rem, 3.4vw, 2.75rem);
  line-height: 1.12;
  letter-spacing: -0.03em;
  color: var(--c-text);
}

.section__lead {
  margin-top: 18px;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--c-muted);
}

/* ── Para quién ──────────────────────────────────────────────────────────── */
.audience {
  padding: 112px 0;
  background: var(--c-surface);
}

.audience__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.audience-card {
  border-radius: 20px;
  padding: 36px;
  border: 1px solid var(--c-border);
}

.audience-card--student { background: var(--c-tint); border-color: var(--c-tint-border); }
.audience-card--counselor { background: var(--c-bg); }

.audience-card__head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}

.audience-card__head > div { min-width: 0; }

.audience-card__icon {
  flex: 0 0 48px;
  width: 48px; height: 48px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--c-surface);
  color: var(--c-primary);
  border: 1px solid var(--c-border);
}

.audience-card--student .audience-card__icon { border-color: var(--c-tint-border); }
.audience-card__icon svg { width: 24px; height: 24px; }

.audience-card__kicker {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-primary);
  margin-bottom: 2px;
}

.audience-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.2rem;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.audience-card__list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 0;
}

.audience-card__list li {
  position: relative;
  padding: 14px 0 14px 22px;
  font-size: 0.95rem;
  line-height: 1.55;
  color: #334155; /* Slate 700 */
  border-top: 1px solid rgba(15, 23, 42, 0.07);
}

.audience-card__list li::before {
  content: '';
  position: absolute;
  left: 2px; top: 23px;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--c-primary);
}

/* ── Steps ───────────────────────────────────────────────────────────────── */
.steps {
  padding: 112px 0;
  background: var(--c-bg);
  border-top: 1px solid var(--c-border);
}

.steps__list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 40px;
  counter-reset: step;
}

.step-card {
  position: relative;
  min-width: 0;
}

/* Línea que une cada paso con el siguiente */
.step-card:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 24px;
  left: 64px;
  right: -28px;
  height: 1px;
  background: repeating-linear-gradient(90deg, var(--c-tint-border) 0 6px, transparent 6px 12px);
}

.step-card__num {
  display: grid;
  place-items: center;
  width: 48px; height: 48px;
  margin-bottom: 24px;
  border-radius: 50%;
  background: var(--c-surface);
  border: 1px solid var(--c-tint-border);
  font-family: 'Poppins', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--c-primary);
}

.step-card:first-child .step-card__num {
  background: var(--c-primary);
  border-color: var(--c-primary);
  color: #fff;
}

.step-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.15rem;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
}

.step-card__desc {
  font-size: 0.95rem;
  line-height: 1.65;
  color: var(--c-muted);
  max-width: 340px;
}

/* ── Ocean ───────────────────────────────────────────────────────────────── */
.ocean {
  padding: 112px 0;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.ocean__inner {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.3fr);
  gap: 72px;
  align-items: start;
}

.ocean__left {
  position: sticky;
  top: 112px;
  min-width: 0;
}

.ocean__intro {
  margin-top: 20px;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--c-muted);
  max-width: 400px;
}

.ocean__hint {
  margin: 20px 0 12px;
  padding: 16px 18px;
  max-width: 400px;
  border-left: 3px solid var(--c-accent2);
  background: var(--c-bg);
  border-radius: 0 12px 12px 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #334155;
}

.ocean__cards {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ocean-card {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr);
  gap: 20px;
  align-items: start;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 22px 24px;
}

.ocean-card__letter {
  display: grid;
  place-items: center;
  width: 52px; height: 52px;
  border-radius: 14px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.5rem;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 10%, #FFFFFF);
}

.ocean-card__body { min-width: 0; }

.ocean-card__name {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 4px;
}

.ocean-card__desc {
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--c-muted);
}

.ocean-card__scale {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  grid-template-areas: "track track" "low high";
  row-gap: 8px;
  column-gap: 12px;
  margin-top: 16px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #475569;
}

.ocean-card__pole { grid-area: low; }
.ocean-card__pole--high { grid-area: high; text-align: right; }

.ocean-card__track {
  grid-area: track;
  position: relative;
  height: 4px;
  border-radius: 4px;
  background: linear-gradient(90deg, #E2E8F0 0%, var(--accent) 100%);
}

.ocean-card__track::before,
.ocean-card__track::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 10px; height: 10px;
  border-radius: 50%;
  transform: translateY(-50%);
  background: var(--c-surface);
  border: 2px solid #CBD5E1;
}

.ocean-card__track::before { left: -1px; }
.ocean-card__track::after  { right: -1px; border-color: var(--accent); }

/* ── Report preview ──────────────────────────────────────────────────────── */
.report-preview {
  padding: 112px 0;
  background: var(--c-bg);
  border-top: 1px solid var(--c-border);
}

.report-preview__inner {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.3fr);
  gap: 72px;
  align-items: start;
}

.report-preview__inner .section__head { margin-bottom: 0; }

.report-preview__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.report-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 26px 24px;
  min-width: 0;
}

.report-card__icon {
  display: grid;
  place-items: center;
  width: 44px; height: 44px;
  margin-bottom: 18px;
  border-radius: 12px;
  background: var(--c-tint);
  color: var(--c-primary);
}

.report-card__icon svg { width: 22px; height: 22px; }

.report-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 8px;
  color: var(--c-text);
}

.report-card__desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--c-muted);
}

/* ── Qué es / qué no es ──────────────────────────────────────────────────── */
.scope {
  padding: 112px 0;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.scope__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  border: 1px solid var(--c-border);
  border-radius: 20px;
  overflow: hidden;
}

.scope__col {
  padding: 36px 40px;
  min-width: 0;
}

.scope__col--is { background: var(--c-tint); }
.scope__col--not { background: var(--c-surface); border-left: 1px solid var(--c-border); }

.scope__heading {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.scope__col--is .scope__heading { color: var(--c-primary); }
.scope__col--not .scope__heading { color: var(--c-muted); }

.scope__list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 16px;
}

.scope__list li {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  gap: 12px;
  align-items: start;
  font-size: 0.98rem;
  line-height: 1.55;
  color: #334155;
}

.scope__mark {
  width: 24px; height: 24px;
  padding: 3px;
  border-radius: 50%;
  fill: none;
  stroke-width: 2.2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.scope__col--is .scope__mark { background: var(--c-primary); stroke: #FFFFFF; }
.scope__col--not .scope__mark { background: #F1F5F9; stroke: #64748B; }

/* ── Register ────────────────────────────────────────────────────────────── */
.register {
  position: relative;
  padding: 112px 0;
  background: var(--c-deep);
  color: #ECFDF5;
  overflow: hidden;
}

/* Anillos concéntricos que evocan el radar, muy tenues */
.register::before {
  content: '';
  position: absolute;
  width: 720px; height: 720px;
  left: -260px; bottom: -380px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 59px, rgba(167, 243, 208, 0.08) 59px 60px);
  pointer-events: none;
}

.register__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 440px);
  gap: 72px;
  align-items: center;
}

.register__copy { min-width: 0; }

.register__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #FFFFFF;
  margin-bottom: 18px;
}

.register__sub {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #A7F3D0;
  max-width: 480px;
}

.register__facts {
  list-style: none;
  padding: 0;
  margin-top: 32px;
  display: grid;
  gap: 12px;
}

.register__facts li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.95rem;
  color: #ECFDF5;
}

.register__facts li::before {
  content: '';
  flex: 0 0 8px;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-accent2);
}

.register__box {
  background: var(--c-surface);
  color: var(--c-text);
  border-radius: 24px;
  padding: 36px;
  box-shadow: 0 30px 60px -30px rgba(0, 0, 0, 0.5);
  min-width: 0;
}

.register__form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--c-text);
}

.register__input {
  background: var(--c-surface);
  border: 1px solid #CBD5E1;
  border-radius: 12px;
  padding: 13px 16px;
  font-size: 0.95rem;
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  width: 100%;
  min-height: 48px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.register__input::placeholder { color: #94A3B8; }

.register__input:focus {
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(4, 120, 87, 0.18);
}

.register__form .btn { margin-top: 6px; }

.register__hint {
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--c-muted);
  text-align: center;
}

.register__login {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  font-size: 0.875rem;
  color: var(--c-muted);
  text-align: center;
}

.register__login a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 4px 6px;
  color: var(--c-primary);
  text-decoration: none;
  font-weight: 600;
}

.register__login a:hover { text-decoration: underline; text-underline-offset: 4px; }

/* ── Footer ──────────────────────────────────────────────────────────────── */
.footer {
  padding: 40px 0;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.footer__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.footer__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 4px;
}

.footer__copy {
  font-size: 0.85rem;
  color: var(--c-muted);
}

.footer__links {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 24px;
}

.footer__links a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--c-muted);
  text-decoration: none;
}

.footer__links a:hover { color: var(--c-primary); }

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1080px) {
  .hero__inner,
  .ocean__inner,
  .report-preview__inner,
  .register__inner { gap: 48px; }
}

@media (max-width: 900px) {
  .landing { --wrap-pad: var(--page-gutter); }
  .landing section[id] { scroll-margin-top: 140px; }

  .nav { position: sticky; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; padding: 12px var(--page-gutter); background: var(--c-surface); backdrop-filter: none; }
  .nav__logo { min-width: 0; }
  .nav__links { display: contents; }
  .nav__links a { font-size: 0.8rem; text-align: center; }
  .nav__links a:first-child { grid-row: 2; grid-column: 1; }
  .nav__links a:nth-child(2) { grid-row: 2; grid-column: 2; }
  .nav__cta { grid-row: 1; grid-column: 2; padding: 8px 12px; }

  .hero { padding: 28px 0 56px; }
  .hero__bg-glow { display: none; }
  .hero__inner { grid-template-columns: 1fr; gap: 36px; }
  .hero__content { text-align: center; }
  .hero__eyebrow { justify-content: center; }
  .hero__eyebrow::before { display: none; }
  .hero__sub { margin-left: auto; margin-right: auto; }
  .hero__actions { justify-content: center; }
  .hero__stats { justify-content: center; margin: 0 auto; }

  .hero__visual { order: -1; width: 100%; max-width: 400px; margin: 0 auto; padding: 16px; border-radius: 20px; }
  .hero__visual-head { padding-bottom: 12px; }
  .hero__visual-note { display: none; }
  .hero__radar-wrap { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 6px; width: 100%; margin: 4px 0 0; }
  .radar__svg { grid-row: 1; grid-column: 1 / -1; width: 100%; max-width: 210px; margin: -6px auto 0; }
  .radar__label { position: static; transform: none; white-space: normal; overflow-wrap: anywhere; text-align: center; font-size: 0.7rem; background: var(--c-bg); padding: 6px 4px; grid-column: span 2; }
  .radar__label--bl,
  .radar__label--tl { grid-column: span 3; }

  .audience,
  .steps,
  .ocean,
  .report-preview,
  .scope,
  .register { padding: 64px 0; }

  .section__head { margin-bottom: 32px; }
  .section__head--row { flex-direction: column; align-items: flex-start; gap: 8px; }

  .audience__grid { grid-template-columns: 1fr; gap: 16px; }
  .audience-card { padding: 28px 24px; }

  .steps__list { grid-template-columns: 1fr; gap: 0; }
  .step-card { display: grid; grid-template-columns: 48px minmax(0, 1fr); column-gap: 20px; padding-bottom: 32px; }
  .step-card:last-child { padding-bottom: 0; }
  .step-card__num { grid-row: 1 / span 2; margin-bottom: 0; }
  .step-card__title { align-self: center; margin: 12px 0 6px; }
  .step-card__desc { grid-column: 2; max-width: none; }
  .step-card:not(:last-child)::after { top: 56px; bottom: 8px; left: 24px; right: auto; width: 1px; height: auto; background: repeating-linear-gradient(180deg, var(--c-tint-border) 0 6px, transparent 6px 12px); }

  .ocean__inner { grid-template-columns: 1fr; gap: 32px; }
  .ocean__left { position: static; }

  .report-preview__inner { grid-template-columns: 1fr; gap: 32px; }

  .scope__grid { grid-template-columns: 1fr; }
  .scope__col { padding: 28px 24px; }
  .scope__col--not { border-left: none; border-top: 1px solid var(--c-border); }

  .register__inner { grid-template-columns: 1fr; gap: 36px; }
  .register__box { padding: 28px 24px; }
  .register__input { font-size: 16px; }

  .footer { padding: 28px 0; }
  .footer__inner { flex-direction: column; text-align: center; gap: 12px; }
  .footer__logo { justify-content: center; }
  .footer__links { justify-content: center; }
}

@media (max-width: 600px) {
  .report-preview__grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .hero__title { font-size: clamp(2.2rem, 11vw, 2.8rem); }
  .hero__eyebrow { font-size: 0.75rem; }
  .hero__actions { flex-direction: column; }
  .hero__actions .btn { width: 100%; justify-content: center; }
  .hero__stats { gap: 14px; }
  .stat__num { font-size: 1.5rem; }
  .stat__label { font-size: 0.72rem; }
  .audience-card { padding: 24px 20px; }
  .audience-card__head { align-items: flex-start; }
  .ocean-card { grid-template-columns: 40px minmax(0, 1fr); gap: 14px; padding: 18px 16px; }
  .ocean-card__letter { width: 40px; height: 40px; border-radius: 12px; font-size: 1.2rem; }
  .report-card { padding: 22px 20px; }
  .register__box { padding: 24px 20px; }
}

@media (max-height: 500px) and (max-width: 900px) {
  .nav { position: static; }
  .landing section[id] { scroll-margin-top: 24px; }
}

/* ── Reduced motion ──────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .btn, .btn__arrow, .text-link span, .nav__links a, .nav__cta { transition: none; }
}
</style>
