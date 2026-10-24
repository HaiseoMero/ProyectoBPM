<template>
  <PublicInfoLayout>
    <header class="info-hero">
      <div class="info-wrap">
        <router-link to="/" class="info-back"><span aria-hidden="true">←</span> Volver al inicio</router-link>
        <p class="info-eyebrow">El test · Big Five</p>
        <h1 class="info-title">Cinco dimensiones.<br /><em>Muchas formas de ser.</em></h1>
        <p class="info-lead">El cuestionario BFI-44 recoge cómo te describes en situaciones cotidianas. Sus resultados se organizan en cinco dimensiones de personalidad, conocidas como OCEAN por sus nombres en inglés.</p>
        <nav class="info-dimension-nav" aria-label="Explorar las dimensiones OCEAN">
          <a v-for="dimension in dimensions" :key="dimension.letter" :href="`#${dimension.id}`" :style="{ '--dimension-color': dimension.color }">
            <strong>{{ dimension.letter }}</strong> {{ dimension.shortName }}
          </a>
        </nav>
      </div>
    </header>

    <section class="info-wrap info-section" aria-labelledby="dimensiones-title">
      <h2 id="dimensiones-title">Conoce cada dimensión de tu perfil.</h2>
      <p class="info-intro">Cada dimensión describe una tendencia, con muchos puntos intermedios. Un puntaje alto o bajo no es una nota ni define por completo quién eres.</p>
    </section>

    <div class="info-wrap info-traits">
      <article v-for="dimension in dimensions" :id="dimension.id" :key="dimension.letter" class="info-card info-trait" :aria-labelledby="`${dimension.id}-title`" :style="{ '--dimension-color': dimension.color, '--dimension-bg': dimension.background }">
        <header class="info-trait__header">
          <span class="info-trait__letter" aria-hidden="true">{{ dimension.letter }}</span>
          <div>
            <h2 :id="`${dimension.id}-title`">{{ dimension.name }}</h2>
            <p class="info-trait__english">{{ dimension.english }}</p>
          </div>
        </header>
        <p>{{ dimension.description }}</p>
        <div class="info-trait__reading">
          <div>
            <h3>Si tu puntaje es más alto</h3>
            <p>{{ dimension.higher }}</p>
          </div>
          <div>
            <h3>Si tu puntaje es más bajo</h3>
            <p>{{ dimension.lower }}</p>
          </div>
        </div>
        <p class="info-trait__example"><strong>En la vida cotidiana:</strong> {{ dimension.example }}</p>
        <p class="info-trait__question">Para reflexionar: {{ dimension.question }}</p>
        <a class="info-source" :href="dimension.source" target="_blank" rel="noopener noreferrer">{{ dimension.sourceLabel }} <span class="info-visually-hidden">(abre en otra pestaña)</span></a>
      </article>
    </div>

    <section class="info-wrap info-section" aria-labelledby="leer-resultados-title">
      <p class="info-eyebrow">Al mirar tu reporte</p>
      <h2 id="leer-resultados-title">Un perfil para entenderte, no una etiqueta.</h2>
      <div class="info-reading-grid">
        <article class="info-card">
          <h3>Mira las cinco dimensiones juntas</h3>
          <p>Puedes preferir grupos pequeños y, al mismo tiempo, disfrutar de ideas nuevas o del trabajo colaborativo. Una sola dimensión no resume todas tus características.</p>
        </article>
        <article class="info-card">
          <h3>Lee los porcentajes con contexto</h3>
          <p>Los porcentajes muestran tu resultado en la escala del cuestionario. Un 70 % no significa que tengas más de ese rasgo que el 70 % de las personas ni que hayas obtenido una nota.</p>
        </article>
        <article class="info-card">
          <h3>Relaciona el resultado con tu experiencia</h3>
          <p>Piensa en ejemplos que reconozcas en tu vida y en otros que no te representen. Esas diferencias también pueden dar lugar a una conversación útil con tu orientador.</p>
        </article>
      </div>
    </section>

    <section class="info-wrap info-section" aria-labelledby="alcance-title">
      <div class="info-note">
        <h3 id="alcance-title">Una herramienta de apoyo al autoconocimiento.</h3>
        <p>El BFI-44 describe dimensiones de personalidad a partir de tus respuestas. Este reporte no es un diagnóstico, una medida de inteligencia ni una prueba de aptitud profesional. Las áreas de estudio que puedas explorar deben considerarse junto con tus intereses, habilidades y contexto, con el acompañamiento de tu orientador.</p>
        <a href="https://www.ocf.berkeley.edu/~johnlab/measures" class="info-source" target="_blank" rel="noopener noreferrer">Más sobre el inventario BFI · Berkeley Personality Lab <span class="info-visually-hidden">(abre en otra pestaña)</span></a>
      </div>
    </section>

    <section class="info-wrap info-section" aria-labelledby="siguiente-title">
      <div class="info-cta">
        <p class="info-eyebrow">A tu ritmo</p>
        <h2 id="siguiente-title">Empieza por cómo te ves hoy.</h2>
        <p>Responde con sinceridad. Puedes guardar tu avance y retomar el cuestionario antes de realizar el envío final.</p>
        <div class="info-actions">
          <router-link to="/auth" class="info-button">Ir a mi cuenta <span aria-hidden="true">→</span></router-link>
          <router-link to="/como-funciona" class="info-button info-button--secondary">Ver cómo funciona</router-link>
        </div>
      </div>
    </section>
  </PublicInfoLayout>
