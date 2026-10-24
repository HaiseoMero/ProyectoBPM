// Navegador contra Vite con API simulada: no consulta ni modifica MySQL.
// Admite VOCALIS_PLAYWRIGHT_MODULE, VOCALIS_CHROME_PATH, VOCALIS_TEST_BASE_URL
// y VOCALIS_TEST_SCREENSHOTS para usar las herramientas ya instaladas.
import assert from 'node:assert/strict'
import process from 'node:process'
import { Buffer } from 'node:buffer'
import { mkdir } from 'node:fs/promises'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { before, after, test } from 'node:test'

const modulePath = process.env.VOCALIS_PLAYWRIGHT_MODULE
  ? pathToFileURL(process.env.VOCALIS_PLAYWRIGHT_MODULE).href : 'playwright'
const { chromium } = await import(modulePath)
const base = process.env.VOCALIS_TEST_BASE_URL || 'http://127.0.0.1:5174'
const screenshots = process.env.VOCALIS_TEST_SCREENSHOTS
const studentName = 'María Fernanda de los Ángeles Contreras Sepúlveda'
const students = [
  { id: 42, name: studentName, email: 'maria.fernanda.contreras.sepulveda@establecimiento.cl', course: '4° Medio A', lastUpdate: '1 de octubre de 2026, 10:30', bpm_estado: 'reporte_listo', hasReport: true },
  { id: 77, name: 'José Miguel Piña', email: 'jose@establecimiento.cl', course: '3° Medio B', lastUpdate: '30 de septiembre de 2026, 09:45', bpm_estado: 'calculando_ocean', hasReport: false },
  { id: 88, name: 'Andrea González', email: 'andrea@establecimiento.cl', course: '4° Medio A', lastUpdate: '1 de octubre de 2026, 09:00', bpm_estado: 'generando_reporte', hasReport: false },
  { id: 100, name: 'Alumno Sin Estado', email: 'correoextraordinariamentelargosinseparadores@establecimiento.cl', course: '3° Medio B', lastUpdate: 'Sin evaluación', bpm_estado: null, hasReport: false },
]
const dimensions = [
  { letter: 'N', name: 'Neuroticismo', score: 90 },
  { letter: 'O', name: 'Apertura', score: 25 },
  { letter: 'A', name: 'Amabilidad', score: 60 },
  { letter: 'C', name: 'Responsabilidad', score: 75 },
  { letter: 'E', name: 'Extraversión', score: 40 },
].map(dim => ({ ...dim, color: '#4F46E5', interpretation: `Descripción de ${dim.name} para la reflexión personal.`, vocationalImpact: 'Este puntaje no determina aptitud ni una carrera adecuada.' }))
const report = {
  studentName, evaluatedAt: '1 de octubre de 2026, 10:30', dimensions, bpm_estado: 'reporte_listo',
  careerAreas: [
    { title: 'Artes y Diseño', desc: 'Referencia exploratoria del prototipo.', carreras: ['Diseño Gráfico', 'Diseño de Comunicación Visual'] },
    { title: 'Ciencias Sociales y Humanidades', desc: 'Área para explorar junto con intereses y contexto personal.', carreras: ['Trabajo Social', 'Pedagogía en Historia, Geografía y Ciencias Sociales'] },
  ],
}
let browser

before(async () => {
  browser = await chromium.launch({ headless: true,
    ...(process.env.VOCALIS_CHROME_PATH ? { executablePath: process.env.VOCALIS_CHROME_PATH } : {}) })
  if (screenshots) await mkdir(screenshots, { recursive: true })
})
after(async () => { await browser?.close() })

