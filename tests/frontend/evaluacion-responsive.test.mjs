// Pruebas en navegador contra Vite, con API simulada: no escriben en MySQL.
// Requiere Playwright y Chromium. Se pueden indicar VOCALIS_PLAYWRIGHT_MODULE,
// VOCALIS_CHROME_PATH y VOCALIS_TEST_BASE_URL sin añadir dependencias al proyecto.
import assert from 'node:assert/strict'
import process from 'node:process'
import { Buffer } from 'node:buffer'
import { readFile, mkdir } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'
import { join } from 'node:path'
import { before, after, test } from 'node:test'

const playwrightModule = process.env.VOCALIS_PLAYWRIGHT_MODULE
  ? pathToFileURL(process.env.VOCALIS_PLAYWRIGHT_MODULE).href : 'playwright'
const { chromium } = await import(playwrightModule)
const base = process.env.VOCALIS_TEST_BASE_URL || 'http://127.0.0.1:5174'
const screenshotDirectory = process.env.VOCALIS_TEST_SCREENSHOTS
const seed = await readFile(new URL('../../backend/app/seed.py', import.meta.url), 'utf8')
const questions = [...seed.matchAll(/\((\d+), '([^']+)', '([OCEAN])', (?:True|False)\)/g)]
  .map(([, id, text, dimension]) => ({ id: Number(id), text, dimension }))
assert.equal(questions.length, 44)
const labels = ['Totalmente en desacuerdo', 'En desacuerdo', 'Neutro', 'De acuerdo', 'Totalmente de acuerdo']
const token = `test.${Buffer.from(JSON.stringify({ role: 'estudiante', exp: Math.floor(Date.now() / 1000) + 3600 })).toString('base64')}.test`
const savedText = 'Todas las respuestas seleccionadas están guardadas.'
const report = { studentName: 'Estudiante de prueba', evaluatedAt: '1 de octubre, 2026', dimensions: [], careerAreas: [] }
let browser

before(async () => {
  browser = await chromium.launch({ headless: true, ...(process.env.VOCALIS_CHROME_PATH ? { executablePath: process.env.VOCALIS_CHROME_PATH } : {}) })
  if (screenshotDirectory) await mkdir(screenshotDirectory, { recursive: true })
})
after(async () => { await browser?.close() })

async function prepare(t, width, settings = {}) {
  const context = await browser.newContext({ viewport: { width, height: 844 },
    hasTouch: width <= 700, isMobile: width <= 700, reducedMotion: 'reduce' })
  const page = await context.newPage()
  page.setDefaultTimeout(15000)
  page.setDefaultNavigationTimeout(15000)
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  const state = {
    questions: settings.questions || questions,
    saved: new Map(settings.saved || []), completed: settings.completed || false,
    failLoads: 0, failSaves: 0, failSubmits: 0, activeSaves: 0, maxActiveSaves: 0,
    saveGate: null, submitGate: null, saves: [], submissions: [], ...settings,
  }
  state.saved = new Map(settings.saved || [])
  await page.route('**/api/**', async route => {
    const path = new URL(route.request().url()).pathname
    let body
    let status = 200
    if (path === '/api/evaluacion/preguntas') {
      if (state.failLoads > 0) { state.failLoads--; status = 503; body = { detail: 'Error de carga de prueba' } }
      else body = state.questions
    } else if (path === '/api/evaluacion/respuestas') {
      body = [...state.saved].map(([preguntaId, valor]) => ({ preguntaId, valor }))
    } else if (path === '/api/evaluacion/estado') {
      body = { tiene_evaluacion: state.saved.size > 0, estado: state.completed ? 'completada' : 'en_progreso', bpm_estado: 'registro' }
    } else if (path === '/api/evaluacion/respuesta') {
      body = route.request().postDataJSON()
      state.saves.push(body)
      state.activeSaves++
      state.maxActiveSaves = Math.max(state.maxActiveSaves, state.activeSaves)
      if (state.saveGate) await state.saveGate
      if (state.failSaves > 0) { state.failSaves--; status = 503; body = { detail: 'Error de conexión de prueba' } }
      else state.saved.set(body.preguntaId, body.valor)
      state.activeSaves--
    } else if (path === '/api/evaluacion/enviar') {
      body = route.request().postDataJSON()
      state.submissions.push(body)
      if (state.submitGate) await state.submitGate
      if (state.failSubmits > 0) { state.failSubmits--; status = 503; body = { detail: 'Error de envío de prueba' } }
      else { state.completed = true; body = { reportId: 1, status: 'success' } }
    } else if (path === '/api/evaluacion/reporte') body = report
    else if (path === '/api/auth/me') body = { role: 'estudiante', name: 'Estudiante de prueba' }
    else throw new Error(`Petición inesperada ${path}`)
    await route.fulfill({ status, json: body })
  })
  await page.addInitScript(value => localStorage.setItem('vocalis_token', value), token)
  t.after(async () => { await context.close(); assert.deepEqual(errors, [], 'Errores JavaScript') })
  await page.goto(`${base}/estudiante/evaluacion`, { waitUntil: 'domcontentloaded' })
  return { page, state }
}

const waitReady = page => page.locator('.question-text').first().waitFor()
const waitSaved = page => page.getByText(savedText, { exact: true }).waitFor()
const nextButton = page => page.getByRole('button', { name: /Siguiente Bloque|Finalizar y Calcular Perfil|Calculando perfil/ })
const choose = (page, id, value) => page.locator(`#question-${id} .radio-container`).nth(value - 1).click()
const savedAnswers = count => questions.slice(0, count).map(q => [q.id, 3])

for (const width of [320, 360, 390, 430, 600, 700, 701, 768, 900, 1024, 1366]) {
  test(`cuestionario ${width}px: controles accesibles y respuestas al cambiar de tamaño`, async t => {
    const { page, state } = await prepare(t, width)
    await waitReady(page)
    const layout = await page.evaluate(() => ({
      width: innerWidth, pageWidth: document.documentElement.scrollWidth,
      tableDisplay: getComputedStyle(document.querySelector('.likert-table')).display,
      optionSizes: [...document.querySelectorAll('.radio-container')].map(element => {
        const bounds = element.getBoundingClientRect()
        return { width: bounds.width, height: bounds.height, left: bounds.left, right: bounds.right }
      }),
    }))
    assert.ok(layout.pageWidth <= layout.width + 1, 'La página se desborda')
    assert.equal(layout.tableDisplay, width <= 700 ? 'block' : 'table')
    assert.equal(await page.getByRole('radio').count(), 50, 'Solo debe existir un conjunto de radios')
    for (const size of layout.optionSizes) {
      assert.ok(size.width >= 44 && size.height >= 44, 'Opción táctil demasiado pequeña')
      if (width <= 700) assert.ok(size.left >= 0 && size.right <= width + 1, 'Opción fuera de pantalla')
    }
    for (const label of labels) {
      assert.equal(await page.getByRole('radio', { name: `1. ${questions[0].text} ${label}`, exact: true }).count(), 1)
    }
    await choose(page, 1, 3)
    await waitSaved(page)
    assert.equal(state.saves.length, 1, 'Una selección debe producir un solo guardado')
    await page.locator('#question-radio-1-3').evaluate(element => { element.dataset.resizeMarker = 'same-control' })
    if (screenshotDirectory && [390, 1366].includes(width)) {
      await page.evaluate(() => document.fonts.ready)
      await page.locator('#question-1').scrollIntoViewIfNeeded()
      await page.screenshot({ path: join(screenshotDirectory, `cuestionario-${width}.png`) })
    }
    await page.setViewportSize({ width: width <= 700 ? 1366 : 390, height: 844 })
    assert.ok(await page.locator('#question-radio-1-3').isChecked())
    assert.equal(await page.locator('#question-radio-1-3').getAttribute('data-resize-marker'), 'same-control')
    assert.equal(state.saves.length, 1)
    await page.reload({ waitUntil: 'domcontentloaded' })
    await waitReady(page)
    assert.ok(await page.locator('#question-radio-1-3').isChecked(), 'El progreso se recupera después de recargar')
  })
}

test('validación: lleva a la primera afirmación pendiente y conserva bloques anteriores', async t => {
  const { page, state } = await prepare(t, 390)
  await waitReady(page)
  await nextButton(page).click()
  assert.equal(await page.getByRole('alert').textContent(), 'Responde la afirmación 1 antes de continuar.')
  assert.equal(await page.evaluate(() => document.activeElement.id), 'question-radio-1-1')
  assert.equal(await page.locator('#question-radio-1-1').getAttribute('aria-invalid'), 'true')
  assert.equal(state.saves.length, 0, 'Enfocar una opción no debe seleccionarla')
  for (const q of questions.slice(0, 10)) await choose(page, q.id, 3)
  await waitSaved(page)
  await nextButton(page).click()
  await page.locator('#question-11').waitFor()
  assert.equal(await page.locator('#questionnaire-block').textContent(), 'Bloque 2 de 5')
  assert.equal(await page.evaluate(() => document.activeElement.id), 'questionnaire-block')
  const bounds = await page.locator('#question-11').boundingBox()
  assert.ok(bounds.y >= 0 && bounds.y < 300, 'El siguiente bloque debe quedar visible')
  await page.getByRole('button', { name: /Bloque Anterior/ }).click()
  await page.locator('#question-1').waitFor()
  assert.ok(await page.locator('#question-radio-1-3').isChecked())
  assert.equal(state.saved.size, 10)
})

test('teclado y cambios rápidos: selección única y guardados en orden', async t => {
  const { page, state } = await prepare(t, 1366)
  await waitReady(page)
  let release
  state.saveGate = new Promise(resolve => { release = resolve })
  await page.locator('#question-radio-1-1').focus()
  await page.keyboard.press('Space')
  await page.keyboard.press('ArrowRight')
  await page.keyboard.press('ArrowRight')
  assert.ok(await page.locator('#question-radio-1-3').isChecked())
  await page.getByText('Guardando respuestas…', { exact: true }).waitFor()
  release()
  await waitSaved(page)
  assert.deepEqual(state.saves, [{ preguntaId: 1, valor: 1 }, { preguntaId: 1, valor: 2 }, { preguntaId: 1, valor: 3 }])
  assert.equal(state.maxActiveSaves, 1)
  assert.equal(state.saved.get(1), 3)
})

test('guardado fallido: conserva la selección, bloquea el envío y permite reintentar', async t => {
  const { page, state } = await prepare(t, 390, { saved: savedAnswers(43), failSaves: 1 })
  await waitReady(page)
  await choose(page, 44, 5)
  await page.getByRole('button', { name: 'Reintentar guardado', exact: true }).waitFor()
  assert.ok(await page.locator('#question-radio-44-5').isChecked())
  await nextButton(page).click()
  await page.getByRole('alert').filter({ hasText: 'Reintenta el guardado' }).waitFor()
  assert.equal(state.submissions.length, 0)
  await page.getByRole('button', { name: 'Reintentar guardado', exact: true }).click()
  await waitSaved(page)
  assert.equal(state.saved.get(44), 5)
  await nextButton(page).click()
  await page.waitForURL('**/estudiante/reporte')
  assert.equal(state.submissions[0].respuestas.length, 44)
})

test('recuperación: reanuda el primer bloque pendiente con los valores guardados', async t => {
  const { page } = await prepare(t, 390, { saved: savedAnswers(13) })
  await waitReady(page)
  assert.equal(await page.locator('#questionnaire-block').textContent(), 'Bloque 2 de 5')
  assert.ok(await page.locator('#question-radio-11-3').isChecked())
  assert.equal(await page.getByRole('progressbar').getAttribute('aria-valuenow'), '13')
  await nextButton(page).click()
  assert.equal(await page.evaluate(() => document.activeElement.id), 'question-radio-14-1')
})

test('envío completo: mantiene los 44 ítems, sus valores y un único envío', async t => {
  const { page, state } = await prepare(t, 390)
  await waitReady(page)
  for (let block = 0; block < 5; block++) {
    const items = questions.slice(block * 10, (block + 1) * 10)
    assert.deepEqual(await page.locator('.question-text > span:first-child').allTextContents(), items.map((q, index) => `${block * 10 + index + 1}. ${q.text}`))
    for (const q of items) await choose(page, q.id, (q.id % 5) + 1)
    await waitSaved(page)
    if (block < 4) {
      await nextButton(page).click()
      await page.locator(`#question-${questions[(block + 1) * 10].id}`).waitFor()
    }
  }
  let release
  state.submitGate = new Promise(resolve => { release = resolve })
  await nextButton(page).click()
  await page.getByRole('button', { name: 'Calculando perfil…', exact: true }).waitFor()
  assert.ok(await page.getByRole('button', { name: /Bloque Anterior/ }).isDisabled())
  assert.ok(await page.locator('input[type=radio]').evaluateAll(inputs => inputs.every(input => input.disabled)))
  release()
  await page.waitForURL('**/estudiante/reporte')
  assert.equal(state.submissions.length, 1)
  assert.equal(state.saves.length, 44)
  assert.deepEqual(state.submissions[0].respuestas, questions.map(q => ({ preguntaId: q.id, valor: (q.id % 5) + 1 })))
})

test('envío fallido: conserva los valores y permite intentar otra vez', async t => {
  const { page, state } = await prepare(t, 390, { saved: savedAnswers(44), failSubmits: 1 })
  await waitReady(page)
  await nextButton(page).click()
  await page.getByRole('alert').filter({ hasText: 'No se pudo finalizar' }).waitFor()
  assert.ok(await page.locator('#question-radio-44-3').isChecked())
  assert.ok(await nextButton(page).isEnabled())
  await nextButton(page).click()
  await page.waitForURL('**/estudiante/reporte')
  assert.deepEqual(state.submissions[0], state.submissions[1])
})

test('carga fallida: ofrece reintento antes de permitir respuestas', async t => {
  const { page } = await prepare(t, 390, { failLoads: 1 })
  await page.getByRole('button', { name: 'Reintentar carga', exact: true }).waitFor()
  assert.equal(await page.getByRole('radio').count(), 0)
  await page.getByRole('button', { name: 'Reintentar carga', exact: true }).click()
  await waitReady(page)
  assert.equal(await page.getByRole('radio').count(), 50)
})

test('evaluación completada: muestra el reporte y no permite responder de nuevo', async t => {
  const { page, state } = await prepare(t, 390, { saved: savedAnswers(44), completed: true })
  await page.getByText('Esta evaluación ya está completada y no se puede editar.', { exact: true }).waitFor()
  assert.equal(await page.getByRole('radio').count(), 0)
  assert.equal(state.saves.length, 0)
  await page.getByRole('link', { name: 'Ver reporte', exact: true }).click()
  await page.waitForURL('**/estudiante/reporte')
})

test('identificadores: respeta el orden visible y guarda los ID reales de la API', async t => {
  const alternate = questions.map(q => ({ ...q, id: q.id + 100 }))
  const { page, state } = await prepare(t, 390, { questions: alternate })
  await waitReady(page)
  assert.equal(await page.locator('#question-101 .question-number').textContent(), '1.')
  await choose(page, 101, 4)
  await waitSaved(page)
  assert.deepEqual(state.saves, [{ preguntaId: 101, valor: 4 }])
})

test('pantalla pequeña: el aviso de guardado no tapa la afirmación pendiente', async t => {
  const { page } = await prepare(t, 320, { failSaves: 1 })
  await waitReady(page)
  await choose(page, 1, 3)
  await page.getByRole('button', { name: 'Reintentar guardado', exact: true }).waitFor()
  await nextButton(page).click()
  const question = await page.locator('#question-2').boundingBox()
  const status = await page.locator('.questionnaire-status').boundingBox()
  assert.ok(question.y >= status.y + status.height, 'La pregunta no debe quedar detrás del aviso')
  assert.equal(await page.evaluate(() => document.activeElement.id), 'question-radio-2-1')
  await page.setViewportSize({ width: 320, height: 400 })
  assert.equal(await page.locator('.questionnaire-status').evaluate(element => getComputedStyle(element).position), 'static')
})
