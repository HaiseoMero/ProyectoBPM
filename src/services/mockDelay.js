// Simula la latencia de una petición de red real mientras no existe backend.
// Se usa únicamente dentro de los servicios *mock*; una vez conectado FastAPI,
// esta utilidad deja de ser necesaria porque axios ya trae su propia latencia real.
export function mockDelay(ms = 400) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