async function prepare(t, width, role, path, settings = {}) {
  const context = await browser.newContext({ viewport: { width, height: 844 },
    isMobile: width <= 600, hasTouch: width <= 600, reducedMotion: 'reduce' })
  const page = await context.newPage()
  page.setDefaultTimeout(12000)
  const errors = []
  const state = { students, report, reportStatus: 200, stateStatus: 200,
    studentsFailures: 0, requests: [], unassignedCourses: [], assignmentStatus: 200, ...settings }
  page.on('pageerror', error => errors.push(error.message))
  await page.route('**/api/**', async route => {
    const request = route.request()
    const url = new URL(request.url()).pathname
    state.requests.push(url)
    const isAssignment = /^\/api\/orientador\/cursos\/\d+\/asignar$/.test(url)
    assert.equal(request.method(), isAssignment ? 'POST' : 'GET')
    let body
    let status = 200
    if (url === '/api/auth/me') body = { name: role === 'orientador' ? 'Orientadora de prueba' : studentName, role }
    else if (url === '/api/orientador/cursos/sin-asignar') {
      status = state.coursesStatus || 200
      body = status === 200 ? state.unassignedCourses : { detail: 'Fallo de prueba' }
    } else if (isAssignment) {
      if (state.assignmentGate) await state.assignmentGate
      status = state.assignmentStatus
      const id = Number(url.split('/')[4])
      if ([200, 404, 409].includes(status)) state.unassignedCourses = state.unassignedCourses.filter(course => course.id !== id)
      if (status === 200) state.students = [...state.students, {
        id: 123, name: 'Estudiante del nuevo curso', email: 'nuevo@example.test', course: '2° Medio C', lastUpdate: 'Sin evaluación', hasReport: false,
      }]
      body = status === 200 ? { id, orientador_id: 1 } : { detail: 'No se puede asignar' }
    } else if (url === '/api/orientador/estudiantes') {
      if (state.studentsGate) await state.studentsGate
      if (state.studentsFailures) { state.studentsFailures--; status = 503; body = { detail: 'Fallo de prueba' } }
      else body = state.students
    } else if (url === '/api/evaluacion/reporte' || /^\/api\/orientador\/estudiante\/\d+\/reporte$/.test(url)) {
      if (state.reportGate) await state.reportGate
      status = state.reportStatus
      body = status === 200 ? state.report : { detail: 'Fallo de prueba' }
    } else if (url === '/api/evaluacion/estado') {
      status = state.stateStatus
      body = status === 200 ? (state.evaluationState || {
        tiene_evaluacion: true, estado: 'procesada', bpm_estado: 'reporte_listo',
        orientador_nombre: 'Orientadora con nombre y apellidos extensos',
        registro_fecha: '2026-09-29T10:00:00', evaluacion_fecha: '2026-09-30T11:00:00', reporte_fecha: '2026-10-01T10:30:00',
      }) : { detail: 'Fallo de prueba' }
    } else { errors.push(`Petición inesperada ${url}`); status = 500; body = {} }
    await route.fulfill({ status, json: body })
  })
  const token = `test.${Buffer.from(JSON.stringify({ role, exp: Math.floor(Date.now() / 1000) + 3600 })).toString('base64')}.test`
  await page.addInitScript(value => localStorage.setItem('vocalis_token', value), token)
  t.after(async () => { await context.close(); assert.deepEqual(errors, [], 'Errores JavaScript o peticiones inesperadas') })
  await page.goto(`${base}${path}`, { waitUntil: 'domcontentloaded' })
  return { page, state }
}

async function assertLayout(page) {
  const layout = await page.evaluate(() => ({
    width: innerWidth, pageWidth: document.documentElement.scrollWidth,
    overflowing: [...document.querySelectorAll('main .btn, main .btn-table, .filter-input, .filter-select, .accordion-header, .radar__svg, .radar-legend__item')]
      .filter(el => el.getClientRects().length && el.getBoundingClientRect().width > 0)
      .map(el => { const box = el.getBoundingClientRect(); return { className: el.getAttribute('class'), left: box.left, right: box.right, height: box.height } }),
  }))
  assert.ok(layout.pageWidth <= layout.width + 1, `Página desbordada: ${layout.pageWidth} > ${layout.width}`)
  for (const el of layout.overflowing) {
    assert.ok(el.left >= 0 && el.right <= layout.width + 1, `Elemento fuera de pantalla: ${el.className}`)
    if (/btn|filter-|accordion-header/.test(el.className)) assert.ok(el.height >= 44, `Control pequeño: ${el.className}`)
  }
}

async function capture(page, name, width) {
  if (!screenshots || ![390, 1366].includes(width)) return
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: join(screenshots, `${name}-${width}.png`), fullPage: true })
}

