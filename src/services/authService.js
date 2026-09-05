import http from './http'

/**
 * Autentica al usuario.
 */
async function login(credentials) {
  try {
    const { data } = await http.post('/auth/login', {
      username: credentials.email, // FastAPI OAuth2PasswordRequestForm expects username
      password: credentials.password
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    // Save token
    localStorage.setItem('vocalis_token', data.access_token)
    
    return { role: data.role }
  } catch (error) {
    if (error.response?.status === 401) {
      const err = new Error('Credenciales no reconocidas. Revisa tu correo o contraseña.')
      err.code = 'INVALID_CREDENTIALS'
      throw err
    }
    throw error
  }
}

/**
 * Registra un nuevo usuario.
 */
async function register(payload) {
  // Map frontend form keys to backend schema
  const dataPayload = {
    email: payload.email,
    password: payload.password,
    nombre_completo: payload.name,
    rol: payload.role,
    edad: payload.edad ? parseInt(payload.edad) : undefined,
    curso: payload.curso,
    establecimiento: payload.establecimiento,
    departamento: payload.departamento
  }
  const { data } = await http.post('/auth/register', dataPayload)
  return data
}

export default { login, register }
