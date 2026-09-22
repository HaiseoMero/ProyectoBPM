import http from './http'

/**
 * Autentica al usuario contra POST /auth/login (JSON body).
 */
async function login(credentials) {
  try {
    const { data } = await http.post('/auth/login', {
      email: credentials.email,
      password: credentials.password
    })

    // Guardar token JWT
    localStorage.setItem('vocalis_token', data.access_token)

    return { role: data.role, name: data.name }
  } catch (error) {
    if (error.response?.status === 401) {
      const err = new Error('Credenciales no reconocidas. Revisa tu correo o contraseña.')
      err.code = 'INVALID_CREDENTIALS'
      throw err
    }
    if (error.response?.status === 409) {
      throw new Error(error.response.data?.detail || 'El email ya está registrado.')
    }
    throw new Error(error.response?.data?.detail || 'Error de conexión con el servidor.')
  }
}

/**
 * Registra un nuevo usuario contra POST /auth/register (JSON body).
 */
async function register(payload) {
  try {
    const body = {
      email: payload.email,
      password: payload.password,
      nombre_completo: payload.name,
      role: payload.role,
      nivel: payload.nivel || undefined,
      letra: payload.letra || undefined,
      departamento: payload.departamento || undefined
    }
    const { data } = await http.post('/auth/register', body)
    return data
  } catch (error) {
    if (error.response?.status === 409) {
      throw new Error('Este correo ya está registrado. Intenta iniciar sesión.')
    }
    throw new Error(error.response?.data?.detail || 'Error al registrar. Intenta nuevamente.')
  }
}

/**
 * Obtiene el perfil del usuario autenticado desde GET /auth/me.
 */
async function getProfile() {
  try {
    const { data } = await http.get('/auth/me')
    return data
  } catch (error) {
    console.error('Error al obtener perfil:', error)
    return null
  }
}

/**
 * Cierra la sesión eliminando el token.
 */
function logout() {
  localStorage.removeItem('vocalis_token')
  window.location.replace('/auth')
}

export default { login, register, logout, getProfile }
