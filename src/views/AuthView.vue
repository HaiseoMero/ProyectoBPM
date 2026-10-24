<template>
  <div class="auth-page">
    <div class="auth-bg-glow auth-bg-glow--1"></div>
    <div class="auth-bg-glow auth-bg-glow--2"></div>

    <router-link to="/" class="auth-back-btn">
      <span class="btn__arrow" aria-hidden="true">←</span> Volver al inicio
    </router-link>

    <main class="auth-container">
      <div class="auth-box">
        <div class="auth-logo">
          <span class="auth-logo-icon">◈</span>
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
/* Contenedor e infraestructura de página unificada a los tokens de la landing */
.auth-page {
  --c-bg:       #F8FAFC;
  --c-surface:  #FFFFFF;
  --c-primary:  #4F46E5;
  --c-accent1:  #0EA5E9;
  --c-text:     #0F172A;
  --c-muted:    #64748B;
  --c-border:   #E2E8F0;
  --r-card:     16px;

  min-height: 100vh;
  min-height: 100dvh;
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
  gap: 24px;
  position: relative;
  overflow: clip;
  padding: 32px var(--page-gutter);
}

/* Sistema de Glow Backgrounds exactos del Home */
.auth-bg-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  z-index: 0;
}
.auth-bg-glow--1 {
  width: 400px; height: 400px;
  background: rgba(79, 70, 229, 0.10);
  top: -50px; left: -50px;
}
.auth-bg-glow--2 {
  width: 450px; height: 450px;
  background: rgba(14, 165, 233, 0.08);
  bottom: -100px; right: -50px;
}

/* Botón flotante para regresar */
.auth-back-btn {
  position: relative;
  align-self: flex-start;
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
  z-index: 10;
}
.auth-back-btn:hover { color: var(--c-primary); }

/* Formulario Centrado con arquitectura responsiva */
.auth-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 460px;
  margin: auto;
  min-width: 0;
}
.auth-box {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.04);
  text-align: center;
}

/* Logo Corporativo */
.auth-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.4rem;
  color: var(--c-text);
  margin-bottom: 24px;
}
.auth-logo-icon { color: var(--c-primary); }

.auth-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.8rem;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
  color: var(--c-text);
}
.auth-sub {
  font-size: 0.88rem;
  line-height: 1.5;
  color: var(--c-muted);
  margin-bottom: 32px;
}

/* Formulario estructural */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

/* Selector dinámico de Roles */
.role-fieldset { border: 0; padding: 0; margin: 0; min-width: 0; }
.role-fieldset legend { margin-bottom: 8px; }
.role-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 4px;
}
.role-btn {
  flex: 1;
  min-width: 0;
  padding: 11px;
  border-radius: 12px;
  border: 1px solid var(--c-border);
  background: var(--c-bg);
  color: var(--c-muted);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}
.role-btn--active {
  background: var(--c-primary);
  color: #FFFFFF;
  border-color: var(--c-primary);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
}

/* Elementos de entrada de texto validados */
.input-group { width: 100%; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
.input-group label, .role-fieldset legend { font-size: 0.85rem; font-weight: 600; color: var(--c-text); }
.form-row {
  display: flex;
  gap: 12px;
}
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
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  border-radius: 12px;
  padding: 16px 20px;
  box-sizing: border-box;
  font-size: 1rem;
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  width: 100%;
  min-height: 48px;
  transition: all 0.2s;
  outline: none;
}
.register__input:focus {
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
  background: #FFFFFF;
}

/* Botones compartidos con la Landing */
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
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
}
.btn--primary:hover:not(:disabled) {
  transform: translateY(-1px);
  background: #4338CA;
}
.btn--primary:disabled {
  background: var(--c-border);
  color: var(--c-muted);
  cursor: not-allowed;
  box-shadow: none;
}
.btn--full { width: 100%; justify-content: center; }
.btn__arrow { transition: transform 0.2s; }
.btn:hover .btn__arrow { transform: translateX(3px); }

/* Alertas de error de credenciales */
.auth-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  text-align: left;
}
.auth-alert--error {
  background: #FEF2F2;
  border: 1px solid #FCA5A5;
}
.auth-alert--success {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
}
.auth-alert--success .auth-alert__text { color: #065F46; }
.auth-alert__text {
  font-size: 0.82rem;
  color: #991B1B;
  font-weight: 500;
  line-height: 1.4;
}

.auth-toggle-text {
  margin-top: 24px;
  font-size: 0.85rem;
  color: var(--c-muted);
}
.auth-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  border: 0;
  padding: 8px;
  background: transparent;
  color: var(--c-primary);
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
}
.auth-toggle-btn:hover { text-decoration: underline; }

.section__eyebrow {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 8px;
}

/* Adaptación responsiva */
@media (max-width: 900px) {
  .auth-bg-glow { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .auth-back-btn, .role-btn, .register__input, .btn, .btn__arrow { transition: none; }
}
@media (max-width: 600px) {
  .auth-page { padding-top: 16px; padding-bottom: max(24px, env(safe-area-inset-bottom)); gap: 16px; }
  .auth-container { margin: 0 auto; }
  .auth-box { padding: 28px 20px; border-radius: 20px; }
  .auth-title { font-size: clamp(1.4rem, 6vw, 1.8rem); }
  .auth-logo { margin-bottom: 16px; }
  .auth-sub { margin-bottom: 24px; }
  .register__input { padding: 14px 12px; }
  .register__select { padding-right: 32px; }
  .form-row { gap: 10px; }
  .role-btn { font-size: 0.85rem; }
  .btn--full { border-radius: 12px; padding: 14px 16px; }
  .auth-toggle-text { margin-top: 16px; }
}
</style>
