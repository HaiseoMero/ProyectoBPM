![image1.png](images2.0/image1.png)


**FACULTAD DE INGENIERÍA**

**ESCUELA DE INFORMÁTICA**

**INGENIERÍA EN COMPUTACIÓN E INFORMÁTICA**

**APLICACIÓN WEB BASADA EN PROCESOS DE NEGOCIO PARA LA GESTIÓN DE LA ORIENTACIÓN VOCACIONAL Y EL AUTOCONOCIMIENTO EN ESTUDIANTES CHILENOS**

Proyecto de título para optar al título de Ingeniero en Computación e Informática

Autor:

José Miguel Piña Benítez

Profesor Guía:

Lismary Alejandra Cubillan Aizpurua

**Santiago, Chile**

**2026**


![image2.png](images2.0/image2.png)


**FACULTAD DE INGENIERÍA**

**INGENIERÍA EN COMPUTACIÓN E INFORMÁTICA**

**DECLARACIÓN DE ORIGINALIDAD** **Y USO DE INTELIGENCIA ARTIFICIAL**

Quienes suscriben en calidad de autor/es el trabajo de titulación presentado para su defensa y evaluación, declaran por este medio que:

- El contenido es original; las fuentes, herramientas y aplicaciones utilizadas que contribuyeron a la investigación realizada están debidamente citadas en el texto y acreditadas en el apartado de las referencias, conforme con los requisitos que establece el estilo bibliográfico APA y respetando los aspectos que conciernen a la propiedad intelectual.

- Se reconoce el uso de herramienta(s) de inteligencia artificial (IA) en el proceso de elaboración del trabajo académico, con la finalidad detallada a continuación:

**COMPLETAR EL ÍTEM O ÍTEMS UTILIZADOS SEGÚN CORRESPONDA.**


| **FINALIDAD** | **DECLARACIÓN DE USO** | **NOMBRE DE HERRAMIENTA(S)****,** **VERSIÓN** **O FECHA DE CONSULTA** |
| --- | --- | --- |
| Generación de Ideas | Se utilizó IA para obtener una lluvia de ideas como base inicial de apoyo que facilite la creatividad y la determinación  del alcance y etapas del trabajo. | Claude (Anthropic), modelo Claude Sonnet 4.5. Consultado entre sept.–oct. 2026. |
| Revisión de fuentes | Se utilizó IA como apoyo para comprender, analizar y evaluar conceptos y teorías relevantes presentes en fuentes científicas y académicas autorizadas relacionados con el trabajo. | Codex (OpenAI). Apoyo en la revisión de información bibliográfica sobre el BFI-44, su versión en español, reglas de puntuación y límites de interpretación, así como en la organización de citas y referencias APA 7. Consultado entre septiembre y octubre de 2026. |
| Revisión de la Redacción | Se utilizó IA para revisar el contenido escrito en el trabajo, a fin de mejorar la calidad de redacción. | Claude (Anthropic), modelo Claude Sonnet 4.5. Consultado el 27 sept. 2026. |
| Verificación de Datos | Se utilizó IA para comprobar la precisión, eficiencia y relevancia de los datos utilizados en el trabajo. | Claude (Anthropic), modelo Claude Sonnet 4.5. Consultado entre 3 sept.–27 sept. 2026. |
| Generación de Códigos | Se utilizó IA para generar códigos automatizados, buscando optimizar tareas de programación, reducir posibles errores de codificación manual y lograr soluciones rápidas y creativas. | Google Antigravity (IDE), modelos Gemini 3.1 Pro (High), Claude Opus 4.6, Claude Sonnet 4.6 y Codex (OpenAi). Consultado entre 3 sept.–8 oct. 2026. |
| Generación de recursos multimediales | Se utilizó IA para generar recursos visuales como imágenes, diagramas, videos u otros, con el propósito explicar o ejemplificar ideas y contribuir a una mejor comprensión del tema en cuestión. | Google Antigravity con @mermaid-js/mermaid-cli (diagramas) y Puppeteer (capturas de pantalla automatizadas); Claude (Anthropic) para el ensamblado final del documento .docx. Consultado entre sept.–oct. 2026. |
| Otras finalidades |  |  |


