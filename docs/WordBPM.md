**FACULTAD DE INGENIERÍA**

**INGENIERÍA EN COMPUTACIÓN E INFORMÁTICA**

**APLICACIÓN WEB BASADA EN PROCESOS DE NEGOCIO PARA LA GESTIÓN DE LA
ORIENTACIÓN VOCACIONAL Y EL AUTOCONOCIMIENTO EN ESTUDIANTES CHILENOS**

Proyecto de título para optar al título de Ingeniero en Computación e
Informática

**Autor**

**José Miguel Piña Benítez**

**PROFESOR GUÍA**

**Lismary Alejandra Cubillan Aizpurua**

**SANTIAGO, CHILE**

**2025**

**FACULTAD DE INGENIERÍA**

**INGENIERÍA EN COMPUTACIÓN E INFORMÁTICA**

**DECLARACIÓN DE ORIGINALIDAD Y PROPIEDAD**

Yo, José Miguel Piña Benítez, declaro por este medio que el trabajo de
titulación presentado para su defensa y evaluación es original; las
fuentes, herramientas y aplicaciones utilizadas que contribuyeron a la
investigación realizada están debidamente citadas en el texto y
acreditadas en el apartado de las referencias, conforme con los
requisitos que establece el estilo bibliográfico APA 7.0 y respetando
los aspectos que conciernen a la propiedad intelectual.

Por lo tanto, ante cualquier falta de integridad académica encontrada y
que atente contra la Ley N°17.336 de Propiedad Intelectual, se asume la
responsabilidad que representa para tal efecto, dejando constancia de
ello, en la ciudad de Santiago

> Facultad de Ingeniería
>
> Escuela Computación e Informática
>
> Título del trabajo: Aplicación web basada en procesos de negocio para
> la gestión de la orientación vocacional y el autoconocimiento en
> estudiantes chilenos

**Nombre y firma del autor**

**AGRADECIMIENTOS**

Quisiera expresar mi más profundo agradecimiento y afecto a mi profesora
guía, Lismary Alejandra Cubillan Aizpurua, por sus valiosas
retroalimentaciones, directrices y por su inagotable paciencia para
guiar el desarrollo de este proyecto, permitiéndome estructurar una
propuesta metodológica robusta y de alto estándar académico.

Asimismo, agradezco a la Facultad de Ingeniería de la Universidad Andrés
Bello por brindarme las herramientas conceptuales y técnicas necesarias
para afrontar los desafíos del desarrollo de software moderno y la
ingeniería de procesos.

**ÍNDICE GENERAL**

# Tabla de contenido {#tabla-de-contenido .TOC-Heading}

