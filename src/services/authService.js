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
      edad: payload.edad ? parseInt(payload.edad) : undefined,
      curso_id: payload.curso_id ? parseInt(payload.curso_id) : undefined,
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
 * Cierra la sesión eliminando el token.
 */
function logout() {
  localStorage.removeItem('vocalis_token')
}

export default { login, register, logout }