for (const width of [320, 360, 390, 430, 600, 601, 768, 900, 901, 1024, 1100, 1101, 1200, 1201, 1366]) {
  test(`paneles y reporte a ${width}px: contenido completo y controles visibles`, async t => {
    const { page: student } = await prepare(t, width, 'estudiante', '/estudiante/dashboard')
    await student.getByRole('button', { name: 'Ver Reporte Completo' }).waitFor()
    await assertLayout(student)
    for (const label of ['Registro', 'Calculando perfil', 'Generando reporte', 'Reporte disponible']) {
      assert.ok(await student.locator('.bpm-step__label').getByText(label, { exact: true }).isVisible())
    }
    assert.equal(await student.locator('.bpm-step[aria-current="step"] .bpm-step__label').textContent(), 'Reporte disponible')
    assert.equal(await student.locator('.q-stat').count(), 5)
    await capture(student, 'panel-estudiante', width)
    await student.getByRole('link', { name: 'Bitácora', exact: true }).click()
    await student.waitForURL('**#history-section')
    await student.locator('.history-title').waitFor()
    assert.equal(await student.locator('.timeline-item').count(), 3)
    await assertLayout(student)
    await capture(student, 'bitacora', width)

    const { page: counselor } = await prepare(t, width, 'orientador', '/orientador/dashboard')
    await counselor.locator('.table-row').first().waitFor()
    await assertLayout(counselor)
    assert.equal(await counselor.locator('.table-row').count(), 4)
    assert.equal(await counselor.getByRole('button', { name: /^Ver reporte de/ }).count(), 4)
    const tableDisplay = await counselor.locator('.students-table').evaluate(el => getComputedStyle(el).display)
    assert.equal(tableDisplay, width <= 1100 ? 'block' : 'table')
    if (width <= 1100) {
      assert.ok(await counselor.locator('.cell-label').first().isVisible())
      assert.equal(await counselor.locator('.table-container').evaluate(el => el.scrollWidth <= el.clientWidth + 1), true)
    }
    if (width <= 900) assert.equal(await counselor.getByLabel('Buscar estudiante').evaluate(el => getComputedStyle(el).fontSize), '16px')
    await capture(counselor, 'panel-orientador', width)

    const { page: result } = await prepare(t, width, 'estudiante', '/estudiante/reporte')
    await result.locator('.radar__svg').waitFor()
    await assertLayout(result)
    assert.equal(await result.getByRole('img', { name: 'Puntajes de las cinco dimensiones BFI-44' }).count(), 1)
    assert.equal(await result.locator('.radar-legend__item').count(), 5)
    assert.equal(await result.locator('.accordion-header').count(), 5)
    await capture(result, 'reporte', width)
  })
}

test('filtros combinados y cambio de tamaño conservan el mismo alumno y controles', async t => {
  const { page } = await prepare(t, 390, 'orientador', '/orientador/dashboard')
  await page.locator('.table-row').first().waitFor()
  assert.deepEqual(await page.locator('.metric-num').allTextContents(), ['4', '2', '1'])
  await page.getByLabel('Buscar estudiante').fill('maria.fernanda')
  await page.getByLabel('Curso', { exact: true }).selectOption('4° Medio A')
  await page.getByLabel('Estado del Flujo Camunda').selectOption('reporte_listo')
  assert.equal(await page.locator('.table-row').count(), 1)
  assert.equal(await page.locator('.student-name').textContent(), studentName)
  await page.locator('.table-row').evaluate(el => { el.dataset.marker = 'same-student' })
  await page.setViewportSize({ width: 1366, height: 844 })
  await assertLayout(page)
  assert.equal(await page.locator('.table-row').getAttribute('data-marker'), 'same-student')
  assert.equal(await page.getByLabel('Buscar estudiante').inputValue(), 'maria.fernanda')
  assert.equal(await page.getByLabel('Curso', { exact: true }).inputValue(), '4° Medio A')
  assert.equal(await page.getByLabel('Estado del Flujo Camunda').inputValue(), 'reporte_listo')
  await page.setViewportSize({ width: 320, height: 844 })
  await assertLayout(page)
  await page.getByLabel('Buscar estudiante').fill('')
  await page.getByLabel('Curso', { exact: true }).selectOption('')
  await page.getByLabel('Estado del Flujo Camunda').selectOption('unavailable')
  assert.equal(await page.locator('.student-name').textContent(), 'Alumno Sin Estado')
  await page.getByLabel('Estado del Flujo Camunda').selectOption('calculando_ocean')
  assert.equal(await page.locator('.student-name').textContent(), 'José Miguel Piña')
  await page.getByLabel('Estado del Flujo Camunda').selectOption('generando_reporte')
  assert.equal(await page.locator('.student-name').textContent(), 'Andrea González')
  await page.getByLabel('Estado del Flujo Camunda').selectOption('registro')
  await page.getByText(/No se encontraron estudiantes/).waitFor()
  assert.equal(await page.locator('.table-row').count(), 0)
  assert.match(await page.locator('.pagination-info').textContent(), /Mostrando 0 de 4/)
})

