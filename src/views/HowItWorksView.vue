<template>
  <PublicInfoLayout>
    <header class="info-hero">
      <div class="info-wrap">
        <router-link to="/" class="info-back"><span aria-hidden="true">←</span> Volver al inicio</router-link>
        <p class="info-eyebrow">Cómo funciona Vócalis</p>
        <h1 class="info-title">Un espacio para<br /><em>conocerte mejor.</em></h1>
        <p class="info-lead">Responde a tu ritmo, conoce tus resultados y úsalos para conversar sobre tu futuro. Vócalis acompaña tu proceso de orientación vocacional con información sobre tu forma habitual de pensar, sentir y actuar.</p>
        <div class="info-facts" aria-label="Características del cuestionario">
          <span class="info-fact"><strong>44</strong> afirmaciones</span>
          <span class="info-fact"><strong>5</strong> opciones de respuesta</span>
          <span class="info-fact"><strong>A tu ritmo</strong> · sin límite de tiempo</span>
        </div>
      </div>
    </header>

    <section class="info-wrap info-section" aria-labelledby="recorrido-title">
      <p class="info-eyebrow">Tu recorrido</p>
      <h2 id="recorrido-title">De tus respuestas a una conversación.</h2>
      <p class="info-intro">Puedes empezar desde tu computador o teléfono. Estas son las etapas que encontrarás en la plataforma.</p>
      <div class="info-step-grid">
        <article v-for="step in steps" :key="step.number" class="info-card">
          <span class="info-step-number" aria-hidden="true">{{ step.number }}</span>
          <h3>{{ step.title }}</h3>
          <p>{{ step.text }}</p>
        </article>
      </div>
    </section>

    <section class="info-wrap info-section" aria-labelledby="antes-title">
      <div class="info-note">
        <h3 id="antes-title">Responde pensando en cómo eres habitualmente.</h3>
        <p>No hay respuestas correctas ni un perfil ideal. Lee cada afirmación y elige cuánto estás de acuerdo, desde «Totalmente en desacuerdo» hasta «Totalmente de acuerdo». Piensa en tu vida cotidiana, sin intentar responder como crees que otras personas esperan.</p>
        <router-link to="/el-test">Conoce las cinco dimensiones del test <span aria-hidden="true">→</span></router-link>
      </div>
    </section>

    <section class="info-wrap info-section" aria-labelledby="dudas-title">
      <p class="info-eyebrow">Antes de comenzar</p>
      <h2 id="dudas-title">Tus dudas, en simple.</h2>
      <div class="info-faq">
        <details v-for="question in questions" :key="question.title">
          <summary>{{ question.title }}</summary>
          <p>{{ question.text }}</p>
        </details>
      </div>
    </section>

    <section class="info-wrap info-section" aria-labelledby="empezar-title">
      <div class="info-cta">
        <p class="info-eyebrow">El siguiente paso</p>
        <h2 id="empezar-title">Tu futuro también se conversa.</h2>
        <p>El cuestionario aporta una mirada sobre tu personalidad. Junto a tus intereses, habilidades y experiencias, puede ayudarte a preparar preguntas para tu orientador y explorar opciones con más contexto.</p>
        <div class="info-actions">
          <router-link to="/auth" class="info-button">Ir a mi cuenta <span aria-hidden="true">→</span></router-link>
          <router-link to="/el-test" class="info-button info-button--secondary">Conocer el test OCEAN</router-link>
        </div>
      </div>
    </section>
  </PublicInfoLayout>
</template>

<script setup>
import PublicInfoLayout from '../components/PublicInfoLayout.vue'

const steps = [
  { number: '01', title: 'Crea tu cuenta o inicia sesión', text: 'Ingresa como estudiante y completa los datos de tu establecimiento y curso. Desde tu panel podrás acceder al cuestionario y consultar el avance de tu proceso.' },
  { number: '02', title: 'Responde las 44 afirmaciones', text: 'El cuestionario se presenta por bloques. En cada afirmación eliges una de cinco respuestas según cuánto te describe. Antes de avanzar, completa las preguntas del bloque.' },
  { number: '03', title: 'Haz una pausa si la necesitas', text: 'Tus respuestas se guardan a medida que avanzas. Antes de salir, espera el aviso de guardado. Cuando regreses a tu panel, «Continuar cuestionario BFI-44» te permitirá recuperar lo que llevas respondido.' },
  { number: '04', title: 'Consulta tus resultados y coméntalos', text: 'Al responder todo y hacer el envío final, tendrás un reporte con las cinco dimensiones y un gráfico de tu perfil. Tu orientador asignado puede consultar los resultados para acompañarte en la reflexión.' },
]
const questions = [
  { title: '¿Necesito terminarlo de una vez?', text: 'No. Puedes dejarlo pendiente y continuar después desde la misma cuenta. Espera a que aparezca «Todas las respuestas seleccionadas están guardadas» antes de cerrar la página.' },
  { title: '¿Puedo cambiar una respuesta?', text: 'Sí, mientras el cuestionario siga pendiente puedes revisar y cambiar tus respuestas. Después del envío final, la plataforma conserva esa evaluación y no permite volver a responderla con la misma cuenta.' },
  { title: '¿Qué voy a encontrar en mi reporte?', text: 'Encontrarás un gráfico y una explicación de Apertura, Responsabilidad, Extraversión, Amabilidad y Neuroticismo. Si aparecen áreas profesionales para explorar, puedes usarlas como referencias para conversar sobre tus intereses y experiencias.' },
  { title: '¿El resultado me dice qué carrera estudiar?', text: 'El resultado aporta información para conocerte y conversar con tu orientador. La elección también considera tus intereses, habilidades, oportunidades y circunstancias personales; el cuestionario por sí solo no determina una carrera.' },
  { title: '¿Quién puede consultar mis resultados?', text: 'Puedes verlos desde tu cuenta. El orientador al que esté asignado tu curso también puede consultarlos para apoyar el seguimiento de tu proceso de orientación.' },
]
</script>
