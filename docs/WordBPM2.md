![Logotipo Descripción generada
automáticamente](media/image1.png){width="1.9043996062992126in"
height="1.968503937007874in"}

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

2026

![](media/image2.png){width="2.03125in" height="1.9194444444444445in"}

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

[2.2 Descripción de problemas / oportunidades de mejora
[4](#descripción-de-problemas-oportunidades-de-mejora)](#descripción-de-problemas-oportunidades-de-mejora)

[2.3 Análisis de causas del problema (Diagrama de Ishikawa)
[5](#análisis-de-causas-del-problema-diagrama-de-ishikawa)](#análisis-de-causas-del-problema-diagrama-de-ishikawa)

[2.4 Objetivo general [6](#objetivo-general)](#objetivo-general)

[2.5 Objetivos específicos y métricas
[7](#objetivos-específicos-y-métricas)](#objetivos-específicos-y-métricas)

[2.6 Alcance del Proyecto y Definición del MVP
[9](#alcance-del-proyecto-y-definición-del-mvp)](#alcance-del-proyecto-y-definición-del-mvp)

[IV. CAPÍTULO III: METODOLOGÍA
[11](#capítulo-iii-metodología)](#capítulo-iii-metodología)

[3.1 Metodología de Desarrollo Híbrida
[11](#metodología-de-desarrollo-híbrida)](#metodología-de-desarrollo-híbrida)

[3.2 Herramientas y Ambiente de Desarrollo
[11](#herramientas-y-ambiente-de-desarrollo)](#herramientas-y-ambiente-de-desarrollo)

[3.3 Descripción general de la propuesta de solución (Arquitectura
Macro)
[12](#descripción-general-de-la-propuesta-de-solución-arquitectura-macro)](#descripción-general-de-la-propuesta-de-solución-arquitectura-macro)

[3.4 Planes de Gestión (Riesgos, Calidad y Pruebas)
[13](#planes-de-gestión-riesgos-calidad-y-pruebas)](#planes-de-gestión-riesgos-calidad-y-pruebas)

[3.5 Cronograma del Proyecto (Planificación de Sprints)
[13](#cronograma-del-proyecto-planificación-de-sprints)](#cronograma-del-proyecto-planificación-de-sprints)

[3.6 Prototipo (Diseño de Interfaces y Flujo de Navegación)
[16](#prototipo-diseño-de-interfaces-y-flujo-de-navegación)](#prototipo-diseño-de-interfaces-y-flujo-de-navegación)

[3.6.1 Pantalla de Login y Registro Centralizado
[16](#pantalla-de-login-y-registro-centralizado)](#pantalla-de-login-y-registro-centralizado)

[3.6.2 Pantalla del Panel Principal del Estudiante (Dashboard)
[17](#pantalla-del-panel-principal-del-estudiante-dashboard)](#pantalla-del-panel-principal-del-estudiante-dashboard)

[3.6.3 Pantalla del Cuestionario Big Five (BFI-44)
[18](#pantalla-del-cuestionario-big-five-bfi-44)](#pantalla-del-cuestionario-big-five-bfi-44)

[3.6.4 Pantalla de Reporte Vocacional Enriquecido
[19](#pantalla-de-reporte-vocacional-enriquecido)](#pantalla-de-reporte-vocacional-enriquecido)

[3.6.5 Pantalla del Panel de Administración del Orientador
[22](#pantalla-del-panel-de-administración-del-orientador)](#pantalla-del-panel-de-administración-del-orientador)

[![](media/image3.png){width="5.940277777777778in"
height="3.5076388888888888in"} [22](#section)](#section)

[V. CAPÍTULO IV: DISCUSIÓN DE RESULTADOS
[23](#capítulo-iv-discusión-de-resultados)](#capítulo-iv-discusión-de-resultados)

[4.1 Ingeniería de Requerimientos y Casos de Uso
[23](#ingeniería-de-requerimientos-y-casos-de-uso)](#ingeniería-de-requerimientos-y-casos-de-uso)

[4.2 Modelos de Procesos, Datos y Arquitectura del Sistema
[25](#modelos-de-procesos-datos-y-arquitectura-del-sistema)](#modelos-de-procesos-datos-y-arquitectura-del-sistema)

[4.2.1 Diagrama de Procesos BPMN Completo (Orquestación Camunda 8)
[25](#diagrama-de-procesos-bpmn-completo-orquestación-camunda-8)](#diagrama-de-procesos-bpmn-completo-orquestación-camunda-8)

[4.2.2 Diagrama Entidad-Relación (DER) de la Base de Datos
[26](#diagrama-entidad-relación-der-de-la-base-de-datos)](#diagrama-entidad-relación-der-de-la-base-de-datos)

[4.2.3 Diagrama de Clases UML del Sistema
[28](#diagrama-de-clases-uml-del-sistema)](#diagrama-de-clases-uml-del-sistema)

[4.2.4 Diagrama de Componentes y Despliegue Físico
[29](#diagrama-de-componentes-y-despliegue-físico)](#diagrama-de-componentes-y-despliegue-físico)

[**REFERENCIAS BIBLIOGRÁFICAS** [31](#_Toc241354898)](#_Toc241354898)

[GLOSARIO [32](#glosario)](#glosario)

**\**

**RESUMEN EJECUTIVO\
Presentación del problema**\
En la enseñanza media chilena, la orientación vocacional incluye la
reflexión sobre el proyecto de vida y la exploración de alternativas de
estudio y trabajo (Ministerio de Educación de Chile, 2024). Cuando las
evaluaciones, sus resultados y las acciones de seguimiento se
administran en registros separados, resulta más difícil mantener la
continuidad y consultar el avance de cada estudiante. Este proyecto
aborda la gestión de esa información y del flujo de orientación mediante
una aplicación web.

La propuesta busca reunir información del estudiante, incorporar un
instrumento de apoyo al autoconocimiento y facilitar al orientador la
consulta de resultados y estados del proceso. La decisión académica o
profesional sigue dependiendo de la reflexión del estudiante y de
factores personales, familiares, educativos y sociales (Lowman, 2022).

La pregunta que guía el proyecto es: ¿De qué manera una aplicación web
basada en procesos de negocio puede mejorar la gestión, continuidad y
trazabilidad de las evaluaciones de autoconocimiento y del seguimiento
de estudiantes de enseñanza media?

**Objetivo general**\
Mejorar la gestión, continuidad y trazabilidad del proceso de
orientación vocacional y autoconocimiento de estudiantes de enseñanza
media, mediante el desarrollo de una aplicación web basada en procesos
de negocio (BPM) que permita gestionar evaluaciones de autoconocimiento,
centralizar sus resultados y apoyar el seguimiento realizado por los
orientadores.

**Metodología**\
Se propone combinar prácticas de planificación y control del proyecto
tomadas de la guía PMBOK con iteraciones de desarrollo inspiradas en
Scrum (Project Management Institute, 2021; Schwaber & Sutherland, 2020).
La solución prevista utiliza FastAPI para la API, Vue.js para la
interfaz, MySQL para los datos y Camunda 8 para orquestar estados y
tareas del proceso. El BFI de 44 ítems se plantea como instrumento de
apoyo al autoconocimiento; su aplicación e interpretación deben
documentar la versión en español y sus reglas de puntuación
(Benet-Martínez & John, 1998; John & Srivastava, 1999).

**Resultados esperados**\
Se espera entregar un producto mínimo viable (MVP) que permita el
registro de usuarios, la aplicación digital del BFI-44, el cálculo de
sus cinco dimensiones, la visualización de resultados y la consulta del
estado de cada estudiante por parte del orientador. Las pruebas
funcionales, de integración y de usabilidad permitirán evaluar el
cumplimiento de los requerimientos definidos. Los resultados del
cuestionario se presentarán como información para la reflexión y el
acompañamiento, sin determinar una carrera para el estudiante.

**Conclusiones y recomendaciones**

La contribución esperada es una gestión más ordenada del proceso de
orientación: información centralizada, estados visibles y resultados
disponibles para el seguimiento. La utilidad efectiva de la aplicación
deberá establecerse con las pruebas y criterios de éxito definidos en el
proyecto; no se atribuyen al software cambios directos en la elección de
carrera o en la deserción.

**Palabras Clave:** Gestión de Procesos de Negocio (BPM), Orientación
Vocacional, Modelo Big Five (OCEAN), Aplicación Web, Camunda.

# CAPÍTULO I: INTRODUCCIÓN

## 1.1 Introducción

La transición desde la enseñanza media hacia estudios superiores,
formación técnica o trabajo implica explorar alternativas y
relacionarlas con intereses, habilidades y circunstancias personales. El
currículo chileno contempla un taller de decisión vocacional y proyecto
de vida para 3.º y 4.º medio (Ministerio de Educación de Chile, 2024).
En ese contexto, las herramientas de autoconocimiento pueden aportar
información para la conversación con el orientador, junto con otras
fuentes sobre intereses y aptitudes (Lowman, 2022).

El problema que aborda este proyecto se sitúa en la gestión del proceso
de orientación: cuando las evaluaciones y sus resultados no se integran
con el seguimiento, el orientador dispone de menos información
organizada para acompañar a cada estudiante. La propuesta busca
facilitar ese trabajo mediante un registro centralizado y un flujo de
actividades trazable.

## 1.2 Importancia de resolver el problema

Mejorar el acceso del orientador a evaluaciones, resultados y estados
del proceso puede facilitar la continuidad del acompañamiento. La
automatización de tareas de registro y cálculo busca reducir trabajo
manual, pero ese efecto deberá comprobarse durante la validación. La
aplicación entrega información de apoyo: interpretar el contexto del
estudiante y orientar sus decisiones sigue siendo una tarea humana
(Lowman, 2022).

## 1.3 Breve discusión bibliográfica

Desde la perspectiva tecnológica, la implementación de sistemas basados en la web ofrece ventajas significativas frente a los instrumentos tradicionales en papel, destacando su alta accesibilidad descentralizada, capacidad de escalabilidad a múltiples establecimientos y un menor costo operativo en su distribución (Pressman & Maxim, 2020).

El taller de Decisión Vocacional y Proyecto de Vida del currículo
chileno sitúa la exploración de opciones en el marco de la reflexión
personal (Ministerio de Educación de Chile, 2024). Para la evaluación de
carrera, Lowman (2022) propone integrar intereses, habilidades y
personalidad, por lo que una medida de rasgos no basta por sí sola para
indicar una ocupación. El BFI-44 describe cinco dimensiones amplias de
personalidad; la investigación sobre su versión en español se realizó
con poblaciones distintas de los escolares chilenos, lo que exige
cautela al trasladar sus interpretaciones a este proyecto
(Benet-Martínez & John, 1998; John & Srivastava, 1999). Desde el punto
de vista técnico, Camunda 8 permite modelar y ejecutar procesos BPMN con
tareas y estados explícitos, capacidad pertinente para registrar el
avance de una evaluación y su seguimiento (Camunda, s. f.).

## 1.4 Contribución del trabajo

La aplicación propuesta busca centralizar datos de estudiantes,
resultados de autoconocimiento y estados del proceso de orientación. El
flujo BPM permite representar las etapas de evaluación y consulta por el
orientador (Camunda, s. f.). Los reportes entregarán información
descriptiva para apoyar la conversación orientadora; su utilidad se
evaluará con los criterios de prueba del proyecto.

## 1.5 Trabajo a realizar en el proyecto

El proyecto contempla el análisis de necesidades, el diseño y desarrollo
de una aplicación web, y su validación. La solución integrará Camunda 8
para la gestión del flujo, una versión documentada del BFI-44 para
apoyar el autoconocimiento y un panel que permita al orientador
consultar resultados y avance. El sistema no reemplaza el acompañamiento
profesional ni decide el futuro académico del estudiante.

## 1.6 Organización y presentación de este trabajo

Este documento se estructura de la siguiente manera: el Capítulo II
delimita el problema, sus causas abordables, los objetivos y el alcance
del MVP. El Capítulo III describe la metodología, las herramientas, los
riesgos, las pruebas, el cronograma y los prototipos de interfaz. El
Capítulo IV presenta los requerimientos y los modelos de procesos, datos
y arquitectura incluidos en esta propuesta.

# CAPÍTULO II: IDENTIFICACIÓN DEL PROBLEMA / OPORTUNIDAD

## 2.1 Presentación y fundamentación del problema

El problema central de este proyecto es la gestión fragmentada de la
información y de las actividades de orientación vocacional en el
contexto escolar considerado. Cuando la aplicación de instrumentos, sus
resultados y el seguimiento se realizan por vías separadas, se dificulta
consultar el avance de cada estudiante y mantener continuidad en el
acompañamiento. La aplicación puede contribuir a centralizar esos
registros y a hacer visible el estado del proceso. La incertidumbre
sobre el futuro profesional y las presiones del entorno son factores
relevantes, pero no pueden resolverse directamente mediante el software.

## 2.2 Descripción de problemas / oportunidades de mejora

La oportunidad de mejora se organiza en tres aspectos del proceso de
orientación que pueden traducirse en requerimientos del sistema:

- Continuidad del proceso: si las actividades se concentran en una etapa
  y no se conserva un historial accesible, el orientador tiene menos
  elementos para dar seguimiento. El sistema registrará estados y
  resultados de las evaluaciones realizadas.

- Integración de información: cuando las herramientas de
  autoconocimiento no forman parte del mismo flujo de trabajo, sus
  resultados pueden quedar separados de las demás acciones de
  orientación. La aplicación incorporará el cuestionario y centralizará
  sus resultados.

- Apoyo al orientador: el registro y procesamiento manual de respuestas
  puede dificultar la consulta individual. La aplicación automatizará el
  cálculo y presentará los resultados para su revisión, sin sustituir la
  interpretación y el acompañamiento del profesional.

## 2.3 Análisis de causas del problema (Diagrama de Ishikawa)

El diagrama de Ishikawa organiza las causas en seis categorías: Mano de
Obra, Medición, Materiales, Máquinas, Método y Medio Ambiente. Las
causas vinculadas con herramientas digitales, instrumentos integrados,
registro de resultados y seguimiento son las más cercanas al alcance de
la aplicación; las presiones familiares y sociales constituyen factores
de contexto.

Mano de Obra: disponibilidad de tiempo y carga de registro del
orientador para acompañar y revisar individualmente el avance de los
estudiantes.

- Máquinas: disponibilidad y uso limitado de herramientas digitales
  centralizadas para registrar actividades y resultados de orientación.

- Medición: falta de instrumentos de autoconocimiento integrados al
  proceso y de registros periódicos de avance consultables por el
  orientador.

Materiales: recursos e información de apoyo distribuidos en distintos
medios, lo que dificulta su consulta junto con los resultados de las
evaluaciones.

- Método: secuencia de actividades poco integrada y seguimiento que
  puede concentrarse en etapas tardías de la enseñanza media.

- Medio Ambiente: presión familiar y expectativas sociales que influyen
  en las decisiones del estudiante y quedan fuera de la solución
  tecnológica.

![](media/image4.png){width="5.706127515310587in"
height="2.662338145231846in"}

> **Nota para el autor:** Reemplazar el diagrama PNG anterior por una versión que tenga un círculo verde encerrando las causas de Máquinas y Medición (abordables por el MVP) y un círculo rojo en Medio Ambiente (causas de contexto no abordables), tal como solicitó la profesora.

## 2.4 Objetivo general

Mejorar la gestión, continuidad y trazabilidad del proceso de
orientación vocacional y autoconocimiento de estudiantes de enseñanza
media, mediante el desarrollo de una aplicación web basada en procesos
de negocio (BPM) que permita gestionar evaluaciones de autoconocimiento,
centralizar sus resultados y apoyar el seguimiento realizado por los
orientadores.

## 2.5 Objetivos específicos y métricas

La matriz relaciona cada objetivo con un resultado verificable. Los
denominadores de las métricas se fijarán al aprobar el listado de
requerimientos y los casos de prueba del MVP; los porcentajes se
calcularán sobre esos conjuntos definidos y se evaluarán al cierre del
proyecto, previsto para noviembre de 2026.

  -----------------------------------------------------------------------------------------
  Objetivo específico Situación actual  Resultado        Métrica          Criterio de éxito
                                        esperado                          
  ------------------- ----------------- ---------------- ---------------- -----------------
  OE1. Mejorar la     Las necesidades y Documento de     Requerimientos   100 % de los
  identificación de   reglas del        necesidades,     revisados y      requerimientos de
  las necesidades     proceso aún no se actores, flujo   priorizados /    la línea base
  asociadas al        encuentran        actual y         requerimientos   revisados y
  proceso de          consolidadas en   requerimientos   identificados en priorizados antes
  orientación         un conjunto       priorizados y    la línea base ×  de cerrar el
  vocacional y        priorizado de     revisados.       100.             análisis;
  autoconocimiento,   requerimientos.                                     registro de
  mediante el                                                             revisión con
  análisis y                                                              estudiantes y
  priorización de los                                                     orientadores.
  requerimientos                                                          
  funcionales y no                                                        
  funcionales de                                                          
  estudiantes y                                                           
  orientadores.                                                           

  OE2. Fortalecer la  No existe un      Arquitectura,    Requerimientos   100 % de los
  centralización y    diseño integrado  modelo de datos, aprobados        requerimientos
  trazabilidad de la  que vincule       interfaces y     trazados a un    aprobados con
  información         información,      BPMN vinculados  componente de    trazabilidad al
  generada durante el roles, interfaces con los          diseño / total   diseño antes de
  proceso de          y estados del     requerimientos   de               iniciar su
  orientación         proceso.          aprobados.       requerimientos   implementación;
  vocacional,                                            aprobados × 100. revisión de
  mediante el diseño                                                      consistencia
  de la arquitectura                                                      entre modelos.
  de software, modelo                                                     
  de datos,                                                               
  interfaces y flujo                                                      
  de procesos BPM de                                                      
  la solución.                                                            

  OE3. Mejorar la     Las actividades   MVP con          Requerimientos   100 % de los
  gestión y           de evaluación,    cuestionario,    funcionales del  requerimientos
  seguimiento del     cálculo y         cálculo de       MVP que cumplen  funcionales
  proceso de          consulta de       dimensiones,     sus criterios de críticos del MVP
  orientación         resultados no     visualización de aceptación /     y al menos 90 %
  vocacional y        están integradas  resultados y     total de         del total cumplen
  autoconocimiento,   en una            consulta del     requerimientos   sus criterios de
  mediante el         aplicación.       avance por el    funcionales del  aceptación al
  desarrollo de                         orientador.      MVP × 100.       cierre del
  funcionalidades                                                         desarrollo.
  para la aplicación                                                      
  de instrumentos,                                                        
  procesamiento de                                                        
  resultados,                                                             
  generación de                                                           
  reportes y                                                              
  monitoreo del                                                           
  avance de los                                                           
  estudiantes.                                                            

  OE4. Asegurar el    Aún no se dispone Informe de       Casos críticos   100 % de casos
  cumplimiento de los de resultados de  pruebas          aprobados /      críticos
  requerimientos      pruebas del flujo funcionales, de  casos críticos   funcionales y de
  definidos para la   integrado ni de   integración y de ejecutados ×     integración
  gestión del proceso evaluación de     usabilidad con   100; puntaje de  aprobados;
  de orientación      usabilidad.       incidencias y    usabilidad       puntaje medio de
  vocacional,                           acciones         obtenido /       usabilidad ≥ 85 %
  mediante la                           correctivas.     puntaje máximo   en la muestra
  validación                                             posible × 100.   definida, con
  funcional, de                                                           instrumento y
  integración y                                                           cálculo
  usabilidad de la                                                        documentados.
  aplicación                                                              
  utilizando                                                              
  escenarios de                                                           
  prueba y criterios                                                      
  de éxito medibles.                                                      
  -----------------------------------------------------------------------------------------

**\**

## 2.6 Alcance del Proyecto y Definición del MVP

Dada la naturaleza individual del proyecto académico, se ha acotado un
Producto Mínimo Viable (MVP) que abarca los siguientes módulos e hitos
de desarrollo críticos:

- **Registro y Autenticación:** Formularios de captura de datos básicos
  estudiantiles y validación de seguridad mediante tokens JWT.

- **Cuestionario BFI-44:** se propone digitalizar los 44 ítems de la
  versión en español estudiada por Benet-Martínez y John (1998), con
  cinco opciones de respuesta. Antes de implementarla se cotejarán los
  enunciados, el orden de los ítems y la clave de puntuación de la
  versión elegida. La adaptación chilena de Lara et al. (2021) se
  estudió en universitarios y obtuvo una versión final de 32 ítems; por
  ello, no constituye una validación del BFI-44 en estudiantes chilenos
  de enseñanza media.

- **Cálculo y reporte:** las respuestas se codificarán de 1 a 5. Los
  ítems de puntuación inversa se recodificarán como 6 menos la respuesta
  original. El resultado de cada dimensión será la media aritmética de
  sus ítems, una vez recodificados los que corresponda; su rango seguirá
  siendo de 1 a 5. No se calculará un perfil hasta completar las 44
  respuestas. El reporte mostrará apertura, responsabilidad,
  extraversión, amabilidad y neuroticismo en un gráfico de radar
  (Berkeley Personality Lab, s. f.; John & Srivastava, 1999).

**Interpretación de resultados:** los puntajes se presentarán como
descripciones de las respuestas del estudiante para apoyar la reflexión
con el orientador. No se usarán percentiles ni categorías clínicas sin
normas apropiadas para esta población. El cuestionario no determina la
carrera que debe elegir una persona; cualquier sugerencia de áreas de
estudio requerirá una fundamentación adicional (Lara et al., 2021;
Lowman, 2022). Para estructurar estas sugerencias de áreas de exploración, el sistema se fundamenta en la correlación teórica documentada entre los rasgos del modelo de los Cinco Grandes y los intereses vocacionales del modelo RIASEC de Holland. Metaanálisis exhaustivos (Barrick et al., 2003; Larson et al., 2002) evidencian que rasgos como la Apertura a la Experiencia se asocian fuertemente a intereses Artísticos e Investigativos, mientras que la Extraversión se vincula a perfiles Emprendedores y Sociales. El prototipo utiliza estas correlaciones generales para mapear el perfil dominante del estudiante hacia familias de carreras afines, funcionando como un puente exploratorio y no como una prueba de aptitudes.

- Orquestación BPM: registro y coordinación de los estados de evaluación
  y consulta mediante un proceso modelado en BPMN y ejecutado con
  Camunda 8 (Camunda, s. f.).

- Panel del orientador: consulta de estudiantes asignados, estado del
  proceso y resultados de autoconocimiento para apoyar el seguimiento.

Quedan fuera del MVP la exportación automática de reportes en PDF, la
analítica predictiva institucional avanzada y las pruebas automatizadas
de la interfaz frontend.

# CAPÍTULO III: METODOLOGÍA

## 3.1 Metodología de Desarrollo Híbrida

Se propone combinar prácticas de planificación, riesgos, calidad y
seguimiento del proyecto descritas por el Project Management Institute
(2021) con ciclos de desarrollo inspirados en Scrum (Schwaber &
Sutherland, 2020). La adaptación responde al carácter individual y
académico del trabajo: cada ciclo tendrá entregables revisables y el
plan general conservará hitos y criterios de evaluación definidos.

La planificación inicial establece alcance, dependencias y criterios de
prueba; las iteraciones permiten revisar el diseño y la implementación
conforme se verifican los requerimientos. El proyecto no aplicará todos
los roles y eventos de Scrum como si se tratara de un equipo de
desarrollo completo, sino prácticas de trabajo iterativo pertinentes a
una persona.

## 3.2 Herramientas y Ambiente de Desarrollo

La selección tecnológica busca cubrir la interfaz, la API, la
persistencia y la coordinación del flujo con herramientas que puedan
integrarse en el entorno de desarrollo previsto:

- Backend: FastAPI (Python) para exponer la API y generar documentación
  interactiva de sus endpoints (FastAPI, s. f.).

- Motor BPM: Camunda 8 en una instalación local para representar y
  ejecutar el flujo BPMN de evaluación y seguimiento (Camunda, s. f.).

- Frontend: Vue.js 3 y Axios para construir la interfaz y comunicarse
  con la API.

- Base de datos: MySQL 8.0 para persistir usuarios, respuestas,
  resultados y estados; SQLAlchemy para el mapeo entre la aplicación y
  las tablas.

- **Control de Versiones y Entorno:** Git con repositorios remotos en
  GitHub; desarrollo sobre Visual Studio Code operado de forma nativa
  bajo el sistema operativo CachyOS (distribución basada en Arch Linux).

## 3.3 Descripción general de la propuesta de solución (Arquitectura Macro)

![](media/image5.png){width="5.940277777777778in"
height="3.3409722222222222in"}**\**

## 3.4 Planes de Gestión (Riesgos, Calidad y Pruebas)

Gestión de riesgos: la integración entre Camunda 8, la API y la base de
datos puede requerir ajustes técnicos. Se realizará una prueba de
concepto al inicio del desarrollo para comprobar el flujo mínimo. La
dedicación prevista se registrará en una bitácora semanal para detectar
retrasos y ajustar el plan.

Gestión de la calidad: se revisará el código backend conforme a PEP 8 y
se cubrirá con pruebas la lógica de cálculo y los casos críticos de
negocio. El objetivo de respuesta de la API es de hasta 3 segundos en un
escenario de hasta 30 usuarios concurrentes; antes de evaluar ese umbral
se documentarán equipo, red, operaciones medidas y procedimiento de
carga.

Gestión de pruebas: se ejecutarán pruebas unitarias del cálculo y la
API, pruebas de integración entre interfaz, backend, base de datos y
motor BPM, y escenarios completos de uso. El informe indicará casos
ejecutados, resultados, incidencias y correcciones. La usabilidad se
medirá con un instrumento y una fórmula definidos antes de aplicarlo a
la muestra.

## 3.5 Cronograma del Proyecto (Planificación de Sprints)

El proyecto se planifica entre abril y noviembre de 2026. Abril se
destina al análisis y la preparación de requerimientos; los ciclos de
desarrollo descritos a continuación cubren mayo a septiembre. Octubre y
noviembre se reservan para resolver incidencias, consolidar los
resultados de las pruebas, completar la documentación y preparar la
entrega final. Las fechas y duraciones concretas de cada sprint deberán
quedar registradas en el cronograma.

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

Las pantallas siguientes ilustran el acceso de estudiantes y
orientadores, la aplicación del BFI-44, la consulta de resultados y el
seguimiento. Los prototipos representan la propuesta de interfaz; las
funciones definitivas del MVP se establecen en la sección 2.6 y en los
requerimientos.

### 3.6.1 Pantalla de Login y Registro Centralizado

Esta interfaz permite el acceso seguro a la plataforma mediante
credenciales validadas (correo electrónico y contraseña cifrada). Cuenta
con un selector dinámico para desviar el flujo según el rol del usuario
(Estudiante u Orientador Escolar). El formulario de registro solicita
datos de entrada clave como nombre completo, edad, establecimiento
educativo y curso correspondiente.

> ![](media/image6.png){width="5.940277777777778in"
> height="3.0381944444444446in"}

**\**

### 3.6.2 Pantalla del Panel Principal del Estudiante (Dashboard)

Una vez autenticado, el estudiante accede a un panel intuitivo y lúdico
que le da la bienvenida y le muestra el estado actual de su proceso
guiado por el motor BPM Camunda. Si es su primera navegación, se
despliega un botón destacado con la acción \"Iniciar Evaluación
Vocacional\". Si posee registros previos, el panel expone un acceso
directo a su historial de perfiles guardados.

![](media/image7.png){width="5.940277777777778in"
height="3.5118055555555556in"}

**\**

### 3.6.3 Pantalla del Cuestionario Big Five (BFI-44)

La pantalla presentará los 44 ítems de la versión en español elegida, en
una secuencia paginada con cinco opciones de respuesta por ítem. Se
conservarán el orden y la numeración utilizados por la clave de
puntuación. Cada ítem deberá responderse antes de generar el resultado,
de modo que la media de cada dimensión se calcule sobre todos sus ítems
(Benet-Martínez & John, 1998; Berkeley Personality Lab, s. f.).

Puntuación de las dimensiones: los ítems inversos son 6, 21 y 31 para
extraversión; 2, 12, 27 y 37 para amabilidad; 8, 18, 23 y 43 para
responsabilidad; 9, 24 y 34 para neuroticismo; y 35 y 41 para apertura.
Cada respuesta inversa se transforma mediante 6 − respuesta. Luego se
promedian, respectivamente, 8, 9, 9, 8 y 10 ítems por dimensión, según
la clave del BFI-44. La correspondencia entre esta numeración y los
enunciados en español se verificará antes de la implementación (Berkeley
Personality Lab, s. f.; John & Srivastava, 1999).

![](media/image8.png){width="5.940277777777778in"
height="3.956521216097988in"}

**\**

### 3.6.4 Pantalla de Reporte Vocacional Enriquecido

El reporte propuesto mostrará los cinco promedios del BFI-44, cada uno
entre 1 y 5, junto con un gráfico de radar y una explicación breve de
cada dimensión. El cálculo base utiliza neuroticismo; si la interfaz
muestra «estabilidad emocional», ese valor se obtendrá como 6 menos el
promedio de neuroticismo y se identificará como una transformación para
facilitar la lectura. Los resultados describen respuestas al
cuestionario y no equivalen a un diagnóstico ni a una recomendación
automática de carrera (Berkeley Personality Lab, s. f.; Lowman, 2022).

Alcance de la interpretación: la versión española publicada fue
estudiada en poblaciones distintas de los escolares chilenos
(Benet-Martínez & John, 1998). La adaptación realizada en Chile utilizó
universitarios y redujo el instrumento a 32 ítems (Lara et al., 2021).
Por ello, el prototipo presentará los puntajes como apoyo al
autoconocimiento y a la conversación con el orientador, sin afirmar
validez psicométrica del BFI-44 para esta población. Adicionalmente, las sugerencias de carreras se basan en metaanálisis sobre la intersección de la personalidad (Cinco Grandes) y los intereses vocacionales (RIASEC) (Barrick et al., 2003; Larson et al., 2002), y deben interpretarse únicamente como tendencias exploratorias.

![](media/image9.png){width="5.940277777777778in"
height="4.147916666666666in"}![](media/image10.png){width="5.940277777777778in"
height="3.4479166666666665in"}![](media/image11.png){width="5.940277777777778in"
height="4.147916666666666in"}![](media/image12.png){width="5.940277777777778in"
height="3.7930555555555556in"}

**\**

### 3.6.5 Pantalla del Panel de Administración del Orientador

El panel del orientador reúne la lista de estudiantes asignados, su
curso, el estado del proceso y los resultados disponibles. La consulta
del historial y los filtros mostrados en el prototipo deberán vincularse
con requerimientos aprobados antes de considerarse funcionalidades
comprometidas del MVP.

# ![](media/image3.png){width="5.940277777777778in" height="3.5076388888888888in"}

[\
]{.mark}

# CAPÍTULO IV: DISCUSIÓN DE RESULTADOS

## 4.1 Ingeniería de Requerimientos y Casos de Uso

Los requerimientos se organizan según los actores Estudiante y
Orientador; cualquier función de administración deberá especificarse
como requerimiento adicional si se mantiene en el MVP. Los casos de uso
permiten revisar qué actor realiza cada acción y vincularla con los
objetivos, los componentes diseñados y los escenarios de prueba.

Diagrama de casos de uso.

**Diagrama de actividades.**

![](media/image13.png){width="3.7296872265966754in"
height="5.552858705161855in"}

**\**

## 4.2 Modelos de Procesos, Datos y Arquitectura del Sistema

Los modelos incluidos en esta sección representan el flujo de
orientación, la organización de los datos y los componentes de la
aplicación. Su descripción permite relacionar cada diseño con los
requerimientos y revisar la coherencia entre proceso, persistencia e
interfaces.

### 4.2.1 Diagrama de Procesos BPMN Completo (Orquestación Camunda 8)

El diagrama BPMN representa las tareas del estudiante y del sistema, los
eventos y las decisiones asociadas al avance de la evaluación. Sirve
como base para definir los estados que la aplicación registrará y
mostrará al orientador (Camunda, s. f.).

![](media/image14.png){width="5.940277777777778in"
height="1.8880982064741907in"}

![](media/image15.png){width="6.273305993000875in"
height="1.4767443132108486in"}**\**

### 4.2.2 Diagrama Entidad-Relación (DER) de la Base de Datos

El diagrama entidad-relación muestra las entidades y relaciones
previstas para almacenar usuarios, evaluaciones, preguntas, respuestas,
reportes y estados del proceso. Su revisión debe comprobar que cada dato
requerido por las funcionalidades y las pruebas tenga una ubicación y
una relación definidas.

![](media/image16.png){width="3.9368055555555554in"
height="6.711805555555555in"}**\**

### 4.2.3 Diagrama de Clases UML del Sistema

![](media/image17.png){width="5.345099518810149in"
height="7.278261154855643in"}

**\**

### 4.2.4 Diagrama de Componentes y Despliegue Físico

![](media/image18.png){width="5.920606955380578in"
height="4.160869422572178in"}

![](media/image19.png){width="5.938888888888889in"
height="5.6090277777777775in"}

**\**

[]{#_Toc241354898 .anchor}**REFERENCIAS BIBLIOGRÁFICAS**

Barrick, M. R., Mount, M. K., & Gupta, R. (2003). Meta-analysis of the relationship between the Five-Factor Model of personality and Holland's occupational types. *Personnel Psychology, 56*(1), 45-74. https://doi.org/10.1111/j.1744-6570.2003.tb00143.x

Benet-Martínez, V., & John, O. P. (1998). Los Cinco Grandes across
cultures and ethnic groups: Multitrait-multimethod analyses of the Big
Five in Spanish and English. *Journal of Personality and Social
Psychology, 75*(3), 729--750. https://doi.org/10.1037/0022-3514.75.3.729

Berkeley Personality Lab. (s. f.). *Big Five Inventory (BFI-44)*
\[Cuestionario e instrucciones de puntuación\].
https://www.ocf.berkeley.edu/\~johnlab/docs.php?file=BFI-44.pdf

Camunda. (s. f.). *Processes*. Camunda 8 Docs.
https://docs.camunda.io/docs/components/concepts/processes/

FastAPI. (s. f.). *FastAPI*. https://fastapi.tiangolo.com/

John, O. P., & Srivastava, S. (1999). The Big Five trait taxonomy:
History, measurement, and theoretical perspectives. En L. A. Pervin & O.
P. John (Eds.), *Handbook of personality: Theory and research* (2.ª ed.,
pp. 102--138). Guilford Press.

Lara, L., Monje, M. F., Fuster-Villaseca, J., & Dominguez-Lara, S.
(2021). Adaptación y validación del Big Five Inventory para estudiantes
universitarios chilenos. *Revista Mexicana de Psicología, 38*(2),
83--94.

Larson, L. M., Rottinghaus, P. J., & Borgen, F. H. (2002). Meta-analyses of Big Six Interests and Big Five Personality Factors. *Journal of Vocational Behavior, 61*(2), 217-239. https://doi.org/10.1006/jvbe.2001.1854

Lowman, R. L. (2022). *Career assessment: Integrating interests,
abilities, and personality*. American Psychological Association.
https://doi.org/10.1037/0000254-000

Ministerio de Educación de Chile. (2024). *Taller de orientación:
Decisión vocacional y proyecto de vida*. Currículum Nacional.
https://www.curriculumnacional.cl/recursos/taller-orientacion-decision-vocacional-proyecto-vida

Pressman, R. S., & Maxim, B. R. (2020). *Software engineering: A practitioner's approach* (9th ed.). McGraw-Hill Education.

Project Management Institute. (2021). *A guide to the project management
body of knowledge (PMBOK guide)* (7th ed.).

Schwaber, K., & Sutherland, J. (2020). *The Scrum guide: The definitive
guide to Scrum: The rules of the game*.
https://scrumguides.org/scrum-guide.html

# 

# GLOSARIO

- API REST (Representational State Transfer Application Programming
  Interface): interfaz mediante la cual el frontend realiza solicitudes
  HTTP al backend.

- ASGI (Asynchronous Server Gateway Interface): especificación de
  interfaz entre aplicaciones web Python y servidores compatibles, como
  Uvicorn.

- **Axios:** Librería de JavaScript basada en promesas encargada de
  gestionar y ejecutar solicitudes HTTP desde el cliente hacia la API de
  backend de manera optimizada y asíncrona.

- BFI-44 (Big Five Inventory de 44 ítems): cuestionario de autoinforme
  para describir cinco dimensiones amplias de personalidad. La versión
  en español, su numeración y sus reglas de puntuación deben
  identificarse antes de la aplicación digital (Benet-Martínez & John,
  1998; Berkeley Personality Lab, s. f.).

- BPM (Business Process Management): enfoque para modelar, ejecutar y
  revisar procesos de trabajo.

- **BPMN (Business Process Model and Notation):** Estándar gráfico
  internacional de modelado que provee una notación de diagramación en
  carriles (*lanes*) para representar visualmente las etapas operativas
  y lógicas de un proceso de negocio.

- **CachyOS:** Sistema operativo basado en la distribución Arch Linux,
  optimizado a nivel de kernel y compilación de paquetes para entregar
  una baja latencia y alto rendimiento en el ambiente de desarrollo
  local.

- Camunda 8: plataforma de orquestación que permite ejecutar procesos
  modelados en BPMN y registrar el avance de sus instancias (Camunda, s.
  f.).

- **Escala Likert:** Herramienta de medición psicométrica psicológica
  que mide actitudes o respuestas en un gradiente lineal de opciones,
  implementada en este software en una matriz obligatoria de 5 puntos de
  valoración.

- FastAPI: framework de Python para construir API con documentación
  interactiva generada a partir de sus endpoints (FastAPI, s. f.).

- JWT (JSON Web Token): formato de token firmado que permite transportar
  declaraciones de identidad; su contenido no queda cifrado
  automáticamente.

- **MVP (Minimum Viable Product / Producto Mínimo Viable):** Versión
  inicial y acotada de un producto de software que reúne las
  funcionalidades esenciales y críticas para ser desplegado de forma
  operativa cumpliendo con los estándares de calidad definidos.

- **MySQL 8.0:** Sistema de gestión de bases de datos relacionales
  (*RDBMS*) de código abierto, utilizado para la persistencia e
  integridad estructural de la información transaccional del
  perfilamiento estudiantil.

- OCEAN: acrónimo de Openness (apertura), Conscientiousness
  (responsabilidad), Extraversion (extraversión), Agreeableness
  (amabilidad) y Neuroticism (neuroticismo). Si se informa estabilidad
  emocional, se debe aclarar su relación inversa con neuroticismo.

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