test('orientador: un único acceso al reporte correcto y acciones pendientes deshabilitadas', async t => {
  const { page, state } = await prepare(t, 390, 'orientador', '/orientador/dashboard')
  await page.locator('.table-row').first().waitFor()
  assert.equal(await page.getByRole('button', { name: 'Ver reporte de José Miguel Piña', exact: true }).isDisabled(), true)
  await page.getByRole('button', { name: `Ver reporte de ${studentName}`, exact: true }).click()
  await page.waitForURL('**/orientador/estudiante/42/reporte')
  await page.locator('.radar__svg').waitFor()
  assert.match(await page.locator('.report-student').textContent(), new RegExp(studentName))
  assert.equal(state.requests.filter(url => url === '/api/orientador/estudiante/42/reporte').length, 1)
  assert.equal(state.requests.includes('/api/evaluacion/reporte'), false)
  await assertLayout(page)
  await page.getByRole('link', { name: 'Panel de alumnos', exact: true }).click()
  await page.waitForURL('**/orientador/dashboard')
  await page.locator('.table-row').first().waitFor()
})

test('estudiante: bitácora y reporte mantienen el acceso al panel', async t => {
  const { page } = await prepare(t, 390, 'estudiante', '/estudiante/dashboard#history-section')
  await page.locator('.timeline-item').first().waitFor()
  await page.getByRole('link', { name: 'Panel principal', exact: true }).click()
  await page.getByRole('button', { name: 'Ver Reporte Completo' }).click()
  await page.waitForURL('**/estudiante/reporte')
  await page.locator('.radar__svg').waitFor()
  await page.getByRole('link', { name: 'Bitácora', exact: true }).click()
  await page.waitForURL('**/estudiante/dashboard#history-section')
  await page.locator('.timeline-item').first().waitFor()
  assert.equal(await page.locator('.timeline-item').count(), 3)
})

test('reporte: los ejes y porcentajes corresponden a OCEAN aunque cambie el orden del JSON', async t => {
  const { page } = await prepare(t, 390, 'estudiante', '/estudiante/reporte')
  await page.locator('.radar__svg').waitFor()
  assert.deepEqual(await page.locator('.radar-legend dt').allTextContents(), ['O Apertura', 'C Responsabilidad', 'E Extraversión', 'A Amabilidad', 'N Neuroticismo'])
  assert.deepEqual(await page.locator('.radar-legend dd').allTextContents(), ['25%', '75%', '40%', '60%', '90%'])
  assert.equal(await page.locator('.badge-value').textContent(), 'Neuroticismo (90%)')
  const points = (await page.locator('.radar__data').getAttribute('points')).split(' ').map(point => point.split(',').map(Number))
  for (const [i, angle] of [-90, -18, 54, 126, 198].entries()) {
    const radius = [25, 75, 40, 60, 90][i] / 100 * 120
    assert.ok(Math.abs(points[i][0] - (160 + radius * Math.cos(angle * Math.PI / 180))) < 0.001)
    assert.ok(Math.abs(points[i][1] - (160 + radius * Math.sin(angle * Math.PI / 180))) < 0.001)
  }
})

test('acordeones: toque, Enter y Espacio abren y cierran el contenido asociado', async t => {
  const { page } = await prepare(t, 320, 'estudiante', '/estudiante/reporte')
  const toggle = page.locator('#dimension-toggle-N')
  await toggle.waitFor()
  assert.equal(await toggle.getAttribute('aria-expanded'), 'true')
  assert.equal(await toggle.getAttribute('aria-controls'), 'dimension-content-N')
  await toggle.click()
  assert.equal(await page.locator('#dimension-content-N').isVisible(), false)
  await toggle.focus()
  await page.keyboard.press('Enter')
  assert.equal(await page.locator('#dimension-content-N').isVisible(), true)
  await page.keyboard.press('Space')
  assert.equal(await toggle.getAttribute('aria-expanded'), 'false')
  assert.equal(await page.locator('#dimension-content-N').isVisible(), false)
  await page.locator('#dimension-toggle-C').click()
  assert.equal(await page.locator('#dimension-content-C').isVisible(), true)
  await page.setViewportSize({ width: 1366, height: 844 })
  assert.equal(await page.locator('#dimension-content-C').isVisible(), true)
  assert.equal(await page.locator('#dimension-content-N').isVisible(), false)
})