Adaptado de: Avello-Sáez, D., Lucero-González, N., & Villagrán, I. (2024). Desarrollo de una declaración de uso de inteligencia artificial con una perspectiva de integridad académica en educación médica y ciencias de la salud. Revista Médica Clínica Las Condes, 35(5–6), 412–420.[https://doi.org/10.1016/j.rmclc.2024.06.003](https://doi.org/10.1016/j.rmclc.2024.06.003)

Ante cualquier falta de originalidad detectada que vulnere la integridad académica e infrinja la Ley N°17.336 de Propiedad Intelectual, se asume la responsabilidad que representa para tal efecto, dejando constancia de ello con fecha ____ de _____________de ________ en la ciudad de ______________.


| **NOMBRE COMPLETO DEL AUTOR** | **FIRMA** |
| --- | --- |
| José Miguel Piña Benítez |  |
|  |  |
|  |  |
|  |  |
|  |  |
| **Facultad:** **INGENIERÍA** |  |
| **Carrera o Programa:** **INGENIERÍA EN COMPUTACIÓN E INFORMÁTICA** |  |
| Título del trabajo: Aplicación web basada en procesos de negocio para la gestión de la orientación vocacional y el autoconocimiento en estudiantes chilenos |  |


**DEDICATORIA**

**AGRADECIMIENTOS**

Quisiera expresar mi más profundo agradecimiento y afecto a mi profesora guía, Lismary Alejandra Cubillan Aizpurua, por sus valiosas retroalimentaciones, directrices y por su inagotable paciencia para guiar el desarrollo de este proyecto, permitiéndome estructurar una propuesta metodológica robusta y de alto estándar académico.

Asimismo, agradezco a la Facultad de Ingeniería de la Universidad Andrés Bello por brindarme las herramientas conceptuales y técnicas necesarias para afrontar los desafíos del desarrollo de software moderno y la ingeniería de procesos.

**ÍNDICE DE TABLAS**

Matriz de métricas y criterios de éxito de los objetivos específicos5

**Í****NDICE DE FIGURAS**

Diagrama de Ishikawa4

Arquitectura general de la solución10

Pantalla de inicio de sesión y registro12

Panel principal del estudiante12

Cuestionario Big Five (BFI-44)13

Reporte vocacional: familias de carreras y áreas de afinidad14

Reporte vocacional: perfil e interpretación de dimensiones14

Reporte vocacional: continuación de la interpretación15

Reporte vocacional: vista general15

Panel de gestión y monitoreo del orientador16

Diagrama de casos de uso18

Diagrama de procesos BPMN en Camunda 818

Diagrama de componentes19

Diagrama de despliegue físico20

Diagrama entidad-relación de la base de datos21

Diagrama de clases UML del sistema22

**RESUMEN EJECUTIVO**

**Presentación del problema**

En la enseñanza media chilena, la orientación vocacional incluye la reflexión sobre el proyecto de vida y la exploración de alternativas de estudio y trabajo (Ministerio de Educación de Chile, 2024). Cuando las evaluaciones, sus resultados y las acciones de seguimiento se administran en registros separados, resulta más difícil mantener la continuidad y consultar el avance de cada estudiante. Este proyecto aborda la gestión de esa información y del flujo de orientación mediante una aplicación web.

La propuesta busca reunir información del estudiante, incorporar un instrumento de apoyo al autoconocimiento y facilitar al orientador la consulta de resultados y estados del proceso. La decisión académica o profesional sigue dependiendo de la reflexión del estudiante y de factores personales, familiares, educativos y sociales (Lowman, 2022).

La pregunta que guía el proyecto es: ¿De qué manera una aplicación web basada en procesos de negocio puede mejorar la gestión, continuidad y trazabilidad de las evaluaciones de autoconocimiento y del seguimiento de estudiantes de enseñanza media?

**Objetivo general**

Mejorar la gestión, continuidad y trazabilidad del proceso de orientación vocacional y autoconocimiento de estudiantes de enseñanza media, mediante el desarrollo de una aplicación web basada en procesos de negocio (BPM) que permita gestionar evaluaciones de autoconocimiento, centralizar sus resultados y apoyar el seguimiento realizado por los orientadores.

**Metodología**

Se propone combinar prácticas de planificación y control del proyecto tomadas de la guía PMBOK con iteraciones de desarrollo inspiradas en Scrum (Project Management Institute, 2021; Schwaber & Sutherland, 2020). La solución prevista utiliza FastAPI para la API, Vue.js para la interfaz, MySQL para los datos y Camunda 8 para orquestar estados y tareas del proceso. El BFI de 44 ítems se plantea como instrumento de apoyo al autoconocimiento; su aplicación e interpretación deben documentar la versión en español y sus reglas de puntuación (Benet-Martínez & John, 1998; John & Srivastava, 1999).

**Resultados esperados**

Se espera entregar un producto mínimo viable (MVP) que permita el registro de usuarios, la aplicación digital del BFI-44, el cálculo de sus cinco dimensiones, la visualización de resultados y la consulta del estado de cada estudiante por parte del orientador. Las pruebas funcionales, de integración y de usabilidad permitirán evaluar el cumplimiento de los requerimientos definidos. Los resultados del cuestionario se presentarán como información para la reflexión y el acompañamiento, sin determinar una carrera para el estudiante.

**Conclusiones y recomendaciones**

La contribución esperada es una gestión más ordenada del proceso de orientación: información centralizada, estados visibles y resultados disponibles para el seguimiento. La utilidad efectiva de la aplicación deberá establecerse con las pruebas y criterios de éxito definidos en el proyecto; no se atribuyen al software cambios directos en la elección de carrera o en la deserción.

Palabras Clave: Gestión de Procesos de Negocio (BPM), Orientación Vocacional, Modelo Big Five (OCEAN), Aplicación Web, Camunda.

**ABSTRACT**

**Problem statement**

In Chilean secondary education, vocational guidance includes reflection on life goals and the exploration of study and employment options (Ministerio de Educación de Chile, 2024). When assessments, their results, and follow-up activities are managed in separate records, maintaining continuity and reviewing each student’s progress becomes more difficult. This project addresses the management of that information and the vocational guidance workflow through a web application.

The proposal aims to bring together student information, incorporate an instrument to support self-knowledge, and help counselors consult results and process statuses. Academic or career decisions continue to depend on students’ reflection and on personal, family, educational, and social factors (Lowman, 2022).

The question guiding this project is: How can a web application based on business processes improve the management, continuity, and traceability of self-knowledge assessments and the follow-up of secondary school students?

**General objective**

To improve the management, continuity, and traceability of the vocational guidance and self-knowledge process for secondary school students by developing a web application based on business process management (BPM) that manages self-knowledge assessments, centralizes their results, and supports follow-up by counselors.

**Methodology**

The proposed methodology combines project planning and control practices from the PMBOK Guide with development iterations inspired by Scrum (Project Management Institute, 2021; Schwaber & Sutherland, 2020). The planned solution uses FastAPI for the API, Vue.js for the interface, MySQL for data storage, and Camunda 8 to orchestrate process statuses and tasks. The 44-item BFI is proposed as an instrument to support self-knowledge; its administration and interpretation must document the Spanish version and its scoring rules (Benet-Martínez & John, 1998; John & Srivastava, 1999).

**Expected results**

The expected deliverable is a minimum viable product (MVP) that enables user registration, digital administration of the BFI-44, calculation of its five dimensions, visualization of results, and consultation of each student’s status by the counselor. Functional, integration, and usability tests will assess compliance with the defined requirements. Questionnaire results will be presented as information to support reflection and guidance, without determining a career for the student.

**Conclusions and recommendations**

The expected contribution is more organized management of the vocational guidance process: centralized information, visible statuses, and results available for follow-up. The application’s actual usefulness must be established through the tests and success criteria defined in the project; direct changes in career choices or dropout rates are not attributed to the software.

Key Words: Business Process Management (BPM), Vocational Guidance, Big Five Model (OCEAN), Web Application, Camunda.

# CAPÍTULO I: INTRODUCCIÓN

## Contexto y motivación

La transición desde la enseñanza media hacia estudios superiores, formación técnica o trabajo implica explorar alternativas y relacionarlas con intereses, habilidades y circunstancias personales. El currículo chileno contempla un taller de decisión vocacional y proyecto de vida para 3.º y 4.º medio (Ministerio de Educación de Chile, 2024). En ese contexto, las herramientas de autoconocimiento pueden aportar información para la conversación con el orientador, junto con otras fuentes sobre intereses y aptitudes (Lowman, 2022).

El problema que aborda este proyecto se sitúa en la gestión del proceso de orientación: cuando las evaluaciones y sus resultados no se integran con el seguimiento, el orientador dispone de menos información organizada para acompañar a cada estudiante. La propuesta busca facilitar ese trabajo mediante un registro centralizado y un flujo de actividades trazable.

## Importancia de resolver el problema de…

Mejorar el acceso del orientador a evaluaciones, resultados y estados del proceso puede facilitar la continuidad del acompañamiento. La automatización de tareas de registro y cálculo busca reducir trabajo manual, pero ese efecto deberá comprobarse durante la validación. La aplicación entrega información de apoyo: interpretar el contexto del estudiante y orientar sus decisiones sigue siendo una tarea humana (Lowman, 2022).

## Breve discusión bibliográfica

El taller de Decisión Vocacional y Proyecto de Vida del currículo chileno sitúa la exploración de opciones en el marco de la reflexión personal (Ministerio de Educación de Chile, 2024). Para la evaluación de carrera, Lowman (2022) propone integrar intereses, habilidades y personalidad, por lo que una medida de rasgos no basta por sí sola para indicar una ocupación. El BFI-44 describe cinco dimensiones amplias de personalidad; la investigación sobre su versión en español se realizó con poblaciones distintas de los escolares chilenos, lo que exige cautela al trasladar sus interpretaciones a este proyecto (Benet-Martínez & John, 1998; John & Srivastava, 1999). Desde el punto de vista técnico, Camunda 8 permite modelar y ejecutar procesos BPMN con tareas y estados explícitos, capacidad pertinente para registrar el avance de una evaluación y su seguimiento (Camunda, s. f.).

## Contribución del trabajo

La aplicación propuesta busca centralizar datos de estudiantes, resultados de autoconocimiento y estados del proceso de orientación. El flujo BPM permite representar las etapas de evaluación y consulta por el orientador (Camunda, s. f.). Los reportes entregarán información descriptiva para apoyar la conversación orientadora; su utilidad se evaluará con los criterios de prueba del proyecto.

## Trabajo a realizar en el proyecto.

El proyecto contempla el análisis de necesidades, el diseño y desarrollo de una aplicación web, y su validación. La solución integrará Camunda 8 para la gestión del flujo, una versión documentada del BFI-44 para apoyar el autoconocimiento y un panel que permita al orientador consultar resultados y avance. El sistema no reemplaza el acompañamiento profesional ni decide el futuro académico del estudiante.

## Organización y presentación de este trabajo

Este documento se estructura de la siguiente manera: el Capítulo II delimita el problema, sus causas abordables, los objetivos y el alcance del MVP. El Capítulo III describe la metodología, las herramientas, los riesgos, las pruebas, el cronograma y los prototipos de interfaz. El Capítulo IV presenta los requerimientos y los modelos de procesos, datos y arquitectura incluidos en esta propuesta.

# CAPÍTULO II: IDENTIFICACIÓN DEL PROBLEMA / OPORTUNIDAD

## Presentación y fundamentación del problema / oportunidad de mejora

El problema central de este proyecto es la gestión fragmentada de la información y de las actividades de orientación vocacional en el contexto escolar considerado. Cuando la aplicación de instrumentos, sus resultados y el seguimiento se realizan por vías separadas, se dificulta consultar el avance de cada estudiante y mantener continuidad en el acompañamiento. La aplicación puede contribuir a centralizar esos registros y a hacer visible el estado del proceso. La incertidumbre sobre el futuro profesional y las presiones del entorno son factores relevantes, pero no pueden resolverse directamente mediante el software.

## Descripción de problemas / oportunidades de mejora

La oportunidad de mejora se organiza en tres aspectos del proceso de orientación que pueden traducirse en requerimientos del sistema:

Continuidad del proceso: si las actividades se concentran en una etapa y no se conserva un historial accesible, el orientador tiene menos elementos para dar seguimiento. El sistema registrará estados y resultados de las evaluaciones realizadas.

Integración de información: cuando las herramientas de autoconocimiento no forman parte del mismo flujo de trabajo, sus resultados pueden quedar separados de las demás acciones de orientación. La aplicación incorporará el cuestionario y centralizará sus resultados.

Apoyo al orientador: el registro y procesamiento manual de respuestas puede dificultar la consulta individual. La aplicación automatizará el cálculo y presentará los resultados para su revisión, sin sustituir la interpretación y el acompañamiento del profesional.

## Identificación cuantitativa de problemas (ISHIKAWA / ARBOL DE OPORTUNIDADES)

El diagrama de Ishikawa organiza las causas en seis categorías: Mano de Obra, Medición, Materiales, Máquinas, Método y Medio Ambiente. Las causas vinculadas con herramientas digitales, instrumentos integrados, registro de resultados y seguimiento son las más cercanas al alcance de la aplicación; las presiones familiares y sociales constituyen factores de contexto.

Mano de Obra: disponibilidad de tiempo y carga de registro del orientador para acompañar y revisar individualmente el avance de los estudiantes.

Máquinas: disponibilidad y uso limitado de herramientas digitales centralizadas para registrar actividades y resultados de orientación.

Medición: falta de instrumentos de autoconocimiento integrados al proceso y de registros periódicos de avance consultables por el orientador.

Materiales: recursos e información de apoyo distribuidos en distintos medios, lo que dificulta su consulta junto con los resultados de las evaluaciones.

Método: secuencia de actividades poco integrada y seguimiento que puede concentrarse en etapas tardías de la enseñanza media.

Medio Ambiente: presión familiar y expectativas sociales que influyen en las decisiones del estudiante y quedan fuera de la solución tecnológica.


![image3.png](images2.0/image3.png)


## Objetivo general

Mejorar la gestión, continuidad y trazabilidad del proceso de orientación vocacional y autoconocimiento de estudiantes de enseñanza media, mediante el desarrollo de una aplicación web basada en procesos de negocio (BPM) que permita gestionar evaluaciones de autoconocimiento, centralizar sus resultados y apoyar el seguimiento realizado por los orientadores.

## Objetivos específicos

OE1. Mejorar la identificación de las necesidades asociadas al proceso de orientación vocacional y autoconocimiento, mediante el análisis y priorización de los requerimientos funcionales y no funcionales de estudiantes y orientadores.

OE2. Fortalecer la centralización y trazabilidad de la información generada durante el proceso de orientación vocacional, mediante el diseño de la arquitectura de software, modelo de datos, interfaces y flujo de procesos BPM de la solución.

OE3. Mejorar la gestión y seguimiento del proceso de orientación vocacional y autoconocimiento, mediante el desarrollo de funcionalidades para la aplicación de instrumentos, procesamiento de resultados, generación de reportes y monitoreo del avance de los estudiantes.

OE4. Asegurar el cumplimiento de los requerimientos definidos para la gestión del proceso de orientación vocacional, mediante la validación funcional, de integración y usabilidad de la aplicación utilizando escenarios de prueba y criterios de éxito medibles.

## Métricas de los Objetivos Específicos

La matriz relaciona cada objetivo con un resultado verificable. Los denominadores de las métricas se fijarán al aprobar el listado de requerimientos y los casos de prueba del MVP; los porcentajes se calcularán sobre esos conjuntos definidos y se evaluarán al cierre del proyecto, previsto para noviembre de 2026.


| Objetivo específico | Situación actual | Resultado esperado | Métrica | Criterio de éxito |
| --- | --- | --- | --- | --- |
| OE1. Mejorar la identificación de las necesidades asociadas al proceso de orientación vocacional y autoconocimiento, mediante el análisis y priorización de los requerimientos funcionales y no funcionales de estudiantes y orientadores. | Las necesidades y reglas del proceso aún no se encuentran consolidadas en un conjunto priorizado de requerimientos. | Documento de necesidades, actores, flujo actual y requerimientos priorizados y revisados. | Requerimientos revisados y priorizados / requerimientos identificados en la línea base × 100. | 100 % de los requerimientos de la línea base revisados y priorizados antes de cerrar el análisis; registro de revisión con estudiantes y orientadores. |
| OE2. Fortalecer la centralización y trazabilidad de la información generada durante el proceso de orientación vocacional, mediante el diseño de la arquitectura de software, modelo de datos, interfaces y flujo de procesos BPM de la solución. | No existe un diseño integrado que vincule información, roles, interfaces y estados del proceso. | Arquitectura, modelo de datos, interfaces y BPMN vinculados con los requerimientos aprobados. | Requerimientos aprobados trazados a un componente de diseño / total de requerimientos aprobados × 100. | 100 % de los requerimientos aprobados con trazabilidad al diseño antes de iniciar su implementación; revisión de consistencia entre modelos. |
| OE3. Mejorar la gestión y seguimiento del proceso de orientación vocacional y autoconocimiento, mediante el desarrollo de funcionalidades para la aplicación de instrumentos, procesamiento de resultados, generación de reportes y monitoreo del avance de los estudiantes. | Las actividades de evaluación, cálculo y consulta de resultados no están integradas en una aplicación. | MVP con cuestionario, cálculo de dimensiones, visualización de resultados y consulta del avance por el orientador. | Requerimientos funcionales del MVP que cumplen sus criterios de aceptación / total de requerimientos funcionales del MVP × 100. | 100 % de los requerimientos funcionales críticos del MVP y al menos 90 % del total cumplen sus criterios de aceptación al cierre del desarrollo. |
| OE4. Asegurar el cumplimiento de los requerimientos definidos para la gestión del proceso de orientación vocacional, mediante la validación funcional, de integración y usabilidad de la aplicación utilizando escenarios de prueba y criterios de éxito medibles. | Aún no se dispone de resultados de pruebas del flujo integrado ni de evaluación de usabilidad. | Informe de pruebas funcionales, de integración y de usabilidad con incidencias y acciones correctivas. | Casos críticos aprobados / casos críticos ejecutados × 100; puntaje de usabilidad obtenido / puntaje máximo posible × 100. | 100 % de casos críticos funcionales y de integración aprobados; puntaje medio de usabilidad ≥ 85 % en la muestra definida, con instrumento y cálculo documentados. |


## Limitaciones y alcances del proyecto

Dada la naturaleza individual del proyecto académico, se ha acotado un Producto Mínimo Viable (MVP) que abarca los siguientes módulos e hitos de desarrollo críticos:

**Registro y Autenticación:** Formularios de captura de datos básicos estudiantiles y validación de seguridad mediante tokens JWT.

**Cuestionario BFI-44:** se propone digitalizar los 44 ítems de la versión en español estudiada por Benet-Martínez y John (1998), con cinco opciones de respuesta. Antes de implementarla se cotejarán los enunciados, el orden de los ítems y la clave de puntuación de la versión elegida. La adaptación chilena de Lara et al. (2021) se estudió en universitarios y obtuvo una versión final de 32 ítems; por ello, no constituye una validación del BFI-44 en estudiantes chilenos de enseñanza media.

**Cálculo y reporte:** las respuestas se codificarán de 1 a 5. Los ítems de puntuación inversa se recodificarán como 6 menos la respuesta original. El resultado de cada dimensión será la media aritmética de sus ítems, una vez recodificados los que corresponda; su rango seguirá siendo de 1 a 5. No se calculará un perfil hasta completar las 44 respuestas. El reporte mostrará apertura, responsabilidad, extraversión, amabilidad y neuroticismo en un gráfico de radar (Berkeley Personality Lab, s. f.; John & Srivastava, 1999).

**Interpretación de resultados:** los puntajes se presentarán como descripciones de las respuestas del estudiante para apoyar la reflexión con el orientador. No se usarán percentiles ni categorías clínicas sin normas apropiadas para esta población. El cuestionario no determina la carrera que debe elegir una persona; cualquier sugerencia de áreas de estudio requerirá una fundamentación adicional (Lara et al., 2021; Lowman, 2022).

Orquestación BPM: registro y coordinación de los estados de evaluación y consulta mediante un proceso modelado en BPMN y ejecutado con Camunda 8 (Camunda, s. f.).

Panel del orientador: consulta de estudiantes asignados, estado del proceso y resultados de autoconocimiento para apoyar el seguimiento.

Quedan fuera del MVP la exportación automática de reportes en PDF, la analítica predictiva institucional avanzada y las pruebas automatizadas de la interfaz frontend.

## Normativa y leyes asociadas al proyecto

El desarrollo y operación de la aplicación web **Vócalis** se enmarca en la legislación chilena vigente sobre protección de datos personales, las orientaciones curriculares del Ministerio de Educación de Chile (MINEDUC) para la enseñanza media y los lineamientos éticos internacionales aplicables a los instrumentos de autoconocimiento y al desarrollo seguro de software.

### 1. Marco Legal Chileno de Protección de Datos

#### A. Ley N° 19.628 sobre Protección de la Vida Privada
La Ley N° 19.628 regula el tratamiento automatizado de datos de carácter personal en Chile. Dado que los usuarios principales del sistema corresponden a estudiantes de 3.° y 4.° año de enseñanza media (entre 15 y 18 años), el diseño del MVP incorpora resguardos concretos de privacidad:

1. **Principio de Finalidad (Art. 4° y 9°):** Los datos registrados (nombre completo, correo electrónico, fecha de nacimiento, establecimiento, curso y respuestas al cuestionario) se utilizan exclusivamente para apoyar el proceso de orientación vocacional escolar, sin cesión a terceros ni uso comercial.
2. **Resguardo Técnico de Credenciales y Datos (Art. 11):** Para proteger las cuentas y respuestas almacenadas en MySQL, la aplicación implementa:
   - Almacenamiento cifrado irreversible de contraseñas mediante el algoritmo `Bcrypt`, evitando guardar claves en texto plano.
   - Autenticación mediante tokens firmados `JWT` (algoritmo HS256) con expiración de 24 horas y verificación de cuenta activa (`is_active`) en cada petición a la API.
   - Filtrado de datos sensibles en los errores de validación de entrada, evitando exponer contraseñas o el código de registro de orientador en las respuestas HTTP.
3. **Acceso Restringido por Rol y Curso:** Los reportes de autoconocimiento solo pueden ser consultados por el propio estudiante autenticado y por el orientador asignado a su curso (`curso.orientador_id`), rechazando con error `403` o `404` cualquier consulta hacia estudiantes de otros cursos o establecimientos.

#### B. Ley N° 21.096 sobre Protección Constitucional de los Datos Personales
Esta reforma constitucional al Artículo 19 N° 4 consagra el derecho a la protección de los datos personales. En la plataforma, este principio se refleja en la transparencia sobre el alcance de la información recopilada y en la visibilidad acotada únicamente al orientador responsable del acompañamiento escolar.

#### C. Ley N° 21.180 sobre Transformación Digital
Si bien regula principalmente a organismos públicos, promueve la sustitución de registros dispersos en papel por flujos digitales trazables. El proyecto adopta este enfoque al centralizar el registro de la evaluación y su estado de avance mediante el motor de procesos Camunda 8.

### 2. Marco Educativo Nacional (MINEDUC)

#### A. Ley N° 20.370 General de Educación (LGE)
La Ley General de Educación establece en sus Artículos 2°, 20° y 30° que la enseñanza media busca promover en los estudiantes el autoconocimiento, la reflexión personal y la preparación para continuar estudios superiores o integrarse a la vida laboral. La plataforma apoya directamente este propósito formativo.

#### B. Bases Curriculares de 3.° y 4.° Medio (Decreto N° 193/2019 MINEDUC)
El currículo nacional contempla el espacio de **Taller de Orientación: Decisión Vocacional y Proyecto de Vida** (Ministerio de Educación de Chile, 2024), el cual concibe la orientación como un proceso continuo de reflexión acompañada y no como un evento aislado. El panel del orientador facilita este seguimiento al consolidar el estado de avance de los cursos asignados.

### 3. Criterios Éticos en el Uso del Cuestionario BFI-44 y Estándares Técnicos

De acuerdo con las directrices de la *International Test Commission (ITC)*, la *American Psychological Association (APA)* y la literatura especializada en evaluación vocacional (Lowman, 2022; Benet-Martínez & John, 1998; Lara et al., 2021):

1. **Apoyo Reflexivo y No Determinismo:** El inventario BFI-44 describe cinco dimensiones amplias de personalidad (Apertura, Responsabilidad, Extraversión, Amabilidad y Neuroticismo) y no mide aptitudes académicas ni define la carrera que debe estudiar un alumno.
2. **Acompañamiento del Orientador:** Los resultados y áreas exploratorias presentados en el reporte constituyen un insumo para la conversación pedagógica con el orientador escolar, sin reemplazar su criterio profesional.
3. **Neutralidad en las Sugerencias Exploratorias:** Cuando un perfil presenta puntajes uniformes, empates entre dimensiones o predominio exclusivo de neuroticismo, el sistema omite sugerencias forzadas y retorna una lista vacía de áreas (`careerAreas = []`), priorizando la orientación personalizada.

| Ámbito Normativo | Estándar de Referencia | Aplicación Concreta en el Proyecto |
|:---|:---|:---|
| **Seguridad Web** | Buenas prácticas OWASP | Consultas parametrizadas con SQLAlchemy ORM, control de acceso por rol (`estudiante` / `orientador`), contraseñas con Bcrypt y control de orígenes CORS. |
| **Integridad de Datos** | Transacciones ACID (MySQL InnoDB) | Unicidad de evaluación por estudiante (`uq_evaluacion_estudiante`), validación de rango Likert (1 a 5) y tabla de eventos pendientes (`bpm_evento`) para sincronización con Camunda 8. |
| **Calidad de Código** | PEP 8 (Python) y ESLint (Vue.js) | Validación tipada de esquemas con Pydantic en FastAPI y revisión estática de componentes en el frontend Vue.js 3. |

## Propuesta de solución de alto nivel (nivel macro)

La solución propuesta para **Vócalis** consiste en una aplicación web cliente-servidor integrada con un motor de procesos de negocio (BPM), organizada en tres capas principales que desacoplan la presentación visual, las reglas de negocio y el almacenamiento de datos:

1. **Capa de Presentación (Frontend Web en Vue.js 3):**
   Aplicación de página única (*Single Page Application*, SPA) construida con **Vue.js 3**, **Vite** y **Axios**. Ofrece vistas diferenciadas según el rol autenticado mediante guardias de navegación en Vue Router: para el estudiante, dispone de un panel con el estado de su proceso, el cuestionario BFI-44 paginado con guardado progresivo y el reporte con gráfico de radar; para el orientador, provee un panel de seguimiento por curso y acceso a los reportes de sus alumnos asignados.

2. **Capa de Lógica de Negocio (API REST en FastAPI):**
   Servicio backend desarrollado en **Python** con **FastAPI**, estructurado en routers modulares bajo el prefijo `/api`. Centraliza el registro e inicio de sesión con JWT, la entrega de las 44 preguntas en español, el cálculo de los puntajes de las cinco dimensiones OCEAN con recodificación de los 16 ítems inversos (`ocean_scorer.py`), la generación del reporte descriptivo y las reglas de autorización de cursos del orientador.

3. **Capa de Persistencia y Orquestación de Procesos (MySQL 8.0 y Camunda 8):**
   - **MySQL 8.0 con SQLAlchemy:** Persiste de forma relacional los usuarios, estudiantes, orientadores, cursos, evaluaciones, preguntas, respuestas, reportes y el estado del flujo BPM.
   - **Camunda 8 (Zeebe):** Ejecuta el modelo BPMN 2.0 (`evaluacion-vocacional.bpmn`) que coordina las etapas desde el inicio de la evaluación hasta la disponibilidad del reporte para el orientador, apoyado por *workers* en Python (`pyzeebe`) y una tabla de respaldo de eventos (`bpm_evento`) que reintenta el envío si el motor BPM no está disponible temporalmente.

# CAPÍTULO III: METODOLOGÍA

## Metodología de desarrollo del proyecto

Se propone combinar prácticas de planificación, riesgos, calidad y seguimiento del proyecto descritas por el Project Management Institute (2021) con ciclos de desarrollo inspirados en Scrum (Schwaber & Sutherland, 2020). La adaptación responde al carácter individual y académico del trabajo: cada ciclo tendrá entregables revisables y el plan general conservará hitos y criterios de evaluación definidos.

La planificación inicial establece alcance, dependencias y criterios de prueba; las iteraciones permiten revisar el diseño y la implementación conforme se verifican los requerimientos. El proyecto no aplicará todos los roles y eventos de Scrum como si se tratara de un equipo de desarrollo completo, sino prácticas de trabajo iterativo pertinentes a una persona.

## Plan de proyecto

La programación de las etapas de gestión, desarrollo y control del proyecto se estructura en tres fases secuenciales comprendidas entre abril y noviembre de 2026, asegurando trazabilidad entre el levantamiento conceptual, la construcción incremental del MVP y la verificación técnica:

| Macroetapa del Plan | Período | Actividades de Gestión y Desarrollo | Mecanismos de Control y Entregables |
|:---|:---|:---|:---|
| **1. Inicio y Análisis** | Abril 2026 | Revisión bibliográfica y curricular (MINEDUC y BFI-44), delimitación ética del instrumento, levantamiento de actores y priorización de requerimientos (`RF` y `RNF`). | Línea base de requerimientos aprobada, definición del alcance del MVP y criterios de éxito por objetivo (`OE1`). |
| **2. Diseño y Construcción Iterativa** | Mayo – Septiembre 2026 | Seis sprints incrementales para implementar autenticación JWT, modelo relacional MySQL, cuestionario BFI-44, cálculo OCEAN, integración Camunda 8 y panel del orientador. | Control de versiones en Git, migraciones versionadas en Alembic y entregas parciales verificables (`OE2` y `OE3`). |
| **3. Verificación y Cierre** | Octubre – Noviembre 2026 | Ejecución de la suite de pruebas automatizadas, pruebas de concurrencia y carga (30 usuarios), ajustes de retroalimentación docente y redacción final de la memoria. | Informe de 199 pruebas aprobadas, benchmark de latencia, protocolo de usabilidad y documento final (`OE4`). |

## Herramientas y ambiente de desarrollo

La selección tecnológica busca cubrir la interfaz, la API, la persistencia y la coordinación del flujo con herramientas que puedan integrarse en el entorno de desarrollo previsto:

- **Backend:** FastAPI (Python) para exponer la API REST y generar documentación interactiva de sus endpoints (FastAPI, s. f.).
- **Motor BPM:** Camunda 8 en una instalación local contenedorizada para representar y ejecutar el flujo BPMN de evaluación y seguimiento (Camunda, s. f.).
- **Frontend:** Vue.js 3, Vite y Axios para construir la interfaz reactiva y comunicarse de forma asíncrona con la API.
- **Base de datos:** MySQL 8.0 (motor InnoDB) para persistir usuarios, respuestas, resultados y estados; SQLAlchemy 2.0 y Alembic para el mapeo objeto-relacional y las migraciones de esquema.
- **Control de versiones y entorno:** Git con repositorios remotos en GitHub; desarrollo sobre Visual Studio Code operado de forma nativa bajo el sistema operativo CachyOS (distribución basada en Arch Linux) y compatibilizado con Windows mediante Docker Compose.

## Descripción general de la propuesta de solución

A nivel arquitectónico, la plataforma conecta al estudiante y al orientador escolar mediante una interfaz web SPA en Vue.js 3 que consume los servicios RESTful de FastAPI. El backend coordina tanto la persistencia relacional en MySQL 8.0 como el avance del proceso vocacional en Camunda 8 (Zeebe), tal como se ilustra en el esquema general de la solución:

![Arquitectura general de la solución](images2.0/image4.png)

*Figura 2: Arquitectura general e integración de componentes de la propuesta de solución.*

## Propuesta de controles y evidencia a implementar en los flujos de la propuesta de solución

Para resguardar la consistencia funcional, la seguridad de acceso y la trazabilidad del flujo de orientación, se definieron controles verificables en cada etapa operativa de la aplicación:

| Flujo del Sistema | Control Aplicado | Implementación en el Sistema | Evidencia de Verificación |
|:---|:---|:---|:---|
| **Registro de Usuarios** | Unicidad de correo y validación de rol orientador. | Índice único en `usuario.email` y verificación del código institucional de orientador. | Pruebas automatizadas en `test_auth_registro.py` (37 casos aprobados). |
| **Inicio de Sesión** | Contraseña cifrada y control de vigencia de cuenta. | Hash `Bcrypt` y verificación de `is_active = True` al emitir y validar el token JWT. | Rechazo HTTP 401 ante credenciales inválidas o cuentas inactivas. |
| **Aplicación BFI-44** | Intento único por estudiante y guardado progresivo. | Restricción única `uq_evaluacion_estudiante` y bloqueo de fila (`FOR UPDATE`) al registrar cada respuesta. | Pruebas de integridad y concurrencia en `test_evaluacion_respuestas.py` (35 casos). |
| **Cálculo y Envío** | Exigencia de los 44 ítems completos en escala 1 a 5. | Validación con esquemas Pydantic y recodificación `6 - valor` en los 16 ítems inversos. | Pruebas unitarias exactas en `test_ocean_scorer.py` y rechazo HTTP 422 si faltan respuestas. |
| **Orquestación BPM** | Respaldo de mensajes ante desconexión de Camunda 8. | Registro transaccional del evento en `bpm_evento` junto con el reporte antes de publicar por gRPC a Zeebe. | Pruebas de caída y reintento en `test_bpm_delivery.py` y `test_bpm_mysql.py`. |
| **Reporte Vocacional** | Presentación orientativa no determinista. | Textos descriptivos por dimensión y retorno sin áreas forzadas (`[]`) ante perfiles neutros o empates. | Pruebas de reglas exploratorias en `test_career_areas.py` y `test_reportes.py`. |
| **Seguimiento Orientador** | Aislamiento de acceso por curso y establecimiento. | Comprobación de `curso.orientador_id` antes de listar alumnos o abrir un reporte individual. | Bloqueo HTTP 403 comprobado en pruebas de autorización cruzada. |

## Plan de gestión de calidad y pruebas

**Gestión de la calidad:** Se revisará el código backend conforme a PEP 8 y el frontend con ESLint, cubriendo mediante pruebas automatizadas la lógica de cálculo psicométrico, las reglas de autorización por rol y los casos críticos de negocio, con una meta mínima del 80 % de cobertura en el backend. El objetivo de respuesta de la API es de hasta 3 segundos en un escenario de hasta 30 usuarios concurrentes, documentando equipo, operaciones medidas y procedimiento de carga.

**Gestión de pruebas:** Se ejecutarán pruebas unitarias del cálculo OCEAN y de la API, pruebas de integración entre interfaz, backend, base de datos MySQL y motor BPM Camunda 8, y escenarios completos de extremo a extremo. El registro de resultados detallará los casos ejecutados, evidencias y correcciones aplicadas, mientras que la usabilidad se evaluará mediante el instrumento estándar *System Usability Scale* (SUS) documentado antes de su aplicación a la muestra.

## Plan de riesgos

La gestión preventiva de riesgos identifica los eventos técnicos, operativos y de alcance capaces de afectar el cumplimiento de los objetivos del proyecto, estableciendo acciones concretas de mitigación y contingencia:

| ID | Riesgo Identificado | Nivel (Prob. / Impacto) | Estrategia Preventiva de Mitigación | Plan de Contingencia Aplicable |
|:---|:---|:---|:---|:---|
| **RSG-01** | Desconexión o falla temporal en la comunicación gRPC entre FastAPI y Camunda 8 Zeebe. | Media / Alto | Prueba de concepto temprana en el Sprint 1 y desacoplamiento entre la base de datos y el broker BPM. | Almacenamiento de eventos en tabla `bpm_evento` (*Transactional Outbox*) con reintento automático en segundo plano sin perder reportes. |
| **RSG-02** | Condiciones de carrera o duplicidad de evaluaciones ante clics múltiples o concurrencia. | Media / Alto | Restricción única `uq_evaluacion_estudiante` en MySQL, cola secuencial en frontend y bloqueo de fila `FOR UPDATE`. | Reintento controlado ante bloqueos transitorios de InnoDB y rechazo HTTP 400/409 ante envíos repetidos. |
| **RSG-03** | Interpretación determinista o prescriptiva de las sugerencias vocacionales del reporte BFI-44. | Media / Medio | Fundamentación teórica exploratoria (RIASEC) y advertencias visibles sobre el rol insustituible del orientador. | Ajuste de etiquetas a *"Áreas profesionales para explorar"* y retorno vacío (`[]`) ante perfiles uniformes o empates. |
| **RSG-04** | Sobrecarga de trabajo y desviación de plazos por tratarse de un desarrollo individual. | Media / Medio | Acotamiento estricto del MVP (excluyendo exportación PDF y analítica predictiva) y seguimiento semanal por sprint. | Uso de la holgura planificada en octubre-noviembre para estabilización, pruebas de carga y cierre documental. |

## Cronograma del Proyecto (Planificación de Sprints)

El proyecto se planifica entre abril y noviembre de 2026. Abril se destina al análisis y la preparación de requerimientos; los ciclos de desarrollo descritos a continuación cubren mayo a septiembre. Octubre y noviembre se reservan para resolver incidencias, consolidar los resultados de las pruebas, completar la documentación y preparar la entrega final:

- **Sprint 1 (Mayo 2026):** Inicialización del entorno contenedorizado, despliegue local de Camunda 8, prueba de concepto de integración y desarrollo de la capa de registro y autenticación JWT.
- **Sprint 2 (Junio 2026):** Modelado BPMN 2.0 de la evaluación, maquetación del cuestionario BFI-44 en Vue.js 3 con guardado progresivo y codificación del algoritmo de puntajes OCEAN.
- **Sprint 3 (Junio – Julio 2026):** Construcción de la interfaz gráfica de resultados (gráfico de radar SVG), lógica de reportes descriptivos, áreas exploratorias e integración resiliente del flujo con Zeebe.
- **Sprint 4 (Julio – Agosto 2026):** Implementación del panel de control para el perfil de orientador escolar, filtros de seguimiento por curso y consulta autorizada de reportes estudiantiles.
- **Sprints 5 y 6 (Agosto – Septiembre 2026):** Refinamiento responsivo de interfaces (escritorio y móvil), asignación de cursos libres, validaciones de seguridad y suite automatizada de concurrencia.

## Prototipo

Las pantallas siguientes ilustran el diseño de acceso para estudiantes y orientadores, la aplicación digital del BFI-44, la visualización de resultados y el panel de seguimiento. Los prototipos representan la línea base visual de la interfaz y su correspondencia con el alcance del MVP definido en el Capítulo II.

### Pantalla de Login y Registro Centralizado

Esta interfaz permite el acceso seguro a la plataforma mediante credenciales validadas (correo electrónico y contraseña cifrada con `Bcrypt`). Cuenta con un selector por perfil para diferenciar el flujo entre Estudiante y Orientador Escolar, solicitando en el registro los antecedentes escolares necesarios (nombre completo, fecha de nacimiento, establecimiento educativo, curso o código institucional de orientador).

![Pantalla de inicio de sesión y registro](images2.0/image5.png)

*Figura 3: Prototipo de la pantalla de inicio de sesión y registro por rol.*

### Pantalla del Panel Principal del Estudiante (Dashboard)

Una vez autenticado, el estudiante accede a un panel claro que presenta la etapa actual de su proceso coordinado con Camunda 8. Si aún no ha rendido el instrumento, destaca la acción **"Iniciar Evaluación Vocacional"**; una vez completado el cuestionario, habilita el acceso directo a su reporte y bitácora de avance.

![Panel principal del estudiante](images2.0/image6.png)

*Figura 4: Prototipo del panel principal del estudiante con indicador de estado BPM.*

### Pantalla del Cuestionario Big Five (BFI-44)

La vista presenta los 44 ítems de la versión en español estudiada por Benet-Martínez y John (1998) en bloques paginados con cinco opciones de respuesta Likert (1 a 5), conservando el orden y numeración oficial de la clave de puntuación. Cada ítem debe ser respondido antes del envío definitivo para calcular los promedios sobre el conjunto completo (Berkeley Personality Lab, s. f.).

**Puntuación de las dimensiones:** Los 16 ítems inversos corresponden a los números 6, 21 y 31 en Extraversión; 2, 12, 27 y 37 en Amabilidad; 8, 18, 23 y 43 en Responsabilidad; 9, 24 y 34 en Neuroticismo; y 35 y 41 en Apertura. Cada respuesta inversa se transforma mediante `6 − respuesta`, promediando luego los 8, 9, 9, 8 y 10 ítems respectivos por dimensión (John & Srivastava, 1999).

![Pantalla del cuestionario Big Five BFI-44](images2.0/image7.png)

*Figura 5: Prototipo de aplicación paginada del cuestionario BFI-44.*

### Pantalla de Reporte Vocacional Enriquecido

El reporte presenta los resultados de las cinco dimensiones del BFI-44 mediante un gráfico de radar pentagonal y un acordeón interactivo con descripciones comprensibles para el estudiante. Los puntajes describen las respuestas declaradas en el autoinforme y **no constituyen un diagnóstico clínico ni una recomendación automática de carrera** (Berkeley Personality Lab, s. f.; Lowman, 2022).

**Alcance interpretativo y ajuste de neutralidad vocacional:** Dado que la versión en español fue estudiada en poblaciones distintas de escolares chilenos (Benet-Martínez & John, 1998) y la adaptación nacional en universitarios redujo el inventario a 32 ítems (Lara et al., 2021), la sección orientativa se fundamenta únicamente en correlaciones exploratorias entre los Cinco Grandes y las tipologías RIASEC de Holland documentadas en metaanálisis (Barrick et al., 2003; Larson et al., 2002). Atendiendo específicamente a las observaciones docentes sobre los prototipos iniciales que se muestran a continuación, en la implementación final del MVP (`src/views/ReporteView.vue` y `backend/app/routers/reporte.py`) se reemplazaron los encabezados prescriptivos (*"Carreras recomendadas"* e *"Impacto vocacional"*) por formulaciones neutrales (*"Áreas profesionales para explorar"*, *"Alcance del puntaje"*, *"Ejemplos de carreras"* y la nota expresa *"no acreditan afinidad ni aptitud profesional"*), además de omitir cualquier área sugerida (`careerAreas = []`) ante perfiles con empate o sin respaldo en las reglas definidas.

![Reporte vocacional: vista general y radar](images2.0/image11.png)

*Figura 6: Prototipo del reporte vocacional — Vista general y gráfico de radar de cinco ejes.*

![Reporte vocacional: interpretación de dimensiones parte 1](images2.0/image9.png)

*Figura 7: Prototipo del reporte vocacional — Despliegue descriptivo de Apertura, Responsabilidad y Extraversión.*

![Reporte vocacional: interpretación de dimensiones parte 2](images2.0/image10.png)

*Figura 8: Prototipo del reporte vocacional — Despliegue descriptivo de Amabilidad y Neuroticismo.*

![Reporte vocacional: áreas de afinidad exploratorias](images2.0/image8.png)

*Figura 9: Prototipo inicial de áreas de afinidad (ajustado en el MVP final a lenguaje exploratorio no determinista).*

### Pantalla del Panel de Gestión y Monitoreo del Orientador

El panel del orientador centraliza la lista de estudiantes pertenecientes a sus cursos asignados, sus indicadores agregados (*Alumnos Asignados*, *Flujos en Evaluación* y *Reportes Listos*), los filtros por curso o etapa en Camunda 8 y el acceso directo a la revisión individual del reporte para apoyar las sesiones de orientación.

![Panel de gestión y monitoreo del orientador](images2.0/image12.png)

*Figura 10: Prototipo del panel de gestión y monitoreo del orientador escolar.*

# CAPÍTULO IV: DISCUSIÓN DE RESULTADOS

## Gestión de proyecto

### 1. Aplicación de la Metodología Híbrida (PMBOK y Scrum Adaptado)

Para conducir el desarrollo de **Vócalis**, se aplicó la metodología híbrida definida en el Capítulo III, articulando las prácticas de planificación, control de alcance, riesgos y aseguramiento de calidad de la guía **PMBOK (7.ª edición)** con ciclos iterativos e incrementales basados en **Scrum** (Project Management Institute, 2021; Schwaber & Sutherland, 2020).

Atendiendo al carácter individual de este proyecto de título, las responsabilidades se estructuraron de manera práctica: el autor asumió la gestión y priorización de requerimientos (*Product Backlog*) junto con el diseño, programación y ejecución de pruebas de cada incremento, mientras que la profesora guía actuó como contraparte académica en las revisiones de avance por hito, validando el cumplimiento metodológico y el alineamiento con el alcance comprometido del MVP.

### 2. Iteraciones Ejecutadas, Entregables y Relación con los Objetivos Específicos

En coherencia con el horizonte planificado entre abril y noviembre de 2026, el trabajo se ejecutó mediante una fase inicial de análisis, seis sprints de construcción e integración y una etapa final de validación y consolidación documental:

| Iteración | Período | Actividades Desarrolladas | Entregables Principales | Obj. | Resultado Obtenido |
|:---|:---|:---|:---|:---|:---|
| **Fase Inicial: Análisis** | Abril 2026 | Revisión curricular MINEDUC y literatura BFI-44; identificación de actores; priorización de requerimientos del MVP. | Especificación de requerimientos RF/RNF y definición de alcance y exclusiones. | **OE1** | 100 % de requerimientos de la línea base definidos y priorizados. |
| **Sprint 1: Base y Acceso** | Mayo 2026 | Configuración de Docker Compose (MySQL 8.0 y Camunda 8), prueba de concepto BPM y módulo de registro/login con JWT y Bcrypt. | Entorno contenedorizado, tablas de usuarios/roles, endpoints `/api/auth/*` y vista `AuthView.vue`. | **OE1, OE2** | Registro diferenciado por rol y autenticación JWT operativa (37 pruebas). |
| **Sprint 2: BFI-44 y Cálculo** | Junio 2026 | Modelado del proceso BPMN 2.0, carga de los 44 ítems en español (`seed.py`), interfaz del cuestionario y motor `ocean_scorer.py`. | Diagrama `evaluacion-vocacional.bpmn`, vista `EvaluacionView.vue` y cálculo con 16 ítems inversos. | **OE2, OE3** | Guardado progresivo de respuestas y cálculo exacto de las 5 dimensiones. |
| **Sprint 3: Reporte y Flujo BPM** | Junio – Julio 2026 | Construcción del gráfico de radar SVG, textos interpretativos, áreas exploratorias RIASEC y conexión de *workers* con Zeebe. | Vista `ReporteView.vue`, servicio `bpm_service.py`, `worker.py` y tabla `bpm_evento`. | **OE2, OE3** | Reportes generados de forma atómica y sincronización resiliente con Camunda 8. |
| **Sprint 4: Panel Orientador** | Julio – Agosto 2026 | Implementación del panel del orientador, filtros por curso y estado del proceso, y consulta autorizada de reportes de alumnos. | Vista `OrientadorDashboardView.vue`, router `orientador.py` y asignación de cursos libres. | **OE3** | Seguimiento por curso y control estricto de acceso entre orientadores. |
| **Sprints 5 y 6: Ajuste y Calidad** | Agosto – Septiembre 2026 | Migraciones Alembic de unicidad y contexto escolar, soporte responsivo escritorio/móvil y suite de pruebas de seguridad y concurrencia. | Revisiones Alembic, scripts de inicio local/Wi-Fi y suite de 199 pruebas en Pytest. | **OE3, OE4** | 89,80 % de cobertura backend y 0 errores de concurrencia en MySQL. |
| **Cierre y Validación** | Octubre – Noviembre 2026 | Prueba de carga con 30 usuarios concurrentes, preparación de pauta de usabilidad y consolidación del informe final (Hito 2 y cierre). | Script `measure_latency.py`, reporte `validacion_mvp.md`, trazabilidad y memoria completa. | **OE4** | 199/199 pruebas aprobadas y latencia p95 de 1,216 s (< 3,0 s). |

### 3. Evidencias de Control del Desarrollo

El avance de las iteraciones quedó respaldado mediante tres mecanismos verificables en el repositorio del proyecto:
1. **Historial de Versiones en Git:** Registro incremental de cambios por módulo funcional (autenticación, evaluación, motor OCEAN, integración Zeebe, panel de orientador y correcciones de validación).
2. **Migraciones Versionadas con Alembic:** Evolución controlada del esquema relacional en MySQL mediante tres revisiones secuenciales (`20260922_eval_unique`, `20260922_registro_contexto` y `20260924_bpm_outbox`), verificadas en bases temporales aisladas sin pérdida de datos.
3. **Verificación Automatizada Continua:** Ejecución sistemática de la suite `pytest` sobre `backend/tests`, alcanzando **199 pruebas aprobadas** y **89,80 % de cobertura combinada** medida con `coverage.py`.

## Diseño de los componentes funcionales de la propuesta de solución

El diseño funcional de **Vócalis** formaliza las interacciones entre los actores del proceso educativo (Estudiante y Orientador Escolar) y los componentes tecnológicos del sistema. A continuación se presenta el diagrama general de casos de uso, las especificaciones detalladas de los diez casos de uso que conforman el MVP, el modelo de proceso BPMN 2.0 y los diagramas de secuencia correspondientes.

### 1. Diagrama General y Especificación Detallada de Casos de Uso

El siguiente diagrama resume el alcance funcional comprometido para ambos perfiles de usuario y las tareas coordinadas con el motor de procesos Camunda 8, distinguiendo explícitamente la exportación en PDF como trabajo futuro fuera del MVP:

![Diagrama General de Casos de Uso del Sistema](images2.0/image13.png)

*Figura 11: Diagrama general de casos de uso del sistema Vócalis.*

A continuación se especifican los diez casos de uso principales del sistema:

#### CU-01: Registro de Usuario en la Plataforma
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-01 — Registro de Usuario en la Plataforma |
| **Actores** | Estudiante, Orientador Escolar |
| **Descripción** | Permite crear una nueva cuenta en la plataforma, registrando los datos académicos y de establecimiento según el rol seleccionado. |
| **Precondición** | El usuario dispone de un correo electrónico válido no registrado previamente en la base de datos. |
| **Flujo Principal** | 1. El usuario accede a la vista de autenticación y selecciona la opción de registro.<br>2. Elige su perfil: *Estudiante* u *Orientador Escolar*.<br>3. Si es Estudiante, ingresa nombre completo, correo, contraseña, fecha de nacimiento, establecimiento, nivel y letra del curso.<br>4. Si es Orientador, ingresa nombre completo, correo, contraseña, departamento, establecimiento y el código institucional de registro.<br>5. El backend valida los datos con Pydantic, cifra la contraseña con `Bcrypt` y abre una transacción con aislamiento `SERIALIZABLE`.<br>6. Si el curso indicado no existe en el establecimiento, se crea automáticamente; si existe un único orientador en dicho colegio, el curso queda asociado a su cargo.<br>7. El sistema confirma el registro (HTTP 200) y redirige al inicio de sesión. |
| **Flujos Alternativos** | • **FA-1 (Correo ya registrado):** Retorna HTTP 409 informando que el correo ya posee una cuenta.<br>• **FA-2 (Código de orientador inválido):** Retorna HTTP 403 sin crear registros.<br>• **FA-3 (Fecha de nacimiento inválida):** Retorna HTTP 422 ante fechas futuras o fuera de rango. |
| **Postcondición** | Se almacenan de forma atómica las filas correspondientes en `usuario` y `estudiante` (u `orientador`). |

#### CU-02: Autenticación e Inicio de Sesión
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-02 — Autenticación e Inicio de Sesión |
| **Actores** | Estudiante, Orientador Escolar |
| **Descripción** | Verifica las credenciales del usuario y emite un token JWT firmado para autorizar las sesiones en el navegador. |
| **Precondición** | El usuario se encuentra registrado y su cuenta permanece activa (`is_active = True`). |
| **Flujo Principal** | 1. El usuario ingresa su correo electrónico y contraseña en `AuthView.vue`.<br>2. El backend recupera el usuario por correo y comprueba el hash mediante `Bcrypt`.<br>3. Verifica que el indicador `is_active` sea verdadero.<br>4. Genera un token JWT firmado (HS256) con vigencia de 24 horas que incluye `sub` (correo) y `role`.<br>5. El cliente web almacena el token en `localStorage` y redirige al panel correspondiente al rol (`/estudiante/dashboard` u `/orientador/dashboard`). |
| **Flujos Alternativos** | • **FA-1 (Credenciales incorrectas o cuenta inactiva):** Retorna HTTP 401 con mensaje uniforme de error de autenticación. |
| **Postcondición** | Sesión autenticada en el cliente web con token JWT vigente. |

#### CU-03: Consulta de Identidad del Usuario Activo
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-03 — Obtener Perfil de Usuario Autenticado |
| **Actores** | Estudiante, Orientador Escolar |
| **Descripción** | Entrega los datos básicos de identidad del usuario autenticado para desplegar su nombre y rol en la navegación lateral. |
| **Precondición** | Solicitud HTTP acompañada de cabecera `Authorization` con token Bearer JWT válido. |
| **Flujo Principal** | 1. El frontend realiza una petición `GET /api/auth/me`.<br>2. La dependencia de seguridad valida la firma, expiración y estado activo del usuario.<br>3. El servicio consulta el perfil asociado y retorna `{ id, email, role, name }`. |
| **Postcondición** | La interfaz muestra el nombre real y rol verificado del usuario en sesión. |

#### CU-04: Guardado Progresivo de Respuestas del Cuestionario BFI-44
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-04 — Guardar Respuesta Parcial de Evaluación |
| **Actores** | Estudiante |
| **Descripción** | Registra individualmente la opción Likert (1 a 5) marcada en cada reactivo del BFI-44, permitiendo retomar el cuestionario ante recargas o cortes de conexión. |
| **Precondición** | Estudiante autenticado sin una evaluación previamente cerrada en estado `completada`. |
| **Flujo Principal** | 1. El estudiante selecciona un valor entre 1 y 5 en un ítem de `EvaluacionView.vue`.<br>2. El cliente encola la petición `POST /api/evaluacion/respuesta` con `{ preguntaId, valor }`.<br>3. El backend bloquea la fila del estudiante y su evaluación activa mediante `SELECT ... FOR UPDATE`.<br>4. Si aún no existe evaluación, la crea en estado `en_progreso`, registra el estado inicial `registro` en `proceso_bpm` y encola el evento de inicio para Camunda 8.<br>5. Inserta o actualiza el valor en la tabla `respuesta` y confirma la transacción (HTTP 200). |
| **Flujos Alternativos** | • **FA-1 (Evaluación ya finalizada):** Retorna HTTP 400 impidiendo modificar respuestas cerradas.<br>• **FA-2 (Ítem o rango inválido):** Retorna HTTP 422 si la pregunta no existe o el valor no está entre 1 y 5.<br>• **FA-3 (Colisión transaccional):** El endpoint reintenta automáticamente ante bloqueos transitorios de MySQL. |
| **Postcondición** | La respuesta queda persistida en MySQL y disponible para continuar el cuestionario. |

#### CU-05: Envío Definitivo del BFI-44 y Generación de Reporte
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-05 — Finalizar Evaluación y Calcular Perfil OCEAN |
| **Actores** | Estudiante |
| **Descripción** | Verifica la completitud de los 44 reactivos, calcula los puntajes OCEAN, almacena el reporte descriptivo y notifica el avance al motor BPM Camunda 8. |
| **Precondición** | El estudiante ha respondido la totalidad de los 44 ítems del inventario BFI-44. |
| **Flujo Principal** | 1. El estudiante presiona "Finalizar y Enviar Evaluación".<br>2. El frontend espera a que finalice cualquier guardado parcial en curso y envía `POST /api/evaluacion/enviar`.<br>3. El backend bloquea la evaluación (`FOR UPDATE`) y verifica que existan exactamente las 44 respuestas válidas sin duplicados ni omisiones.<br>4. El servicio `ocean_scorer.py` recodifica los 16 ítems inversos (`6 - respuesta`), calcula el promedio por dimensión y normaliza el puntaje.<br>5. Se guarda el `ReporteVocacional`, se inserta el evento `completar` en `bpm_evento` y se marca la evaluación como `completada`.<br>6. Tras confirmar el commit en MySQL, se publica el mensaje `CuestionarioCompletado` hacia Zeebe y el cliente redirige a `/estudiante/reporte`. |
| **Flujos Alternativos** | • **FA-1 (Cuestionario incompleto):** Retorna HTTP 422 si faltan ítems por responder.<br>• **FA-2 (Zeebe no disponible):** El reporte permanece confirmado en MySQL y el proceso en segundo plano reintenta el envío del evento pendiente. |
| **Postcondición** | Evaluación cerrada como intento único, reporte persistido y flujo BPM avanzado. |

#### CU-06: Consulta de Estado de Evaluación y Bitácora BPM
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-06 — Consultar Estado del Proceso Vocacional |
| **Actores** | Estudiante |
| **Descripción** | Informa al estudiante la etapa actual de su evaluación dentro del flujo coordinado con Camunda 8 y el orientador asignado a su curso. |
| **Precondición** | Estudiante autenticado. |
| **Flujo Principal** | 1. Al cargar el panel principal, el cliente solicita `GET /api/evaluacion/estado`.<br>2. El backend consulta `evaluacion`, `proceso_bpm` y el orientador asociado al curso del alumno.<br>3. Retorna el estado de la evaluación, la etapa BPM (`registro`, `calculando_ocean`, `generando_reporte` o `reporte_listo`), las marcas de tiempo y el nombre del orientador. |
| **Postcondición** | El panel del estudiante actualiza el indicador visual de progreso y su bitácora. |

#### CU-07: Visualización del Reporte de Autoconocimiento Personal
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-07 — Consultar Reporte Vocacional Propio |
| **Actores** | Estudiante |
| **Descripción** | Presenta al estudiante sus puntajes en las cinco dimensiones del BFI-44 mediante un gráfico de radar SVG, descripciones por rasgo y áreas profesionales exploratorias. |
| **Precondición** | El estudiante cuenta con su evaluación en estado `completada` y reporte generado. |
| **Flujo Principal** | 1. El estudiante ingresa a `/estudiante/reporte`, disparando `GET /api/evaluacion/reporte`.<br>2. El backend recupera el `ReporteVocacional` asociado al estudiante autenticado.<br>3. Construye la respuesta `ReporteOut` con puntajes, textos interpretativos y áreas para explorar.<br>4. `ReporteView.vue` dibuja el polígono pentagonal en SVG, la leyenda accesible y el acordeón de dimensiones con nota explícita de alcance no determinista. |
| **Postcondición** | El estudiante visualiza sus resultados como insumo de reflexión personal y diálogo con su orientador. |

#### CU-08: Monitoreo de Estudiantes y Estados por el Orientador
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-08 — Listar Estudiantes Asignados y Avance BPM |
| **Actores** | Orientador Escolar |
| **Descripción** | Permite al orientador supervisar la nómina de estudiantes de sus cursos asignados, filtrando por curso, búsqueda nominal o etapa del proceso BPM. |
| **Precondición** | Orientador autenticado con uno o más cursos asociados a su cargo. |
| **Flujo Principal** | 1. El orientador accede a `/orientador/dashboard` (`GET /api/orientador/estudiantes`).<br>2. El backend consulta los alumnos pertenecientes exclusivamente a cursos donde `curso.orientador_id` coincide con el orientador autenticado.<br>3. Retorna nombre, correo, curso, fecha de actualización, estado BPM e indicador `hasReport`.<br>4. La vista calcula en tiempo real los contadores de alumnos asignados, evaluaciones en curso y reportes listos. |
| **Postcondición** | El orientador dispone de visibilidad centralizada sobre el avance de sus cursos. |

#### CU-09: Revisión del Reporte de un Estudiante por el Orientador
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-09 — Consultar Reporte Individual de Alumno Asignado |
| **Actores** | Orientador Escolar |
| **Descripción** | Permite al orientador abrir el reporte completo BFI-44 de un estudiante de sus cursos para preparar y conducir sesiones de acompañamiento vocacional. |
| **Precondición** | El estudiante pertenece a un curso asignado al orientador y ha finalizado su evaluación. |
| **Flujo Principal** | 1. El orientador selecciona "Ver Reporte" sobre un alumno (`GET /api/orientador/estudiante/{id}/reporte`).<br>2. El backend valida que el curso del estudiante pertenezca al orientador solicitante.<br>3. Retorna el objeto `ReporteOut` incluyendo el nombre del estudiante evaluado y el estado BPM.<br>4. La interfaz presenta el reporte en modo de consulta profesional para el orientador. |
| **Flujos Alternativos** | • **FA-1 (Alumno de otro orientador o establecimiento):** Retorna HTTP 403 denegando el acceso.<br>• **FA-2 (Alumno sin evaluación finalizada):** Retorna HTTP 404 indicando que aún no existe reporte. |
| **Postcondición** | El orientador revisa los resultados descriptivos del alumno resguardando la confidencialidad escolar. |

#### CU-10: Asignación de Cursos sin Orientador en el Establecimiento
| Atributo | Especificación |
|:---|:---|
| **Identificador y Nombre** | CU-10 — Reclamar Curso Vacante del Establecimiento |
| **Actores** | Orientador Escolar |
| **Descripción** | Permite a un orientador consultar y asumir formalmente la supervisión de cursos de su mismo establecimiento que aún no cuentan con orientador asignado. |
| **Precondición** | Existen cursos en el establecimiento del orientador con `orientador_id` nulo. |
| **Flujo Principal** | 1. El panel del orientador consulta `GET /api/orientador/cursos/sin-asignar`.<br>2. El backend retorna los cursos del mismo colegio sin orientador junto con su número de estudiantes.<br>3. El orientador presiona "Asignar a mi cargo" (`POST /api/orientador/cursos/{curso_id}/asignar`).<br>4. El backend ejecuta una actualización atómica condicionada a que `orientador_id IS NULL`.<br>5. Confirma la operación (HTTP 200) y actualiza inmediatamente la nómina del panel. |
| **Flujos Alternativos** | • **FA-1 (Curso ya asignado concurrentemente):** Retorna HTTP 409 informando que el curso ya fue tomado.<br>• **FA-2 (Curso de otro establecimiento):** Retorna HTTP 404. |
| **Postcondición** | El curso y sus estudiantes quedan vinculados al orientador en MySQL. |

### 2. Modelo de Proceso de Negocio BPMN 2.0 (Orquestación Camunda 8)

El flujo de negocio ejecutable (`bpmn/evaluacion-vocacional.bpmn`) coordina el recorrido de cada evaluación a través de tres carriles (*lanes*) de responsabilidad: el **Estudiante**, el **Sistema / Camunda 8** y el **Orientador Escolar**. Para facilitar su lectura en formato vertical, las siguientes dos vistas muestran de izquierda a derecha la secuencia completa del proceso:

![Diagrama BPMN Parte 1: Carril del Estudiante](images2.0/image14.png)

*Figura 12: Diagrama BPMN 2.0 (Parte 1) — Inicio de evaluación, carga de reactivos BFI-44 y guardado parcial.*

![Diagrama BPMN Parte 2: Orquestación Camunda 8 y Revisión del Orientador](images2.0/image15.png)

*Figura 13: Diagrama BPMN 2.0 (Parte 2) — Tareas de servicio en Camunda 8 y seguimiento por el orientador.*

En la implementación real sobre Zeebe, al crearse la evaluación se inicia una instancia del proceso `evaluacion-vocacional`, quedando a la espera del mensaje correlacionado `CuestionarioCompletado` (asociado por `evaluacion_id`). Una vez recibido dicho mensaje tras el envío de las 44 respuestas, el motor activa secuencialmente los tres *Service Tasks* atendidos por `worker.py` (`calcular-ocean`, `generar-reporte` y `notificar-orientador`), actualizando de forma trazable la tabla `proceso_bpm` hasta alcanzar el estado `reporte_listo`.

### 3. Diagramas de Secuencia del Sistema

Los siguientes cuatro diagramas de secuencia detallan el intercambio cronológico de mensajes entre las vistas Vue.js 3, los routers y servicios de FastAPI, la base de datos MySQL 8.0 y el motor Camunda 8:

#### DS-01: Autenticación, Emisión JWT y Redirección por Roles (CU-02 y CU-03)

Modela la verificación criptográfica de credenciales con `Bcrypt`, la comprobación de vigencia de la cuenta (`is_active`), la firma del token JWT y la protección de rutas en el cliente mediante `Vue Router`.

![Diagrama de Secuencia DS-01: Autenticación y Emisión JWT](images2.0/image20.png)

*Figura 14: Diagrama de secuencia DS-01 — Autenticación, emisión JWT y redirección según rol.*

#### DS-02: Guardado Incremental de Respuestas BFI-44 con Bloqueo Pesimista (CU-04)

Representa la cola secuencial de autoguardado en el navegador y el bloqueo de filas (`SELECT ... FOR UPDATE`) en MySQL InnoDB, evitando condiciones de carrera cuando el estudiante responde con rapidez.

![Diagrama de Secuencia DS-02: Guardado Incremental BFI-44](images2.0/image21.png)

*Figura 15: Diagrama de secuencia DS-02 — Guardado progresivo de respuestas con bloqueo de fila.*

#### DS-03: Finalización del Cuestionario, Transacción ACID y Orquestación Zeebe (CU-05 y CU-06)

Ilustra el cierre transaccional de las 44 respuestas, el cálculo de dimensiones en `ocean_scorer.py`, el respaldo del evento en la tabla `bpm_evento` (*Transactional Outbox*) y la ejecución asíncrona de los *workers* en Camunda 8.

![Diagrama de Secuencia DS-03: Finalización BFI-44 y Orquestación Zeebe](images2.0/image22.png)

*Figura 16: Diagrama de secuencia DS-03 — Envío definitivo, persistencia ACID y avance en Camunda 8.*

#### DS-04: Supervisión, Asignación de Cursos y Consulta de Reportes por el Orientador (CU-08 a CU-10)

Describe la carga filtrada de estudiantes asignados, el reclamo atómico de cursos vacantes dentro del mismo establecimiento y la verificación de pertenencia escolar previa a mostrar un reporte individual.

![Diagrama de Secuencia DS-04: Gestión y Consulta de Reportes por el Orientador](images2.0/image23.png)

*Figura 17: Diagrama de secuencia DS-04 — Panel del orientador, asignación de cursos y consulta autorizada.*

## Matriz de trazabilidad de Requerimientos

La matriz de trazabilidad relaciona cada requerimiento funcional (`RF`) y no funcional (`RNF`) del MVP con los objetivos específicos del proyecto (`OE1` a `OE4`), el sprint en que fue abordado, los artefactos de diseño asociados, los módulos implementados en el código fuente y los casos de prueba que verifican su cumplimiento:

| ID / Tipo | Descripción del Requerimiento | Obj. y Sprint | Componente de Diseño | Módulo Implementado | Verificación y Estado |
|:---|:---|:---|:---|:---|:---|
| **RF-01**<br>Funcional | Registro diferenciado de estudiantes (con curso y fecha de nacimiento) y orientadores (con código institucional). | OE1, OE2<br>Sprint 1 | CU-01<br>Tablas `usuario`, `estudiante`, `orientador`, `curso` | `routers/auth.py`<br>`services/auth_service.py`<br>`views/AuthView.vue` | CP-01 a CP-04<br>`test_auth_registro.py`<br>**Aprobado** |
| **RF-02**<br>Funcional | Inicio de sesión seguro con emisión de token JWT (24 h) y rechazo de cuentas inactivas. | OE1, OE3<br>Sprint 1 | CU-02, DS-01<br>Tabla `usuario` | `routers/auth.py`<br>`utils/security.py` | CP-05<br>`test_auth_registro.py`<br>**Aprobado** |
| **RF-03**<br>Funcional | Consulta del perfil autenticado (`/api/auth/me`) y protección de rutas por rol en el navegador. | OE2, OE3<br>Sprint 1 | CU-03, DS-01<br>Guardias Vue Router | `routers/auth.py`<br>`router/index.js` | `test_auth_registro.py`<br>**Aprobado** |
| **RF-04**<br>Funcional | Aplicación digital de los 44 ítems del BFI-44 con guardado progresivo e intento único por estudiante. | OE2, OE3<br>Sprint 2 | CU-04, DS-02<br>Tablas `pregunta`, `evaluacion`, `respuesta` | `routers/evaluacion.py`<br>`views/EvaluacionView.vue` | CP-06, CP-07<br>`test_evaluacion_respuestas.py`<br>**Aprobado** |
| **RF-05**<br>Funcional | Validación de las 44 respuestas completas y cálculo OCEAN con recodificación de los 16 ítems inversos. | OE2, OE3<br>Sprint 2 | CU-05, DS-03<br>Servicio `ocean_scorer` | `services/ocean_scorer.py`<br>`routers/evaluacion.py` | CP-08, CP-09<br>`test_ocean_scorer.py`<br>**Aprobado** |
| **RF-06**<br>Funcional | Generación y consulta del reporte de autoconocimiento con gráfico de radar de cinco ejes e interpretaciones. | OE3<br>Sprint 3 | CU-07<br>Tabla `reporte_vocacional` | `routers/reporte.py`<br>`views/ReporteView.vue` | CP-10<br>`test_reportes.py`<br>**Aprobado** |
| **RF-07**<br>Funcional | Presentación de áreas profesionales exploratorias no deterministas con resguardo de neutralidad ante empates. | OE1, OE3<br>Sprint 3 | CU-07<br>Reglas `get_career_areas` | `routers/reporte.py`<br>`views/ReporteView.vue` | `test_career_areas.py` (29 casos)<br>**Aprobado** |
| **RF-08**<br>Funcional | Panel del orientador con listado de alumnos asignados, contadores resumen y filtros por curso y estado BPM. | OE2, OE3<br>Sprint 4 | CU-08, DS-04<br>Vista Orientador | `routers/orientador.py`<br>`views/OrientadorDashboardView.vue` | `test_orientador_estado.py`<br>**Aprobado** |
| **RF-09**<br>Funcional | Visualización del reporte individual de un estudiante por parte del orientador asignado a su curso. | OE2, OE3<br>Sprint 4 | CU-09, DS-04<br>Control por `curso.orientador_id` | `routers/orientador.py`<br>`views/ReporteView.vue` | CP-11, CP-12<br>`test_reportes.py`<br>**Aprobado** |
| **RF-10**<br>Funcional | Consulta y asignación atómica de cursos sin orientador dentro de un mismo establecimiento escolar. | OE2, OE3<br>Sprint 5 | CU-10, DS-04<br>Tabla `curso` | `routers/orientador.py`<br>(`/cursos/sin-asignar`) | CP-13<br>`test_asignacion_cursos.py`<br>**Aprobado** |
| **RF-11**<br>Funcional | Coordinación de estados del proceso vocacional en Camunda 8 mediante BPMN 2.0 y *workers* asíncronos. | OE2, OE3<br>Sprint 3 |CU-05, CU-06, BPMN<br>Tablas `proceso_bpm`, `bpm_evento` | `services/bpm_service.py`<br>`worker.py` | CP-14, CP-15<br>`test_bpm_delivery.py`<br>**Aprobado** |
| **RNF-01**<br>Rendimiento | Tiempo de respuesta HTTP menor o igual a 3,0 segundos (p95) bajo carga de 30 usuarios concurrentes. | OE4<br>Cierre | Vista de Procesos y Física (Modelo 4+1) | `main.py` / `database.py`<br>`scripts/measure_latency.py` | Prueba de 1.500 solicitudes (p95 = 1,216 s)<br>**Aprobado** |
| **RNF-02**<br>Seguridad | Cifrado irreversible de contraseñas (`Bcrypt`) y control estricto de autorización por roles (`JWT`). | OE1, OE2<br>Sprint 1 | Vista Lógica (Seguridad) | `utils/security.py`<br>`utils/dependencies.py` | CP-01 a CP-05, CP-12<br>**Aprobado** |
| **RNF-03**<br>Mantenibilidad | Cobertura de pruebas automatizadas del backend igual o superior al 80 % del código de aplicación. | OE4<br>Sprints 5–6 | Plan de Calidad y Pruebas | Suite `backend/tests/` (199 pruebas) | Medición `coverage.py` (89,80 %)<br>**Aprobado** |
| **RNF-04**<br>Compatibilidad | Interfaz web responsiva operable en pantallas de escritorio (1440×900) y teléfonos móviles (390×844). | OE2, OE4<br>Sprint 5 | Vista de Desarrollo (SPA Vue 3) | Vistas `.vue` y hojas CSS adaptativas | 34 verificaciones en navegador real<br>**Aprobado** |
| **RNF-05**<br>Fiabilidad | Conservación del reporte en MySQL y reintento automático de mensajes ante caída temporal de Camunda 8. | OE2, OE3<br>Sprints 3–5 | Tabla `bpm_evento` (Outbox) | `services/bpm_service.py` | CP-14 (`test_bpm_delivery.py`)<br>**Aprobado** |
| **RNF-06**<br>Usabilidad | Evaluación de usabilidad percibida (meta ≥ 85 %) con instrumento documentado sobre muestra de usuarios. | OE4<br>Cierre | Plan de Pruebas (Escala SUS) | Protocolo en `docs/validacion_mvp.md` | Pauta lista; aplicación a muestra pendiente<br>**Pendiente** |

## Arquitectura de software a implementar (Modelo 4+1 Vistas de Kruchten)

Para documentar de manera integral la arquitectura de software de **Vócalis**, se aplica el **Modelo de 4+1 Vistas de Kruchten** (1995), describiendo la solución desde cinco perspectivas complementarias: vista lógica, vista de procesos, vista de desarrollo, vista física y vista integradora de escenarios.

![Modelo Arquitectónico 4+1 Vistas de Kruchten](images2.0/image24.png)

*Figura 18: Síntesis del Modelo 4+1 Vistas de Kruchten aplicado a la plataforma Vócalis.*

### 1. Vista Lógica (Componentes y Dominio)

La vista lógica organiza el sistema en capas con responsabilidades bien delimitadas entre la interfaz de usuario, el enrutamiento HTTP, los servicios de negocio y el acceso a datos:

![Diagrama de Componentes de Software](images2.0/image16.png)

*Figura 19: Diagrama de componentes de software e integración entre capas de Vócalis.*

1. **Capa de Presentación SPA (`src/`):** Componentes y vistas en Vue.js 3 que consumen la API REST a través de una instancia centralizada de Axios (`services/http.js`), adjuntando automáticamente el token Bearer JWT y gestionando el cierre de sesión ante respuestas HTTP 401.
2. **Capa de Controladores REST (`backend/app/routers/`):** Cuatro routers modulares (`auth.py`, `evaluacion.py`, `reporte.py` y `orientador.py`) encargados de validar esquemas de entrada/salida con Pydantic v2 y verificar permisos mediante dependencias inyectadas (`Depends(get_current_user)`).
3. **Capa de Servicios de Negocio (`backend/app/services/`):**
   - `ocean_scorer.py`: Módulo de cálculo puro sin acoplamiento a base de datos; aplica la inversión `6 - respuesta` sobre los 16 ítems inversos del BFI-44, promedia cada dimensión (rango 1,0 a 5,0) y entrega su valor normalizado entre 0,0 y 1,0.
   - `bpm_service.py`: Gestiona el inicio de instancias y publicación de mensajes por gRPC hacia Camunda 8, apoyado en la tabla `bpm_evento` para reintentos automáticos con espera exponencial.
   - `auth_service.py`: Resuelve la creación atómica de cuentas por rol, la verificación de contraseñas con `Bcrypt` y la obtención del nombre completo según perfil.
4. **Capa de Persistencia ORM (`backend/app/models/`):** Diez entidades declarativas en SQLAlchemy 2.0 asíncrono (`AsyncSession`) que imponen claves foráneas, restricciones únicas (`uq_evaluacion_estudiante`, curso único por establecimiento) y validación de rango Likert (`1` a `5`).

### 2. Vista de Procesos (Concurrencia y Sincronización BPM)

La vista de procesos aborda la ejecución asíncrona, el ciclo de vida del servicio y el control de concurrencia sobre los datos:

1. **Ejecución Asíncrona No Bloqueante (ASGI / Uvicorn):** El backend opera sobre el bucle de eventos `asyncio` de Python. Tanto las consultas SQL mediante `aiomysql` como la comunicación gRPC con Zeebe se ejecutan de forma asíncrona (`await`), permitiendo atender decenas de solicitudes simultáneas sin bloquear el proceso principal.
2. **Tareas de Segundo Plano en el Ciclo de Vida (`lifespan`):** Al iniciar FastAPI (`main.py`), el gestor de contexto levanta dos corrutinas supervisadas:
   - `start_worker()`: Conecta el cliente `pyzeebe` con Camunda 8 y mantiene en escucha los *workers* de las tareas `calcular-ocean`, `generar-reporte` y `notificar-orientador`.
   - `retry_pending_events()`: Revisa periódicamente cada 5 segundos la tabla `bpm_evento` para reenviar mensajes pendientes hacia Zeebe aplicando retroceso exponencial (hasta 300 segundos entre intentos).
3. **Control de Concurrencia en MySQL InnoDB:** El guardado y envío de respuestas bloquea de forma exclusiva el registro de evaluación del alumno (`SELECT ... FOR UPDATE`), impidiendo intentos duplicados o escrituras cruzadas. Por su parte, el despachador de eventos emplea `FOR UPDATE SKIP LOCKED` para procesar entregas pendientes sin contención.

### 3. Vista de Desarrollo (Organización Modular del Código)

El repositorio del proyecto separa claramente el código del servidor backend, la aplicación cliente frontend, el modelo BPMN ejecutable y los artefactos de prueba y migración, tal como se resume en la siguiente tabla:

| Ruta / Paquete | Capa Tecnológica | Responsabilidad y Contenido Principal |
|:---|:---|:---|
| `backend/app/models/` | Persistencia (SQLAlchemy 2.0) | Definición de las 10 tablas relacionales (`usuario`, `estudiante`, `orientador`, `curso`, `evaluacion`, `pregunta`, `respuesta`, `reporte`, `proceso_bpm`, `bpm_evento`). |
| `backend/app/routers/` | API REST (FastAPI) | Endpoints agrupados por dominio: `/api/auth`, `/api/evaluacion`, `/api/orientador` y generación de estructura `ReporteOut`. |
| `backend/app/schemas/` | Validación (Pydantic v2) | Contratos tipados de entrada y salida HTTP, validadores de fecha ISO, rango entero Likert y sanitización de errores. |
| `backend/app/services/` | Dominio y Orquestación | Cálculo BFI-44 (`ocean_scorer.py`), cliente gRPC y outbox (`bpm_service.py`), y lógica de registro/autenticación (`auth_service.py`). |
| `backend/alembic/` | Migraciones de Esquema | Historial versionado e idempotente de cambios DDL sobre MySQL (`20260922` y `20260924`). |
| `backend/tests/` | Aseguramiento de Calidad | Suite automatizada con 199 pruebas unitarias, de integración, seguridad y concurrencia en Pytest. |
| `src/views/` y `src/components/` | Interfaz Web (Vue.js 3) | Vistas SPA (`HomeView`, `AuthView`, `EstudianteDashboardView`, `EvaluacionView`, `ReporteView`, `OrientadorDashboardView`) y navegación compartida. |
| `src/router/` y `src/services/` | Navegación y Cliente HTTP | Rutas protegidas por rol (`index.js`), interceptor JWT en Axios (`http.js`) y servicios de consumo de API. |
| `bpmn/` | Proceso de Negocio | Archivo estándar BPMN 2.0 `evaluacion-vocacional.bpmn` desplegado sobre Camunda 8. |

### 4. Vista Física (Despliegue e Infraestructura Contenedorizada)

La vista física define la disposición de nodos de ejecución, puertos de red y contenedores que soportan la operación local e institucional de la plataforma. El entorno de desarrollo principal fue configurado sobre CachyOS (Arch Linux) y compatibilizado también con Windows 10/11 mediante Docker Compose:

![Diagrama de Despliegue Inicial en Servidor de Aplicaciones](images2.0/image17.png)

*Figura 20: Esquema general de nodos del entorno de servidor de aplicaciones, base de datos y motor BPM.*

![Vista Física Detallada de Contenedores y Puertos](images2.0/image28.png)

*Figura 21: Topología detallada de despliegue con proxy Vite, FastAPI/Uvicorn y contenedores Docker Compose.*

Para facilitar las pruebas desde teléfonos móviles conectados a la misma red local Wi-Fi sin exponer directamente el servidor de aplicaciones ni relajar las políticas CORS, Vite opera en el puerto `5173` actuando como *reverse proxy* de las rutas `/api` hacia Uvicorn en `127.0.0.1:8000`, mientras MySQL (`3306`), Zeebe (`26500`), Elasticsearch (`9200`) y Camunda Operate (`8081`) se ejecutan de manera aislada en contenedores Docker.

### 5. Vista de Escenarios (+1 / Casos Integradores)

La quinta vista valida la coherencia de las cuatro vistas previas recorriendo dos escenarios transversales del MVP:

1. **Escenario Integrado de Evaluación y Seguimiento:** Un estudiante accede desde su navegador web o móvil (Vista Física), inicia sesión con JWT (Vista Lógica), responde los 44 ítems del BFI-44 en la interfaz Vue.js 3 (Vista de Desarrollo) y envía su evaluación. FastAPI registra en una única transacción ACID el reporte y el evento de salida (Vista de Procesos), Zeebe ejecuta los tres *workers* hasta marcar `reporte_listo` y el orientador visualiza de inmediato el resultado en su panel de curso.
2. **Escenario de Tolerancia a Caída Temporal del Motor BPM:** Si el contenedor de Camunda Zeebe no se encuentra disponible en el instante en que un alumno finaliza su cuestionario, MySQL confirma igualmente las 44 respuestas y el reporte vocacional sin pérdida de información. El evento queda almacenado con estado `pendiente` en `bpm_evento` y el bucle asíncrono de FastAPI reintenta su publicación automáticamente hasta restablecer la sincronización completa del proceso.

## Planes de gestión del proyecto

En concordancia con la metodología híbrida adoptada y las observaciones académicas del Hito 2, a continuación se desarrollan de manera contextualizada los seis planes de gestión que gobernaron el desarrollo, control y verificación del proyecto **Vócalis**, detallando procedimientos, responsables, mecanismos de control y evidencias concretas de aplicación.

### 1. Plan de Gestión de Calidad

#### A. Estándares y Criterios de Calidad
El aseguramiento de calidad se estructuró tomando como referencia las características del estándar **ISO/IEC 25010** pertinentes al MVP (adecuación funcional, fiabilidad transaccional, eficiencia de desempeño, seguridad de acceso y mantenibilidad), junto con el cumplimiento de **PEP 8** en Python y **ESLint** en el código Vue.js 3.

#### B. Métricas de Control y Evidencias Obtenidas
| Métrica de Calidad | Umbral Comprometido | Resultado Verificado | Mecanismo de Control y Evidencia |
|:---|:---|:---|:---|
| **Cobertura de Pruebas Backend** | Igual o superior a 80,0 % | **89,80 %** combinada | Medición con `coverage.py` sobre `backend/app` (91,33 % en líneas y 82,55 % en ramas). |
| **Aprobación Funcional e Integración** | 100 % de casos críticos | **199 de 199 aprobadas** | Ejecución automatizada con `pytest` (189 pruebas generales + 10 pruebas de concurrencia en MySQL). |
| **Tiempo de Respuesta API (p95)** | Máximo 3,0 s con 30 usuarios | **1,216 s** (máx. 1,276 s) | Prueba de carga de 1.500 solicitudes HTTP ejecutada mediante `backend/scripts/measure_latency.py`. |
| **Calidad Estática y Compilación** | 0 errores de sintaxis o build | **0 errores** | Revisión estática con ESLint, esquemas tipados Pydantic v2 y construcción limpia con `vite build`. |

#### C. Responsables y Procedimiento de Revisión
El autor (desarrollador responsable) condicionó el cierre de cada sprint a tres controles obligatorios: validación de contratos de datos en FastAPI, ejecución íntegra de la suite de regresión en Pytest sin fallos ni pruebas omitidas, y verificación visual del flujo entre vistas Vue.js, MySQL y Camunda Operate.

### 2. Plan de Gestión de Cambios

#### A. Procedimiento de Control de Cambios
Para evitar desviaciones de alcance (*scope creep*) o roturas del esquema relacional durante las iteraciones, todo ajuste detectado durante la construcción o a partir de la retroalimentación docente siguió un flujo formal de cinco etapas:

![Procedimiento de Control de Cambios y Migraciones](images2.0/image25.png)

*Figura 22: Flujo de control de cambios apoyado en Git, migraciones Alembic y pruebas de regresión.*

1. **Detección y Registro:** Identificación de un defecto, brecha de seguridad o ambigüedad funcional (por ejemplo, riesgo de doble evaluación por alumno o cursos creados sin orientador).
2. **Análisis de Impacto:** Revisión de las tablas MySQL, rutas REST, vistas frontend y tareas BPMN afectadas por la modificación.
3. **Contraste de Alcance:** Verificación por el autor —en alineación con las observaciones de la profesora guía— de que el cambio fortalece el MVP comprometido sin incorporar módulos excluidos.
4. **Implementación y Migración Segura:** Codificación modular acompañada de su script de migración versionado en Alembic (`upgrade` y `downgrade`), preservando los datos previos.
5. **Verificación de Regresión:** Incorporación de pruebas específicas del cambio y ejecución completa de la suite Pytest antes de consolidar la versión en Git.

#### B. Registro de Cambios Aplicados (Evidencia)
| Código | Cambio Controlado | Motivación Técnica / Funcional | Evidencia en el Repositorio |
|:---|:---|:---|:---|
| **CHG-01** | Restricción de intento único por estudiante | Garantizar la regla de negocio del MVP evitando múltiples evaluaciones paralelas para un mismo alumno. | Migración Alembic `20260922_eval_unique` y pruebas `test_evaluacion_unique_migration.py`. |
| **CHG-02** | Contexto escolar y fecha de nacimiento validada | Permitir asociar cursos por establecimiento y derivar dinámicamente la edad del estudiante. | Migración `20260922_registro_contexto` y validaciones en `schemas/auth.py`. |
| **CHG-03** | Tabla `bpm_evento` (*Transactional Outbox*) | Evitar pérdida de sincronización si Zeebe no responde al finalizar el cuestionario. | Migración `20260924_bpm_outbox`, `bpm_service.py` y `test_bpm_delivery.py`. |
| **CHG-04** | Lenguaje neutral en sugerencias de reporte | Atender observación docente del Hito 2 para evitar interpretaciones vocacionales deterministas. | Ajuste de textos y reglas en `ReporteView.vue`, `reporte.py` y `test_career_areas.py`. |

### 3. Plan de Gestión de Comunicaciones

El plan establece los canales, formatos, frecuencias y responsables de comunicación entre los actores involucrados en el proyecto académico:

| Interesado | Rol | Información Entregada / Recibida | Canal y Formato | Frecuencia |
|:---|:---|:---|:---|:---|
| **Profesora Guía (Lismary Cubillan)** | Supervisión y evaluación metodológica | Entregas de Hito, avances de arquitectura, trazabilidad, planes de gestión y correcciones aplicadas. | Plataforma institucional UNAB, informes en formato Word y sesiones de retroalimentación. | Por Hito académico / Seguimiento periódico |
| **Autor (José Miguel Piña)** | Planificación, diseño, construcción y pruebas | Pautas de rúbrica, observaciones docentes, registro de commits y bitácora semanal de avance. | Repositorio Git, documentación técnica en `docs/` y control de sprints. | Continua / Semanal |
| **Orientadores Escolares (Muestra)** | Usuarios de validación del seguimiento | Demostración guiada del panel de cursos, lectura de reportes y pauta de usabilidad. | Interfaz web responsiva y formulario estructurado de evaluación. | Fase de cierre y validación |
| **Estudiantes de Media (Muestra)** | Usuarios de validación del cuestionario | Instrucciones de uso ético del BFI-44, aplicación de los 44 ítems y lectura del reporte. | Aplicación web en computador o teléfono móvil en red local. | Fase de cierre y validación |

### 4. Plan de Gestión del Alcance

#### A. Estructura de Desglose del Trabajo (EDT / WBS)
El trabajo total requerido para completar el proyecto se descompuso en cinco paquetes principales verificables:

![Estructura de Desglose del Trabajo (EDT / WBS)](images2.0/image26.png)

*Figura 23: Estructura de Desglose del Trabajo (EDT / WBS) del proyecto Vócalis.*

#### B. Control de Línea Base e Inclusiones / Exclusiones del MVP
- **Alcance Incluido y Verificado:** Autenticación JWT diferenciada por rol, cuestionario digital BFI-44 en español con autoguardado e intento único, cálculo de las cinco dimensiones OCEAN con 16 reactivos inversos, reporte con gráfico de radar SVG y áreas exploratorias neutrales, panel de seguimiento y asignación de cursos para el orientador, y orquestación BPMN en Camunda 8 con respaldo transaccional.
- **Exclusiones Controladas:** Se mantuvieron formalmente fuera del MVP la exportación automática del reporte a archivo PDF y los modelos predictivos longitudinales, registrándolos como líneas de evolución futura para concentrar el esfuerzo de ingeniería en la confiabilidad, seguridad y trazabilidad del flujo principal.

### 5. Plan de Gestión del Cronograma

#### A. Programación por Iteraciones (Abril – Noviembre 2026)
El cronograma maestro articula las etapas definidas en el Capítulo III con las entregas incrementales ejecutadas en los seis sprints de desarrollo y la fase de cierre documental:

![Cronograma Maestro de Ejecución por Iteraciones](images2.0/image27.png)

*Figura 24: Cronograma de ejecución por iteraciones del proyecto Vócalis (abril – noviembre de 2026).*

#### B. Seguimiento y Control de Desviaciones
El control temporal se realizó contrastando al término de cada sprint los incrementos operativos contra los objetivos específicos (`OE1` a `OE4`):
- **Abril 2026:** Levantamiento curricular y definición de línea base de requerimientos completados según lo previsto.
- **Mayo a Julio 2026 (Sprints 1 a 3):** La sobrecarga técnica de integrar comunicación asíncrona gRPC con Camunda 8 se absorbió dentro del Sprint 3 incorporando el patrón *Transactional Outbox*, evitando retrasar la construcción del reporte y el panel del orientador.
- **Julio a Septiembre 2026 (Sprints 4 a 6):** Se completaron el panel del orientador, el reclamo de cursos sin asignar y la corrección de bloqueos concurrentes en MySQL.
- **Octubre a Noviembre 2026 (Cierre):** Consolidación de pruebas de carga (1.500 solicitudes), incorporación exhaustiva de las correcciones del Hito 2 en la memoria y preparación del cierre final.

### 6. Plan de Pruebas

#### A. Niveles de Prueba, Entorno y Responsables
La estrategia de verificación fue diseñada y ejecutada por el autor combinando cinco niveles complementarios:
1. **Pruebas Unitarias:** Comprobación aislada de la aritmética del BFI-44 (`ocean_scorer.py`), recodificación de los 16 ítems inversos y reglas de neutralidad de áreas exploratorias (`get_career_areas`).
2. **Pruebas Funcionales y de Autorización API:** Verificación de los diez casos de uso (`CU-01` a `CU-10`), validaciones Pydantic HTTP 422, expiración/revocación JWT y aislamiento de reportes entre orientadores (HTTP 403/404).
3. **Pruebas de Integración y Resiliencia BPM:** Validación del flujo completo entre FastAPI, base de datos relacional y Camunda 8, simulando caídas y reconexiones del broker Zeebe.
4. **Pruebas de Concurrencia y Rendimiento en MySQL 8.0:** Ejecución sobre contenedor real MySQL 8.0 InnoDB para comprobar envíos simultáneos sin duplicados y medir tiempos de respuesta bajo 30 usuarios concurrentes.
5. **Protocolo de Evaluación de Usabilidad (OE4 / RNF-06):** Para evaluar la meta de satisfacción igual o superior al 85 % en la muestra definida de 5 participantes (estudiantes y orientadores), se estableció el instrumento estándar **System Usability Scale (SUS)** de 10 afirmaciones Likert (1 a 5), cuyo puntaje global en escala de 0 a 100 se calcula sumando `(respuesta - 1)` en los ítems impares y `(5 - respuesta)` en los ítems pares, multiplicando el total por `2,5`. El protocolo e instructivo se encuentran formalizados en `docs/validacion_mvp.md` para su aplicación empírica en el cierre del período.

## Casos de prueba específicos y evidencia de ejecución

Con el propósito de evidenciar el cumplimiento del **Plan de Pruebas** y del **Objetivo Específico 4 (OE4)**, a continuación se detallan los quince casos de prueba representativos que verifican el registro de usuarios, la aplicación del cuestionario BFI-44, el cálculo psicométrico OCEAN, la generación de reportes, el seguimiento por parte del orientador y la sincronización con Camunda 8.

### 1. Catálogo de Casos de Prueba Ejecutados

| ID y Módulo | Escenario de Prueba | Entrada y Acción Ejecutada | Resultado Esperado | Evidencia Real Obtenida | Estado |
|:---|:---|:---|:---|:---|:---|
| **CP-01**<br>Registro | Alta exitosa de estudiante con curso y edad derivada | `POST /api/auth/register` con rol `estudiante`, fecha `2008-05-15`, colegio y curso `4° Medio A`. | HTTP 200; creación atómica de usuario, curso y estudiante. | Registro persistido; edad calculada correctamente (`test_auth_registro.py`). | **Aprobado** |
| **CP-02**<br>Registro | Rechazo de correo electrónico duplicado | Intento de registro utilizando un correo ya existente en `usuario`. | HTTP 409 Conflict sin duplicar registros en la base de datos. | HTTP 409 retornado; integridad de tabla intacta (`test_auth_registro.py`). | **Aprobado** |
| **CP-03**<br>Registro | Alta de orientador con código institucional válido | `POST /api/auth/register` con rol `orientador` y código válido del establecimiento. | HTTP 200; cuenta de orientador creada y vinculada a su colegio. | Validación segura del código y creación exitosa (`test_auth_registro.py`). | **Aprobado** |
| **CP-04**<br>Seguridad | Rechazo de orientador con código inválido o vacío | Solicitud de registro de orientador con código erróneo o en blanco. | HTTP 403 Forbidden sin almacenar datos ni filtrar el secreto. | HTTP 403 verificado; base de datos sin cambios (`test_auth_registro.py`). | **Aprobado** |
| **CP-05**<br>Acceso JWT | Bloqueo de inicio de sesión para cuenta inactiva | `POST /api/auth/login` con credenciales correctas pero `is_active = False`. | HTTP 401 Unauthorized denegando la emisión del token JWT. | HTTP 401 confirmado tanto en login como en `/auth/me` (`test_auth_registro.py`). | **Aprobado** |
| **CP-06**<br>Cuestionario | Guardado progresivo de ítem individual BFI-44 | `POST /api/evaluacion/respuesta` enviando `{preguntaId: 1, valor: 4}`. | HTTP 200; crea evaluación `en_progreso` y guarda respuesta con bloqueo de fila. | Respuesta almacenada bajo `FOR UPDATE` (`test_evaluacion_respuestas.py`). | **Aprobado** |
| **CP-07**<br>Cuestionario | Impedimento de edición sobre evaluación cerrada | Envío de nueva respuesta cuando la evaluación del alumno ya está `completada`. | HTTP 400 Bad Request preservando el intento único del MVP. | HTTP 400 retornado; respuestas originales intactas (`test_evaluacion_respuestas.py`). | **Aprobado** |
| **CP-08**<br>Validación | Rechazo de envío final con cuestionario incompleto | `POST /api/evaluacion/enviar` con solo 43 respuestas o ítems fuera de rango 1 a 5. | HTTP 422 indicando conjunto incompleto o valor inválido. | HTTP 422 capturado; no se genera reporte parcial (`test_evaluacion_respuestas.py`). | **Aprobado** |
| **CP-09**<br>Cálculo OCEAN | Exactitud aritmética y recodificación de 16 inversos | Evaluación controlada con puntajes extremos (1 y 5) y neutros (3) en los 44 ítems. | Inversión `6 - valor` en los 16 ítems inversos y normalización exacta entre 0,0 y 1,0. | Puntajes exactos verificados por dimensión (`test_ocean_scorer.py`). | **Aprobado** |
| **CP-10**<br>Reporte | Consulta de reporte propio y neutralidad exploratoria | `GET /api/evaluacion/reporte` por estudiante con evaluación finalizada y caso de empate. | HTTP 200 con 5 dimensiones para radar SVG; `careerAreas = []` si hay empate o perfil neutro. | Estructura `ReporteOut` íntegra y neutralidad validada (`test_reportes.py`, `test_career_areas.py`). | **Aprobado** |
| **CP-11**<br>Orientador | Revisión autorizada de reporte de alumno asignado | `GET /api/orientador/estudiante/{id}/reporte` sobre alumno de un curso propio. | HTTP 200 entregando puntajes, interpretaciones y estado BPM del estudiante. | Consulta exitosa y trazable para acompañamiento (`test_reportes.py`). | **Aprobado** |
| **CP-12**<br>Autorización | Bloqueo de consulta cruzada hacia otro orientador | Orientador solicita reporte de un estudiante perteneciente a otro curso o colegio. | HTTP 403 Forbidden resguardando la privacidad escolar (Ley N° 19.628). | Acceso denegado con HTTP 403 en todos los casos (`test_reportes.py`). | **Aprobado** |
| **CP-13**<br>Cursos | Asignación atómica de curso libre por orientador | Dos solicitudes sobre `POST /api/orientador/cursos/{id}/asignar` para un curso vacante. | El primer orientador obtiene HTTP 200; una solicitud simultánea recibe HTTP 409. | 1 fila actualizada; colisión controlada con HTTP 409 (`test_asignacion_cursos.py`). | **Aprobado** |
| **CP-14**<br>BPM Outbox | Resiliencia ante desconexión temporal de Camunda 8 | Envío definitivo de las 44 respuestas con el gateway gRPC de Zeebe detenido. | El reporte se confirma en MySQL y el evento `completar` queda pendiente para reintento. | Cero pérdida de reportes; reenvío exitoso al reconectar (`test_bpm_delivery.py`). | **Aprobado** |
| **CP-15**<br>Concurrencia | Doble envío simultáneo del mismo estudiante en MySQL | Dos peticiones concurrentes a `/api/evaluacion/enviar` sobre MySQL 8.0 real. | Solo una transacción genera reporte (HTTP 200) y la otra recibe HTTP 400. | Un único reporte y un único evento creados (`test_bpm_mysql.py`). | **Aprobado** |

### 2. Resultados Consolidados de la Suite Automatizada y Prueba de Carga

La ejecución integral de la suite de pruebas backend sobre Python 3 y MySQL 8.0 arrojó **199 pruebas aprobadas, 0 fallidas y 0 omitidas**, alcanzando una cobertura verificada de **89,80 %** sobre el código de aplicación (`backend/app`). Complementariamente, para validar el requerimiento no funcional **RNF-01**, se ejecutó el benchmark automatizado `backend/scripts/measure_latency.py` simulando **30 usuarios concurrentes** realizando el flujo completo de registro, inicio de sesión, respuesta a ítems, envío final y lectura de reporte:

| Indicador de Rendimiento Medido | Criterio de Éxito (RNF-01) | Resultado Obtenido | Estado de Cumplimiento |
|:---|:---|:---|:---|
| **Usuarios simultáneos simulados** | 30 usuarios concurrentes | **30 usuarios concurrentes** | Cumplido |
| **Volumen total de peticiones HTTP** | Ciclo completo de evaluación | **1.500 solicitudes ejecutadas** | Cumplido |
| **Tasa de respuestas exitosas** | 100 % sin errores de servidor (5xx) | **100 % exitosas (0 fallos)** | Cumplido |
| **Latencia en Percentil 95 (p95)** | Menor o igual a 3,000 segundos | **1,216 segundos** (máx. 1,276 s) | **Superado ampliamente** |

Estos resultados demuestran que la arquitectura asíncrona en FastAPI junto con el pool de conexiones de SQLAlchemy 2.0 y los índices de MySQL InnoDB responden en menos de la mitad del tiempo máximo exigido para la operación simultánea de un curso escolar completo.

## Diseño y modelo de la base de datos (DER) y diagrama de clases UML

En atención a las observaciones docentes, a continuación se presenta y explica detalladamente el modelo relacional de datos y el diagrama de clases estructural de **Vócalis**, verificando que las entidades, atributos, relaciones, restricciones y operaciones soportan la totalidad de las funcionalidades comprometidas para el MVP.

### 1. Modelo Entidad-Relación (DER) de la Base de Datos

El esquema persistente en **MySQL 8.0** (motor transaccional **InnoDB**) está compuesto por **diez tablas normalizadas en Tercera Forma Normal (3FN)**, diseñadas para resguardar la integridad referencial, asegurar el intento único de evaluación por estudiante y mantener sincronizado el avance con Camunda 8:

![Diagrama Entidad-Relación (DER) de la Base de Datos](images2.0/image18.png)

*Figura 25: Modelo Entidad-Relación (DER) completo de las 10 tablas implementadas en MySQL 8.0.*

La siguiente tabla sintetiza la responsabilidad, claves y relaciones de cada entidad del modelo de datos:

| Entidad (Tabla MySQL) | Claves y Restricciones Clave | Relaciones | Propósito Funcional en el Sistema |
|:---|:---|:---|:---|
| `usuario` | `PK id`; `UNIQUE email` | `1:1` con `estudiante` u `orientador` | Credenciales unificadas con hash `Bcrypt`, rol (`estudiante` / `orientador`) y vigencia (`is_active`). |
| `estudiante` | `PK id`; `UNIQUE usuario_id`; `FK curso_id` |Pertenece a `curso`; realiza `evaluacion` | Perfil escolar del alumno con nombre completo, `fecha_nacimiento` ISO y edad calculada dinámicamente. |
| `orientador` | `PK id`; `UNIQUE usuario_id` | Supervisa `1:N` registros en `curso` | Perfil profesional con nombre, departamento de orientación y nombre del establecimiento escolar. |
| `curso` | `PK id`; `UNIQUE (establecimiento, nombre)` | Asocia `orientador` (`nullable`) y alumnos | Agrupación académica (ej. `4° Medio A`); admite cursos libres (`orientador_id IS NULL`) para asignación posterior. |
| `evaluacion` | `PK id`; `UNIQUE estudiante_id` (`uq_evaluacion_estudiante`) | `1:N` con `respuesta` y `bpm_evento`; `1:1` con reporte | Registra el intento único del alumno, su estado (`en_progreso`, `completada`) y fecha `completed_at`. |
| `pregunta` | `PK id`; `UNIQUE orden` (1 al 44) | `1:N` hacia `respuesta` | Catálogo inmutable de los 44 ítems en español del BFI-44, su dimensión (`O, C, E, A, N`) e indicador `es_invertida`. |
| `respuesta` | `PK id`; `UNIQUE (evaluacion_id, pregunta_id)` | Vincula `evaluacion` y `pregunta` | Almacena la opción seleccionada con restricción `CHECK (valor >= 1 AND valor <= 5)` para el autoguardado. |
| `reporte_vocacional` | `PK id`; `UNIQUE evaluacion_id` | `1:1` con `evaluacion` | Persiste en columnas nativas `JSON` los puntajes normalizados, textos descriptivos y áreas exploratorias. |
| `proceso_bpm` | `PK id`; `UNIQUE evaluacion_id` | `1:1` con `evaluacion` | Guarda la clave de instancia Zeebe (`process_instance_key`) y la etapa actual mostrada en los paneles. |
| `bpm_evento` | `PK id`; `UNIQUE (evaluacion_id, tipo)`; `UNIQUE message_id` | `N:1` con `evaluacion` | Tabla *Transactional Outbox* que respalda mensajes hacia Camunda 8 con conteo de intentos y `proximo_intento`. |

### 2. Diagrama de Clases UML del Sistema

El diagrama de clases modela la estructura orientada a objetos implementada en Python (modelos SQLAlchemy 2.0 y servicios de dominio), explicitando las enumeraciones tipadas, la multiplicidad de las asociaciones y las operaciones de negocio que materializan los casos de uso:

![Diagrama de Clases UML del Dominio](images2.0/image19.png)

*Figura 26: Diagrama de clases UML del dominio y capa de servicios de la plataforma Vócalis.*

#### Correspondencia entre Clases, Atributos y Operaciones del MVP:
1. **Enumeraciones del Dominio (`RolEnum`, `EstadoEvaluacion`, `DimensionEnum`):** Restringen en tiempo de validación y persistencia los valores admitidos para los roles de acceso, el ciclo de vida de la evaluación y los cinco factores del modelo Big Five (`O`, `C`, `E`, `A`, `N`).
2. **Jerarquía de Identidad (`Usuario`, `Estudiante`, `Orientador`, `Curso`):** `Usuario` encapsula la verificación de contraseña y emisión del token JWT; `Estudiante` expone la propiedad derivada `edad` a partir de `fecha_nacimiento` e inicia o responde su evaluación; `Orientador` agrupa las operaciones de supervisión (`listarEstudiantesAsignados`, `consultarReporteEstudiante`, `listarCursosSinAsignar` y `reclamarCurso`), operando sobre `Curso.asignarOrientador()`.
3. **Núcleo de Evaluación y Reporte (`Evaluacion`, `Pregunta`, `Respuesta`, `ReporteVocacional`):** `Evaluacion` gobierna la colección de hasta 44 objetos `Respuesta` asociados a `Pregunta`, invocando `calcularPuntajesOCEAN()` (implementado en `ocean_scorer.py`) y `generarReporteVocacional()`, mientras `ReporteVocacional.build_reporte_out()` ensambla el contrato de salida consumido tanto por el estudiante como por su orientador.
4. **Coordinación de Proceso (`ProcesoBPM` y `BPMEvento`):** `ProcesoBPM.advance_to()` actualiza de manera monótona e idempotente el estado del flujo ejecutado por los *workers*, en tanto `BPMEvento` respalda la publicación y reintento asíncrono (`dispatch_event` y `retry_pending_events`) hacia el motor Camunda 8.

# CONCLUSIONES Y RECOMENDACIONES

## 1. Conclusiones del Proyecto

El desarrollo del proyecto de título **Vócalis** permitió diseñar, construir y verificar una aplicación web orientada a procesos de negocio (BPM) destinada a resolver la fragmentación informativa y la falta de seguimiento trazable en la orientación vocacional de enseñanza media. Al contrastar el sistema implementado con los objetivos formulados en el Capítulo II, se establecen las siguientes conclusiones:

### Cumplimiento del Objetivo Específico 1 (Análisis y Priorización de Requerimientos)
Se consolidó y priorizó el 100 % de los requerimientos funcionales (`RF-01` a `RF-11`) y no funcionales (`RNF-01` a `RNF-06`) del Producto Mínimo Viable, articulando el marco curricular del Ministerio de Educación de Chile (MINEDUC), los resguardos de privacidad de la Ley N° 19.628 y los criterios éticos de uso del inventario BFI-44. Esta delimitación aseguró desde la base que el software opere como un instrumento de autoconocimiento reflexivo acompañado por el orientador escolar y no como un clasificador determinista de carreras.

### Cumplimiento del Objetivo Específico 2 (Diseño de Arquitectura, Datos y Flujo BPM)
Se estructuró una arquitectura en capas desacoplada y verificable, documentada integralmente mediante las cinco vistas del **Modelo 4+1 de Kruchten**, los diez casos de uso especificados, cuatro diagramas de secuencia, el modelo BPMN 2.0 y un esquema relacional en MySQL 8.0 de diez entidades normalizadas. La incorporación de restricciones de unicidad (`uq_evaluacion_estudiante`) y de la tabla de respaldo transaccional `bpm_evento` garantizó consistencia íntegra entre los datos de evaluación y los estados de Camunda 8.

### Cumplimiento del Objetivo Específico 3 (Construcción e Integración del MVP)
Se implementó en su totalidad el MVP integrando **Vue.js 3**, **FastAPI (Python)**, **MySQL 8.0** y **Camunda 8 (Zeebe)**, logrando:
- Autenticación diferenciada por rol con contraseñas cifradas (`Bcrypt`), tokens `JWT` y revocación inmediata de cuentas inactivas.
- Aplicación paginada de los 44 reactivos del BFI-44 en español con autoguardado progresivo protegido por bloqueos de fila (`FOR UPDATE`).
- Cálculo exacto de las cinco dimensiones OCEAN con recodificación de los 16 ítems inversos (`6 - respuesta`), visualización en gráfico de radar SVG pentagonal y sugerencias exploratorias con resguardo de neutralidad ante empates o perfiles uniformes.
- Panel de gestión para el orientador escolar con métricas dinámicas, filtros por curso y estado BPM, revisión protegida de reportes y asignación atómica de cursos vacantes dentro del establecimiento.

### Cumplimiento del Objetivo Específico 4 (Validación Funcional, de Integración y Rendimiento)
La verificación técnica del sistema demostró el cumplimiento sobresaliente de los umbrales de ingeniería comprometidos:
- **Pruebas automatizadas y cobertura:** Se aprobaron **199 de 199 pruebas automatizadas** en Pytest (0 fallos), alcanzando un **89,80 % de cobertura combinada** en el backend y superando la meta mínima del 80 %.
- **Eficiencia bajo carga concurrente:** Frente a 30 usuarios simultáneos y 1.500 peticiones HTTP ejecutadas, el percentil 95 de tiempo de respuesta fue de **1,216 segundos** (máximo 1,276 s), cumpliendo con amplio margen el criterio de hasta 3,0 segundos.
- **Tolerancia a fallos y preparación de usabilidad:** Se comprobó experimentalmente que la caída temporal del motor Zeebe no provoca pérdida de reportes gracias al reintento automático de eventos, dejando además formalizado el protocolo e instrumento **SUS** para completar la medición empírica de usabilidad con la muestra de 5 usuarios en el cierre final.

## 2. Recomendaciones y Trabajo Futuro

A partir de los aprendizajes técnicos y metodológicos obtenidos durante el proyecto, se proponen cuatro líneas concretas de continuidad:

1. **Aplicación Empírica de la Pauta de Usabilidad (SUS):** Ejecutar las sesiones guiadas previstas con la muestra de estudiantes de enseñanza media y orientadores escolares utilizando el protocolo documentado, registrando los puntajes obtenidos frente al criterio de satisfacción igual o superior al 85 %.
2. **Exportación Institucional de Reportes en PDF:** Incorporar en una siguiente iteración un servicio dedicado de generación de documentos PDF para facilitar el archivo físico o envío institucional de las fichas de reflexión vocacional cuando el establecimiento lo requiera.
3. **Estudio Psicométrico y Baremación Escolar Local:** Colaborar con profesionales de psicología educacional para evaluar la adaptación lingüística y propiedades psicométricas del instrumento específicamente en población chilena de 3.° y 4.° medio, complementando los antecedentes universitarios disponibles (Lara et al., 2021).
4. **Seguimiento Longitudinal Multianual:** Extender el modelo de datos para admitir comparaciones evolutivas entre 3.° y 4.° medio y bitácoras de entrevistas del orientador, enriqueciendo el acompañamiento a lo largo de toda la trayectoria escolar.

# REFERENCIAS BIBLIOGRÁFICAS

Barrick, M. R., Mount, M. K., & Gupta, R. (2003). Meta-analysis of the relationship between the Five-Factor Model of personality and Holland's occupational types. *Personnel Psychology, 56*(1), 45–74. https://doi.org/10.1111/j.1744-6570.2003.tb00143.x

Benet-Martínez, V., & John, O. P. (1998). Los Cinco Grandes across cultures and ethnic groups: Multitrait-multimethod analyses of the Big Five in Spanish and English. *Journal of Personality and Social Psychology, 75*(3), 729–750. https://doi.org/10.1037/0022-3514.75.3.729

Berkeley Personality Lab. (s. f.). *Big Five Inventory (BFI-44)* [Cuestionario e instrucciones de puntuación]. University of California, Berkeley. https://www.ocf.berkeley.edu/~johnlab/docs.php?file=BFI-44.pdf

Biblioteca del Congreso Nacional de Chile. (1999). *Ley N° 19.628 sobre protección de la vida privada*. Ley Chile. https://www.bcn.cl/leychile/navegar?idNorma=141599

Biblioteca del Congreso Nacional de Chile. (2009). *Ley N° 20.370 que establece la Ley General de Educación*. Ley Chile. https://www.bcn.cl/leychile/navegar?idNorma=1006043

Camunda. (s. f.). *Processes and Zeebe architecture*. Camunda 8 Documentation. https://docs.camunda.io/docs/components/concepts/processes/

FastAPI. (s. f.). *FastAPI framework, high performance, easy to learn, fast to code, ready for production*. https://fastapi.tiangolo.com/

John, O. P., & Srivastava, S. (1999). The Big Five trait taxonomy: History, measurement, and theoretical perspectives. En L. A. Pervin & O. P. John (Eds.), *Handbook of personality: Theory and research* (2.ª ed., pp. 102–138). Guilford Press.

Kruchten, P. (1995). The 4+1 view model of architecture. *IEEE Software, 12*(6), 42–50. https://doi.org/10.1109/52.469759

Lara, L., Monje, M. F., Fuster-Villaseca, J., & Dominguez-Lara, S. (2021). Adaptación y validación del Big Five Inventory para estudiantes universitarios chilenos. *Revista Mexicana de Psicología, 38*(2), 83–94.

Larson, L. M., Rottinghaus, P. J., & Borgen, F. H. (2002). Meta-analyses of Big Six Interests and Big Five Personality Factors. *Journal of Vocational Behavior, 61*(2), 217–239. https://doi.org/10.1006/jvbe.2001.1854

Lowman, R. L. (2022). *Career assessment: Integrating interests, abilities, and personality*. American Psychological Association. https://doi.org/10.1037/0000254-000

Ministerio de Educación de Chile. (2019). *Bases Curriculares 3° y 4° año de Educación Media (Decreto Supremo N° 193)*. Unidad de Currículum y Evaluación.

Ministerio de Educación de Chile. (2024). *Taller de orientación: Decisión vocacional y proyecto de vida*. Currículum Nacional. https://www.curriculumnacional.cl/recursos/taller-orientacion-decision-vocacional-proyecto-vida

Pressman, R. S., & Maxim, B. R. (2020). *Software engineering: A practitioner's approach* (9.ª ed.). McGraw-Hill Education.

Project Management Institute. (2021). *A guide to the project management body of knowledge (PMBOK guide)* (7.ª ed.). Project Management Institute.

Schwaber, K., & Sutherland, J. (2020). *The Scrum guide: The definitive guide to Scrum: The rules of the game*. https://scrumguides.org/scrum-guide.html

# GLOSARIO

- **ACID (Atomicity, Consistency, Isolation, Durability):** Conjunto de propiedades transaccionales que garantizan escrituras íntegras y confiables en motores relacionales como MySQL InnoDB.
- **Alembic:** Herramienta de migración y versionamiento incremental de esquemas de bases de datos utilizada junto con SQLAlchemy en Python.
- **API REST (Representational State Transfer):** Interfaz de comunicación cliente-servidor basada en peticiones HTTP sin estado e intercambio de estructuras JSON.
- **ASGI (Asynchronous Server Gateway Interface):** Especificación estándar de interfaz asíncrona entre servidores web Python como Uvicorn y frameworks como FastAPI.
- **Axios:** Librería cliente HTTP basada en promesas utilizada en el frontend Vue.js 3 para consumir los endpoints del backend e inyectar el token de sesión.
- **Bcrypt:** Función criptográfica adaptativa con sal aleatoria empleada para almacenar contraseñas de forma irreversible en la base de datos.
- **BFI-44 (Big Five Inventory de 44 ítems):** Cuestionario de autoinforme compuesto por 44 afirmaciones para describir cinco dimensiones amplias de personalidad (Benet-Martínez & John, 1998; Berkeley Personality Lab, s. f.).
- **BPM (Business Process Management):** Enfoque sistemático para modelar, automatizar, ejecutar y supervisar flujos de procesos de trabajo.
- **BPMN 2.0 (Business Process Model and Notation):** Notación gráfica estándar internacional basada en carriles (*lanes*), tareas y eventos para modelar procesos ejecutables.
- **CachyOS:** Distribución GNU/Linux basada en Arch Linux optimizada en rendimiento, utilizada como sistema operativo principal en el ambiente de desarrollo del proyecto.
- **Camunda 8 (Zeebe):** Plataforma de orquestación de procesos de negocio basada en eventos distribuidos y comunicación gRPC para ejecutar modelos BPMN 2.0 (Camunda, s. f.).
- **Escala Likert:** Escala psicométrica ordinal de respuesta graduada, implementada en el cuestionario de Vócalis con cinco niveles obligatorios de acuerdo (1 a 5).
- **FastAPI:** Framework web asíncrono de Python para el desarrollo de APIs tipadas con validación automática mediante Pydantic y documentación OpenAPI integrada (FastAPI, s. f.).
- **gRPC:** Protocolo de llamadas a procedimientos remotos de alto desempeño sobre HTTP/2 utilizado por el backend para comunicarse con el broker Zeebe de Camunda 8.
- **JWT (JSON Web Token):** Formato estándar de token firmado digitalmente (RFC 7519) empleado para autenticar sesiones y transportar el rol del usuario entre cliente y servidor.
- **MVP (Minimum Viable Product / Producto Mínimo Viable):** Versión funcional acotada del sistema que implementa los módulos esenciales comprometidos bajo criterios verificables de calidad.
- **MySQL 8.0:** Sistema de gestión de bases de datos relacionales utilizado con el motor InnoDB para persistir usuarios, cursos, respuestas, reportes y estados BPM.
- **OCEAN:** Acrónimo en inglés de las cinco dimensiones del modelo Big Five: *Openness* (Apertura a la experiencia), *Conscientiousness* (Responsabilidad), *Extraversion* (Extraversión), *Agreeableness* (Amabilidad) y *Neuroticism* (Neuroticismo).
- **ORM (Object-Relational Mapping):** Técnica que vincula clases del lenguaje Python con tablas relacionales de MySQL mediante SQLAlchemy 2.0.
- **PyZeebe:** Librería asíncrona de Python que permite publicar mensajes y registrar *workers* de servicio contra Camunda 8 Zeebe.
- **SPA (Single Page Application):** Aplicación web de página única que actualiza dinámicamente las vistas en el navegador sin recargar el documento completo.
- **Transactional Outbox:** Patrón de diseño que almacena los eventos dirigidos a un sistema externo (Camunda 8) dentro de la misma transacción relacional de negocio (`bpm_evento`), evitando pérdida de mensajes ante desconexiones.
- **Uvicorn:** Servidor web ASGI ligero de alto rendimiento encargado de ejecutar la aplicación FastAPI.
- **Vue.js 3:** Framework progresivo de JavaScript utilizado junto con Vite y Vue Router para construir las interfaces reactivas del estudiante y del orientador escolar.

# ANEXOS

## Anexo A: Guía de Configuración y Puesta en Marcha del Entorno

### 1. Requisitos del Ambiente de Ejecución
- **Sistema Operativo:** CachyOS / distribuciones GNU/Linux modernas o Windows 10/11 (PowerShell 5.1+).
- **Infraestructura de Contenedores:** Docker Engine y Docker Compose v2 con al menos 8 GB de memoria RAM disponibles (16 GB recomendados para ejecutar simultáneamente Camunda 8 y Elasticsearch).
- **Intérpretes y Herramientas:** Python 3.11 o superior, Node.js 20.19 o superior con `npm`, y Git.

### 2. Parámetros de Configuración del Backend (`backend/.env`)
Previo al inicio del servicio API, se definen las siguientes variables de entorno a partir de la plantilla `backend/.env.example`:

| Variable de Entorno | Propósito en el Sistema | Valor de Referencia en Desarrollo |
|:---|:---|:---|
| `DATABASE_URL` | Cadena de conexión asíncrona hacia MySQL 8.0 (`aiomysql`). | `mysql+aiomysql://vocalis:vocalis_pass@localhost:3306/vocalis_db` |
| `ZEEBE_GATEWAY` | Dirección y puerto gRPC del broker Camunda 8 Zeebe. | `localhost:26500` |
| `JWT_SECRET` | Clave secreta para firma HS256 de tokens de sesión. | Clave alfanumérica privada definida por entorno |
| `JWT_EXPIRATION_HOURS` | Tiempo de vigencia del token JWT emitido al iniciar sesión. | `24` |
| `CORS_ORIGINS` | Lista de orígenes web autorizados para consumir la API REST. | `http://localhost:5173` |
| `ORIENTADOR_REGISTRATION_CODE` | Código institucional requerido para registrar cuentas de orientador. | Secreto institucional del establecimiento |

### 3. Secuencia Operativa de Arranque Local y en Red Wi-Fi
1. **Inicio de contenedores base:** Levantar mediante `docker compose` los servicios `mysql`, `elasticsearch`, `zeebe` y `operate`, verificando que los puertos `3306`, `26500` y `8081` se encuentren operativos.
2. **Preparación de base de datos:** Dentro del entorno virtual de `backend/`, instalar dependencias (`requirements.txt`), aplicar las migraciones vigentes con `alembic upgrade head` y cargar el catálogo inicial de las 44 preguntas del BFI-44 ejecutando `python -m app.seed`.
3. **Ejecución de servicios de aplicación:** Iniciar el backend FastAPI con `uvicorn` en el puerto `8000` y el servidor frontend Vite con `npm run dev` en el puerto `5173`. En equipos Windows, este flujo completo puede ejecutarse directamente mediante `INICIAR_PROYECTO.cmd` (modo escritorio) o `INICIAR_PROYECTO_WIFI.cmd` (modo red local para pruebas desde teléfonos móviles conectados a la misma red Wi-Fi), deteniendo los procesos al finalizar con `DETENER_PROYECTO.cmd`.

## Anexo B: Manual Resumido de Uso — Perfil Estudiante

1. **Registro e ingreso:** Desde la pantalla de acceso, seleccionar la opción de registro con perfil **Estudiante**, completando nombre completo, correo electrónico, contraseña, fecha de nacimiento, establecimiento, nivel (por ejemplo, `4° Medio`) y letra del curso. Posteriormente, iniciar sesión con las credenciales creadas.
2. **Aplicación del cuestionario BFI-44:** En el panel principal del estudiante, presionar **Iniciar Evaluación Vocacional**. Responder las 44 afirmaciones en escala de 1 (*Totalmente en desacuerdo*) a 5 (*Totalmente de acuerdo*). Cada selección se almacena automáticamente ("Respuesta guardada"), permitiendo avanzar por bloques sin perder progreso.
3. **Envío único y lectura del reporte:** Al completar los 44 reactivos, presionar **Finalizar y Enviar Evaluación**. El sistema redirige al reporte de resultados, donde es posible revisar el gráfico de radar de cinco dimensiones, desplegar la descripción de cada factor y consultar áreas profesionales exploratorias para conversar con el orientador escolar.

## Anexo C: Manual Resumido de Uso — Perfil Orientador Escolar

1. **Registro institucional:** En el formulario de registro, elegir **Orientador Escolar**, ingresando nombre completo, correo, contraseña, departamento, establecimiento y el **Código Institucional de Registro** asignado al colegio.
2. **Supervisión de cursos y avance BPM:** Al ingresar al **Panel de Gestión y Monitoreo**, revisar los indicadores superiores (*Alumnos Asignados*, *Flujos en Evaluación* y *Reportes Listos*) y utilizar los filtros por nombre, curso o etapa del flujo BPM para identificar estudiantes pendientes o completados.
3. **Asignación de cursos libres y revisión de reportes:** Si existen cursos del establecimiento sin orientador asignado, reclamarlos desde la sección de cursos disponibles presionando **Asignar a mi cargo**. Para los estudiantes con evaluación finalizada, presionar **Ver Reporte** a fin de consultar su perfil BFI-44 previo a la sesión de orientación.

## Anexo D: Guía de Auditoría del Proceso en Camunda Operate

1. **Ingreso a la consola web:** Con los contenedores activos, abrir `http://localhost:8081` en el navegador e iniciar sesión con las credenciales locales de desarrollo de Camunda Operate (`demo` / `demo`).
2. **Inspección del modelo BPMN:** Seleccionar el proceso desplegado `evaluacion-vocacional` para visualizar en tiempo real el diagrama BPMN 2.0 y la cantidad de instancias ubicadas en espera del cuestionario o finalizadas.
3. **Verificación de variables e incidentes:** Al seleccionar una instancia individual, es posible auditar el identificador correlacionado (`evaluacion_id`), la recepción del mensaje `CuestionarioCompletado` y el paso secuencial por las tareas automáticas `calcular-ocean`, `generar-reporte` y `notificar-orientador`.