[RESUMEN EJECUTIVO [v](#_Toc232975646)](#_Toc232975646)

[Objetivo y Pregunta inicial [v](#_Toc232975647)](#_Toc232975647)

[Metodología [vi](#_Toc232975648)](#_Toc232975648)

[Resultados Obtenidos [vi](#_Toc232975649)](#_Toc232975649)

[II. CAPÍTULO I: INTRODUCCIÓN
[1](#capítulo-i-introducción)](#capítulo-i-introducción)

[1.1 Introducción [1](#introducción)](#introducción)

[1.2 Importancia de resolver el problema
[1](#importancia-de-resolver-el-problema)](#importancia-de-resolver-el-problema)

[1.3 Breve discusión bibliográfica
[2](#breve-discusión-bibliográfica)](#breve-discusión-bibliográfica)

[1.4 Contribución del trabajo
[2](#contribución-del-trabajo)](#contribución-del-trabajo)

[1.5 Trabajo a realizar en el proyecto
[2](#trabajo-a-realizar-en-el-proyecto)](#trabajo-a-realizar-en-el-proyecto)

[1.6 Organización y presentación de este trabajo
[3](#organización-y-presentación-de-este-trabajo)](#organización-y-presentación-de-este-trabajo)

[III. CAPÍTULO II: IDENTIFICACIÓN DEL PROBLEMA / OPORTUNIDAD
[4](#capítulo-ii-identificación-del-problema-oportunidad)](#capítulo-ii-identificación-del-problema-oportunidad)

[2.1 Presentación y fundamentación del problema
[4](#presentación-y-fundamentación-del-problema)](#presentación-y-fundamentación-del-problema)

[El núcleo de la problemática radica en los desafíos que experimentan
los jóvenes chilenos para decidir su futuro profesional, los cuales se
ven acentuados por ciertas brechas en la actualización metodológica y
tecnológica de los sistemas de apoyo actuales. La falta de un
acompañamiento continuo genera elecciones reactivas bajo plazos
limitados o presiones del medio ambiente social, derivando en
insatisfacción vocacional o posible deserción temprana en las aulas
universitarias. [4](#_Toc232975659)](#_Toc232975659)

[2.2 Descripción de problemas / oportunidades de mejora
[4](#descripción-de-problemas-oportunidades-de-mejora)](#descripción-de-problemas-oportunidades-de-mejora)

[2.3 Identificación cuantitativa de problemas (Diagrama de Ishikawa)
[4](#identificación-cuantitativa-de-problemas-diagrama-de-ishikawa)](#identificación-cuantitativa-de-problemas-diagrama-de-ishikawa)

[2.4 Objetivo general [5](#objetivo-general)](#objetivo-general)

[2.5 Objetivos específicos y métricas
[6](#objetivos-específicos-y-métricas)](#objetivos-específicos-y-métricas)

[2.6 Alcance del Proyecto y Definición del MVP
[7](#alcance-del-proyecto-y-definición-del-mvp)](#alcance-del-proyecto-y-definición-del-mvp)

[IV. CAPÍTULO III: METODOLOGÍA
[8](#capítulo-iii-metodología)](#capítulo-iii-metodología)

[3.1 Metodología de Desarrollo Híbrida
[8](#metodología-de-desarrollo-híbrida)](#metodología-de-desarrollo-híbrida)

[3.2 Herramientas y Ambiente de Desarrollo
[8](#herramientas-y-ambiente-de-desarrollo)](#herramientas-y-ambiente-de-desarrollo)

[3.3 Descripción general de la propuesta de solución (Arquitectura
Macro)
[9](#descripción-general-de-la-propuesta-de-solución-arquitectura-macro)](#descripción-general-de-la-propuesta-de-solución-arquitectura-macro)

[3.4 Planes de Gestión (Riesgos, Calidad y Pruebas)
[10](#planes-de-gestión-riesgos-calidad-y-pruebas)](#planes-de-gestión-riesgos-calidad-y-pruebas)

[3.5 Cronograma del Proyecto (Planificación de Sprints)
[10](#cronograma-del-proyecto-planificación-de-sprints)](#cronograma-del-proyecto-planificación-de-sprints)

[3.6 Prototipo (Diseño de Interfaces y Flujo de Navegación)
[11](#prototipo-diseño-de-interfaces-y-flujo-de-navegación)](#prototipo-diseño-de-interfaces-y-flujo-de-navegación)

[3.6.1 Pantalla de Login y Registro Centralizado
[12](#pantalla-de-login-y-registro-centralizado)](#pantalla-de-login-y-registro-centralizado)

[3.6.2 Pantalla del Panel Principal del Estudiante (Dashboard)
[13](#pantalla-del-panel-principal-del-estudiante-dashboard)](#pantalla-del-panel-principal-del-estudiante-dashboard)

[3.6.3 Pantalla del Cuestionario Big Five (BFI-44)
[14](#pantalla-del-cuestionario-big-five-bfi-44)](#pantalla-del-cuestionario-big-five-bfi-44)

[3.6.4 Pantalla de Reporte Vocacional Enriquecido
[15](#pantalla-de-reporte-vocacional-enriquecido)](#pantalla-de-reporte-vocacional-enriquecido)

[3.6.5 Pantalla del Panel de Administración del Orientador
[18](#pantalla-del-panel-de-administración-del-orientador)](#pantalla-del-panel-de-administración-del-orientador)

[[18](#section)](#section)

[V. CAPÍTULO IV: DISCUSIÓN DE RESULTADOS
[19](#capítulo-iv-discusión-de-resultados)](#capítulo-iv-discusión-de-resultados)

[4.1 Ingeniería de Requerimientos y Casos de Uso
[19](#ingeniería-de-requerimientos-y-casos-de-uso)](#ingeniería-de-requerimientos-y-casos-de-uso)

[[20](#_Toc232975680)](#_Toc232975680)

[4.2 Espacios para Modelos de Procesos y Datos de Próxima Incorporación
[21](#espacios-para-modelos-de-procesos-y-datos-de-próxima-incorporación)](#espacios-para-modelos-de-procesos-y-datos-de-próxima-incorporación)

[4.2.1 Diagrama de Procesos BPMN Completo (Orquestación Camunda 8)
[21](#diagrama-de-procesos-bpmn-completo-orquestación-camunda-8)](#diagrama-de-procesos-bpmn-completo-orquestación-camunda-8)

[4.2.2 Diagrama Entidad-Relación (DER) de la Base de Datos
[22](#diagrama-entidad-relación-der-de-la-base-de-datos)](#diagrama-entidad-relación-der-de-la-base-de-datos)

[4.2.3 Diagrama de Clases UML del Sistema
[23](#diagrama-de-clases-uml-del-sistema)](#diagrama-de-clases-uml-del-sistema)

[4.2.4 Diagrama de Componentes y Despliegue Físico
[24](#diagrama-de-componentes-y-despliegue-físico)](#diagrama-de-componentes-y-despliegue-físico)

[**REFERENCIAS BIBLIOGRÁFICAS** [25](#_Toc232975686)](#_Toc232975686)

[GLOSARIO (si aplica) [26](#glosario)](#glosario)

**\**

[]{#_Toc232975646 .anchor}**RESUMEN EJECUTIVO\
\
Presentación del problema\**
El sistema educativo chileno enfrenta desafíos en la orientación
vocacional de estudiantes que se encuentran próximos a egresar de la
enseñanza media. En muchos casos, los jóvenes deben tomar decisiones
académicas y profesionales con un nivel limitado de autoconocimiento
respecto de sus intereses, preferencias y características personales,
mientras que los mecanismos de orientación disponibles suelen variar
significativamente entre establecimientos educacionales.

La ausencia de procesos estandarizados que integren herramientas de
apoyo al autoconocimiento dificulta el seguimiento y la trazabilidad de
las acciones de orientación vocacional, limitando la capacidad de los
establecimientos para acompañar de manera consistente a los estudiantes
durante la toma de decisiones.

Ante este escenario, surge la siguiente pregunta de investigación: ¿De
qué manera una solución tecnológica basada en la gestión de procesos de
negocio (BPM), apoyada por herramientas de evaluación de personalidad,
puede optimizar, estandarizar y otorgar trazabilidad al proceso de
orientación vocacional escolar?

[]{#_Toc232975647 .anchor}**Objetivo y Pregunta inicial\**
Para responder a esta interrogante, el proyecto plantea como objetivo
general desarrollar una aplicación web interactiva basada en BPM para la
gestión de los procesos de orientación vocacional y autoconocimiento,
resolviendo de manera directa la ausencia de herramientas digitales
centralizadas y de métricas científicas transferibles en los
establecimientos.

[]{#_Toc232975648 .anchor}**Metodología\**
Metodológicamente, se implementó un enfoque híbrido que combina las
buenas prácticas de la guía PMBOK para la gestión formal del proyecto
(riesgos, calidad y cronograma) con el marco ágil Scrum para el
desarrollo iterativo del producto en Sprints de tres semanas. El stack
tecnológico de código abierto seleccionado está compuesto por FastAPI
(Python 3.11) en el backend, Vue.js 3 en el frontend, MySQL 8.0 para la
persistencia de datos relacionales y el motor Camunda Platform 8 para la
orquestación automatizada de los flujos bajo la notación BPMN. El
diagnóstico psicométrico se estructuró a través del instrumento
científico validado BFI-44 (Big Five Inventory).

[]{#_Toc232975649 .anchor}**Resultados Obtenidos\**
Como resultado, se construyó un Producto Mínimo Viable (MVP)
completamente funcional que automatiza el registro de usuarios, la
ejecución y almacenamiento del test de 44 ítems, y el cálculo inmediato
de las cinco dimensiones de la personalidad (OCEAN). El sistema genera
un reporte vocacional enriquecido con gráficos de radar y sugerencias de
afinidad profesional alineadas al estudiante, centralizando toda la
información en un panel de seguimiento en tiempo real para el
orientador.

**Conclusiones y recomendaciones**

En conclusión, el proyecto evidencia el potencial de la automatización
mediante BPM para mejorar la gestión de los procesos de orientación
vocacional escolar, reduciendo tareas administrativas manuales y
proporcionando trazabilidad sobre las actividades realizadas por
estudiantes y orientadores. Los resultados obtenidos mediante el MVP
desarrollado sugieren que este enfoque puede contribuir a una gestión
más estructurada y centralizada del proceso de acompañamiento
vocacional.

**Palabras Clave:** Gestión de Procesos de Negocio (BPM), Orientación
Vocacional, Modelo Big Five (OCEAN), Aplicación Web, Camunda.

# CAPÍTULO I: INTRODUCCIÓN

## 1.1 Introducción

La transición desde la educación media hacia la educación superior o el
mundo laboral representa uno de los hitos más críticos y estresantes en
la vida de los jóvenes chilenos. En el contexto actual, la elección de
una carrera profesional no solo define el futuro económico del
individuo, sino también su sentido de propósito y realización personal.
Sin embargo, el sistema educativo nacional enfrenta un desafío
estructural: muchos estudiantes egresan de cuarto medio con dudas
respecto a sus opciones académicas y profesionales, asociado a múltiples
factores, entre ellos el limitado acceso a procesos sistemáticos de
orientación vocacional y autoconocimiento.

El problema se ubica específicamente en la etapa de formación
secundaria, donde la orientación vocacional suele ser tratada como un
proceso administrativo anexo y no como un eje central del desarrollo del
estudiante. Esta desconexión genera que la toma de decisiones sea
reactiva y basada en presiones externas, en lugar de ser un proceso
reflexivo y basado en datos reales sobre las habilidades y rasgos
intrínsecos del joven.

## 1.2 Importancia de resolver el problema

Abordar las deficiencias de la orientación vocacional en Chile es
fundamental para optimizar los recursos del sistema educativo y
contribuir a una toma de decisiones académicas más informada en la
educación superior que se genera por decisiones desinformadas o
influenciadas por el entorno social y familiar. Al automatizar la
entrega de información y las evaluaciones de personalidad basadas en
instrumentos psicométricos validados, se reduce de manera considerable
el procesamiento manual de encuestas por parte de los departamentos de
orientación escolar, permitiendo a los orientadores y docentes enfocar
sus esfuerzos en el acompañamiento humano personalizado de los casos de
mayor complejidad.

## 1.3 Breve discusión bibliográfica

Según la literatura educativa contemporánea, la orientación no debe
limitarse a la mera entrega informativa de mallas curriculares y ofertas
académicas, sino que debe constituir un proceso continuo de
autoconocimiento en el cual el estudiante identifique con precisión sus
intereses y aptitudes individuales. Desde la perspectiva tecnológica,
las aplicaciones web ofrecen marcadas ventajas en accesibilidad,
escalabilidad y costo, permitiendo que soluciones personalizadas y
robustas compitan eficazmente con softwares comerciales complejos,
volviéndose viables para establecimientos educacionales vulnerables o
con presupuestos limitados.

## 1.4 Contribución del trabajo

La presente aplicación web busca contribuir a optimizar los procesos de
gestión de la orientación vocacional en instituciones educativas que
operan con métodos manuales o intervenciones fragmentadas. Su diseño,
fundamentado en patrones de procesos de negocios (BPM), automatiza
tareas como la aplicación del test de personalidad, el almacenamiento en
tiempo real del perfil estudiantil y la generación de reportes
automáticos enriquecidos. Esto favorece una mayor trazabilidad de la
evolución vocacional del alumno y una toma de decisiones eficiente
basada en datos objetivos.

## 1.5 Trabajo a realizar en el proyecto

El trabajo consiste en desarrollar e implementar una aplicación web
interactiva basada en patrones de procesos de negocio (BPM) para la
gestión de la orientación vocacional y el autoconocimiento, integrando
el motor Camunda Platform 8 para la orquestación del flujo y el modelo
Big Five de personalidad como eje de evaluación científica, resolviendo
la falta de herramientas digitales y el acompañamiento reactivo en los
estudiantes de enseñanza media chilenos.

## 1.6 Organización y presentación de este trabajo

Este documento se estructura de la siguiente manera: El Capítulo II
detalla la identificación, fundamentación y desglose cuantitativo del
problema, así como los objetivos y el alcance del sistema. El Capítulo
III expone el marco metodológico, el stack de herramientas de desarrollo
open-source, planes de calidad, gestión de riesgos, el cronograma
detallado por sprints y el diseño exhaustivo de las interfaces a través
de la sección de Prototipo. El Capítulo IV proyecta la matriz de
trazabilidad y los aspectos de diseño arquitectónico y de base de datos
del sistema.

# CAPÍTULO II: IDENTIFICACIÓN DEL PROBLEMA / OPORTUNIDAD

## 2.1 Presentación y fundamentación del problema

[]{#_Toc232975659 .anchor}El núcleo de la problemática radica en los
desafíos que experimentan los jóvenes chilenos para decidir su futuro
profesional, los cuales se ven acentuados por ciertas brechas en la
actualización metodológica y tecnológica de los sistemas de apoyo
actuales. La falta de un acompañamiento continuo genera elecciones
reactivas bajo plazos limitados o presiones del medio ambiente social,
derivando en insatisfacción vocacional o posible deserción temprana en
las aulas universitarias.

## 2.2 Descripción de problemas / oportunidades de mejora

Se identifican tres síntomas críticos dentro del modelo de orientación
vigente:

- **Orientación Tardía y Reactiva:** El acompañamiento se intensifica
  erróneamente solo en 4to medio, impidiendo una exploración progresiva
  y forzando decisiones apresuradas bajo la presión de las pruebas de
  admisión.

- **Enfoque Centrado en Contenidos:** Se priorizan contenidos académicos
  abstractos en lugar del desarrollo de competencias blandas o el
  autoconocimiento científico de aptitudes.

- **Acompañamiento Individual Insuficiente:** Existe una excesiva carga
  administrativa y carencia de profesionales capacitados de forma
  específica, reduciendo al alumno a una mera estadística.

## 2.3 Identificación cuantitativa de problemas (Diagrama de Ishikawa)

El análisis causal se estructura a partir del Diagrama de Ishikawa,
abarcando las siguientes dimensiones identificadas en el entorno
escolar:

- **Máquinas:** Herramientas digitales sumamente limitadas y baja
  adopción de tecnología interactiva o plataformas centralizadas en la
  nube.

- **Medición:** Ausencia de tests de autoconocimiento integrados
  metodológicamente y nulo seguimiento periódico de la evolución
  vocacional del alumno.

- **Método:** Orientación enfocada de manera reactiva en el último año
  de enseñanza media con un sesgo centrado estrictamente en contenidos
  tradicionales.

- **Medio Ambiente:** Presión del entorno familiar por optar a carreras
  convencionales, expectativas sociales poco realistas.

## 2.4 Objetivo general

Desarrollar una aplicación web interactiva basada en patrones de
procesos de negocio (BPM) para la gestión de la orientación vocacional y
el autoconocimiento, con la finalidad de resolver las dificultades que
enfrentan los jóvenes chilenos para elegir su futuro profesional debido
a la falta de herramientas digitales y la orientación tardía.

## 2.5 Objetivos específicos y métricas

A continuación, se detalla la matriz de desglose de objetivos
específicos, métricas asociadas y sus respectivos criterios de éxito:

  ---------------------------------------------------------------------------------------
  Objetivo         Situación       Resultado        Métrica           Criterio de éxito
  específico       actual          esperado                           
  ---------------- --------------- ---------------- ----------------- -------------------
  Analizar los     Procesos        Informe de       Cantidad de       Identificar y
  procesos         gestionados     diagnóstico      procesos          documentar al menos
  actuales de      manualmente,    detallado del    documentados.     el 90% de los
  orientación      con orientación sistema actual                     procesos
  vocacional.      tardía y        de orientación.                    principales.
                   fragmentada.                                       

  Diseñar la       No existe un    Prototipo        Número de módulos Diseñar al menos el
  arquitectura     diseño          arquitectónico   y funcionalidades 100% de los módulos
  técnica del      estructurado    del sistema con  diseñadas.        definidos en la
  sistema.         del sistema ni  sus módulos                        EDT.
                   integración     funcionales.                       
                   digital de                                         
                   datos.                                             

  Desarrollar los  Ausencia de     Aplicación       Porcentaje de     Lograr la
  módulos          sistemas        funcional con    cumplimiento      funcionalidad total
  funcionales de   automatizados y almacenamiento   funcional.        (100%) de los
  la aplicación.   herramientas    de datos en                        módulos de
                   interactivas    tiempo real.                       autoconocimiento.
                   atractivas.                                        

  Validar el       No se dispone   Reporte de       Porcentaje de     Lograr al menos una
  funcionamiento   de herramientas pruebas          satisfacción de   satisfacción ≥ 85%
  del sistema con  para validar    funcionales,     los usuarios.     en los usuarios
  usuarios.        procesos ni     unitarias y de                     evaluadores.
                   experiencia de  satisfacción de                    
                   usuario.        usuario.                           
  ---------------------------------------------------------------------------------------

**\**

## 2.6 Alcance del Proyecto y Definición del MVP

Dada la naturaleza individual del proyecto académico, se ha acotado un
Producto Mínimo Viable (MVP) que abarca los siguientes módulos e hitos
de desarrollo críticos:

- **Registro y Autenticación:** Formularios de captura de datos básicos
  estudiantiles y validación de seguridad mediante tokens JWT.

- **Cuestionario Científico BFI-44:** Implementación digital completa
  del inventario Big Five compuesto por 44 ítems evaluados bajo escala
  Likert de 5 puntos, garantizando robustez psicométrica.

- **Cálculo y Reporte Automático:** Algoritmo de procesamiento inmediato
  de las dimensiones OCEAN (Apertura, Responsabilidad, Extraversión,
  Amabilidad, Estabilidad Emocional), estructurando una visualización
  enriquecida en gráfico de radar.

- **Orquestación BPM:** Control de estados del flujo del usuario
  administrado mediante el motor de procesos Camunda 8.

- **Panel de Control del Orientador:** Interfaz básica de monitoreo para
  visualizar la lista de estudiantes asignados y acceder a sus
  respectivos resultados.

Quedan fuera del alcance del MVP y proyectados como mejoras futuras: La
exportación automatizada de reportes en formato PDF, la analítica
predictiva institucional avanzada y las pruebas de interfaz
automatizadas de frontend.

# CAPÍTULO III: METODOLOGÍA

## 3.1 Metodología de Desarrollo Híbrida

Para la ejecución idónea del proyecto se optó por una metodología de
enfoque híbrido. Se utiliza la guía PMBOK para estructurar los
macroprocesos de gestión organizativa (tales como la planificación de la
calidad, la mitigación oportuna de riesgos y el control estricto del
cronograma general) en coexistencia armónica con el marco ágil Scrum
para guiar de manera iterativa el desarrollo del producto de software.

Este enfoque híbrido subsana las carencias del modelo tradicional
Waterfall (descartado debido a su rigidez conceptual ante requerimientos
evolutivos) y del Scrum puro (el cual carece de mecanismos formales para
dar soporte al cumplimiento y control de hitos administrativos de
carácter académico).

## 3.2 Herramientas y Ambiente de Desarrollo

La selección del stack tecnológico responde rigurosamente a
restricciones de costo y robustez, priorizando ecosistemas open-source
con amplio respaldo en la industria:

- **Backend:** Framework FastAPI (Python 3.11) por su óptimo rendimiento
  asíncrono y la autogeneración interactiva de documentación mediante
  Swagger UI.

- **Motor BPM:** Camunda Platform 8 (versión Self-Managed ejecutada en
  entorno local) encargado de la automatización secuencial del proceso
  vocacional bajo notación BPMN.

- **Frontend:** Vue.js (versión 3) complementado con la librería Axios
  para la gestión fluida de peticiones HTTP en una arquitectura SPA.

- **Base de Datos:** MySQL 8.0 administrado mediante MySQL Workbench,
  interactuando con el backend mediante el ORM SQLAlchemy.

- **Control de Versiones y Entorno:** Git con repositorios remotos en
  GitHub; desarrollo sobre Visual Studio Code operado de forma nativa
  bajo el sistema operativo CachyOS (distribución basada en Arch Linux).

## 3.3 Descripción general de la propuesta de solución (Arquitectura Macro)

**\**

## 3.4 Planes de Gestión (Riesgos, Calidad y Pruebas)

**Gestión de Riesgos:** Se contempla como riesgo principal la
complejidad técnica al integrar las llamadas de servicios de Camunda 8
con los endpoints asíncronos de FastAPI. La mitigación consiste en
priorizar una prueba de concepto (PoC) durante el primer sprint del
proyecto. Ante retrasos por carga académica paralela, se establece una
bitácora de dedicación mínima de 10 horas semanales.

**Gestión de la Calidad:** El código fuente backend debe alinearse
estrictamente a las convenciones estilísticas de la guía PEP 8. Se exige
cobertura de pruebas unitarias sobre los controladores de negocio y un
umbral de tiempo de respuesta para la API REST que no exceda los 3
segundos bajo una concurrencia normal de hasta 30 usuarios en red
escolar.

**Gestión de Pruebas:** Se define un ciclo compuesto por pruebas
unitarias automatizadas (vía Pytest para la API de backend), pruebas
integrales de comunicación de interfaz y pruebas de sistema de extremo a
extremo que validen de forma limpia la completitud del flujo de proceso
orquestado por el motor.

## 3.5 Cronograma del Proyecto (Planificación de Sprints)

El desarrollo se desglosa temporalmente en ciclos fijos de tres semanas
cada uno, abarcando desde abril de 2026 hasta la entrega final
programada para finales de noviembre de 2026:

- **Sprint 1 (Mayo 2026):** Inicialización del entorno, despliegue local
  de Camunda, PoC de integración y desarrollo de la capa de
  autenticación JWT.

- **Sprint 2 (Junio 2026):** Modelado BPMN de la evaluación, maquetación
  del cuestionario BFI-44 en Vue.js y codificación del algoritmo de
  puntajes OCEAN.

- **Sprint 3 (Junio - Julio 2026):** Construcción de la interfaz gráfica
  de resultados (Gráfico de Radar), lógica de reportes interpretativos y
  pruebas integradas de flujo.

- **Sprint 4 (Julio - Agosto 2026):** Implementación del panel de
  control para el perfil de usuario orientador y seguimiento de progreso
  de alumnos.

- **Sprints 5 y 6 (Agosto - Septiembre 2026):** Refinamiento de
  interfaces, pruebas de usabilidad con un grupo muestra de 5 usuarios
  reales y validación de seguridad.

## 3.6 Prototipo (Diseño de Interfaces y Flujo de Navegación)

A continuación, se detalla la propuesta de pantallas y la arquitectura
visual del sistema. Esta sección establece los espacios correspondientes
y la descripción funcional interactiva para la integración de los
mockups definitivos del sistema:

### 3.6.1 Pantalla de Login y Registro Centralizado

Esta interfaz permite el acceso seguro a la plataforma mediante
credenciales validadas (correo electrónico y contraseña cifrada). Cuenta
con un selector dinámico para desviar el flujo según el rol del usuario
(Estudiante u Orientador Escolar). El formulario de registro solicita
datos de entrada clave como nombre completo, edad, establecimiento
educativo y curso correspondiente.

**\**

### 3.6.2 Pantalla del Panel Principal del Estudiante (Dashboard)

Una vez autenticado, el estudiante accede a un panel intuitivo y lúdico
que le da la bienvenida y le muestra el estado actual de su proceso
guiado por el motor BPM Camunda. Si es su primera navegación, se
despliega un botón destacado con la acción \"Iniciar Evaluación
Vocacional\". Si posee registros previos, el panel expone un acceso
directo a su historial de perfiles guardados.

**\**

### 3.6.3 Pantalla del Cuestionario Big Five (BFI-44)

Esta pantalla renderiza de manera interactiva los 44 ítems del
instrumento psicométrico Big Five. Para evitar la fatiga cognitiva del
usuario, las preguntas se distribuyen de forma paginada (en bloques de
10 preguntas por vista). Cada ítem se responde obligatoriamente a través
de una matriz de opciones con escala Likert de 5 puntos (desde
\"Totalmente en desacuerdo\" hasta \"Totalmente de acuerdo\"). El
progreso parcial se almacena de forma asíncrona en la base de datos
MySQL.

**\**

### 3.6.4 Pantalla de Reporte Vocacional Enriquecido

Al completar los 44 ítems, el motor procesa el flujo y calcula los
puntajes OCEAN. Esta interfaz despliega los resultados de forma visual y
de fácil lectura. Incorpora un componente gráfico de tipo radar que
mapea los niveles de las cinco grandes dimensiones de la personalidad,
acompañado de bloques de texto interpretativo personalizado, listado de
familias de carreras afines y recomendaciones orientativas accionables
basadas en el perfil dominante.

**\**

### 3.6.5 Pantalla del Panel de Administración del Orientador

Interfaz exclusiva para los usuarios con el rol de Orientador o Docente.
Muestra un listado centralizado con los nombres, cursos y el estado del
proceso BPM de todos los estudiantes bajo su tutela. Permite aplicar
filtros de búsqueda avanzados y hacer clic sobre cualquier registro
estudiantil para auditar el historial de respuestas y visualizar en
tiempo real el reporte vocacional generado por el software.

# 

[\
]{.mark}

# CAPÍTULO IV: DISCUSIÓN DE RESULTADOS

## 4.1 Ingeniería de Requerimientos y Casos de Uso

Los requerimientos del sistema se estructuran a partir de los actores
identificados (Estudiante, Orientador y Administrador). El flujo
completo se valida mediante el modelado del comportamiento dinámico y
estático del software utilizando la notación estándar UML.

Diagrama de casos de uso.

**Diagrama de actividades.**

[]{#_Toc232975680 .anchor}

**\**

## 4.2 Espacios para Modelos de Procesos y Datos de Próxima Incorporación

Para garantizar la completitud técnica solicitada por la comisión
evaluadora en las fases posteriores del proyecto de título, se reservan
explícitamente los apartados correspondientes para la integración de los
siguientes diagramas de ingeniería de software:

### 4.2.1 Diagrama de Procesos BPMN Completo (Orquestación Camunda 8)

Este diagrama técnico detallará la secuencia exacta de tareas
automatizadas y manuales integradas en el motor de flujos, especificando
las compuertas lógicas de decisión (ej. control de cuestionario completo
o incompleto), los eventos de inicio/fin y el paso de variables entre el
pool del estudiante y el backend del sistema.

**\**

### 4.2.2 Diagrama Entidad-Relación (DER) de la Base de Datos

Mapeo visual relacional de persistencia de datos en MySQL 8.0. Detallará
las llaves primarias, foráneas, tipos de datos y restricciones de
integridad para las tablas de: usuario, estudiante, orientador,
evaluacion, pregunta, respuesta, reporte_vocacional y proceso_bpm.

**\**

### 4.2.3 Diagrama de Clases UML del Sistema

**\**

### 4.2.4 Diagrama de Componentes y Despliegue Físico

[]{#_Toc232975686 .anchor}**REFERENCIAS BIBLIOGRÁFICAS**

> John, O. P., & Srivastava, S. (1999). The Big Five trait taxonomy:
> History, measurement, and theoretical perspectives. *Handbook of
> personality: Theory and research*, 2(1999), 102-138.
>
> Project Management Institute. (2021). *A guide to the project
> management body of knowledge (PMBOK guide)* (7th ed.). Project
> Management Institute.
>
> Schwaber, K., & Beedle, M. (2002). *Agile software development with
> Scrum*. Prentice Hall.

# 

# GLOSARIO

- **API REST (Representational State Transfer Application Programming
  Interface):** Interfaz de programación de aplicaciones que utiliza
  peticiones HTTP para transferir datos y permitir la comunicación sutil
  entre el frontend desarrollado en Vue.js 3 y el servidor backend en
  FastAPI.

- **ASGI (Asynchronous Server Gateway Interface):** Especificación de
  interfaz espiritual sucesora de WSGI, utilizada por el servidor
  Uvicorn para gestionar de manera asíncrona y con alto rendimiento las
  múltiples peticiones concurrentes orientadas a la aplicación web.

- **Axios:** Librería de JavaScript basada en promesas encargada de
  gestionar y ejecutar solicitudes HTTP desde el cliente hacia la API de
  backend de manera optimizada y asíncrona.

- **BFI-44 (Big Five Inventory de 44 ítems):** Cuestionario psicométrico
  estandarizado y validado científicamente que consta de 44 afirmaciones
  autoevaluables, utilizado como núcleo logicial para caracterizar el
  perfil de personalidad del estudiante.

- **BPM (Business Process Management):** Disciplina de gestión
  corporativa que integra metodologías y tecnologías para optimizar,
  estandarizar y modelar flujos de trabajo de extremo a extremo dentro
  de una organización o sistema institucional.

- **BPMN (Business Process Model and Notation):** Estándar gráfico
  internacional de modelado que provee una notación de diagramación en
  carriles (*lanes*) para representar visualmente las etapas operativas
  y lógicas de un proceso de negocio.

- **CachyOS:** Sistema operativo basado en la distribución Arch Linux,
  optimizado a nivel de kernel y compilación de paquetes para entregar
  una baja latencia y alto rendimiento en el ambiente de desarrollo
  local.

- **Camunda Platform 8:** Motor de orquestación y automatización de
  procesos de negocio nativo en la nube que interpreta modelos BPMN para
  coordinar y registrar los estados de las tareas del sistema.

- **Escala Likert:** Herramienta de medición psicométrica psicológica
  que mide actitudes o respuestas en un gradiente lineal de opciones,
  implementada en este software en una matriz obligatoria de 5 puntos de
  valoración.

- **FastAPI:** Framework web moderno y de código abierto basado en
  Python 3.11, seleccionado por su alta velocidad de ejecución asíncrona
  y la autogeneración nativa de documentación interactiva orientada a
  endpoints.

- **JWT (JSON Web Token):** Estándar abierto basado en JSON empleado
  para la transmisión segura de tokens de identidad cifrados que validan
  los accesos restringidos y la seguridad de los usuarios orientadores.

- **MVP (Minimum Viable Product / Producto Mínimo Viable):** Versión
  inicial y acotada de un producto de software que reúne las
  funcionalidades esenciales y críticas para ser desplegado de forma
  operativa cumpliendo con los estándares de calidad definidos.

- **MySQL 8.0:** Sistema de gestión de bases de datos relacionales
  (*RDBMS*) de código abierto, utilizado para la persistencia e
  integridad estructural de la información transaccional del
  perfilamiento estudiantil.

- **OCEAN:** Acrónimo mnemotécnico en inglés que define las cinco
  dimensiones fundamentales medibles en el inventario Big Five:
  *Openness* (Apertura), *Conscientiousness* (Responsabilidad),
  *Extraversion* (Extraversión), *Agreeableness* (Amabilidad) y
  *Neuroticism* (Estabilidad Emocional).

- **ORM (Object-Relational Mapping):** Técnica de programación para
  convertir datos entre el sistema de tipos de un lenguaje orientado a
  objetos (Python) y una base de datos relacional (MySQL), implementada
  mediante la librería SQLAlchemy.

- **SPA (Single Page Application):** Arquitectura de aplicación web que
  carga una única página HTML y actualiza dinámicamente el contenido de
  la interfaz de usuario interactiva a medida que este interactúa con el
  sistema, eliminando la recarga completa del navegador.

- **SQLAlchemy:** Kit de herramientas SQL y mapeador de objetos
  relacionales (ORM) para Python que proporciona la flexibilidad y
  automatización requeridas para mapear clases a tablas MySQL.

- **Uvicorn:** Servidor web ASGI rápido y de producción para Python,
  utilizado como entorno para ejecutar de forma nativa la lógica y los
  controladores de FastAPI.

- **Vue.js 3:** Framework progresivo de JavaScript de código abierto
  enfocado en la capa visual, utilizado para modularizar componentes web
  y construir interfaces de usuario de alta velocidad transaccional.

# 

# 

# 

# 