test('orientador: carga, error y reintento conservan los filtros', async t => {
  let release
  const gate = new Promise(resolve => { release = resolve })
  const { page, state } = await prepare(t, 320, 'orientador', '/orientador/dashboard', { studentsFailures: 1, studentsGate: gate })
  await page.getByRole('status').getByText('Cargando estudiantes…', { exact: true }).waitFor()
  await page.getByLabel('Curso', { exact: true }).selectOption('')
  await page.getByLabel('Buscar estudiante').fill('José')
  release()
  await page.getByRole('alert').waitFor()
  await assertLayout(page)
  state.studentsGate = null
  await page.getByRole('button', { name: 'Reintentar', exact: true }).click()
  await page.locator('.table-row').waitFor()
  assert.equal(await page.locator('.student-name').textContent(), 'José Miguel Piña')
  assert.equal(await page.getByLabel('Buscar estudiante').inputValue(), 'José')
})

test('orientador: sin alumnos asignados se muestra el estado vacío', async t => {
  const { page } = await prepare(t, 320, 'orientador', '/orientador/dashboard', { students: [] })
  await page.getByText('Todavía no tienes estudiantes asignados.', { exact: true }).waitFor()
  assert.deepEqual(await page.locator('.metric-num').allTextContents(), ['0', '0', '0'])
  assert.equal(await page.getByRole('button', { name: /^Ver reporte de/ }).count(), 0)
  await assertLayout(page)
})

test('estudiante: sin evaluación ni fechas se ofrece cuestionario y bitácora vacía', async t => {
  const { page } = await prepare(t, 320, 'estudiante', '/estudiante/dashboard', {
    reportStatus: 404, evaluationState: { tiene_evaluacion: false, estado: null, bpm_estado: 'registro' },
  })
  await page.getByRole('button', { name: 'Iniciar cuestionario BFI-44', exact: true }).waitFor()
  await assertLayout(page)
  await page.getByRole('link', { name: 'Bitácora', exact: true }).click()
  await page.getByText('Aún no hay fechas registradas en tu bitácora.', { exact: true }).waitFor()
  await assertLayout(page)
})

test('estudiante: fallo de consulta no ofrece iniciar otra evaluación', async t => {
  const { page } = await prepare(t, 390, 'estudiante', '/estudiante/dashboard', { reportStatus: 503, stateStatus: 503 })
  await page.getByRole('alert').waitFor()
  assert.equal(await page.getByRole('button', { name: 'Iniciar cuestionario BFI-44', exact: true }).count(), 0)
  await assertLayout(page)
})

test('reporte: carga pendiente sin datos y contenido neutral sin áreas', async t => {
  let release
  const gate = new Promise(resolve => { release = resolve })
  const { page } = await prepare(t, 390, 'estudiante', '/estudiante/reporte', { reportGate: gate, report: { ...report, careerAreas: [] } })
  await page.getByRole('status').getByText('Cargando tu reporte…', { exact: true }).waitFor()
  assert.equal(await page.locator('.radar__data').count(), 0)
  release()
  await page.locator('.radar__svg').waitFor()
  await page.getByText(/Las reglas actuales no permiten sugerir un área/).waitFor()
  assert.equal(await page.locator('.career-area-card').count(), 0)
  await assertLayout(page)
})

for (const [role, path] of [['estudiante', '/estudiante/reporte'], ['orientador', '/orientador/estudiante/42/reporte']]) {
  for (const [state, label] of [['reporte_listo', 'Reporte disponible'], ['generando_reporte', 'Generando reporte'], [null, 'Estado no disponible'], ['otro', 'Estado no disponible']]) {
    test(`${role}: el aviso del reporte muestra ${label} para ${state}`, async t => {
      const { page, state: api } = await prepare(t, 390, role, path, { report: { ...report, bpm_estado: state } })
      await page.locator('.radar__svg').waitFor()
      assert.equal(await page.locator('.bpm-status-text').textContent(), `Estado del proceso: ${label}`)
      assert.equal(api.requests.includes('/api/evaluacion/estado'), false, 'El estado pertenece al reporte, no a la sesión del orientador')
    })
  }
}

