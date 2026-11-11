<template>
  <div class="auth-page">
    <aside class="auth-aside">
      <router-link to="/" class="auth-aside__brand" aria-label="Vócalis, volver al inicio">
        <span class="auth-logo-icon" aria-hidden="true">◈</span>
        <span>Vócalis</span>
      </router-link>
      <div class="auth-aside__body">
        <p class="auth-aside__eyebrow">Cuestionario BFI-44</p>
        <p class="auth-aside__title">Tu perfil, a tu ritmo.</p>
        <ul class="auth-aside__list">
          <li>44 afirmaciones, unos 8 minutos.</li>
          <li>Tus respuestas se guardan mientras avanzas.</li>
          <li>Tu orientador te acompaña en la lectura de resultados.</li>
        </ul>
      </div>
      <p class="auth-aside__foot">Proyecto de Título · Ingeniería en Informática · 2026</p>
    </aside>

    <div class="auth-panel">
    <router-link to="/" class="auth-back-btn">
      <span class="btn__arrow" aria-hidden="true">←</span> Volver al inicio
    </router-link>

    <main class="auth-container">
      <div class="auth-box">
        <div class="auth-logo">
          <span class="auth-logo-icon" aria-hidden="true">◈</span>
          <span class="auth-logo-text">Vócalis</span>
        </div>

        <div class="section__eyebrow">
          {{ isLogin ? 'Control de acceso' : 'Registro de nuevos usuarios' }}
        </div>
        <h1 class="auth-title">
          {{ isLogin ? 'Bienvenido de vuelta' : 'Crea tu cuenta' }}
        </h1>
        <p class="auth-sub">
          {{ isLogin ? 'Ingresa tus credenciales para acceder de forma segura.' : 'Únete a la plataforma para descubrir o guiar rutas vocacionales.' }}
        </p>

        <div v-if="errorMessage" class="auth-alert auth-alert--error" role="alert">
          <p class="auth-alert__text">{{ errorMessage }}</p>
        </div>

        <div v-if="successMessage" class="auth-alert auth-alert--success" role="status">
          <p class="auth-alert__text">{{ successMessage }}</p>
        </div>

        <form class="auth-form" :aria-busy="loading" @submit.prevent="handleSubmit">
          
          <fieldset v-if="!isLogin" class="role-fieldset" :disabled="loading">
            <legend>Tipo de cuenta</legend>
            <div class="role-selector">
            <button 
              type="button" 
              class="role-btn" 
              :class="{ 'role-btn--active': form.role === 'estudiante' }"
              :aria-pressed="form.role === 'estudiante'"
              @click="setRole('estudiante')"
            >
              Estudiante
            </button>
            <button 
              type="button" 
              class="role-btn" 
              :class="{ 'role-btn--active': form.role === 'orientador' }"
              :aria-pressed="form.role === 'orientador'"
              @click="setRole('orientador')"
            >
              Orientador Escolar
            </button>
            </div>
          </fieldset>

          <div v-if="!isLogin" class="input-group">
            <label for="nombre-completo">Nombre completo</label>
            <input
              id="nombre-completo"
              name="nombre_completo"
              autocomplete="name"
              v-model="form.name"
              class="register__input"
              type="text"
              placeholder="Nombre completo"
              :required="!isLogin"
            />
          </div>

          <div v-if="!isLogin && form.role === 'estudiante'" class="input-group">
            <label for="fecha-nacimiento">Fecha de nacimiento</label>
            <input id="fecha-nacimiento" v-model="form.fecha_nacimiento"
              class="register__input" name="fecha_nacimiento" autocomplete="bday" type="date" required />
          </div>

          <div v-if="!isLogin && form.role === 'estudiante'" class="form-row form-row--curso">
            <div class="input-group">
              <label for="nivel">Nivel</label>
              <select 
                id="nivel"
                name="nivel"
                v-model="form.nivel" 
                class="register__input register__select" 
                :required="!isLogin && form.role === 'estudiante'"
              >
                <option value="" disabled selected>Selecciona tu nivel</option>
                <option value="1° Medio">1° Medio</option>
                <option value="2° Medio">2° Medio</option>
                <option value="3° Medio">3° Medio</option>
                <option value="4° Medio">4° Medio</option>
              </select>
            </div>
            <div class="input-group input-group--letra">
              <label for="letra">Letra</label>
              <input 
                id="letra"
                name="letra"
                autocapitalize="characters"
                :spellcheck="false"
                v-model="form.letra" 
                class="register__input register__input--letra" 
                type="text" 
                placeholder="A" 
                maxlength="1"
                pattern="[A-La-l]"
                title="Debe ser una letra entre la A y la L"
                @input="form.letra = form.letra.toUpperCase().replace(/[^A-LA-L]/g, '')"
                :required="!isLogin && form.role === 'estudiante'" 
              />
            </div>
          </div>
          
          <div v-if="!isLogin" class="input-group">
            <label for="establecimiento">Establecimiento educacional</label>
            <input
              id="establecimiento"
              name="establecimiento"
              autocomplete="organization"
              v-model="form.establecimiento"
              class="register__input"
              type="text"
              placeholder="Establecimiento Educacional"
              maxlength="255"
              required
            />
          </div>

          <div v-if="!isLogin && form.role === 'orientador'" class="input-group">
            <label for="departamento">Departamento o unidad</label>
            <input
              id="departamento"
              name="departamento"
              v-model="form.departamento"
              class="register__input"
              type="text"
              placeholder="Departamento o Unidad (Ej: Convivencia Escolar)"
              :required="!isLogin && form.role === 'orientador'"
            />
          </div>

          <div v-if="!isLogin && form.role === 'orientador'" class="input-group">
            <label for="codigo-verificacion">Código privado de verificación</label>
            <input id="codigo-verificacion" name="codigo_verificacion" v-model="form.codigo_verificacion" class="register__input"
              type="password" autocomplete="off" placeholder="Código privado de verificación"
              aria-label="Código privado de verificación" required />
          </div>

          <div class="input-group">
            <label for="correo">Correo electrónico</label>
            <input
              id="correo"
              name="email"
              :autocomplete="isLogin ? 'username' : 'email'"
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
          
          <div class="input-group">
            <label for="contrasena">Contraseña</label>
            <input
              id="contrasena"
              name="password"
              :autocomplete="isLogin ? 'current-password' : 'new-password'"
              minlength="6"
              v-model="form.password"
              class="register__input"
              type="password"
              placeholder="Contraseña"
              required
            />
          </div>

          <button type="submit" class="btn btn--primary btn--full" :disabled="loading">
            {{ loading ? 'Procesando...' : (isLogin ? 'Iniciar Sesión' : 'Registrar mi cuenta gratis') }}
            <span v-if="!loading" class="btn__arrow" aria-hidden="true">→</span>
          </button>
        </form>

        <p class="auth-toggle-text">
          {{ isLogin ? '¿No tienes una cuenta académica?' : '¿Ya te encuentras registrado?' }}
          <button type="button" class="auth-toggle-btn" :disabled="loading" @click="toggleMode">
            {{ isLogin ? 'Regístrate aquí' : 'Inicia sesión aquí' }}
          </button>
        </p>
      </div>
    </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authService from '../services/authService'

