import axios from 'axios'

// /api usa el mismo origen que la página, también al entrar desde un teléfono.
// Vite reenvía estas peticiones al backend local durante el desarrollo.
// VITE_API_BASE_URL permite indicar otra API en un despliegue propio.
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
})

// Adjunta el token JWT (una vez que exista autenticación real) a cada
// petición saliente.
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('vocalis_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Punto único para manejar sesión expirada / no autorizada cuando el
// backend esté conectado.
http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('vocalis_token')
    }
    return Promise.reject(error)
  }
)

export default http