test('orientador: toma un curso a cargo, bloquea doble envío y actualiza alumnos sin perder filtros', async t => {
  let release
  const assignmentGate = new Promise(resolve => { release = resolve })
  const { page, state } = await prepare(t, 320, 'orientador', '/orientador/dashboard', {
    unassignedCourses: [{ id: 5, nombre: '2° Medio C', total_estudiantes: 1 }], assignmentGate,
  })
  const action = page.getByRole('button', { name: 'Tomar a cargo 2° Medio C', exact: true })
  await action.waitFor()
  await assertLayout(page)
  await capture(page, 'cursos-sin-asignar', 390)
  await page.getByLabel('Buscar estudiante').fill('nuevo')
  await action.click()
  assert.equal(await action.isDisabled(), true)
  assert.equal(await page.getByRole('button', { name: 'Actualizar cursos', exact: true }).isDisabled(), true)
  release()
  await page.getByText('Ahora tienes a cargo el curso 2° Medio C.', { exact: true }).waitFor()
  await page.getByText('No hay cursos sin asignar en tu establecimiento.', { exact: true }).waitFor()
  await page.getByText('Estudiante del nuevo curso', { exact: true }).waitFor()
  assert.equal(await page.getByLabel('Buscar estudiante').inputValue(), 'nuevo')
  assert.equal(state.requests.filter(path => path.endsWith('/asignar')).length, 1)
  assert.equal(await page.locator('.metric-num').first().textContent(), '5')
  await assertLayout(page)
})

for (const status of [409, 503]) {
  test(`orientador: asignación fallida ${status} informa y conserva los alumnos`, async t => {
    const { page } = await prepare(t, 390, 'orientador', '/orientador/dashboard', {
      unassignedCourses: [{ id: 5, nombre: '2° Medio C', total_estudiantes: 1 }], assignmentStatus: status,
    })
    await page.getByRole('button', { name: 'Tomar a cargo 2° Medio C', exact: true }).click()
    await page.getByRole('alert').waitFor()
    assert.match(await page.getByRole('alert').textContent(), status === 409 ? /Otro orientador ya tomó/ : /No se pudo confirmar/)
    assert.equal(await page.locator('.table-row').count(), 4)
    if (status === 409) await page.getByText('No hay cursos sin asignar en tu establecimiento.', { exact: true }).waitFor()
    else assert.equal(await page.getByRole('button', { name: 'Tomar a cargo 2° Medio C', exact: true }).isEnabled(), true)
    await assertLayout(page)
  })
}

test('orientador: un fallo al consultar cursos permite actualizar sin perder alumnos', async t => {
  const { page, state } = await prepare(t, 390, 'orientador', '/orientador/dashboard', { coursesStatus: 503 })
  await page.getByRole('alert').waitFor()
  state.coursesStatus = 200
  await page.getByRole('button', { name: 'Actualizar cursos', exact: true }).click()
  await page.getByText('No hay cursos sin asignar en tu establecimiento.', { exact: true }).waitFor()
  assert.equal(await page.locator('.table-row').count(), 4)
})

for (const [status, message] of [[403, 'No tienes permiso para consultar el reporte de este estudiante.'], [404, 'No hay un reporte disponible.'], [503, 'No se pudo cargar el reporte. Intenta nuevamente.']]) {
  test(`reporte del orientador: error ${status} muestra mensaje y permite regresar`, async t => {
    const { page } = await prepare(t, 320, 'orientador', '/orientador/estudiante/42/reporte', { reportStatus: status })
    await page.getByRole('alert').waitFor()
    assert.equal(await page.getByRole('alert').textContent(), message)
    assert.equal(await page.locator('.radar__data').count(), 0)
    await assertLayout(page)
    await page.getByRole('link', { name: 'Panel de alumnos', exact: true }).click()
    await page.waitForURL('**/orientador/dashboard')
    await page.locator('.table-row').first().waitFor()
  })
}
