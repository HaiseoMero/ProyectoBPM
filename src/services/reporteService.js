import { mockDelay } from './mockDelay'
// import http from './http' // Descomentar cuando exista el backend FastAPI

// Interpretaciones por dimensión OCEAN. El texto interpretativo es contenido
// editorial estable; los puntajes numéricos sí vienen del backend.
const DIMENSION_META = [
  {
    letter: 'O',
    name: 'Apertura a la Experiencia',
    color: '#4F46E5',
    interpretation:
      'Tu puntuación refleja una mente altamente creativa, con un marcado interés por la innovación, la resolución de problemas lógicos abstractos y el gusto por el aprendizaje de nuevas herramientas operativas y tecnológicas.',
    vocationalImpact: 'Excelente adaptación a carreras de base tecnológica y científica de alta tasa de actualización.',
  },
  {
    letter: 'C',
    name: 'Responsabilidad (Conciencia)',
    color: '#10B981',
    interpretation:
      'Muestras altos niveles de organización, autodisciplina y orientación al logro. Tiendes a planificar tus actividades escolares con orden y posees la capacidad de perseverar ante problemas complejos.',
    vocationalImpact: 'Indica alta probabilidad de éxito académico en ingenierías y metodologías de gestión estructuradas.',
  },
  {
    letter: 'E',
    name: 'Extraversión',
    color: '#F59E0B',
    interpretation:
      'Posees un nivel equilibrado de extroversión. Trabajas cómodamente en equipo y puedes defender tus posturas técnicas, pero también disfrutas y requieres de espacios individuales de trabajo concentrado.',
    vocationalImpact: 'Afinidad con entornos laborales híbridos que combinen desarrollo individual y células de diseño ágil.',
  },
  {
    letter: 'A',
    name: 'Amabilidad',
    color: '#EC4899',
    interpretation:
      'Tu perfil denota una alta empatía, espíritu colaborativo y orientación al apoyo de tus pares. Valoras los entornos de trabajo armónicos y tiendes a buscar soluciones de mutuo beneficio.',
    vocationalImpact: 'Apto para el desarrollo de soluciones informáticas orientadas a resolver necesidades sociales o de usuarios reales.',
  },
  {
    letter: 'N',
    name: 'Neuroticismo (Estabilidad Emocional)',
    color: '#EF4444',
    interpretation:
      'Tu puntaje indica una moderada a buena gestión frente al estrés y la frustración. Mantienes la calma bajo la presión de plazos acotados o problemas de código complejos.',
    vocationalImpact: 'Buen desempeño en entornos de resolución de incidencias informáticas y gestión de proyectos.',
  },
]

const CAREER_AREAS = [
  {
    title: 'Tecnología e Informática',
    desc: 'Tu alta Apertura combinada con Responsabilidad encaja perfectamente con el diseño de arquitecturas lógicas y el desarrollo de sistemas complejos.',
    carreras: ['Ingeniería en Computación e Informática', 'Ciencia de Datos', 'Ingeniería Civil en Informática'],
  },
  {
    title: 'Ingeniería y Gestión de Procesos',
    desc: 'La capacidad de organización y enfoque estructurado te capacita para modelar y optimizar flujos organizacionales complejos.',
    carreras: ['Ingeniería Civil Industrial', 'Ingeniería en Informática Educativa', 'Gestión de Procesos de Negocios'],
  },
]

/**
 * Obtiene el reporte vocacional más reciente del estudiante autenticado.
 * TODO backend: reemplazar por `const { data } = await http.get('/evaluacion/reporte')`
 * y usar `data.scores`, `data.evaluatedAt` en vez de los valores fijos.
 */
async function getLatestReport() {
  await mockDelay()

  const scores = { O: 0.85, C: 0.72, E: 0.58, A: 0.76, N: 0.42 }

  const dimensions = DIMENSION_META.map((meta) => ({
    ...meta,
    score: Math.round(scores[meta.letter] * 100),
  }))

  return {
    evaluatedAt: '19 de junio de 2026',
    scores,
    dimensions,
    careerAreas: CAREER_AREAS,
  }
}

export default { getLatestReport }