const router = useRouter()
const route = useRoute()

// Estados reactivos de control
const isLogin = ref(true) // Parte por defecto en modo Login
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Formulario reactivo unificado
const form = ref({
  role: 'estudiante', // 'estudiante' o 'orientador'
  name: '',
  email: '',
  password: '',
  nivel: '',
  letra: '',
  establecimiento: '',
  departamento: '',
  fecha_nacimiento: '',
  codigo_verificacion: ''
})

// Si se llega desde la landing con datos precargados, abrir directo en modo registro
onMounted(() => {
  if (route.query.mode === 'register') {
    isLogin.value = false
  }
  if (route.query.name) form.value.name = String(route.query.name)
  if (route.query.email) form.value.email = String(route.query.email)
})

// Cambiar entre Login y Registro
function toggleMode() {
  isLogin.value = !isLogin.value
  errorMessage.value = ''
  successMessage.value = ''
  form.value.password = ''
  form.value.codigo_verificacion = ''
}

// Configurar rol seleccionado dinámicamente
function setRole(newRole) {
  form.value.role = newRole
  form.value.codigo_verificacion = ''
}

// Procesar el envío del formulario
async function handleSubmit() {
  if (loading.value) return
  errorMessage.value = ''
  successMessage.value = ''

  // Validación básica del lado del cliente antes de enviar
  if (!form.value.email.includes('@')) {
    errorMessage.value = 'Por favor, ingresa un correo electrónico institucional válido.'
    return
  }

  if (form.value.password.length < 6) {
    errorMessage.value = 'La contraseña debe contener al menos 6 caracteres por seguridad.'
    return
  }

  loading.value = true

  try {
    if (isLogin.value) {
      const { role } = await authService.login(form.value)
      router.push(role === 'orientador' ? '/orientador/dashboard' : '/estudiante/dashboard')
    } else {
      await authService.register(form.value)
      successMessage.value = 'Cuenta registrada con éxito. Ingresa tus credenciales para iniciar sesión.'
      isLogin.value = true
    }
  } catch (err) {
    errorMessage.value = err.message || 'Ocurrió un problema al procesar la solicitud. Intenta nuevamente.'
  } finally {
    form.value.codigo_verificacion = ''
    loading.value = false
  }
}
</script>


