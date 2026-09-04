<template>
  <div class="auth-page">
    <div class="auth-bg-glow auth-bg-glow--1"></div>
    <div class="auth-bg-glow auth-bg-glow--2"></div>

    <router-link to="/" class="auth-back-btn">
      <span class="btn__arrow">←</span> Volver al inicio
    </router-link>

    <div class="auth-container">
      <div class="auth-box">
        <div class="auth-logo">
          <span class="auth-logo-icon">◈</span>
          <span class="auth-logo-text">Vócalis</span>
        </div>

        <div class="section__eyebrow">
          {{ isLogin ? 'Control de acceso' : 'Registro de nuevos usuarios' }}
        </div>
        <h2 class="auth-title">
          {{ isLogin ? 'Bienvenido de vuelta' : 'Crea tu cuenta' }}
        </h2>
        <p class="auth-sub">
          {{ isLogin ? 'Ingresa tus credenciales para acceder de forma segura.' : 'Únete a la plataforma para descubrir o guiar rutas vocacionales.' }}
        </p>

        <div v-if="errorMessage" class="auth-alert auth-alert--error">
          <p class="auth-alert__text">{{ errorMessage }}</p>
        </div>

        <div v-if="successMessage" class="auth-alert auth-alert--success">
          <p class="auth-alert__text">{{ successMessage }}</p>
        </div>

        <form class="auth-form" @submit.prevent="handleSubmit">
          
          <div v-if="!isLogin" class="role-selector">
            <button 
              type="button" 
              class="role-btn" 
              :class="{ 'role-btn--active': form.role === 'estudiante' }"
              @click="setRole('estudiante')"
            >
              Estudiante
            </button>
            <button 
              type="button" 
              class="role-btn" 
              :class="{ 'role-btn--active': form.role === 'orientador' }"
              @click="setRole('orientador')"
            >
              Orientador Escolar
            </button>
          </div>

          <div v-if="!isLogin" class="input-group">
            <input
              v-model="form.name"
              class="register__input"
              type="text"
              placeholder="Nombre completo"
              :required="!isLogin"
            />
          </div>

          <div v-if="!isLogin && form.role === 'estudiante'" class="form-row">
            <div class="input-group">
              <input 
                v-model="form.edad" 
                class="register__input" 
                type="number" 
                placeholder="Edad" 
                min="12" max="99"
                :required="!isLogin && form.role === 'estudiante'" 
              />
            </div>
            <div class="input-group">
              <input 
                v-model="form.curso" 
                class="register__input" 
                type="text" 
                placeholder="Curso (Ej: 4° Medio A)" 
                :required="!isLogin && form.role === 'estudiante'" 
              />
            </div>
          </div>
          
          <div v-if="!isLogin && form.role === 'estudiante'" class="input-group">
            <input
              v-model="form.establecimiento"
              class="register__input"
              type="text"
              placeholder="Establecimiento Educacional"
              :required="!isLogin && form.role === 'estudiante'"
            />
          </div>

          <div v-if="!isLogin && form.role === 'orientador'" class="input-group">
            <input
              v-model="form.departamento"
              class="register__input"
              type="text"
              placeholder="Departamento o Unidad (Ej: Convivencia Escolar)"
              :required="!isLogin && form.role === 'orientador'"
            />
          </div>

          <div class="input-group">
            <input
              v-model="form.email"
              class="register__input"
              type="email"
              placeholder="tu@correo.cl"
              required
            />
          </div>
          
          <div class="input-group">
            <input
              v-model="form.password"
              class="register__input"
              type="password"
              placeholder="Contraseña"
              required
            />
          </div>

          <button type="submit" class="btn btn--primary btn--full" :disabled="loading">
            {{ loading ? 'Procesando...' : (isLogin ? 'Iniciar Sesión' : 'Registrar mi cuenta gratis') }}
            <span v-if="!loading" class="btn__arrow">→</span>
          </button>
        </form>

        <p class="auth-toggle-text">
          {{ isLogin ? '¿No tienes una cuenta académica?' : '¿Ya te encuentras registrado?' }}
          <a href="#" @click.prevent="toggleMode">
            {{ isLogin ? 'Regístrate aquí' : 'Inicia sesión aquí' }}
          </a>
        </p>
      </div>
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
  edad: '',
  curso: '',
  establecimiento: '',
  departamento: ''
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
}

// Configurar rol seleccionado dinámicamente
function setRole(newRole) {
  form.value.role = newRole
}

// Procesar el envío del formulario
async function handleSubmit() {
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
      successMessage.value = 'Cuenta registrada con éxito. Iniciando sesión de forma automática.'
      isLogin.value = true
    }
  } catch (err) {
    errorMessage.value = err.message || 'Ocurrió un problema al procesar la solicitud. Intenta nuevamente.'
  } finally {
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
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 40px 24px;
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
  position: absolute;
  top: 32px; left: 32px;
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
.role-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 4px;
}
.role-btn {
  flex: 1;
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
.input-group { width: 100%; }
.form-row {
  display: flex;
  gap: 12px;
}
.form-row .input-group:first-child { flex: 0.35; }

.register__input {
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  border-radius: 12px;
  padding: 14px 16px;
  font-size: 0.92rem;
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  width: 100%;
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
.auth-toggle-text a {
  color: var(--c-primary);
  text-decoration: none;
  font-weight: 600;
}
.auth-toggle-text a:hover { text-decoration: underline; }

.section__eyebrow {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 8px;
}

/* Adaptación responsiva */
@media (max-width: 480px) {
  .auth-box { padding: 32px 20px; }
  .auth-back-btn { position: relative; top: 0; left: 0; margin-bottom: 24px; }
}
</style>