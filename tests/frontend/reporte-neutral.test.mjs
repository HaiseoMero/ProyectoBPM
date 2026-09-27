// Renderiza la plantilla real: prueba presentación, no servicios ni navegación.
// Ejecutar: node --test tests/frontend/reporte-neutral.test.mjs
import assert from 'node:assert/strict'
import { Buffer } from 'node:buffer'
import { readFileSync } from 'node:fs'
import test from 'node:test'
import { parse, compileTemplate } from '@vue/compiler-sfc'
import { createSSRApp, h } from 'vue'
import { renderToString } from 'vue/server-renderer'

const filename = new URL('../../src/views/ReporteView.vue', import.meta.url)
const { descriptor } = parse(readFileSync(filename, 'utf8'))
const compiled = compileTemplate({
  source: descriptor.template.content,
  filename: filename.pathname,
  id: 'reporte-neutral-test',
  ssr: true,
  ssrCssVars: []
})
assert.deepEqual(compiled.errors, [])
const code = compiled.code.replace(/from "(vue(?:\/server-renderer)?)"/g,
  (_, specifier) => `from ${JSON.stringify(import.meta.resolve(specifier))}`)
const { ssrRender } = await import(`data:text/javascript;base64,${Buffer.from(code).toString('base64')}`)

async function renderReport(isOrientador, careerAreas) {
  const dimension = careerAreas.length
    ? { letter: 'O', name: 'Apertura', interpretation: 'Creatividad y curiosidad.' }
    : { letter: 'N', name: 'Neuroticismo', interpretation: 'No indica una inclinación profesional.' }
  const app = createSSRApp({
    ssrRender,
    data: () => ({
      isOrientador, careerAreas, loading: false, errorMessage: '',
      studentInitials: 'AP', displayedStudentName: 'Alumno Prueba', evaluatedAt: '24 de Sep, 2026',
      expandedIndexes: [0], radarDimensions: [], radarGridPoints: [], radarAxes: [], radarDots: [],
      hasRadarScores: false, dominantTraitLabel: `${dimension.name} (95%)`,
      dimensionsData: [{ ...dimension, score: 95, color: '#EF4444',
        vocationalImpact: 'Este puntaje por sí solo no permite inferir aptitud ni recomendar una profesión.' }]
    })
  })
  app.component('router-link', { props: ['to'], setup: (props, { slots }) => () => h('a', { href: props.to }, slots.default?.()) })
  return renderToString(app)
}

for (const role of ['estudiante', 'orientador']) {
  test(`${role}: sin áreas se muestran puntajes y explicación neutral`, async () => {
    const html = await renderReport(role === 'orientador', [])
    assert.match(html, /Las reglas actuales no permiten sugerir un área/)
    assert.match(html, /Puntaje: 95%/)
    assert.match(html, /Alcance del puntaje:/)
    assert.match(html, /No indica una inclinación profesional/)
    assert.doesNotMatch(html, /Tecnología e Informática|Carreras Recomendadas|Alto impacto|Áreas de Afinidad/)
  })
  test(`${role}: las áreas existentes se presentan como exploración`, async () => {
    const html = await renderReport(role === 'orientador', [{ title: 'Artes y Diseño',
      desc: 'Referencia exploratoria del prototipo.', carreras: ['Diseño Gráfico'] }])
    assert.match(html, /Áreas profesionales para explorar/)
    assert.match(html, /no acreditan afinidad ni aptitud profesional/)
    assert.match(html, /Ejemplos de carreras:/)
    assert.match(html, /Diseño Gráfico/)
    assert.doesNotMatch(html, /Las reglas actuales no permiten sugerir un área|Carreras Recomendadas/)
  })
}
