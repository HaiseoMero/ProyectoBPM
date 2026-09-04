import { mockDelay } from './mockDelay'
// import http from './http' // Descomentar cuando exista el backend FastAPI

/**
 * Autentica al usuario.
 * TODO backend: reemplazar por `const { data } = await http.post('/auth/login', credentials)`
 * y guardar `data.token` en localStorage.
 */
async function login(credentials) {
  await mockDelay()

  if (credentials.email === 'error@vocalis.cl') {
    const error = new Error('Credenciales no reconocidas. Revisa tu correo o contraseña.')
    error.code = 'INVALID_CREDENTIALS'
    throw error
  }

  const role = credentials.email.includes('orientador') || credentials.role === 'orientador'
    ? 'orientador'
    : 'estudiante'

  return { role }
}

/**
 * Registra un nuevo usuario.
 * TODO backend: reemplazar por `const { data } = await http.post('/auth/register', payload)`
 */
async function register(payload) {
  await mockDelay()
  return { ok: true, payload }
}

export default { login, register }
