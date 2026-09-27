# Contenido exploratorio del reporte

Las cinco descripciones OCEAN son generales y están en español. No clasifican
puntajes como aptitud, éxito o preferencia por una profesión. Neuroticismo se
describe en términos de preocupación/tensión, sin convertirlo en inclinación
profesional ni diagnóstico. `vocationalImpact` se conserva como string por
compatibilidad, con un texto explícito sobre el límite de inferencia del puntaje.

`CAREER_MATRIX` conserva sus seis pares y listas de carreras existentes. Sus textos
describen ámbitos de actividad, sin «ideal para» ni atribuir vocación al estudiante.
Se presentan como referencias exploratorias del prototipo, no como relaciones
Big Five–profesión académicamente validadas. No se agregaron asociaciones.

La selección mantiene coincidencia directa y búsqueda inversa. Devuelve
`careerAreas: []` si no hay una regla, hay menos de dos dimensiones, N está entre
las dos mayores, o un empate impide ordenar las dos primeras inequívocamente
(primera con segunda, o segunda con tercera). No se descarta N para buscar una
pareja alternativa. Tampoco se usa el orden del JSON para resolver empates.
La lista vacía significa ausencia de recomendación con estas reglas, no ausencia
de opciones profesionales para el estudiante. Los puntajes y las cinco
descripciones siguen disponibles en los tres endpoints, con la misma autorización.

## Persistencia histórica: aplazada

Actualmente se persisten `scores_json`; `carreras_json` e `interpretaciones_json`
son columnas disponibles pero no contienen una instantánea versionada. Las
consultas construyen el texto y las áreas usando el código vigente, por lo que
un reporte antiguo puede mostrar textos diferentes tras una actualización.
Esta tarea no rellena esos campos ni inventa contenidos históricos.

Antes de activar esa persistencia deben acordarse una versión de contenido que
identifique conjuntamente matriz, selección/desempates, textos y significado del
resultado neutral; un formato de instantánea; y una política de lectura para
versiones anteriores y registros sin versión. Esa versión identifica lo que
calculó el software, no acredita validez académica. La justificación de las
asociaciones vocacionales sigue pendiente: estas correcciones no la aportan.

Cuando se cierre ese contrato, la instantánea y su versión deben guardarse con
el reporte en su transacción de creación, y leerse sin recalcular con otras
reglas. No es correcto rellenar reportes antiguos con reglas nuevas y presentar
ese contenido como el mostrado originalmente. Por estas razones no se activa
persistencia histórica en este cambio ni se modifica el modelo de evaluación.

## Pruebas

- `backend/tests/test_career_areas.py`: asociaciones conservadas, inversas,
  ausencia de fallback, N, datos insuficientes y empates independientes del orden.
- `backend/tests/test_reportes.py`: contrato neutral en los tres endpoints,
  descripciones españolas, límites de interpretación y lecturas sin alterar
  campos históricos; conserva las pruebas de autorización.
- `tests/frontend/reporte-neutral.test.mjs`: renderizado de la plantilla Vue con
  y sin áreas para ambos roles (`node --test tests/frontend/reporte-neutral.test.mjs`).
  No prueba navegación ni el flujo E2E del navegador.