<style scoped>
/* Acceso: panel verde profundo + formulario, con los tokens globales de base.css */
.auth-page {
  min-height: 100vh;
  min-height: 100dvh;
  display: grid;
  grid-template-columns: minmax(360px, 0.8fr) minmax(0, 1fr);
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
}

/* ── Panel lateral ───────────────────────────────────────────────────────── */
.auth-aside {
  position: sticky;
  top: 0;
  height: 100vh;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 32px;
  padding: 40px 48px;
  background: var(--c-deep);
  color: #ECFDF5;
  overflow: hidden;
}

/* Anillos concéntricos que evocan el radar, muy tenues */
.auth-aside::before {
  content: '';
  position: absolute;
  width: 760px; height: 760px;
  left: -300px; bottom: -380px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 59px, rgba(167, 243, 208, 0.08) 59px 60px);
  pointer-events: none;
}

.auth-aside > * { position: relative; }

.auth-aside__brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
  align-self: flex-start;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  color: #FFFFFF;
  text-decoration: none;
}

.auth-aside__brand .auth-logo-icon { color: var(--c-accent2); }

.auth-aside__eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #BEF264;
  margin-bottom: 14px;
}

.auth-aside__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 3.2vw, 2.75rem);
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #FFFFFF;
  max-width: 340px;
}

.auth-aside__list {
  list-style: none;
  padding: 0;
  margin-top: 32px;
  display: grid;
  gap: 14px;
  max-width: 340px;
}

.auth-aside__list li {
  display: flex;
  align-items: baseline;
  gap: 12px;
  font-size: 0.95rem;
  line-height: 1.5;
  color: #D1FAE5;
}

.auth-aside__list li::before {
  content: '';
  flex: 0 0 8px;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-accent2);
  transform: translateY(-1px);
}

.auth-aside__foot {
  font-size: 0.8rem;
  color: #6EE7B7;
}

/* ── Columna del formulario ─────────────────────────────────────────────── */
.auth-panel {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 32px 48px 48px;
}

.auth-back-btn {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: color 0.2s;
}
.auth-back-btn:hover { color: var(--c-primary); }

.auth-container {
  width: 100%;
  max-width: 460px;
  margin: auto;
  min-width: 0;
}

.auth-box {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 44px 40px;
  box-shadow: var(--shadow-raised);
}

.auth-logo {
  display: none;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  color: var(--c-text);
  margin-bottom: 24px;
}
.auth-logo-icon { color: var(--c-primary); }

.section__eyebrow {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 10px;
}

.auth-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.9rem;
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 8px;
  color: var(--c-text);
}

.auth-sub {
  font-size: 0.92rem;
  line-height: 1.55;
  color: var(--c-muted);
  margin-bottom: 28px;
}

/* ── Formulario ──────────────────────────────────────────────────────────── */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.role-fieldset { border: 0; padding: 0; margin: 0; min-width: 0; }
.role-fieldset legend { margin-bottom: 8px; }

