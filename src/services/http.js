import axios from 'axios'

// Cliente HTTP centralizado. Cuando el backend FastAPI esté disponible,
// basta con definir VITE_API_BASE_URL en el archivo .env para que toda
// la aplicación empiece a consumir datos reales sin tocar los componentes.
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
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
