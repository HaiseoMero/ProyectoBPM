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

// Catálogo extendido para las 12 Áreas de Estudio SIES (Motor Vocacional v2),
// con fotografías dedicadas de resolución 960px en public/areas/ y enlaces de Mineduc.
const todasLasCarreras = Object.values(AREAS).flatMap(a => a.carreras || [])
function findCareer(name) {
  return todasLasCarreras.find(c => c.nombre === name)
}

function buildCareer(nombre, descripcion, link, image) {
  return {
    nombre,
    descripcion,
    fuentes: [link || 'https://www.mifuturo.cl/buscador-de-carreras/'],
    image,
  }
}

Object.assign(AREAS, {
  "Informática, Datos y TI": {
    queSeEstudia: "Reúne disciplinas enfocadas en el desarrollo de software, ciencia de datos, inteligencia artificial, ciberseguridad e infraestructura digital para resolver problemas complejos en todo tipo de organizaciones.",
    habilidades: ["Razonamiento lógico y algorítmico", "Programación y arquitectura de software", "Análisis de datos e IA", "Resolución metódica de problemas"],
    campoLaboral: ["Empresas tecnológicas y startups", "Banca, retail y telecomunicaciones", "Consultoras de TI y ciberseguridad", "Centros de I+D y trabajo remoto global"],
    image: {
      file: "img/area-informatica-ti.jpg",
      author: "SimonWaldherr",
      license: "CC BY-SA 4.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
      source: "https://commons.wikimedia.org/wiki/File:CERN_Computer_Center_02.jpg"
    },
    carreras: [
      { ...findCareer("Ingeniería Informática"), nombre: "Ingeniería Civil Informática" },
      buildCareer(
        "Ciencia de Datos e IA",
        "Forma especialistas en modelamiento estadístico, aprendizaje automático y procesamiento de grandes volúmenes de datos.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=531&pagina=0",
        {
          file: "img/ciencia-de-datos-ia.jpg",
          author: "Luis Llerena",
          license: "CC0",
          licenseUrl: "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          source: "https://commons.wikimedia.org/wiki/File:Analytics_graphs_on_a_MacBook_screen.jpg",
          alt: "Gráficos de análisis de datos y visualización estadística en pantalla"
        }
      ),
      buildCareer(
        "Ciberseguridad",
        "Prepara profesionales para proteger redes, sistemas e información crítica frente a amenazas digitales.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=480&pagina=0",
        {
          file: "img/ciberseguridad.jpg",
          author: "Unknown photographer",
          license: "Public domain",
          licenseUrl: null,
          source: "https://commons.wikimedia.org/wiki/File:NSOC-2012.jpg",
          alt: "Centro de operaciones y monitoreo de seguridad informática"
        }
      ),
      buildCareer(
        "Analista Programador",
        "Carrera técnica y profesional orientada a la construcción, prueba y mantención de aplicaciones web, móviles y empresariales.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=480&pagina=0",
        {
          file: "img/analista-programador.jpg",
          author: "Crew",
          license: "CC0",
          licenseUrl: "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          source: "https://commons.wikimedia.org/wiki/File:Programmer_at_work_(Unsplash).jpg",
          alt: "Desarrollador de software programando en computador portátil"
        }
      )
    ]
  },
  "Ingeniería Civil, Minería y Obras": {
    queSeEstudia: "Aborda el diseño, planificación, construcción y optimización de grandes proyectos de infraestructura, procesos industriales, energía y operaciones mineras.",
    habilidades: ["Planificación y gestión de proyectos", "Cálculo estructural y modelamiento físico", "Liderazgo de equipos en terreno", "Toma de decisiones bajo estándares de seguridad"],
    campoLaboral: ["Compañías mineras y energéticas", "Empresas constructoras y de obras públicas", "Industria manufacturera y logística", "Consultoras de ingeniería y ministerios"],
    image: {
      file: "img/area-ingenieria-mineria-obras.jpg",
      author: "Alexander Gerst",
      license: "CC BY-SA 2.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/2.0",
      source: "https://commons.wikimedia.org/wiki/File:Chuquicamata_copper_mine_-_Chuquicamata-Kupfermine.jpg"
    },
    carreras: [
      buildCareer(
        "Ingeniería Civil en Minas",
        "Forma profesionales para planificar, dirigir y optimizar la extracción y procesamiento sustentable de recursos minerales.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=501&pagina=0",
        {
          file: "img/ingenieria-civil-minas.jpg",
          author: "James St. John",
          license: "CC BY 2.0",
          licenseUrl: "https://creativecommons.org/licenses/by/2.0",
          source: "https://commons.wikimedia.org/wiki/File:Haul_truck_(Continental_Mine,_Butte,_Montana,_USA)_2.jpg",
          alt: "Camión minero de alto tonelaje operando en yacimiento a rajo abierto"
        }
      ),
      buildCareer(
        "Ingeniería Civil Industrial",
        "Integra ciencias de la ingeniería con gestión de operaciones, logística, finanzas y estrategia organizacional.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=495&pagina=0",
        {
          file: "img/ingenieria-civil-industrial.jpg",
          author: "KUKA Roboter GmbH, Bachmann",
          license: "Public domain",
          licenseUrl: null,
          source: "https://commons.wikimedia.org/wiki/File:Factory_Automation_Robotics_Palettizing_Bread.jpg",
          alt: "Línea de producción industrial automatizada con brazos robóticos"
        }
      ),
      buildCareer(
        "Construcción Civil",
        "Prepara especialistas en la ejecución, dirección técnica y control de calidad de obras de edificación e infraestructura.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=156&pagina=0",
        {
          file: "img/construccion-civil.jpg",
          author: "U.S. Air National Guard / Staff Sgt. Brandon Keys",
          license: "Public domain",
          licenseUrl: null,
          source: "https://commons.wikimedia.org/wiki/File:134_Civil_Engineer_Airmen_Conduct_Site_Surveys_in_Korea_(9741411).jpg",
          alt: "Equipo de ingeniería y construcción civil revisando mediciones en terreno"
        }
      ),
      buildCareer(
        "Ingeniería Civil Mecánica / Eléctrica",
        "Se enfoca en el diseño de sistemas de generación eléctrica, automatización, maquinaria industrial y energías renovables.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=492&pagina=0",
        {
          file: "img/ingenieria-mecanica-electrica.jpg",
          author: "Nelson Pérez",
          license: "CC BY-SA 3.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/3.0",
          source: "https://commons.wikimedia.org/wiki/File:Canela_Baja,_Regi%C3%B3n_de_Coquimbo,_Chile_-_panoramio.jpg",
          alt: "Aerogeneradores de parque eólico en Canela Baja, Región de Coquimbo, Chile"
        }
      )
    ]
  },
  "Ciencias Básicas y Exactas": {
    queSeEstudia: "Investiga las leyes fundamentales de la naturaleza, la materia, la vida y el universo mediante el método científico, la matemática avanzada y la experimentación en laboratorio u observatorios.",
    habilidades: ["Pensamiento abstracto y matemático", "Método científico y trabajo de laboratorio", "Observación y análisis riguroso", "Investigación académica y aplicada"],
    campoLaboral: ["Observatorios astronómicos y centros científicos", "Universidades e institutos de investigación", "Laboratorios biotecnológicos y farmacéuticos", "Sector ambiental, minero y de datos"],
    image: AREAS["Tecnología, Ciencias Básicas y Agropecuaria"].image,
    carreras: [
      findCareer("Astronomía"),
      findCareer("Biología"),
      buildCareer(
        "Física",
        "Estudia las propiedades e interacciones fundamentales de la materia y la energía desde la escala cuántica hasta la cosmológica.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=658&pagina=0",
        {
          file: "img/fisica.jpg",
          author: "Gavin Morley",
          license: "CC BY-SA 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Attocube_table_GWMorley.jpg",
          alt: "Mesa óptica con láser experimental en un laboratorio de física"
        }
      ),
      buildCareer(
        "Bioquímica",
        "Analiza los procesos químicos y moleculares de los seres vivos con aplicaciones en salud, biotecnología y genética.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=108&pagina=0",
        {
          file: "img/bioquimica.jpg",
          author: "Thctamm",
          license: "CC BY-SA 3.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/3.0",
          source: "https://commons.wikimedia.org/wiki/File:Biokeemia_labori_laud.JPG",
          alt: "Mesón de laboratorio de bioquímica con micropipetas e instrumental de análisis"
        }
      )
    ]
  },
  "Salud y Terapias": {
    queSeEstudia: "Estudia la prevención, diagnóstico, tratamiento y rehabilitación de la salud física y funcional de las personas, combinando ciencias biomédicas con atención clínica directa.",
    habilidades: ["Razonamiento clínico y precisión", "Empatía y comunicación con pacientes", "Trabajo en equipos multidisciplinarios de salud", "Temple ante situaciones de urgencia"],
    campoLaboral: ["Hospitales públicos y clínicas privadas", "Centros de salud familiar (CESFAM)", "Centros de rehabilitación y laboratorios", "Ejercicio clínico y programas de salud"],
    image: AREAS["Salud (Gestión y Cuidados) y Agropecuaria"].image,
    carreras: [
      findCareer("Medicina"),
      findCareer("Enfermería"),
      findCareer("Kinesiología"),
      findCareer("Tecnología Médica")
    ]
  },
  "Agropecuaria, Veterinaria y Medioambiente": {
    queSeEstudia: "Aborda el cuidado de la salud animal, la producción agroalimentaria sostenible y la conservación de los recursos naturales, bosques y ecosistemas marinos y terrestres.",
    habilidades: ["Trabajo en terreno y contacto con la naturaleza", "Manejo de sistemas biológicos y productivos", "Gestión ambiental y sustentabilidad", "Diagnóstico veterinario y sanitario"],
    campoLaboral: ["Clínicas y hospitales veterinarios", "Empresas agrícolas, frutícolas y forestales", "Organismos ambientales (CONAF, SAG, MMA)", "Centros de conservación y acuicultura"],
    image: {
      file: "img/area-agropecuaria-medioambiente.jpg",
      author: "Delahimalaya-alosandes",
      license: "CC BY-SA 4.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
      source: "https://commons.wikimedia.org/wiki/File:Araucaria_araucana,_Conguill%C3%ADo_National_Park,_Chile.jpg"
    },
    carreras: [
      findCareer("Medicina Veterinaria"),
      findCareer("Agronomía"),
      buildCareer(
        "Ingeniería Forestal",
        "Forma profesionales para la conservación, manejo y restauración de bosques y ecosistemas silvestres.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=524&pagina=0",
        {
          file: "img/ingenieria-forestal.jpg",
          author: "Rmmramos",
          license: "CC BY-SA 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Measuring_Tree_Trunk_Circumference_During_Forest_Fieldwork.jpg",
          alt: "Medición forestal del diámetro de un árbol en terreno"
        }
      ),
      buildCareer(
        "Biología Marina",
        "Estudia la biodiversidad de los océanos y costas, el manejo de recursos hidrobiológicos y la conservación marina.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=106&pagina=0",
        {
          file: "img/biologia-marina.jpg",
          author: "Ray Boland / NOAA/NMFS/PIFD/ESOD",
          license: "Public domain",
          licenseUrl: null,
          source: "https://commons.wikimedia.org/wiki/File:Biological_Technician_Elizabeth_Keenan_swims_past_a_large_Porites_lobata_coralhead_while_conducting_algal_surveys_off_of_Guam_(reef324929763).jpg",
          alt: "Bióloga marina realizando muestreo científico submarino en arrecife"
        }
      )
    ]
  },
  "Administración, Negocios y Finanzas": {
    queSeEstudia: "Se enfoca en la dirección de organizaciones, la economía, las finanzas, la contabilidad, el marketing y el comercio internacional para generar valor de forma sostenible.",
    habilidades: ["Análisis económico y financiero", "Liderazgo y negociación comercial", "Planificación estratégica y control de gestión", "Toma de decisiones basada en indicadores"],
    campoLaboral: ["Empresas privadas de todos los sectores", "Bancos, instituciones financieras y aseguradoras", "Firmas de auditoría y consultoría estratégica", "Emprendimientos y comercio internacional"],
    image: AREAS["Administración, Comercio y Derecho"].image,
    carreras: [
      findCareer("Ingeniería Comercial"),
      findCareer("Auditoría"),
      buildCareer(
        "Ingeniería en Control de Gestión",
        "Se especializa en alinear la estrategia empresarial mediante indicadores de desempeño, presupuestos y análisis de procesos.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=512&pagina=0",
        {
          file: "img/control-de-gestion.jpg",
          author: "rawpixel.com",
          license: "CC0",
          licenseUrl: "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          source: "https://commons.wikimedia.org/wiki/File:Finance_analytics_over_coffee_(Unsplash).jpg",
          alt: "Revisión de indicadores financieros y tableros de control de gestión"
        }
      ),
      buildCareer(
        "Comercio Exterior",
        "Gestiona operaciones de importación, exportación, logística internacional y normativa aduanera.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=141&pagina=0",
        {
          file: "img/comercio-exterior.jpg",
          author: "Downtowngal",
          license: "CC BY-SA 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Container_ship_NYK_Themis_at_the_Port_of_Los_Angeles.jpg",
          alt: "Buque portacontenedores y grúas portuarias de comercio internacional"
        }
      )
    ]
  },
  "Derecho y Gestión Pública": {
    queSeEstudia: "Estudia el sistema jurídico, las leyes, las instituciones del Estado y el diseño y evaluación de políticas públicas para regular la convivencia social y fortalecer la gestión gubernamental.",
    habilidades: ["Argumentación oral y redacción jurídica", "Interpretación de normas y pensamiento crítico", "Negociación y resolución de conflictos", "Gestión de políticas y servicios públicos"],
    campoLaboral: ["Estudios jurídicos, tribunales y fiscalías", "Ministerios, municipalidades y servicios públicos", "Organismos reguladores y parlamento", "Departamentos legales de empresas y ONG"],
    image: {
      file: "img/area-derecho-gestion-publica.jpg",
      author: "Felipe Restrepo Acosta",
      license: "CC BY-SA 4.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
      source: "https://commons.wikimedia.org/wiki/File:2017_Santiago_de_Chile_-_Edificio_de_los_Tribunales_de_Justicia.jpg"
    },
    carreras: [
      findCareer("Derecho"),
      findCareer("Administración Pública"),
      buildCareer(
        "Ciencia Política",
        "Analiza los sistemas políticos, las relaciones internacionales, el poder público y los procesos democráticos.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=133&pagina=0",
        {
          file: "img/ciencia-politica.jpg",
          author: "Carlos Figueroa Rojas",
          license: "CC BY-SA 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Edificio_del_Congreso_Nacional,_Valpara%C3%ADso_20230903_01.jpg",
          alt: "Sede del Congreso Nacional de Chile en Valparaíso"
        }
      ),
      buildCareer(
        "Técnico Jurídico",
        "Apoya la tramitación de causas judiciales, gestión notarial y elaboración de documentos legales.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1458&pagina=0",
        {
          file: "img/tecnico-juridico.jpg",
          author: "Energyme",
          license: "CC BY-SA 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Books_on_Shelf_at_the_Ghalib_Chamber_Law_Library.jpg",
          alt: "Estantería con compendios, códigos y repertorios jurídicos"
        }
      )
    ]
  },
  "Educación y Pedagogías": {
    queSeEstudia: "Aborda los procesos de enseñanza, aprendizaje y desarrollo integral en la infancia, adolescencia y adultez, incluyendo la inclusión educativa y el acompañamiento del lenguaje.",
    habilidades: ["Comunicación pedagógica y liderazgo de aula", "Empatía, paciencia y escucha activa", "Diseño de experiencias de aprendizaje", "Trabajo colaborativo con familias y equipos"],
    campoLaboral: ["Colegios, liceos e instituciones de educación", "Jardines infantiles y salas cuna", "Programas de integración escolar (PIE)", "Centros de diagnóstico y apoyo psicopedagógico"],
    image: AREAS["Educación y Salud (Atención Comunitaria)"].image,
    carreras: [
      findCareer("Pedagogía"),
      findCareer("Educación Parvularia"),
      findCareer("Fonoaudiología"),
      buildCareer(
        "Educación Diferencial",
        "Forma docentes especializados en inclusión educativa y apoyos para estudiantes con necesidades educativas especiales.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=782&pagina=0",
        {
          file: "img/educacion-diferencial.jpg",
          author: "DFID",
          license: "CC BY 2.0",
          licenseUrl: "https://creativecommons.org/licenses/by/2.0",
          source: "https://commons.wikimedia.org/wiki/File:A_Lebanese_teacher_lends_a_hand_to_Syrian_children_in_Zaatari,_Jordan.jpg",
          alt: "Docente acompañando de forma personalizada el aprendizaje en el aula"
        }
      )
    ]
  },
  "Psicología y Ciencias Sociales": {
    queSeEstudia: "Comprende el comportamiento humano, los procesos mentales, las dinámicas familiares y comunitarias y las estructuras sociales y culturales.",
    habilidades: ["Escucha activa y entrevista clínica/social", "Empatía y ética en el acompañamiento", "Investigación cualitativa y cuantitativa", "Intervención comunitaria y organizacional"],
    campoLaboral: ["Consultas psicológicas y centros de salud mental", "Programas sociales, municipios y fundaciones", "Áreas de desarrollo organizacional y convivencia escolar", "Centros de estudios sociales y universidades"],
    image: AREAS["Ciencias Sociales y Humanidades"].image,
    carreras: [
      findCareer("Psicología"),
      findCareer("Trabajo Social"),
      findCareer("Sociología"),
      findCareer("Antropología")
    ]
  },
  "Comunicaciones, Turismo y Gastronomía": {
    queSeEstudia: "Integra la creación y gestión de contenidos informativos, publicitarios y audiovisuales con la hospitalidad, la gastronomía y las experiencias culturales y turísticas.",
    habilidades: ["Expresión oral, escrita y audiovisual", "Relacionamiento interpersonal y trabajo en red", "Creatividad aplicada a campañas y servicios", "Adaptabilidad en entornos dinámicos"],
    campoLaboral: ["Medios de comunicación, productoras y agencias", "Áreas de comunicación corporativa y marketing", "Hotelería, operadores turísticos y eventos", "Restaurantes, proyectos gastronómicos y culturales"],
    image: {
      file: "img/area-comunicaciones-turismo.jpg",
      author: "Alex Proimos from Sydney, Australia",
      license: "CC BY 2.0",
      licenseUrl: "https://creativecommons.org/licenses/by/2.0",
      source: "https://commons.wikimedia.org/wiki/File:On_the_Hill,_Valpara%C3%ADso_(Valparaiso),_Chile_(3927311373).jpg"
    },
    carreras: [
      findCareer("Periodismo"),
      findCareer("Relaciones Públicas"),
      buildCareer(
        "Publicidad",
        "Diseña estrategias creativas, campañas multimediales y posicionamiento de marcas para conectar con distintos públicos.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1004&pagina=0",
        {
          file: "img/publicidad.jpg",
          author: "Ndahiro derrick",
          license: "CC BY 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by/4.0",
          source: "https://commons.wikimedia.org/wiki/File:WLM_international_team_meeting_in_Lagos_01.jpg",
          alt: "Equipo creativo planificando una campaña de comunicación y publicidad"
        }
      ),
      buildCareer(
        "Gastronomía Internacional",
        "Forma profesionales en artes culinarias, gestión de cocinas, patrimonio alimentario y administración gastronómica.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=26&pagina=0",
        {
          file: "img/gastronomia-internacional.jpg",
          author: "Michael Browning",
          license: "CC0",
          licenseUrl: "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          source: "https://commons.wikimedia.org/wiki/File:Chefs_at_Work_(Unsplash).jpg",
          alt: "Chefs preparando y emplatando platos en una cocina profesional"
        }
      )
    ]
  },
  "Arte, Diseño y Arquitectura": {
    queSeEstudia: "Explora la proyección de espacios habitables, el diseño visual e industrial y las artes escénicas, musicales y visuales, uniendo sensibilidad estética con oficio proyectual.",
    habilidades: ["Creatividad e imaginación visual/espacial", "Representación gráfica, modelado y prototipado", "Sensibilidad estética y cultural", "Desarrollo de proyectos autorales y de diseño"],
    campoLaboral: ["Oficinas de arquitectura y urbanismo", "Estudios de diseño gráfico, UX/UI e industrial", "Industrias creativas, animación y producción cultural", "Museos, centros culturales y ejercicio independiente"],
    image: AREAS["Arte, Arquitectura y Humanidades (Comunicaciones)"].image,
    carreras: [
      findCareer("Arquitectura"),
      findCareer("Diseño Gráfico"),
      buildCareer(
        "Artes Visuales",
        "Desarrolla la creación artística contemporánea en pintura, escultura, grabado, fotografía, medios digitales y gestión cultural.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=61&pagina=0",
        {
          file: "img/artes-visuales.jpg",
          author: "Mike Petrucci",
          license: "CC0",
          licenseUrl: "https://creativecommons.org/publicdomain/zero/1.0/deed.en",
          source: "https://commons.wikimedia.org/wiki/File:Mix_of_paints_(Unsplash).jpg",
          alt: "Paleta de pintura artística y pinceles en taller de artes visuales"
        }
      ),
      buildCareer(
        "Animación Digital",
        "Combina ilustración, narrativa audiovisual y modelado 2D/3D para cine, series, videojuegos y medios interactivos.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=49&pagina=0",
        {
          file: "img/animacion-digital.jpg",
          author: "David Revoy",
          license: "CC BY 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Penciling_on_Wacom_Cintiq_13HD_by_David_Revoy.jpg",
          alt: "Ilustración y animación digital sobre tableta gráfica interactiva"
        }
      )
    ]
  },
  "Humanidades, Letras e Historia": {
    queSeEstudia: "Profundiza en el pensamiento humano, los procesos históricos, la literatura, la filosofía, la lingüística y la mediación intercultural a través de las lenguas.",
    habilidades: ["Lectura crítica y escritura argumentativa", "Investigación documental e histórica", "Análisis conceptual y filosófico", "Dominio de idiomas y traducción"],
    campoLaboral: ["Universidades, archivos, bibliotecas y museos", "Editoriales, medios culturales y fundaciones", "Traducción, interpretación y organismos internacionales", "Docencia e investigación en humanidades"],
    image: {
      file: "img/area-humanidades-historia.jpg",
      author: "Chofaska",
      license: "CC BY-SA 3.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/3.0",
      source: "https://commons.wikimedia.org/wiki/File:Biblioteca_Nacional_de_Chile,_Santiago_Chile_(2012-09-30).jpg"
    },
    carreras: [
      buildCareer(
        "Licenciatura en Historia",
        "Investiga y comprende los procesos sociales, políticos y culturales a lo largo del tiempo mediante el análisis de fuentes históricas.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=666&pagina=0",
        {
          file: "img/licenciatura-historia.jpg",
          author: "Thomas Quine",
          license: "CC BY 2.0",
          licenseUrl: "https://creativecommons.org/licenses/by/2.0",
          source: "https://commons.wikimedia.org/wiki/File:Historical_Manuscripts_Commission_(40530477501).jpg",
          alt: "Consulta de fuentes documentales y archivos históricos"
        }
      ),
      buildCareer(
        "Filosofía",
        "Examina de forma crítica los problemas fundamentales del conocimiento, la ética, la lógica, la ciencia y la sociedad.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=664&pagina=0",
        {
          file: "img/filosofia.jpg",
          author: "Joseolgon",
          license: "CC BY 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by/4.0",
          source: "https://commons.wikimedia.org/wiki/File:The_School_of_Athens-Vatican.jpg",
          alt: "La Escuela de Atenas de Rafael, obra clásica alusiva a la filosofía"
        }
      ),
      buildCareer(
        "Literatura y Lingüística",
        "Estudia la estructura del lenguaje humano y la creación literaria, formando investigadores, editores y críticos culturales.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=668&pagina=0",
        {
          file: "img/literatura-linguistica.jpg",
          author: "Asturio Cantabrio",
          license: "CC BY-SA 4.0",
          licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
          source: "https://commons.wikimedia.org/wiki/File:Azumino_Public_Toyoshina_Library_reading_seats_ac_(2).jpg",
          alt: "Sala de lectura y colecciones bibliográficas de literatura y humanidades"
        }
      ),
      buildCareer(
        "Traducción e Interpretación",
        "Forma especialistas en mediación lingüística y traducción escrita u oral entre el español y otros idiomas.",
        "https://www.mifuturo.cl/buscador-de-carreras/?tipo=carrera&find=crr&titulo=1560&pagina=0",
        {
          file: "img/traduccion-interpretacion.jpg",
          author: "Cpl. John Lamb",
          license: "Public domain",
          licenseUrl: null,
          source: "https://commons.wikimedia.org/wiki/File:Staff_planning_classes_120904-M-VK320-050.jpg",
          alt: "Intérprete simultáneo trabajando con audífonos y micrófono en conferencia"
        }
      )
    ]
  }
})

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