/* Selector segmentado */
.role-selector {
  display: flex;
  gap: 4px;
  padding: 4px;
  border-radius: 14px;
  background: #F1F5F9;
  border: 1px solid var(--c-border);
}

.role-btn {
  flex: 1;
  min-width: 0;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--c-muted);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
  font-family: 'Inter', sans-serif;
}
.role-btn:hover { color: var(--c-text); }
.role-btn--active {
  background: var(--c-surface);
  color: var(--c-primary);
  border-color: var(--c-border);
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}

.input-group { width: 100%; min-width: 0; display: flex; flex-direction: column; gap: 8px; }
.input-group label, .role-fieldset legend { font-size: 0.85rem; font-weight: 600; color: var(--c-text); }

.form-row { display: flex; gap: 12px; }
.form-row--curso .input-group:first-child { flex: 1; }
.form-row--curso .input-group--letra { flex: 0 0 72px; }

.register__input--letra {
  text-align: center;
  padding-left: 0;
  padding-right: 0;
}

.register__select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%2364748B%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 10px auto;
  cursor: pointer;
}

.register__input {
  background-color: var(--c-surface);
  border: 1px solid var(--c-border-strong);
  border-radius: 12px;
  padding: 13px 16px;
  box-sizing: border-box;
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
  box-shadow: var(--ring);
}

/* ── Botón ───────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  margin-top: 4px;
  padding: 13px 26px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  border: none;
}
.btn--primary { background: var(--c-primary); color: #fff; }
.btn--primary:hover:not(:disabled) { background: var(--c-primary-strong); }
.btn--primary:disabled {
  background: var(--c-border);
  color: var(--c-muted);
  cursor: not-allowed;
}
.btn--full { width: 100%; justify-content: center; }
.btn__arrow { transition: transform 0.2s; }
.btn:hover .btn__arrow { transform: translateX(3px); }

/* ── Alertas ─────────────────────────────────────────────────────────────── */
.auth-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  border: 1px solid;
  border-left-width: 4px;
}
.auth-alert--error { background: var(--c-danger-bg); border-color: var(--c-danger-border); border-left-color: var(--c-danger); }
.auth-alert--success { background: var(--c-tint); border-color: var(--c-tint-border); border-left-color: var(--c-primary); }
.auth-alert__text {
  font-size: 0.85rem;
  color: #991B1B;
  font-weight: 500;
  line-height: 1.45;
}
.auth-alert--success .auth-alert__text { color: var(--c-primary-strong); }

.auth-toggle-text {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  font-size: 0.875rem;
  color: var(--c-muted);
  text-align: center;
}
.auth-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  border: 0;
  padding: 8px 6px;
  background: transparent;
  color: var(--c-primary);
  font-weight: 600;
  cursor: pointer;
}
.auth-toggle-btn:hover { text-decoration: underline; text-underline-offset: 4px; }

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1080px) {
  .auth-aside { padding: 36px 32px; }
  .auth-panel { padding: 28px 32px 40px; }
}

@media (max-width: 900px) {
  .auth-page { display: flex; flex-direction: column; gap: 0; }
  .auth-aside { display: none; }
  .auth-panel { padding: 24px var(--page-gutter) 40px; background: linear-gradient(180deg, #F1F8F4 0%, var(--c-bg) 320px); flex: 1; }
  .auth-logo { display: flex; }
  .register__input { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  .auth-back-btn, .role-btn, .register__input, .btn, .btn__arrow { transition: none; }
}

@media (max-width: 600px) {
  .auth-panel { padding-top: 16px; padding-bottom: max(24px, env(safe-area-inset-bottom)); gap: 16px; }
  .auth-container { margin: 0 auto; }
  .auth-box { padding: 28px 20px; border-radius: 20px; }
  .auth-title { font-size: clamp(1.5rem, 6.5vw, 1.9rem); }
  .auth-logo { margin-bottom: 16px; }
  .auth-sub { margin-bottom: 24px; }
  .register__input { padding: 13px 12px; }
  .register__select { padding-right: 32px; }
  .form-row { gap: 10px; }
  .btn--full { padding: 13px 16px; }
}
</style>
