# Contenido exploratorio del reporte (MVP)

Las cinco descripciones OCEAN ahora incluyen **interpretaciones dinámicas por cuartil** (0-25%, 26-50%, 51-75%, 76-100%). Estas descripciones mantienen un tono especulativo y exploratorio. No clasifican puntajes como aptitud, éxito o preferencia por una profesión. Neuroticismo se describe en términos de reactividad emocional y manejo del estrés, sin convertirlo en inclinación profesional ni diagnóstico. `vocationalImpact` se conserva como string por compatibilidad, con un texto explícito sobre el límite de inferencia del puntaje.

La `CAREER_MATRIX` ha sido actualizada para cubrir los **6 pares posibles** formados por O, C, E, A, mapeándolos a las **10 áreas del conocimiento oficiales del Mineduc (SIES)** en Chile. Sus textos describen ámbitos de actividad de forma exploratoria (ej. "A modo exploratorio", "Solo como referencia") e incluyen carreras de ejemplo. El sustento teórico para cruzar los Cinco Grandes (OCEAN) con áreas de interés profesional (modelo RIASEC) se basa en metaanálisis documentados (Barrick et al., 2003; Larson et al., 2002), justificando su uso como herramienta de apoyo al orientador.

La selección de áreas obedece a una política de **asignación exploratoria**:
- La dimensión **N (Neuroticismo)** se excluye deliberadamente de la búsqueda del Top 2, ya que no predice intereses profesionales, asegurando que el cruce se haga siempre sobre las 4 dimensiones restantes.
- La matriz ahora garantiza una coincidencia para cualquiera de las 6 combinaciones.
- Los empates en los primeros lugares se resuelven de forma nativa por el ordenamiento estable de Python. El sistema ya no devuelve un resultado neutral (lista vacía) ante empates, priorizando siempre sugerir un área de exploración válida.

## Persistencia histórica: aplazada

Actualmente se persisten `scores_json`; `carreras_json` e `interpretaciones_json`
son columnas disponibles pero no contienen una instantánea versionada. Las
consultas construyen el texto y las áreas usando el código vigente, por lo que
un reporte antiguo puede mostrar textos diferentes tras una actualización.
Esta tarea no rellena esos campos ni inventa contenidos históricos.

Antes de activar esa persistencia deben acordarse una versión de contenido que
identifique conjuntamente matriz, selección/desempates, textos por cuartil y
un formato de instantánea. Esa versión identifica lo que calculó el software,
y refleja la política exploratoria del MVP apoyada en la bibliografía oficial
del proyecto.

Cuando se cierre ese contrato, la instantánea y su versión deben guardarse con
el reporte en su transacción de creación, y leerse sin recalcular con otras
reglas. No es correcto rellenar reportes antiguos con reglas nuevas y presentar
ese contenido como el mostrado originalmente. Por estas razones no se activa
persistencia histórica en este cambio ni se modifica el modelo de evaluación.

## Pruebas

- `backend/tests/test_career_areas.py`: asociaciones nuevas, inversas,
  ausencia de N, datos insuficientes, y resolución estable de empates.
- `backend/tests/test_reportes.py`: contrato exploratorio en los tres endpoints,
  descripciones españolas, límites de interpretación y lecturas sin alterar
  campos históricos; conserva las pruebas de autorización.
- `tests/frontend/reporte-neutral.test.mjs`: renderizado de la plantilla Vue con
  y sin áreas para ambos roles (`node --test tests/frontend/reporte-neutral.test.mjs`).
  No prueba navegación ni el flujo E2E del navegador.
