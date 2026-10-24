// Portada y recorridos completos con datos ficticios. La prueba LAN atraviesa
// el proxy real de Vite hacia una API HTTP de prueba ligada a 127.0.0.1.
// No se conecta a MySQL, Camunda ni a la API real del proyecto.
import assert from 'node:assert/strict'
import process from 'node:process'
import { Buffer } from 'node:buffer'
import { createServer } from 'node:http'
import { readFile, mkdir } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'
import { join } from 'node:path'
import { before, after, test } from 'node:test'

const playwrightModule = process.env.VOCALIS_PLAYWRIGHT_MODULE
  ? pathToFileURL(process.env.VOCALIS_PLAYWRIGHT_MODULE).href : 'playwright'
const { chromium } = await import(playwrightModule)
const base = process.env.VOCALIS_TEST_BASE_URL || 'http://127.0.0.1:5174'
const lanBase = process.env.VOCALIS_TEST_LAN_URL
const screenshotDirectory = process.env.VOCALIS_TEST_SCREENSHOTS
const seed = await readFile(new URL('../../backend/app/seed.py', import.meta.url), 'utf8')
const questions = [...seed.matchAll(/\((\d+), '([^']+)', '([OCEAN])', (?:True|False)\)/g)]
  .map(([, id, text, dimension]) => ({ id: Number(id), text, dimension }))
assert.equal(questions.length, 44)
const name = 'Estudiante de prueba móvil'
const report = {
  studentName: name, evaluatedAt: '1 de octubre de 2026', careerAreas: [],
  dimensions: [
    ['O', 'Apertura', 65], ['C', 'Responsabilidad', 75], ['E', 'Extraversión', 40],
    ['A', 'Amabilidad', 60], ['N', 'Neuroticismo', 35],
  ].map(([letter, name, score]) => ({ letter, name, score, color: '#4F46E5',
    interpretation: 'Descripción ficticia para verificar la presentación.', vocationalImpact: 'No determina aptitud ni una carrera adecuada.' })),
}
const token = role => `test.${Buffer.from(JSON.stringify({ role, exp: Math.floor(Date.now() / 1000) + 3600 })).toString('base64')}.test`
const createState = settings => ({ role: 'estudiante', completed: false, answers: new Map(),
  registrations: [], logins: [], submissions: [], requests: [], errors: [], failLogins: 0, ...settings })
let browser
let apiServer
let lanState

async function apiResponse(state, path, method, body) {
  state.requests.push({ path, method })
  if (path === '/api/auth/register' && method === 'POST') {
    state.registrations.push(body)
    state.role = body.role
    return { status: 201, json: { id: 1, email: body.email, role: body.role } }
  }
  if (path === '/api/auth/login' && method === 'POST') {
    state.logins.push(body)
    if (state.failLogins) { state.failLogins--; return { status: 401, json: { detail: 'Credenciales no reconocidas' } } }
    return { status: 200, json: { access_token: token(state.role), role: state.role, name } }
  }
  if (path === '/api/auth/me') return { status: 200, json: { name, role: state.role } }
  if (path === '/api/evaluacion/estado') return { status: 200, json: {
    tiene_evaluacion: state.answers.size > 0, estado: state.completed ? 'completada' : 'en_progreso',
    bpm_estado: state.completed ? 'reporte_listo' : 'registro',
    registro_fecha: '2026-10-01T10:00:00',
    ...(state.completed ? { evaluacion_fecha: '2026-10-01T11:00:00', reporte_fecha: '2026-10-01T11:01:00' } : {}),
  } }
  if (path === '/api/evaluacion/preguntas') return { status: 200, json: questions }
  if (path === '/api/evaluacion/respuestas') return { status: 200, json: [...state.answers].map(([preguntaId, valor]) => ({ preguntaId, valor })) }
  if (path === '/api/evaluacion/respuesta' && method === 'POST') {
    state.answers.set(body.preguntaId, body.valor)
    return { status: 200, json: { status: 'ok' } }
  }
  if (path === '/api/evaluacion/enviar' && method === 'POST') {
    state.submissions.push(body)
    state.completed = true
    return { status: 200, json: { reportId: 1, status: 'success' } }
  }
  if (path === '/api/evaluacion/reporte') return state.completed
    ? { status: 200, json: report } : { status: 404, json: { detail: 'Reporte no disponible' } }
  if (path === '/api/orientador/cursos/sin-asignar') return { status: 200, json: [] }
  if (path === '/api/orientador/estudiantes') return { status: 200, json: [
    { id: 42, name, email: 'alumno.prueba@example.test', course: '4° Medio A', lastUpdate: '1 de octubre de 2026', bpm_estado: 'reporte_listo', hasReport: true },
    { id: 77, name: 'Alumno pendiente', email: 'pendiente@example.test', course: '3° Medio B', lastUpdate: 'Sin evaluación', bpm_estado: 'registro', hasReport: false },
  ] }
  if (path === '/api/orientador/estudiante/42/reporte') return { status: 200, json: report }
  state.errors.push(`Petición inesperada ${method} ${path}`)
  return { status: 500, json: { detail: 'Ruta no incluida en la API de prueba' } }
}

before(async () => {
  browser = await chromium.launch({ headless: true, ...(process.env.VOCALIS_CHROME_PATH ? { executablePath: process.env.VOCALIS_CHROME_PATH } : {}) })
  if (screenshotDirectory) await mkdir(screenshotDirectory, { recursive: true })
  if (lanBase) {
    lanState = createState({})
    apiServer = createServer(async (request, response) => {
      try {
        const chunks = []
        for await (const chunk of request) chunks.push(chunk)
        const raw = Buffer.concat(chunks).toString()
        const result = await apiResponse(lanState, new URL(request.url, 'http://127.0.0.1').pathname,
          request.method, raw ? JSON.parse(raw) : undefined)
        response.writeHead(result.status, { 'Content-Type': 'application/json' })
        response.end(JSON.stringify(result.json))
      } catch (error) {
        lanState.errors.push(error.message)
        response.writeHead(500)
        response.end('{}')
      }
    })
    await new Promise((resolve, reject) => {
      apiServer.once('error', reject)
      apiServer.listen(Number(process.env.VOCALIS_TEST_API_PORT || 18000), '127.0.0.1', resolve)
    })
  }
})
after(async () => {
  await browser?.close()
  if (apiServer) { apiServer.closeAllConnections(); await new Promise(resolve => apiServer.close(resolve)) }
})

async function prepare(t, width, settings = {}) {
  const context = await browser.newContext({ viewport: { width, height: settings.height || 844 },
    hasTouch: width <= 900, isMobile: width <= 900, reducedMotion: settings.motion || 'reduce' })
  const page = await context.newPage()
  page.setDefaultTimeout(15000)
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  const state = settings.lan ? lanState : createState(settings)
  // Contar únicamente cuadros del radar, sin interferir con la animación.
  await page.addInitScript(() => {
    const original = window.requestAnimationFrame.bind(window)
    window.radarFrames = 0
    window.requestAnimationFrame = callback => original(timestamp => {
      if (callback.name === 'animateRadar') window.radarFrames++
      callback(timestamp)
    })
  })
  if (!settings.lan) await page.route('**/api/**', async route => {
    const request = route.request()
    const body = request.postData() ? request.postDataJSON() : undefined
    const result = await apiResponse(state, new URL(request.url()).pathname, request.method(), body)
    await route.fulfill(result)
  })
  t.after(async () => { await context.close(); assert.deepEqual(errors, [], 'Errores JavaScript'); assert.deepEqual(state.errors, [], 'Peticiones inesperadas') })
  await page.goto(settings.lan ? lanBase : base, { waitUntil: 'domcontentloaded' })
  await page.getByRole('heading', { level: 1 }).waitFor()
  return { page, state }
}

async function assertLayout(page) {
  const result = await page.evaluate(() => ({ width: innerWidth, pageWidth: document.documentElement.scrollWidth,
    boxes: [...document.querySelectorAll('main a, main button, main input, main select, .nav a, .info-nav a, .nav__logo, .hero__stats, .radar__label, .radar__svg')]
      .filter(el => el.getClientRects().length).map(el => {
        const bounds = el.getBoundingClientRect()
        return { tag: el.tagName, text: el.textContent, left: bounds.left, right: bounds.right, height: bounds.height }
      }),
  }))
  assert.ok(result.pageWidth <= result.width + 1, 'Desbordamiento horizontal')
  for (const box of result.boxes) {
    assert.ok(box.left >= 0 && box.right <= result.width + 1, `Elemento fuera de pantalla: ${box.text}`)
    if (['A', 'BUTTON', 'INPUT', 'SELECT'].includes(box.tag)) assert.ok(box.height >= 44, `Control pequeño: ${box.text}`)
  }
}

for (const width of [320, 360, 390, 430, 480, 481, 600, 768, 900, 901, 1024, 1366]) {
  test(`portada ${width}px: navegación, formulario y gráfico legibles`, async t => {
    const { page } = await prepare(t, width)
    await assertLayout(page)
    assert.equal(await page.getByRole('img', { name: /Ejemplo de las cinco dimensiones OCEAN/ }).count(), 1)
    assert.equal(await page.locator('.radar__label').count(), 5)
    assert.equal(await page.locator('.ocean-card').count(), 5)
    assert.equal(await page.locator('.report-card').count(), 4)
    if (width <= 900) {
      assert.equal(await page.getByLabel('Tu nombre', { exact: true }).evaluate(el => getComputedStyle(el).fontSize), '16px')
      assert.equal(await page.locator('.hero__bg-glow').first().isVisible(), false)
    }
    for (const [link, path] of [['Cómo funciona', '/como-funciona'], ['El test', '/el-test']]) {
      await page.getByRole('navigation', { name: 'Navegación de inicio' }).getByRole('link', { name: link, exact: true }).click()
      await page.waitForURL(`**${path}`)
      await page.locator('.info-title').waitFor()
      await assertLayout(page)
      assert.equal(await page.getByRole('navigation', { name: 'Navegación principal' }).getByRole('link', { name: link, exact: true }).getAttribute('aria-current'), 'page')
      if (path === '/el-test') assert.equal(await page.locator('.info-trait').count(), 5)
      await page.getByRole('link', { name: 'Volver al inicio', exact: true }).click()
      await page.waitForURL(base + '/')
    }
    await page.getByRole('link', { name: /Descubrir mi perfil/ }).click()
    await page.getByLabel('Tu nombre', { exact: true }).fill(name)
    await page.getByLabel('Correo electrónico', { exact: true }).fill('movil.prueba@example.test')
    if (screenshotDirectory && [390, 1366].includes(width)) {
      await page.evaluate(() => document.fonts.ready)
      await page.evaluate(() => window.scrollTo(0, 0))
      await page.screenshot({ path: join(screenshotDirectory, `portada-${width}.png`), fullPage: true })
    }
    await page.getByRole('button', { name: /Crear mi cuenta gratis/ }).click()
    await page.waitForURL('**/auth?*')
    assert.equal(await page.getByLabel('Nombre completo', { exact: true }).inputValue(), name)
    assert.equal(await page.getByLabel('Correo electrónico', { exact: true }).inputValue(), 'movil.prueba@example.test')
    await assertLayout(page)
  })
}

test('teléfono horizontal: la navegación deja espacio para leer', async t => {
  const { page } = await prepare(t, 844, { height: 390 })
  assert.equal(await page.locator('.nav').evaluate(el => getComputedStyle(el).position), 'static')
  await page.getByRole('navigation').getByRole('link', { name: 'El test', exact: true }).click()
  await assertLayout(page)
  await page.waitForURL('**/el-test')
  assert.equal(await page.locator('.info-nav').evaluate(el => getComputedStyle(el).position), 'static')
  assert.equal(await page.locator('.info-trait').count(), 5)
})

test('páginas informativas: ambos accesos a cómo funciona, preguntas y dimensiones', async t => {
  const { page, state } = await prepare(t, 390)
  await page.getByRole('link', { name: 'Ver cómo funciona', exact: true }).click()
  await page.waitForURL('**/como-funciona')
  assert.equal(await page.locator('.info-step-grid article').count(), 4)
  await page.getByText('¿Necesito terminarlo de una vez?', { exact: true }).click()
  assert.match(await page.locator('details[open]').innerText(), /misma cuenta/)
  await page.getByRole('navigation', { name: 'Navegación principal' }).getByRole('link', { name: 'El test', exact: true }).click()
  await page.waitForURL('**/el-test')
  await page.reload({ waitUntil: 'domcontentloaded' })
  await page.locator('.info-trait').first().waitFor()
  assert.equal(await page.locator('.info-trait').count(), 5)
  assert.deepEqual(await page.locator('.info-trait__letter').allTextContents(), ['O', 'C', 'E', 'A', 'N'])
  await page.getByRole('navigation', { name: 'Explorar las dimensiones OCEAN' }).getByRole('link', { name: 'N Neuroticismo', exact: true }).click()
  const target = await page.locator('#neuroticismo').boundingBox()
  const nav = await page.locator('.info-nav').boundingBox()
  assert.ok(target.y >= nav.height - 1, 'La navegación tapa la dimensión seleccionada')
  await assertLayout(page)
  assert.equal(state.requests.length, 0, 'Las páginas informativas no requieren datos de una cuenta')
})

test('animación solicitada: el radar se mueve también con movimiento reducido', async t => {
  for (const width of [390, 1366]) {
    const { page } = await prepare(t, width, { motion: 'reduce' })
    await page.waitForFunction(() => window.radarFrames > 2)
    const before = await page.locator('.radar__data').getAttribute('points')
    await page.waitForTimeout(400)
    assert.notEqual(await page.locator('.radar__data').getAttribute('points'), before)
    await page.emulateMedia({ reducedMotion: 'no-preference' })
    await page.emulateMedia({ reducedMotion: 'reduce' })
    const frames = await page.evaluate(() => window.radarFrames)
    await page.waitForFunction(frames => window.radarFrames > frames + 2, frames)
  }
})

for (const width of [390, 1366]) {
  test(`animación continua en ${width}px: cambia de forma después de la entrada`, async t => {
    const { page } = await prepare(t, width, { motion: 'no-preference' })
    await page.waitForFunction(() => window.radarFrames > 2)
    await page.waitForTimeout(3200)
    const frames = await page.evaluate(() => window.radarFrames)
    const points = await page.locator('.radar__data').getAttribute('points')
    await page.waitForTimeout(400)
    assert.ok(await page.evaluate(() => window.radarFrames) > frames)
    assert.notEqual(await page.locator('.radar__data').getAttribute('points'), points)
  })
}

test('animación: salir de pantalla pausa los cuadros y volver los reanuda', async t => {
  const { page } = await prepare(t, 1366, { motion: 'no-preference' })
  await page.waitForFunction(() => window.radarFrames > 2)
  await page.locator('#register').scrollIntoViewIfNeeded()
  await page.waitForTimeout(150)
  const frames = await page.evaluate(() => window.radarFrames)
  await page.waitForTimeout(400)
  assert.equal(await page.evaluate(() => window.radarFrames), frames)
  await page.evaluate(() => window.scrollTo(0, 0))
  await page.waitForFunction(frames => window.radarFrames > frames + 2, frames)
})

test('portada conserva textos, nombres del radar y distribución originales de escritorio', async t => {
  const { page } = await prepare(t, 1366)
  assert.match(await page.locator('.hero__title').innerText(), /Conoce más\s+sobre ti\./)
  assert.doesNotMatch(await page.locator('main').innerText(), /validado científicamente|puedes brillar|compatibilidad con tus|50 países|mayor afinidad/)
  assert.match(await page.locator('.register__sub').innerText(), /Vócalis complementa el acompañamiento de tu orientador/)
  assert.deepEqual(await page.locator('.stat__num').allTextContents(), ['44', '5', '~8'])
  assert.deepEqual(await page.locator('.radar__label').allTextContents(), ['Apertura', 'Responsabilidad', 'Extraversión', 'Amabilidad', 'Neuroticismo'])
  assert.equal(await page.locator('.radar__legend, .radar__axis-letter, .hero__radar-wrap figcaption').count(), 0)
  assert.equal(await page.locator('.hero__radar-wrap').evaluate(el => getComputedStyle(el).display), 'flex')
  assert.equal(await page.locator('.hero__stats').evaluate(el => getComputedStyle(el).display), 'flex')
})

test('animación: ocultar la pestaña o desmontar la portada detiene los cuadros', async t => {
  for (const reason of ['hidden', 'unmount']) {
    const { page } = await prepare(t, 1366, { motion: 'no-preference' })
    await page.waitForFunction(() => window.radarFrames > 2)
    if (reason === 'hidden') await page.evaluate(() => {
      Object.defineProperty(document, 'hidden', { configurable: true, get: () => true })
      document.dispatchEvent(new Event('visibilitychange'))
    })
    else await page.getByRole('navigation').getByRole('link', { name: 'Comenzar gratis', exact: true }).click()
    await page.waitForTimeout(100)
    const frames = await page.evaluate(() => window.radarFrames)
    await page.waitForTimeout(300)
    assert.equal(await page.evaluate(() => window.radarFrames), frames)
    if (reason === 'hidden') await page.evaluate(() => {
      Object.defineProperty(document, 'hidden', { configurable: true, get: () => false })
      document.dispatchEvent(new Event('visibilitychange'))
    })
    if (reason !== 'unmount') await page.waitForFunction(frames => window.radarFrames > frames + 2, frames)
  }
})

async function register(page, role) {
  await page.getByLabel('Tu nombre', { exact: true }).fill(name)
  await page.getByLabel('Correo electrónico', { exact: true }).fill('movil.prueba@example.test')
  await page.getByRole('button', { name: /Crear mi cuenta gratis/ }).click()
  await page.waitForURL('**/auth?*')
  if (role === 'orientador') {
    await page.getByRole('button', { name: 'Orientador Escolar', exact: true }).click()
    await page.getByLabel('Departamento o unidad').fill('Orientación de prueba')
    await page.getByLabel('Código privado de verificación', { exact: true }).fill('CODIGO-FICTICIO-DE-PRUEBA')
  } else {
    await page.getByLabel('Fecha de nacimiento').fill('2008-02-15')
    await page.getByLabel('Nivel', { exact: true }).selectOption('4° Medio')
    await page.getByLabel('Letra', { exact: true }).fill('A')
  }
  await page.getByLabel('Establecimiento educacional').fill('Establecimiento de prueba')
  await page.getByLabel('Contraseña', { exact: true }).fill('ClaveFicticia123')
  await assertLayout(page)
  await page.getByRole('button', { name: /Registrar mi cuenta gratis/ }).click()
  await page.getByRole('status').getByText(/Cuenta registrada con éxito/).waitFor()
  await page.getByLabel('Contraseña', { exact: true }).fill('ClaveFicticia123')
  await page.getByRole('button', { name: /Iniciar Sesión/ }).click()
  await page.waitForURL(`**/${role}/dashboard`)
}

async function completeQuestionnaire(page, state) {
  await page.getByRole('button', { name: 'Iniciar cuestionario BFI-44', exact: true }).click()
  await page.waitForURL('**/estudiante/evaluacion')
  await page.locator('#question-1').waitFor()
  await page.locator('#question-1 .radio-container').nth(2).click()
  await page.getByText('Todas las respuestas seleccionadas están guardadas.', { exact: true }).waitFor()
  await page.reload({ waitUntil: 'domcontentloaded' })
  await page.locator('#question-1').waitFor()
  assert.equal(await page.locator('#question-radio-1-3').isChecked(), true)
  for (let block = 0; block < 5; block++) {
    for (const question of questions.slice(block * 10, (block + 1) * 10)) {
      await page.locator(`#question-${question.id} .radio-container`).nth(2).click()
    }
    await page.getByText('Todas las respuestas seleccionadas están guardadas.', { exact: true }).waitFor()
    await page.getByRole('button', { name: /Siguiente Bloque|Finalizar y Calcular Perfil/ }).click()
    if (block < 4) await page.locator(`#question-${questions[(block + 1) * 10].id}`).waitFor()
  }
  await page.waitForURL('**/estudiante/reporte')
  await page.locator('.radar__svg').waitFor()
  assert.equal(state.submissions.length, 1)
  assert.deepEqual(state.submissions[0].respuestas, questions.map(question => ({ preguntaId: question.id, valor: 3 })))
  await page.locator('#dimension-toggle-E').click()
  assert.equal(await page.locator('#dimension-content-E').isVisible(), true)
  await assertLayout(page)
  await page.getByRole('link', { name: 'Bitácora', exact: true }).click()
  await page.waitForURL('**/estudiante/dashboard#history-section')
  await page.locator('.timeline-item').first().waitFor()
  assert.equal(await page.locator('.timeline-item').count(), 3)
}

for (const width of [390, 1366]) {
  test(`recorrido estudiante ${width}px: registro, ingreso, guardado, 44 respuestas y reporte`, async t => {
    const { page, state } = await prepare(t, width)
    await register(page, 'estudiante')
    assert.equal(state.registrations.length, 1)
    await completeQuestionnaire(page, state)
    await page.getByRole('button', { name: 'Cerrar sesión', exact: true }).click()
    await page.waitForURL('**/auth')
    assert.equal(await page.evaluate(() => localStorage.getItem('vocalis_token')), null)
  })
}

test('recorrido orientador: registro, filtros, reporte correcto y cierre de sesión', async t => {
  const { page, state } = await prepare(t, 390, { role: 'orientador' })
  await register(page, 'orientador')
  await page.locator('.table-row').first().waitFor()
  assert.equal(state.registrations.length, 1)
  assert.equal(state.registrations[0].role, 'orientador')
  await page.getByLabel('Buscar estudiante').fill('alumno.prueba')
  await page.getByLabel('Curso', { exact: true }).selectOption('4° Medio A')
  await page.getByLabel('Estado del Flujo Camunda').selectOption('reporte_listo')
  assert.equal(await page.locator('.table-row').count(), 1)
  await page.getByRole('button', { name: `Ver reporte de ${name}`, exact: true }).click()
  await page.waitForURL('**/orientador/estudiante/42/reporte')
  await page.locator('.radar__svg').waitFor()
  await assertLayout(page)
  await page.getByRole('button', { name: 'Cerrar sesión', exact: true }).click()
  await page.waitForURL('**/auth')
  assert.equal(await page.evaluate(() => localStorage.getItem('vocalis_token')), null)
})

test('ingreso fallido: mensaje legible y reintento sin perder el correo', async t => {
  const { page, state } = await prepare(t, 320, { failLogins: 1 })
  await page.getByRole('navigation').getByRole('link', { name: 'Comenzar gratis', exact: true }).click()
  await page.getByLabel('Correo electrónico', { exact: true }).fill('movil.prueba@example.test')
  await page.getByLabel('Contraseña', { exact: true }).fill('ClaveFicticia123')
  await page.getByRole('button', { name: /Iniciar Sesión/ }).click()
  await page.getByRole('alert').waitFor()
  await assertLayout(page)
  assert.equal(await page.getByLabel('Correo electrónico', { exact: true }).inputValue(), 'movil.prueba@example.test')
  await page.getByRole('button', { name: /Iniciar Sesión/ }).click()
  await page.waitForURL('**/estudiante/dashboard')
  assert.equal(state.logins.length, 2)
})

test('LAN real: ingreso y respuestas pasan por el mismo origen y el proxy de Vite', { skip: !lanBase }, async t => {
  const { page, state } = await prepare(t, 390, { lan: true })
  const apiOrigins = []
  page.on('request', request => {
    const url = new URL(request.url())
    if (url.pathname.startsWith('/api/')) apiOrigins.push(url.origin)
  })
  await register(page, 'estudiante')
  await completeQuestionnaire(page, state)
  assert.ok(apiOrigins.length >= 50)
  assert.ok(apiOrigins.every(origin => origin === new URL(lanBase).origin), 'La API debe usar la dirección de la página, no localhost del teléfono')
  assert.equal(state.answers.size, 44)
  assert.equal(state.registrations.length, 1)
})