</template>

<script setup>
import PublicInfoLayout from '../components/PublicInfoLayout.vue'

const dimensions = [
  {
    id: 'apertura', letter: 'O', name: 'Apertura a la experiencia', shortName: 'Apertura', english: 'Openness to experience', color: '#4F46E5', background: '#EEF2FF',
    description: 'Explora tu interés por las ideas, las experiencias y las formas de expresión que son nuevas para ti. Incluye aspectos como la curiosidad, la imaginación y la apreciación de experiencias artísticas o culturales.',
    higher: 'Puedes disfrutar explorando posibilidades, imaginando alternativas o probando enfoques diferentes.',
    lower: 'Puedes sentirte más cómodo con lo conocido, las rutinas claras y las actividades concretas o familiares.',
    example: 'Ante una actividad nueva, algunas personas prefieren experimentar; otras empiezan por un método que ya conocen.',
    question: '¿En qué situaciones te gusta explorar algo nuevo y en cuáles prefieres mantener lo que ya conoces?',
    source: 'https://dictionary.apa.org/openness-to-experience', sourceLabel: 'Sobre esta dimensión · APA',
  },
  {
    id: 'responsabilidad', letter: 'C', name: 'Responsabilidad', shortName: 'Responsabilidad', english: 'Conscientiousness', color: '#10B981', background: '#ECFDF5',
    description: 'Describe tu tendencia a organizarte, cumplir compromisos y mantener el esfuerzo en las tareas. Se relaciona con la planificación, el orden y la constancia con que abordas tus objetivos.',
    higher: 'Puedes tender a preparar las tareas con anticipación, seguir un plan y revisar detalles antes de terminar.',
    lower: 'Puedes tender a organizar menos tus tareas o decidir sobre la marcha. El resultado invita a revisar qué hábitos te ayudan a cumplir tus compromisos.',
    example: 'Para una entrega escolar, puedes distribuir el trabajo durante la semana o empezar con menos planificación y ajustar el ritmo después.',
    question: '¿Qué forma de organizarte te ayuda a avanzar sin dejar todo para el último momento?',
    source: 'https://dictionary.apa.org/conscientiousness', sourceLabel: 'Sobre esta dimensión · APA',
  },
  {
    id: 'extraversion', letter: 'E', name: 'Extraversión', shortName: 'Extraversión', english: 'Extraversion', color: '#F59E0B', background: '#FFFBEB',
    description: 'Se relaciona con tu orientación hacia la interacción social, la expresión y la actividad en compañía de otras personas. Describe cuánto tiendes a buscar y disfrutar esas experiencias en tu vida habitual.',
    higher: 'Puedes sentirte cómodo conversando, participando en grupos y expresando tus ideas de manera abierta.',
    lower: 'Puedes preferir ambientes tranquilos, grupos pequeños o más tiempo a solas. Eso no define tu capacidad para relacionarte o trabajar con otras personas.',
    example: 'En un trabajo grupal, puedes participar hablando desde el inicio o preferir observar y preparar tu aporte antes de intervenir.',
    question: '¿Qué tamaño de grupo y qué ambiente te permiten participar con mayor comodidad?',
    source: 'https://dictionary.apa.org/extraversion', sourceLabel: 'Sobre esta dimensión · APA',
  },
  {
    id: 'amabilidad', letter: 'A', name: 'Amabilidad', shortName: 'Amabilidad', english: 'Agreeableness', color: '#EC4899', background: '#FDF2F8',
    description: 'Describe tendencias de tu manera de relacionarte con los demás, como la cooperación, la confianza, la consideración y la disposición a ayudar. También se expresa en cómo respondes cuando hay desacuerdos.',
    higher: 'Puedes dar importancia a los acuerdos, considerar las necesidades de otras personas y buscar la colaboración.',
    lower: 'Puedes expresar más críticas, mantener una postura más escéptica o defender tu posición con mayor firmeza. El resultado no es un juicio sobre tu valor como persona.',
    example: 'Ante opiniones distintas, puedes intentar llegar a un consenso o poner primero sobre la mesa tus objeciones a la propuesta.',
    question: '¿Cómo puedes expresar un desacuerdo y, al mismo tiempo, escuchar la perspectiva de los demás?',
    source: 'https://www.colby.edu/wp-content/uploads/2019/06/John_et_al_2008.pdf', sourceLabel: 'Sobre esta dimensión · John, Naumann y Soto (2008)',
  },
  {
    id: 'neuroticismo', letter: 'N', name: 'Neuroticismo', shortName: 'Neuroticismo', english: 'Neuroticism', color: '#EF4444', background: '#FEF2F2',
    description: 'Se refiere a la tendencia a experimentar emociones como preocupación, nerviosismo o tensión. Ayuda a describir diferencias en la sensibilidad emocional ante situaciones exigentes o inciertas.',
    higher: 'Tus respuestas pueden reflejar que experimentas preocupación o tensión con mayor facilidad o intensidad.',
    lower: 'Tus respuestas pueden reflejar una mayor tendencia a mantener la calma ante dificultades. Eso no significa que nunca te preocupes o que no experimentes emociones.',
    example: 'Una presentación frente al curso puede generar mucha preocupación en algunas personas y resultar más tranquila para otras.',
    question: '¿Qué situaciones suelen generarte tensión y qué apoyos te ayudan a afrontarlas?',
    source: 'https://dictionary.apa.org/neuroticism', sourceLabel: 'Sobre esta dimensión · APA',
  },
]
</script>
