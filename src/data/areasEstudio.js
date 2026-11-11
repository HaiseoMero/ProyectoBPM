// Información complementaria para las áreas que entrega el backend
// (backend/app/routers/reporte.py). Se cruza por título exacto del área y
// nombre de la carrera; si algo no coincide, el reporte se muestra igual,
// solo sin el contenido extra.
//
// Fuentes (consultadas el 2026-11-04): mifuturo.cl (Mineduc), buscador de
// carreras, y perfiles institucionales enlazados en `fuentes`.
// - Imágenes: Wikimedia Commons (CC0, dominio público, CC BY, CC BY-SA),
//   guardadas en public/areas/ con autoría y licencia en cada entrada.

export const AREAS = {
  "Tecnología, Ciencias Básicas y Agropecuaria": {
    "queSeEstudia": "Este campo reúne disciplinas que estudian la naturaleza, la vida y los sistemas productivos mediante la observación, la experimentación y el razonamiento matemático. También abarca el desarrollo de tecnologías y soluciones aplicadas, desde el software hasta la producción agrícola sostenible.",
    "habilidades": [
      "Razonamiento lógico-matemático",
      "Método científico y experimentación",
      "Análisis de datos",
      "Programación y uso de herramientas digitales",
      "Trabajo en terreno y laboratorio"
    ],
    "campoLaboral": [
      "Empresas de tecnología y servicios digitales",
      "Centros de investigación y universidades",
      "Sector agrícola, forestal y agroindustrial",
      "Observatorios y organismos científicos"
    ],
    "image": {
      "file": "img/area-1.jpg",
      "author": "ESO/C. Malin",
      "license": "CC BY 4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/4.0",
      "source": "https://commons.wikimedia.org/wiki/File:ALMA_antennas_on_Chajnantor_(malin-dsc0027).jpg"
    },
    "carreras": [
      {
        "nombre": "Ingeniería Informática",
        "descripcion": "Quienes la ejercen analizan, diseñan, desarrollan y mantienen sistemas de software e infraestructura informática para organizaciones de distintos sectores.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=531&pagina=0",
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=480&pagina=0",
          "https://admision.udla.cl/wp-content/uploads/2025/10/UDLA_PE_202510_81_0.pdf"
        ],
        "image": {
          "file": "img/ingenieria-informatica.jpg",
          "author": "Markus Spiske",
          "license": "CC0",
          "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          "source": "https://commons.wikimedia.org/wiki/File:Code_on_computer_monitor_(Unsplash).jpg",
          "alt": "Pantalla con líneas de código de programación"
        }
      },
      {
        "nombre": "Biología",
        "descripcion": "En esta carrera se estudian los seres vivos, desde las moléculas y células hasta los ecosistemas, con énfasis en la investigación científica.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=105&pagina=0",
          "https://www.uchile.cl/carreras/4959/licenciatura-en-ciencias-mencion-en-biologia"
        ],
        "image": {
          "file": "img/biologia.jpg",
          "author": "Nulu iman",
          "license": "CC BY-SA 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Isolation_of_zebra_fish_brain.JPG",
          "alt": "Investigadora observando una muestra en un microscopio de laboratorio"
        }
      },
      {
        "nombre": "Agronomía",
        "descripcion": "Quienes la ejercen diseñan y gestionan sistemas de producción agrícola y pecuaria considerando aspectos técnicos, ambientales y económicos.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=36&pagina=0",
          "https://www.uchile.cl/carreras/4964/ingenieria-agronomica"
        ],
        "image": {
          "file": "img/agronomia.jpg",
          "author": "USDA",
          "license": "Public domain",
          "licenseUrl": null,
          "source": "https://commons.wikimedia.org/wiki/File:Soil_Health_(20220420-NRCS-UNK-002).jpg",
          "alt": "Profesionales conversando en medio de un cultivo agrícola"
        }
      },
      {
        "nombre": "Astronomía",
        "descripcion": "En esta carrera se estudian el origen, la composición y la evolución de los astros y del universo, con una base sólida en física y matemática.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=658&pagina=0",
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=66&pagina=0",
          "https://www.uchile.cl/carreras/4980/astronomia"
        ],
        "image": {
          "file": "img/astronomia.jpg",
          "author": "ESO",
          "license": "CC BY 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Big_and_bigger_telescopes_(eso-paranal-vlt).jpg",
          "alt": "Telescopios del Observatorio Paranal en el desierto de Atacama"
        }
      }
    ]
  },
  "Arte, Arquitectura y Humanidades (Comunicaciones)": {
    "queSeEstudia": "Este campo estudia la creación, el diseño y la comunicación de ideas, espacios y mensajes, combinando sensibilidad estética con conocimiento técnico. Incluye disciplinas que proyectan el entorno construido y otras que producen y gestionan información para distintos públicos.",
    "habilidades": [
      "Expresión visual y creatividad",
      "Comunicación oral y escrita",
      "Pensamiento espacial",
      "Manejo de software de diseño y edición",
      "Investigación y análisis de información"
    ],
    "campoLaboral": [
      "Oficinas de arquitectura y estudios de diseño",
      "Medios de comunicación y agencias",
      "Áreas de comunicaciones de empresas e instituciones",
      "Ejercicio independiente de la profesión"
    ],
    "image": {
      "file": "img/area-2.jpg",
      "author": "Jorgebarrios",
      "license": "CC BY-SA 4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
      "source": "https://commons.wikimedia.org/wiki/File:Museo_Nacional_de_Bellas_Artes_de_Chile_(92025).jpg"
    },
    "carreras": [
      {
        "nombre": "Arquitectura",
        "descripcion": "Quienes la ejercen proyectan y diseñan edificios y espacios urbanos, considerando su función, su entorno y su construcción.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=55&pagina=0",
          "https://www.uchile.cl/carreras/4928/arquitectura"
        ],
        "image": {
          "file": "img/arquitectura.jpg",
          "author": "Designer Mario Kleff",
          "license": "CC BY-SA 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Scale_Architectural_Model_of_a_Mario_Kleff_Design_01.jpg",
          "alt": "Maqueta de una vivienda con jardín y piscina"
        }
      },
      {
        "nombre": "Diseño Gráfico",
        "descripcion": "En esta carrera se estudia cómo crear piezas visuales, como identidades gráficas, publicaciones e interfaces, para comunicar mensajes.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=203&pagina=0",
          "https://www.udla.cl/descargas/arquitectura/PERFIL-DE-EGRESO-DISENO-GRAFICO.pdf"
        ],
        "image": {
          "file": "img/diseno-grafico.jpg",
          "author": "Claireneon",
          "license": "CC BY-SA 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Logo_designer_using_pen_and_paper.jpg",
          "alt": "Mano dibujando bocetos de logotipos sobre papel"
        }
      },
      {
        "nombre": "Periodismo",
        "descripcion": "Quienes la ejercen investigan, verifican y difunden información de interés público a través de distintos medios y formatos.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=893&pagina=0",
          "https://www.uchile.cl/carreras/5025/periodismo"
        ],
        "image": {
          "file": "img/periodismo.jpg",
          "author": "Apdency",
          "license": "CC0",
          "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          "source": "https://commons.wikimedia.org/wiki/File:Interview_Telegraaf_TV.jpg",
          "alt": "Periodista entrevistando con micrófono y cámara"
        }
      },
      {
        "nombre": "Relaciones Públicas",
        "descripcion": "Quienes la ejercen planifican y gestionan la comunicación entre las organizaciones y sus públicos, como clientes, comunidades o medios.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1022&pagina=0",
          "https://www.ust.cl/web/wp-content/uploads/sites/6/2016/03/Perfil-de-Egreso-Relaciones-Publicas-UST-2021.pdf"
        ],
        "image": {
          "file": "img/relaciones-publicas.jpg",
          "author": "USDA",
          "license": "Public domain",
          "licenseUrl": null,
          "source": "https://commons.wikimedia.org/wiki/File:2013_Agricultural_Outlook_Forum_(20130222-OSEC-LSC-0478).jpg",
          "alt": "Personas conversando en un evento de networking"
        }
      }
    ]
  },
  "Ciencias Sociales y Humanidades": {
    "queSeEstudia": "Este campo estudia el comportamiento de las personas, los grupos y las sociedades, así como las culturas y las relaciones que se dan entre ellos. Combina la investigación con la intervención en contextos individuales, comunitarios e institucionales.",
    "habilidades": [
      "Comprensión de fenómenos sociales",
      "Escucha activa y entrevista",
      "Investigación cualitativa y cuantitativa",
      "Pensamiento crítico",
      "Trabajo con comunidades"
    ],
    "campoLaboral": [
      "Servicios públicos y municipios",
      "Organizaciones sociales y fundaciones",
      "Centros de salud y establecimientos educacionales",
      "Consultoras e instituciones de investigación"
    ],
    "image": {
      "file": "img/area-3.jpg",
      "author": "Pablo García Saldaña",
      "license": "CC0",
      "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
      "source": "https://commons.wikimedia.org/wiki/File:Skyline_of_Santiago,_Chile.jpg"
    },
    "carreras": [
      {
        "nombre": "Psicología",
        "descripcion": "En esta carrera se estudian los procesos mentales y el comportamiento humano, y quienes la ejercen trabajan en ámbitos como el clínico, el educacional, el organizacional y el comunitario.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1002&pagina=0",
          "https://www.uchile.cl/carreras/4992/psicologia"
        ],
        "image": {
          "file": "img/psicologia.jpg",
          "author": "Jty33",
          "license": "CC BY-SA 3.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/3.0",
          "source": "https://commons.wikimedia.org/wiki/File:Psychotherapy.JPG",
          "alt": "Sesión de psicoterapia en un consultorio"
        }
      },
      {
        "nombre": "Sociología",
        "descripcion": "Quienes la ejercen investigan y analizan cómo se organizan las sociedades, sus instituciones y sus cambios, para aportar al diseño de políticas y programas.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1027&pagina=0",
          "https://www.uchile.cl/carreras/4991/sociologia"
        ],
        "image": {
          "file": "img/sociologia.jpg",
          "author": "Ngozi Stella Udechukwu",
          "license": "CC BY-SA 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Focus_Group_Discussion_in_Enugu_North.jpg",
          "alt": "Grupo focal de investigación conversando en una sala"
        }
      },
      {
        "nombre": "Antropología",
        "descripcion": "En esta carrera se estudian la diversidad cultural y las formas de vida humanas, en el presente y en el pasado, mediante trabajo de campo.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=51&pagina=0",
          "https://www.uchile.cl/carreras/4990/antropologia-arqueologia"
        ],
        "image": {
          "file": "img/antropologia.jpg",
          "author": "Oertherdb",
          "license": "CC BY-SA 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Daniel_Oerther_and_students_conducting_a_household_interview_in_rural_Gujarat.JPG",
          "alt": "Entrevista de trabajo de campo con una familia en su vivienda"
        }
      },
      {
        "nombre": "Trabajo Social",
        "descripcion": "Quienes la ejercen intervienen junto a personas, familias y comunidades para abordar problemas sociales y facilitar el acceso a derechos y recursos.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1559&pagina=0",
          "https://www.uchile.cl/carreras/105708/trabajo-social"
        ],
        "image": {
          "file": "img/trabajo-social.jpg",
          "author": "Robert Kaufmann",
          "license": "Public domain",
          "licenseUrl": null,
          "source": "https://commons.wikimedia.org/wiki/File:FEMA_-_21803_-_Photograph_by_Robert_Kaufmann_taken_on_01-26-2006_in_Louisiana.jpg",
          "alt": "Equipo de trabajo comunitario revisando materiales"
        }
      }
    ]
  },
  "Administración, Comercio y Derecho": {
    "queSeEstudia": "Este campo estudia cómo se organizan y gestionan las empresas, el Estado y los recursos económicos, y cómo se regulan las relaciones entre personas e instituciones. Incluye la economía, las finanzas, la contabilidad y el sistema jurídico.",
    "habilidades": [
      "Análisis financiero y económico",
      "Argumentación y redacción",
      "Planificación y gestión",
      "Interpretación de normas",
      "Negociación y toma de decisiones"
    ],
    "campoLaboral": [
      "Empresas privadas de distintos rubros",
      "Servicios públicos y municipios",
      "Estudios jurídicos y tribunales",
      "Bancos, auditoras y consultoras"
    ],
    "image": {
      "file": "img/area-4.jpg",
      "author": "Jimmy Baikovicius",
      "license": "CC BY-SA 2.0",
      "licenseUrl": "https://creativecommons.org/licenses/by-sa/2.0",
      "source": "https://commons.wikimedia.org/wiki/File:Sanhattan_skyline.jpg"
    },
    "carreras": [
      {
        "nombre": "Ingeniería Comercial",
        "descripcion": "En esta carrera se estudian la economía y la administración de empresas, y quienes la ejercen trabajan en áreas como finanzas, marketing, operaciones o gestión de personas.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=370&pagina=0",
          "https://www.uchile.cl/carreras/4966/ingenieria-comercial"
        ],
        "image": {
          "file": "img/ingenieria-comercial.jpg",
          "author": "helloquence",
          "license": "CC0",
          "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          "source": "https://commons.wikimedia.org/wiki/File:Helloquence-61189.jpg",
          "alt": "Personas revisando documentos y planillas junto a un computador"
        }
      },
      {
        "nombre": "Derecho",
        "descripcion": "Quienes la ejercen interpretan y aplican las normas jurídicas para asesorar, representar a personas e instituciones o resolver conflictos.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=174&pagina=0",
          "https://www.uchile.cl/carreras/4997/derecho"
        ],
        "image": {
          "file": "img/derecho.jpg",
          "author": "Joe Gratz",
          "license": "CC0",
          "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          "source": "https://commons.wikimedia.org/wiki/File:Courtroom_One_Gavel_-_Flickr_-_Joe_Gratz.jpg",
          "alt": "Mazo de juez sobre un escritorio"
        }
      },
      {
        "nombre": "Administración Pública",
        "descripcion": "Quienes la ejercen diseñan, gestionan y evalúan políticas, programas y servicios del Estado y de los gobiernos locales.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=24&pagina=0",
          "https://www.uchile.cl/carreras/5049/administracion-publica"
        ],
        "image": {
          "file": "img/administracion-publica.jpg",
          "author": "Rodrigo Fernández",
          "license": "CC BY-SA 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:Pza_Constitucion_-palacio_La_Moneda_fachada_norte_-fRF01_20171203.jpg",
          "alt": "Fachada del Palacio de La Moneda en Santiago"
        }
      },
      {
        "nombre": "Auditoría",
        "descripcion": "En Chile suele estudiarse como Contador Auditor; quienes la ejercen elaboran, analizan y revisan la información contable y financiera de las organizaciones.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=157&pagina=0",
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=168&pagina=0",
          "https://www.uchile.cl/carreras/86759/contador-auditor"
        ],
        "image": {
          "file": "img/auditoria.jpg",
          "author": "Dave Dugdale from Superior, USA",
          "license": "CC BY-SA 2.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/2.0",
          "source": "https://commons.wikimedia.org/wiki/File:Analyzing_Financial_Data_(5099605109).jpg",
          "alt": "Mano revisando cifras con una calculadora"
        }
      }
    ]
  },
  "Salud (Gestión y Cuidados) y Agropecuaria": {
    "queSeEstudia": "Este campo estudia el funcionamiento del cuerpo humano y animal, y cómo prevenir, diagnosticar y tratar enfermedades. Combina conocimientos de ciencias biológicas con formación práctica en entornos clínicos y de atención.",
    "habilidades": [
      "Conocimiento de ciencias biológicas",
      "Observación y razonamiento clínico",
      "Trabajo en equipos de salud",
      "Comunicación con pacientes",
      "Manejo de procedimientos y equipos"
    ],
    "campoLaboral": [
      "Hospitales y clínicas",
      "Centros de atención primaria (CESFAM)",
      "Laboratorios clínicos y centros de diagnóstico",
      "Clínicas veterinarias y sector agropecuario"
    ],
    "image": {
      "file": "img/area-5.jpg",
      "author": "Carlos Figueroa Rojas",
      "license": "CC BY-SA 4.0",
      "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
      "source": "https://commons.wikimedia.org/wiki/File:Hospital_Cl%C3%ADnico_de_la_Universidad_de_Chile,_Independencia,_Santiago_20230817_06.jpg"
    },
    "carreras": [
      {
        "nombre": "Medicina",
        "descripcion": "Quienes la ejercen previenen, diagnostican y tratan enfermedades, brindando atención a las personas en las distintas etapas de la vida.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=730&pagina=0",
          "https://www.uchile.cl/carreras/5013/medicina"
        ],
        "image": {
          "file": "img/medicina.jpg",
          "author": "Unknown photographer",
          "license": "Public domain",
          "licenseUrl": null,
          "source": "https://commons.wikimedia.org/wiki/File:Doctor_examines_patient_with_stethoscope_(2).jpg",
          "alt": "Médico auscultando a un paciente junto a su equipo"
        }
      },
      {
        "nombre": "Enfermería",
        "descripcion": "Quienes la ejercen gestionan y entregan cuidados a personas, familias y comunidades, en la atención clínica y en la promoción de la salud.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=238&pagina=0",
          "https://www.uchile.cl/carreras/5010/enfermeria"
        ],
        "image": {
          "file": "img/enfermeria.jpg",
          "author": "Holly Northam",
          "license": "CC BY-SA 3.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/3.0",
          "source": "https://commons.wikimedia.org/wiki/File:Simulating_care_of_the_critically_ill_child.JPG",
          "alt": "Enfermera realizando un procedimiento de simulación clínica"
        }
      },
      {
        "nombre": "Tecnología Médica",
        "descripcion": "Quienes la ejercen realizan exámenes y procedimientos que apoyan el diagnóstico y el tratamiento, en menciones como laboratorio clínico, imagenología u oftalmología.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1547&pagina=0",
          "https://www.uchile.cl/carreras/5017/tecnologia-medica"
        ],
        "image": {
          "file": "img/tecnologia-medica.jpg",
          "author": "Goleisureintl",
          "license": "CC BY 4.0",
          "licenseUrl": "https://creativecommons.org/licenses/by/4.0",
          "source": "https://commons.wikimedia.org/wiki/File:NABL_Accredited_Pathology_Lab_and_Diagnostic_Centre_in_Kharghar,_Navi_Mumbai_-_Full_Body_Checkup,_CBC,_Thyroid_Blood_Test_and_Home_Blood_Collection.jpg",
          "alt": "Muestra de sangre en una centrífuga de laboratorio"
        }
      },
      {
        "nombre": "Medicina Veterinaria",
        "descripcion": "En esta carrera se estudian la salud y el bienestar de los animales, y quienes la ejercen trabajan en clínica, producción animal y salud pública.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=731&pagina=0",
          "https://www.uchile.cl/carreras/4996/medicina-veterinaria"
        ],
        "image": {
          "file": "img/medicina-veterinaria.jpg",
          "author": "Nenad Stojkovic",
          "license": "CC BY 2.0",
          "licenseUrl": "https://creativecommons.org/licenses/by/2.0",
          "source": "https://commons.wikimedia.org/wiki/File:Close-up_of_a_veterinarian_examining_a_maltese_dog_with_a_stethoscope._(51687314898).jpg",
          "alt": "Veterinaria examinando a un perro pequeño"
        }
      }
    ]
  },
  "Educación y Salud (Atención Comunitaria)": {
    "queSeEstudia": "Este campo estudia los procesos de aprendizaje y desarrollo de las personas, y cómo acompañarlos desde la enseñanza y la rehabilitación. Reúne carreras que trabajan directamente con niños, jóvenes, adultos y comunidades.",
    "habilidades": [
      "Comunicación y empatía",
      "Planificación de actividades",
      "Observación y evaluación",
      "Trabajo con familias y comunidades",
      "Trabajo interdisciplinario"
    ],
    "campoLaboral": [
      "Colegios, liceos y jardines infantiles",
      "Centros de salud y rehabilitación",
      "Programas comunitarios y municipales",
      "Consultas particulares"
    ],
    "image": {
      "file": "img/area-6.jpg",
      "author": "Sisib Universidad de Chile",
      "license": "CC BY 2.0",
      "licenseUrl": "https://creativecommons.org/licenses/by/2.0",
      "source": "https://commons.wikimedia.org/wiki/File:Casa_Central_de_la_Universidad_de_Chile.jpg"
    },
    "carreras": [
      {
        "nombre": "Pedagogía",
        "descripcion": "Quienes la ejercen planifican, enseñan y evalúan procesos de aprendizaje en establecimientos educacionales, según el nivel o la asignatura de su especialidad.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=776&pagina=0",
          "https://www.uchile.cl/carreras/105478/pedagogia-en-educacion-basica"
        ],
        "image": {
          "file": "img/pedagogia.jpg",
          "author": "Preply.com Images",
          "license": "CC BY 2.0",
          "licenseUrl": "https://creativecommons.org/licenses/by/2.0",
          "source": "https://commons.wikimedia.org/wiki/File:Maths_Tutor.jpg",
          "alt": "Docente explicando contenidos de matemáticas en una pizarra"
        }
      },
      {
        "nombre": "Educación Parvularia",
        "descripcion": "Quienes la ejercen diseñan y conducen experiencias de aprendizaje para niñas y niños desde el nacimiento hasta los seis años, en conjunto con sus familias.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=783&pagina=0",
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=837&pagina=0",
          "https://www.uchile.cl/carreras/105700/pedagogia-en-educacion-parvularia"
        ],
        "image": {
          "file": "img/educacion-parvularia.jpg",
          "author": "ChinaFlag",
          "license": "Public domain",
          "licenseUrl": null,
          "source": "https://commons.wikimedia.org/wiki/File:Boxwood_PS_kindergarten_classroom.jpg",
          "alt": "Sala de educación parvularia con mesas y material didáctico"
        }
      },
      {
        "nombre": "Fonoaudiología",
        "descripcion": "Quienes la ejercen evalúan y tratan dificultades de la comunicación humana, como el lenguaje, el habla, la voz y la audición, además de la deglución.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=254&pagina=0",
          "https://www.uchile.cl/carreras/5011/fonoaudiologia"
        ],
        "image": {
          "file": "img/fonoaudiologia.jpg",
          "author": "Bundesinnung Hörakustiker (bundesinnung_ha)",
          "license": "CC BY-SA 2.0",
          "licenseUrl": "https://creativecommons.org/licenses/by-sa/2.0",
          "source": "https://commons.wikimedia.org/wiki/File:Audiologist,_2015.jpg",
          "alt": "Evaluación auditiva con audífonos frente a un computador"
        }
      },
      {
        "nombre": "Kinesiología",
        "descripcion": "En esta carrera se estudia el movimiento humano, y quienes la ejercen buscan habilitar, mantener o recuperar la funcionalidad de las personas.",
        "fuentes": [
          "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=644&pagina=0",
          "https://www.uchile.cl/carreras/5012/kinesiologia"
        ],
        "image": {
          "file": "img/kinesiologia.jpg",
          "author": "Shixart1985",
          "license": "CC BY 2.0",
          "licenseUrl": "https://creativecommons.org/licenses/by/2.0",
          "source": "https://commons.wikimedia.org/wiki/File:Physiotherapist_working_examining_treating_injured_leg_of_male_patient.jpg",
          "alt": "Kinesiólogo trabajando en la rehabilitación de una pierna"
        }
      }
    ]
  }
}

