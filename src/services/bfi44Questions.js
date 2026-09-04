// Banco de ítems del Inventario Big Five (BFI-44).
// TODO backend: este arreglo se reemplaza por la tabla `pregunta` en MySQL,
// consultada vía GET /api/evaluacion/preguntas.
export const BFI44_QUESTIONS = [
  // BLOQUE 1 (1-10)
  { id: 1, text: 'Es sociable, conversador y expresivo.', dimension: 'E' },
  { id: 2, text: 'Tiende a ser crítico con los demás.', dimension: 'A' },
  { id: 3, text: 'Hace un trabajo minucioso y detallado.', dimension: 'C' },
  { id: 4, text: 'Es deprimido, triste o melancólico con frecuencia.', dimension: 'N' },
  { id: 5, text: 'Es original, se le ocurren ideas nuevas continuamente.', dimension: 'O' },
  { id: 6, text: 'Es reservado, prefiere guardar las distancias.', dimension: 'E' },
  { id: 7, text: 'Es servicial, cooperador y no busca conflictos.', dimension: 'A' },
  { id: 8, text: 'Puede ser algo descuidado o desorganizado.', dimension: 'C' },
  { id: 9, text: 'Es calmado, maneja bien las situaciones de estrés.', dimension: 'N' },
  { id: 10, text: 'Tiene mucha curiosidad por temas y áreas distintas.', dimension: 'O' },

  // BLOQUE 2 (11-20)
  { id: 11, text: 'Lleno de energía, es una persona muy activa.', dimension: 'E' },
  { id: 12, text: 'Inicia disputas o discusiones con facilidad.', dimension: 'A' },
  { id: 13, text: 'Es un trabajador confiable y cumple sus promesas.', dimension: 'C' },
  { id: 14, text: 'Se pone tenso o ansioso con facilidad.', dimension: 'N' },
  { id: 15, text: 'Es ingenioso, un pensador profundo.', dimension: 'O' },
  { id: 16, text: 'Genera mucho entusiasmo en los grupos.', dimension: 'E' },
  { id: 17, text: 'Tiene un corazón blando, es propenso a perdonar.', dimension: 'A' },
  { id: 18, text: 'Tiende a ser desorganizado en sus tareas escolares.', dimension: 'C' },
  { id: 19, text: 'Se preocupa mucho por cosas sin importancia.', dimension: 'N' },
  { id: 20, text: 'Tiene una imaginación muy activa y viva.', dimension: 'O' },

  // BLOQUE 3 (21-30)
  { id: 21, text: 'Suele ser callado o tímido ante desconocidos.', dimension: 'E' },
  { id: 22, text: 'Tiende a confiar plenamente en las personas.', dimension: 'A' },
  { id: 23, text: 'Tiende a ser flojo o postergar los deberes.', dimension: 'C' },
  { id: 24, text: 'Es emocionalmente estable, difícil de alterar.', dimension: 'N' },
  { id: 25, text: 'Es creativo, inventa soluciones diferentes.', dimension: 'O' },
  { id: 26, text: 'Tiene una personalidad asertiva y dominante.', dimension: 'E' },
  { id: 27, text: 'Puede ser frío o distante con sus pares.', dimension: 'A' },
  { id: 28, text: 'Persevera hasta terminar los planes que empieza.', dimension: 'C' },
  { id: 29, text: 'Es temperamental, cambia de humor con rapidez.', dimension: 'N' },
  { id: 30, text: 'Valora las experiencias artísticas y estéticas.', dimension: 'O' },

  // BLOQUE 4 (31-40)
  { id: 31, text: 'A veces es tímido o le cuesta tomar la iniciativa.', dimension: 'E' },
  { id: 32, text: 'Es considerado y amable con casi todo el mundo.', dimension: 'A' },
  { id: 33, text: 'Hace las cosas de manera eficiente y rápida.', dimension: 'C' },
  { id: 34, text: 'Se mantiene calmado en situaciones de alta presión.', dimension: 'N' },
  { id: 35, text: 'Prefiere trabajos rutinarios y predecibles.', dimension: 'O' },
  { id: 36, text: 'Es extrovertido, le agrada hacer amigos.', dimension: 'E' },
  { id: 37, text: 'A veces es rudo o poco empático con el resto.', dimension: 'A' },
  { id: 38, text: 'Establece planes y metas claras para su futuro.', dimension: 'C' },
  { id: 39, text: 'Se siente nervioso o inseguro de sí mismo.', dimension: 'N' },
  { id: 40, text: 'Le gusta reflexionar y jugar con ideas abstractas.', dimension: 'O' },

  // BLOQUE 5 (41-44)
  { id: 41, text: 'Tiene pocos intereses artísticos o científicos.', dimension: 'O' },
  { id: 42, text: 'Le gusta cooperar en tareas comunitarias.', dimension: 'A' },
  { id: 43, text: 'Se distrae fácilmente de sus responsabilidades.', dimension: 'C' },
  { id: 44, text: 'Tiene sofisticación y buen gusto artístico.', dimension: 'O' },
]
