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
      const err = new Error('Credenciales no reconocidas. Revisa tu correo o contraseña.', { cause: error })
      err.code = 'INVALID_CREDENTIALS'
      throw err
    }
    if (error.response?.status === 409) {
      throw new Error(error.response.data?.detail || 'El email ya está registrado.', { cause: error })
    }
    throw new Error(error.response?.data?.detail || 'Error de conexión con el servidor.', { cause: error })
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
      establecimiento: payload.establecimiento,
      ...(payload.role === 'estudiante' ? {
        nivel: payload.nivel,
        letra: payload.letra,
        fecha_nacimiento: payload.fecha_nacimiento
      } : {
        departamento: payload.departamento || undefined,
        codigo_verificacion: payload.codigo_verificacion
      })
    }
    const { data } = await http.post('/auth/register', body)
    return data
  } catch (error) {
    if (error.response?.status === 409) {
      // eslint-disable-next-line preserve-caught-error -- Axios contiene las credenciales del registro.
      throw new Error(error.response.data?.detail || 'Conflicto durante el registro. Intenta nuevamente.')
    }
    const detail = error.response?.data?.detail
    const fields = { email: 'Correo', password: 'Contraseña', nivel: 'Nivel', letra: 'Letra',
      establecimiento: 'Establecimiento', fecha_nacimiento: 'Fecha de nacimiento',
      nombre_completo: 'Nombre', codigo_verificacion: 'Código de verificación' }
    const message = Array.isArray(detail)
      ? detail.map(item => item.type === 'value_error'
        ? item.msg.replace(/^Value error, /, '')
        : `Revisa el campo ${fields[item.loc?.at(-1)] || 'del formulario'}.`).join(' ')
      : detail
    // No conservar el error Axios: su configuración contiene el código y la contraseña.
    // eslint-disable-next-line preserve-caught-error -- No propagar el código privado en cause.
    throw new Error(message || 'Error al registrar. Intenta nuevamente.')
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