// Quita el prefijo exploratorio que agrega el backend ("A modo exploratorio: X").
export function careerName(value) {
  return String(value).replace(/^[^:]+:\s*/, '').trim()
}

function normalize(text) {
  return careerName(text).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
}

function toImage(image, alt) {
  if (!image) return null
  return { src: `/areas/${image.file.replace(/^img\//, '')}`, alt }
}

export function enrichCareerArea(area) {
  const info = AREAS[area.title]
  if (!info) return area
  const careers = info.carreras || []
  const details = (area.carreras || []).map(value => {
    const match = careers.find(c => normalize(c.nombre) === normalize(value))
    if (!match) return null
    return {
      descripcion: match.descripcion,
      link: match.fuentes?.find(url => url.includes('buscador-de-carreras')) || null,
      image: toImage(match.image, match.image?.alt || `Fotografía relacionada con ${match.nombre}`),
      credit: match.image ? { ...match.image, label: match.nombre } : null,
    }
  })
  const credits = [
    info.image && { ...info.image, label: 'Imagen del área' },
    ...details.map(detail => detail?.credit),
  ].filter(Boolean)
  return {
    ...area,
    info: {
      queSeEstudia: info.queSeEstudia,
      habilidades: info.habilidades || [],
      campoLaboral: info.campoLaboral || [],
      image: toImage(info.image, ''),
    },
    details,
    credits,
  }
}
