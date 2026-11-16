# Traspaso: rediseño verde del frontend de Vócalis a `main`

> Documento para un agente de código (Antigravity / Gemini). Objetivo: dejar en la rama `main` del repositorio **exactamente** el frontend de la rama local `feature/paleta-verde-landing`, y luego subirlo a GitHub (`main` de `HaiseoMero/ProyectoBPM`).

## 1. Contexto

- Proyecto: **Vócalis**, app web de orientación vocacional (test BFI-44 / OCEAN). Frontend Vue 3 (`<script setup>`) + Vite, en la raíz del repo (`src/`, `public/`). Backend FastAPI en `backend/` (NO se toca).
- Repo local: `/Users/josepina/Desktop/Proyecto de titulo/ProyectoBPM`
- Rama base: `main` (commit `a498340`). Rama con los cambios: `feature/paleta-verde-landing` (commit `8c31d42`).
- La rama verde **parte de `main` y solo le agrega commits**: el traspaso es un *fast-forward*, sin conflictos.
- Solo cambian archivos de frontend: 10 archivos de código en `src/` y 30 imágenes nuevas en `public/areas/`. No hay archivos borrados ni renombrados.

Commits que se traspasan:

- `8c31d42` refactor(reporte): simplificar las tarjetas de carreras
- `50e9969` feat(reporte): rediseñar resultados OCEAN y áreas profesionales
- `ac31ccf` feat(frontend): aplicar paleta verde y rediseño visual a todo el frontend

Qué cambia, en resumen:

- Paleta verde centralizada en `src/styles/base.css` y aplicada a todas las vistas.
- Portada (`homeview.vue`) rediseñada: radar de ejemplo, secciones «Para quién es» y «Qué es y qué no es», espectro por rasgo.
- Auth con panel lateral; paneles de estudiante y orientador, cuestionario y páginas informativas con el mismo estilo.
- Reporte (`ReporteView.vue`) rediseñado: dimensiones en orden OCEAN con escala bipolar, radar, y áreas profesionales con tarjetas de carreras (imagen, nombre, descripción y enlace a mifuturo.cl). Datos en el archivo nuevo `src/data/areasEstudio.js`.
- 30 fotos de carreras (Wikimedia Commons, licencia libre; los créditos están en la página del reporte).
- Se mantienen los colores de los rasgos OCEAN y las clases que usan las pruebas.

## 2. Reglas para el agente

1. Toca **solo** `src/` y `public/areas/`. No modifiques `backend/`, `docs/`, `bpmn/`, `tests/`, `vite.config.js` ni `package.json`.
2. **Nunca** incluyas en un commit: archivos `__pycache__/*.pyc` (aparecen modificados en `git status`, ignóralos) ni `docs/Guia_de_estudio_Vocalis.pdf` (sin seguimiento). Usa `git add src public`, **nunca** `git add .` ni `git add -A`.
3. No ejecutes `npm run lint` (los scripts llevan `--fix` y reescriben archivos).
4. No reformatees ni «mejores» el código: el resultado debe ser idéntico byte a byte (se verifica con hashes en la sección 5).
5. No borres la rama `feature/paleta-verde-landing`.
6. Node: si `npm` no está en el PATH, usa `export PATH="$HOME/.nvm/versions/node/v22.23.4/bin:$PATH"`.

## 3. Opción A (recomendada): traspaso con git en el mismo notebook

Úsala si el repo local tiene la rama `feature/paleta-verde-landing` (compruébalo con `git branch --list feature/paleta-verde-landing`).

```bash
cd "/Users/josepina/Desktop/Proyecto de titulo/ProyectoBPM"
git status --short | grep -v __pycache__   # solo debe aparecer ?? docs/Guia_de_estudio_Vocalis.pdf
git switch main
git merge --ff-only feature/paleta-verde-landing
git log --oneline -4                        # el primero debe ser 8c31d42
```

Si `git merge --ff-only` falla porque `main` avanzó, **no fuerces nada**: usa `git merge feature/paleta-verde-landing` y resuelve conflictos quedándote con la versión de la rama verde en `src/` y `public/areas/`; luego sigue con la sección 5.

Con esto ya están todos los cambios. Pasa a la sección 5 (verificar) y 6 (subir a GitHub).

## 4. Opción B: aplicar los cambios a mano (si no existe la rama)

Parte desde `main` limpio (`git switch main`) y:

1. **Imágenes:** copia la carpeta `public/areas/` que está dentro de `/Users/josepina/Desktop/Proyecto de titulo/CAMBIOS_FRONTEND_PALETA_VERDE_imagenes` a la carpeta `public/` del repo (deben quedar en `public/areas/*.jpg`). Son 30 archivos:

   ```bash
   cp -R "/Users/josepina/Desktop/Proyecto de titulo/CAMBIOS_FRONTEND_PALETA_VERDE_imagenes/public/areas" "/Users/josepina/Desktop/Proyecto de titulo/ProyectoBPM/public/"
   ```

2. **Código:** para cada archivo del Anexo, **reemplaza el archivo completo** por el contenido indicado (crea `src/data/areasEstudio.js`, que es nuevo). No mezcles con el contenido anterior.
3. Sigue con la sección 5.

## 5. Verificación (obligatoria en ambas opciones)

**a) Hashes:** cada archivo debe tener exactamente este hash de git (`git hash-object <ruta>`):

| Estado | Archivo | Bytes | `git hash-object` esperado |
|---|---|---|---|
| Nuevo | `public/areas/administracion-publica.jpg` | 138239 | `190b265525b3a4d641472cbf504a09b42bca23e1` |
| Nuevo | `public/areas/agronomia.jpg` | 181809 | `84bc4c139cce84eb2227cad2f2731d5daf6a4ce2` |
| Nuevo | `public/areas/antropologia.jpg` | 192500 | `0802dd8d71a4927bf24fd7d132b8865b65236c8e` |
| Nuevo | `public/areas/area-1.jpg` | 171641 | `cd9cf6d13f3fdfb41b3a8b2019990101b4e9dc52` |
| Nuevo | `public/areas/area-2.jpg` | 217920 | `e05ae098e899eb7c1eee6b8b51ad2b9976c3a719` |
| Nuevo | `public/areas/area-3.jpg` | 129071 | `4c2dbf3487da82bec5e77238b10585ea5c08e218` |
| Nuevo | `public/areas/area-4.jpg` | 111142 | `a2175df6894b9192145830750d1dc0419f60efd2` |
| Nuevo | `public/areas/area-5.jpg` | 196232 | `59b5cf413d5222f41e308b922a32fe59485b42df` |
| Nuevo | `public/areas/area-6.jpg` | 154083 | `2a45fdcb6b635aede184c6767224f7e32c8ada19` |
| Nuevo | `public/areas/arquitectura.jpg` | 205411 | `7f278f1446d316f5c11a9550e4bca5aa355b2884` |
| Nuevo | `public/areas/astronomia.jpg` | 96294 | `50e8407741ecf127092b87572ffaf50ac6cfc5f6` |
| Nuevo | `public/areas/auditoria.jpg` | 90434 | `476ff0ac823627cfbce0e431eefbf2a185578753` |
| Nuevo | `public/areas/biologia.jpg` | 156529 | `2fd21605e6e56e5789f3946272554e4b79f07158` |
| Nuevo | `public/areas/derecho.jpg` | 61945 | `43ae5bf0c97e08ce88810e59c6215cbfd1b2692c` |
| Nuevo | `public/areas/diseno-grafico.jpg` | 96183 | `e06d6e45c0ea9ddf517aada2657fc37981c9c08e` |
| Nuevo | `public/areas/educacion-parvularia.jpg` | 243453 | `f244220229f08792e7ae9e2843f934faab697964` |
| Nuevo | `public/areas/enfermeria.jpg` | 164824 | `04bd03ece844058a5d7541740beba18443326655` |
| Nuevo | `public/areas/fonoaudiologia.jpg` | 133625 | `9b7c4957fc96b1c7c449af09079cb3bdc08f284c` |
| Nuevo | `public/areas/ingenieria-comercial.jpg` | 120986 | `4b1832b17def75c3e6e30a8f1cddff9157daf76e` |
| Nuevo | `public/areas/ingenieria-informatica.jpg` | 163422 | `b4829e85911332edc0a29c9641f6d461c047688e` |
| Nuevo | `public/areas/kinesiologia.jpg` | 100572 | `da5367fd9635d910104af034b8cdad7482b7f689` |
| Nuevo | `public/areas/medicina-veterinaria.jpg` | 93286 | `d8f39f31ba0b24178292c264a16645390041830c` |
| Nuevo | `public/areas/medicina.jpg` | 128599 | `965925efadf03ffdf2b7b6234b2443720d46d363` |
| Nuevo | `public/areas/pedagogia.jpg` | 91550 | `2eab07667a2768f863ba930e9e97ed9b5e56fad7` |
| Nuevo | `public/areas/periodismo.jpg` | 161276 | `5cd0610e3266d8a20c4d66ec8ada54cae0e1698e` |
| Nuevo | `public/areas/psicologia.jpg` | 162652 | `aad11fd6548b0be75def2aec522d1967dda4f29d` |
| Nuevo | `public/areas/relaciones-publicas.jpg` | 152255 | `f55624cd3a91ff4cdad45c50146c45ae0c948e40` |
| Nuevo | `public/areas/sociologia.jpg` | 99503 | `8239b1122bdf49c31ffb2b38b28eddf0411de576` |
| Nuevo | `public/areas/tecnologia-medica.jpg` | 65751 | `744e5dbc01332fd66982270462b3f99c79ea9644` |
| Nuevo | `public/areas/trabajo-social.jpg` | 188299 | `e927fad6a3379ab577bef890ba1a1023fc48e12c` |
| Modificado | `src/components/DashboardNavigation.vue` | 5215 | `f4f59d35929dcf15ff973b23b048b2dfd041e67d` |
| Nuevo | `src/data/areasEstudio.js` | 28963 | `9ae300635fb2460ea91ecdfbd5e030c95ac8ac0a` |
| Modificado | `src/styles/base.css` | 3115 | `760edb9ed4e36ea8366ec2bd48f7265e7b584830` |
| Modificado | `src/styles/public-info.css` | 12704 | `fdcd9915534bf01c9a3e10aa16118d4cf5881b06` |
| Modificado | `src/views/AuthView.vue` | 21174 | `d5457f7487ac0d180d2da4e5f3d942afd849984f` |
| Modificado | `src/views/EvaluacionView.vue` | 28325 | `67d798ae4f82e7504b7865ca42f7dc95e38227db` |
| Modificado | `src/views/OrientadorDashboardView.vue` | 21769 | `804bdd0a362d11feec23dc63b51ec1538b0d4915` |
| Modificado | `src/views/ReporteView.vue` | 35271 | `c5a0d8a993e1947f5f85fe9f39751a2a6fb74db4` |
| Modificado | `src/views/StudentDashboardView.vue` | 22610 | `d24c5c8d4aa226a6ff68a9ae92395b001b5b0b91` |
| Modificado | `src/views/homeview.vue` | 51376 | `7ed9053a8d3993a54c39c574bfb8416f0c1b9855` |

Comprobación automática (debe imprimir `OK` en todas las líneas):

```bash
cd "/Users/josepina/Desktop/Proyecto de titulo/ProyectoBPM"
while read h f; do [ "$(git hash-object "$f")" = "$h" ] && echo "OK   $f" || echo "MAL  $f"; done <<'EOF'
190b265525b3a4d641472cbf504a09b42bca23e1 public/areas/administracion-publica.jpg
84bc4c139cce84eb2227cad2f2731d5daf6a4ce2 public/areas/agronomia.jpg
0802dd8d71a4927bf24fd7d132b8865b65236c8e public/areas/antropologia.jpg
cd9cf6d13f3fdfb41b3a8b2019990101b4e9dc52 public/areas/area-1.jpg
e05ae098e899eb7c1eee6b8b51ad2b9976c3a719 public/areas/area-2.jpg
4c2dbf3487da82bec5e77238b10585ea5c08e218 public/areas/area-3.jpg
a2175df6894b9192145830750d1dc0419f60efd2 public/areas/area-4.jpg
59b5cf413d5222f41e308b922a32fe59485b42df public/areas/area-5.jpg
2a45fdcb6b635aede184c6767224f7e32c8ada19 public/areas/area-6.jpg
7f278f1446d316f5c11a9550e4bca5aa355b2884 public/areas/arquitectura.jpg
50e8407741ecf127092b87572ffaf50ac6cfc5f6 public/areas/astronomia.jpg
476ff0ac823627cfbce0e431eefbf2a185578753 public/areas/auditoria.jpg
2fd21605e6e56e5789f3946272554e4b79f07158 public/areas/biologia.jpg
43ae5bf0c97e08ce88810e59c6215cbfd1b2692c public/areas/derecho.jpg
e06d6e45c0ea9ddf517aada2657fc37981c9c08e public/areas/diseno-grafico.jpg
f244220229f08792e7ae9e2843f934faab697964 public/areas/educacion-parvularia.jpg
04bd03ece844058a5d7541740beba18443326655 public/areas/enfermeria.jpg
9b7c4957fc96b1c7c449af09079cb3bdc08f284c public/areas/fonoaudiologia.jpg
4b1832b17def75c3e6e30a8f1cddff9157daf76e public/areas/ingenieria-comercial.jpg
b4829e85911332edc0a29c9641f6d461c047688e public/areas/ingenieria-informatica.jpg
da5367fd9635d910104af034b8cdad7482b7f689 public/areas/kinesiologia.jpg
d8f39f31ba0b24178292c264a16645390041830c public/areas/medicina-veterinaria.jpg
965925efadf03ffdf2b7b6234b2443720d46d363 public/areas/medicina.jpg
2eab07667a2768f863ba930e9e97ed9b5e56fad7 public/areas/pedagogia.jpg
5cd0610e3266d8a20c4d66ec8ada54cae0e1698e public/areas/periodismo.jpg
aad11fd6548b0be75def2aec522d1967dda4f29d public/areas/psicologia.jpg
f55624cd3a91ff4cdad45c50146c45ae0c948e40 public/areas/relaciones-publicas.jpg
8239b1122bdf49c31ffb2b38b28eddf0411de576 public/areas/sociologia.jpg
744e5dbc01332fd66982270462b3f99c79ea9644 public/areas/tecnologia-medica.jpg
e927fad6a3379ab577bef890ba1a1023fc48e12c public/areas/trabajo-social.jpg
f4f59d35929dcf15ff973b23b048b2dfd041e67d src/components/DashboardNavigation.vue
9ae300635fb2460ea91ecdfbd5e030c95ac8ac0a src/data/areasEstudio.js
760edb9ed4e36ea8366ec2bd48f7265e7b584830 src/styles/base.css
fdcd9915534bf01c9a3e10aa16118d4cf5881b06 src/styles/public-info.css
d5457f7487ac0d180d2da4e5f3d942afd849984f src/views/AuthView.vue
67d798ae4f82e7504b7865ca42f7dc95e38227db src/views/EvaluacionView.vue
804bdd0a362d11feec23dc63b51ec1538b0d4915 src/views/OrientadorDashboardView.vue
c5a0d8a993e1947f5f85fe9f39751a2a6fb74db4 src/views/ReporteView.vue
d24c5c8d4aa226a6ff68a9ae92395b001b5b0b91 src/views/StudentDashboardView.vue
7ed9053a8d3993a54c39c574bfb8416f0c1b9855 src/views/homeview.vue
EOF
```

**b) Pruebas y build:**

```bash
npm test            # esperado: pass 4, fail 0
npm run build       # esperado: termina con ✓ built
```

Nota: `npm run build` reescribe `dist/`. Si hay un `vite preview` + túnel de Cloudflare sirviendo `dist/`, el túnel pasará a mostrar el diseño verde (es lo esperado; no hace falta reiniciar el túnel).

**c) Revisión visual** con `npm run dev` (http://127.0.0.1:5173): portada `/`, `/auth`, panel del estudiante, cuestionario, reporte (ver tarjetas de carreras con fotos) y panel del orientador. Todo debe verse en verde.

Diff esperado de `src/` respecto de `main`:

```text
src/components/DashboardNavigation.vue |   28 +-
 src/data/areasEstudio.js               |  595 +++++++++++++
 src/styles/base.css                    |   35 +-
 src/styles/public-info.css             |   83 +-
 src/views/AuthView.vue                 |  335 +++++---
 src/views/EvaluacionView.vue           |  103 ++-
 src/views/OrientadorDashboardView.vue  |   79 +-
 src/views/ReporteView.vue              |  549 +++++++-----
 src/views/StudentDashboardView.vue     |  280 +++---
 src/views/homeview.vue                 | 1457 ++++++++++++++++++++++----------
 10 files changed, 2570 insertions(+), 974 deletions(-)
```

## 6. Subir a GitHub (`main`)

Solo si la sección 5 salió bien.

```bash
git status --short | grep -v __pycache__   # no debe haber nada pendiente de src/ ni public/
git push origin main
```

Si usaste la **Opción B**, antes del push haz un solo commit, agregando solo frontend:

```bash
git add src public
git status --short | grep -v __pycache__   # revisa que solo haya src/ y public/areas/
git commit -m "feat(frontend): aplicar paleta verde y rediseño del reporte con áreas profesionales"
git push origin main
```

**Permisos:** la cuenta de GitHub `josepina-hash` solo tiene permiso de **lectura** sobre `HaiseoMero/ProyectoBPM`, así que con ella el `git push` será rechazado (403). Hay que hacerlo con una cuenta que tenga permiso de escritura (por ejemplo, la cuenta propietaria del repositorio, `HaiseoMero`) o pedir ese permiso. Si el push falla por permisos, **no** intentes forzarlo ni cambiar el remoto: detente y avisa.

## Anexo: contenido final completo de cada archivo de código

Cada bloque es el archivo **entero** tal como debe quedar (rama `feature/paleta-verde-landing`, commit `8c31d42`). Los bloques usan cinco comillas invertidas (`````) como delimitador; el delimitador **no** es parte del archivo. Cada archivo termina con un salto de línea final.

### `src/components/DashboardNavigation.vue` (reemplazar completo, 160 líneas, hash `f4f59d35929dcf15ff973b23b048b2dfd041e67d`)

`````vue
<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: { type: Array, required: true },
  userName: { type: String, required: true },
  userRole: { type: String, required: true },
  label: { type: String, default: 'Navegación principal' },
})
defineEmits(['logout'])

const initials = computed(() => props.userName.trim().split(/\s+/).filter(Boolean)
  .slice(0, 2).map(part => Array.from(part)[0]).join('').toUpperCase() || '—')
</script>

<template>
  <aside class="dashboard-navigation">
    <div class="navigation-brand">
      <span class="navigation-brand__icon" aria-hidden="true">◈</span>
      <span>Vócalis</span>
    </div>

    <nav class="navigation-links" :aria-label="label">
      <router-link v-for="item in items" :key="item.to" :to="item.to"
        class="navigation-link" :class="{ 'navigation-link--active': item.active }"
        :aria-current="item.active ? 'page' : null">
        {{ item.label }}
      </router-link>
    </nav>

    <div class="navigation-profile">
      <span class="navigation-avatar" aria-hidden="true">{{ initials }}</span>
      <div class="navigation-user">
        <span class="navigation-user__name">{{ userName }}</span>
        <span class="navigation-user__role">{{ userRole }}</span>
      </div>
    </div>
    <button type="button" class="navigation-logout" @click="$emit('logout')">
      Cerrar sesión
    </button>
  </aside>
</template>

<style scoped>
.dashboard-navigation {
  width: var(--sidebar-w);
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 50;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 32px 24px;
  background: var(--c-surface);
  border-right: 1px solid var(--c-border);
  overflow-y: auto;
}
.navigation-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-size: 1.3rem;
  font-weight: 800;
}
.navigation-brand__icon { color: var(--c-primary); }
@media (prefers-reduced-motion: reduce) { .navigation-link, .navigation-logout { transition: none; } }
.navigation-links { display: flex; flex-direction: column; gap: 8px; }
.navigation-link, .navigation-logout {
  display: flex;
  align-items: center;
  min-height: 44px;
  padding: 12px;
  border: 1px solid transparent;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  overflow-wrap: anywhere;
}
.navigation-link { position: relative; color: var(--c-muted); transition: background-color 0.2s, color 0.2s; }
.navigation-link:hover { color: var(--c-text); background: var(--c-bg); }
.navigation-link--active,
.navigation-link--active:hover {
  color: var(--c-primary);
  background: var(--c-tint);
}
.navigation-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid var(--c-border);
}
.navigation-avatar {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--c-tint);
  border: 1px solid var(--c-tint-border);
  color: var(--c-primary);
  font-size: 0.85rem;
  font-weight: 700;
}
.navigation-user { display: flex; flex-direction: column; min-width: 0; }
.navigation-user__name { font-size: 0.88rem; font-weight: 600; overflow-wrap: anywhere; }
.navigation-user__role { font-size: 0.75rem; color: var(--c-muted); }
.navigation-logout { color: var(--c-danger); background: transparent; cursor: pointer; transition: background-color 0.2s; }
.navigation-logout:hover { background: var(--c-danger-bg); }

/* Conserva la apariencia del menú original en escritorio. */
@media (min-width: 901px) {
  .dashboard-navigation { gap: 0; }
  .navigation-brand { margin-bottom: 40px; }
  .navigation-links { flex: 1; }
  .navigation-link { padding: 12px 16px; border: none; border-radius: 12px; }
  /* Marca lateral del enlace activo */
  .navigation-link--active::before {
    content: '';
    position: absolute;
    left: -24px; top: 10px; bottom: 10px;
    width: 3px;
    border-radius: 0 3px 3px 0;
    background: var(--c-primary);
  }
  .navigation-profile { margin-top: 0; }
  .navigation-logout { min-height: 44px; margin-top: 16px; padding: 8px; border: none; border-radius: 8px; font-size: 0.85rem; color: var(--c-danger); }
}

@media (max-width: 900px) {
  .dashboard-navigation {
    position: static;
    width: 100%;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 16px 12px;
    padding: 16px var(--page-gutter);
    border-right: 0;
    border-bottom: 1px solid var(--c-border);
    overflow: visible;
  }
  .navigation-brand { grid-column: 1; grid-row: 1; font-size: 1.2rem; }
  .navigation-logout { grid-column: 2; grid-row: 1; padding: 8px 10px; font-size: 0.85rem; }
  .navigation-profile { grid-column: 1 / -1; grid-row: 2; margin: 0; padding: 0; border: 0; }
  .navigation-avatar { width: 32px; height: 32px; }
  .navigation-links { grid-column: 1 / -1; grid-row: 3; flex-direction: row; flex-wrap: wrap; }
  .navigation-link {
    flex: 1 1 110px;
    justify-content: center;
    text-align: center;
    border-color: var(--c-border);
    padding: 10px 12px;
  }
  .navigation-link--active { border-color: var(--c-tint-border); }
}
</style>
`````

### `src/data/areasEstudio.js` (NUEVO, 595 líneas, hash `9ae300635fb2460ea91ecdfbd5e030c95ac8ac0a`)

`````js
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
`````

### `src/styles/base.css` (reemplazar completo, 91 líneas, hash `760edb9ed4e36ea8366ec2bd48f7265e7b584830`)

`````css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap');

/* Sistema visual Vócalis: paleta verde compartida por todas las vistas. */
:root {
  --c-bg: #F8FAFC;             /* Slate 50 - Fondo general */
  --c-surface: #FFFFFF;        /* Tarjetas */
  --c-primary: #047857;        /* Emerald 700 - Acción principal */
  --c-primary-strong: #065F46; /* Emerald 800 - Hover */
  --c-deep: #064E3B;           /* Emerald 900 - Bloques oscuros */
  --c-accent1: #0D9488;        /* Teal 600 */
  --c-accent2: #84CC16;        /* Lime 500 */
  --c-tint: #ECFDF5;           /* Emerald 50 - Fondos suaves */
  --c-tint-border: #A7F3D0;    /* Emerald 200 - Bordes suaves */
  --c-border: #E2E8F0;         /* Slate 200 */
  --c-border-strong: #CBD5E1;  /* Slate 300 - Bordes de campos */
  --c-text: #0F172A;           /* Slate 900 */
  --c-text-soft: #334155;      /* Slate 700 - Texto de lectura */
  --c-muted: #64748B;          /* Slate 500 */
  --c-accent-completed: #059669; /* Emerald 600 - Estado completado */
  --c-danger: #B91C1C;
  --c-danger-bg: #FEF2F2;
  --c-danger-border: #FCA5A5;
  --c-warning: #92400E;
  --c-warning-bg: #FFFBEB;
  --c-warning-border: #FDE68A;
  --c-info: #0F766E;           /* Teal 700 - Estados informativos */
  --c-info-bg: #F0FDFA;
  --c-info-border: #99F6E4;
  --ring: 0 0 0 3px rgba(4, 120, 87, 0.18);
  --shadow-card: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-raised: 0 1px 2px rgba(15, 23, 42, 0.04), 0 24px 48px -24px rgba(6, 78, 59, 0.22);
  --r-card: 16px;
  --sidebar-w: 260px;
  --page-gutter: clamp(16px, 3vw, 24px);
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  color: var(--c-text);
  background: var(--c-bg);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  line-height: 1.5;
}

h1, h2, h3, h4, h5, h6, p, ul, ol { margin: 0; }
h1, h2, h3, h4, h5, h6 { overflow-wrap: anywhere; }
button, input, select, textarea { font: inherit; }
button, a, input, select, textarea { -webkit-tap-highlight-color: transparent; }
button, input, select, textarea { min-width: 0; }
button { overflow-wrap: anywhere; }
button:disabled { cursor: not-allowed; }
img, svg { max-width: 100%; }

:focus-visible {
  outline: 3px solid var(--c-primary);
  outline-offset: 3px;
}

/* Espacio táctil compartido sin cambiar los radios del cuestionario. */
.btn, .btn-table, .role-btn, .auth-back-btn { min-height: 44px; }
.btn { justify-content: center; text-align: center; max-width: 100%; }
.btn--full { width: 100%; }

.dashboard-layout {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  background: var(--c-bg);
  color: var(--c-text);
}

.dashboard-layout > .main-content {
  flex: 1;
  min-width: 0;
  width: calc(100% - var(--sidebar-w));
  max-width: 1246px;
  margin-left: var(--sidebar-w);
  padding: 40px 48px;
}

@media (max-width: 900px) {
  .dashboard-layout { flex-direction: column; }
  .dashboard-layout > .main-content {
    width: 100%;
    margin-left: 0;
    padding: 24px var(--page-gutter);
  }
  input, select, textarea { font-size: 16px; }
}
`````

### `src/styles/public-info.css` (reemplazar completo, 160 líneas, hash `fdcd9915534bf01c9a3e10aa16118d4cf5881b06`)

`````css
.info-page {
  font-family: 'Inter', sans-serif;
  color: var(--c-text);
  background: var(--c-bg);
  min-height: 100dvh;
}
.info-page a { color: var(--c-primary); }
.info-page main:focus { outline: none; }
.info-visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
.info-skip { position: fixed; left: 16px; top: -100px; z-index: 200; padding: 12px 20px; background: white; border-radius: 12px; }
.info-skip:focus { top: 12px; }
.info-nav {
  position: sticky; top: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 48px; gap: 24px;
  background: rgba(255, 255, 255, .9); backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--c-border);
}
.info-page .info-brand {
  display: inline-flex; align-items: center; gap: 8px; min-height: 44px;
  font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.25rem;
  letter-spacing: -.01em; color: var(--c-text); text-decoration: none;
}
.info-brand__icon { color: var(--c-primary); font-size: 1.4rem; }
.info-nav__links { display: flex; align-items: center; gap: 32px; }
.info-nav__links a {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 44px; text-decoration: none; color: var(--c-muted);
  font-size: .875rem; font-weight: 500; text-align: center;
}
.info-nav__links a:hover, .info-nav__links a[aria-current="page"] { color: var(--c-primary); }
.info-nav__links a[aria-current="page"] { font-weight: 700; }
.info-nav__links .info-nav__cta {
  color: white; background: var(--c-primary); padding: 8px 20px;
  font-weight: 600; border-radius: 100px; transition: background-color .2s;
}
.info-nav__links .info-nav__cta:hover { color: white; background: var(--c-primary-strong); }
.info-page .info-wrap { max-width: 1180px; margin: 0 auto; padding-left: 48px; padding-right: 48px; }
.info-hero {
  position: relative; overflow: hidden;
  padding-top: 64px; padding-bottom: 72px;
  background: linear-gradient(180deg, #F1F8F4 0%, var(--c-bg) 100%);
  border-bottom: 1px solid var(--c-border);
}
/* Trama de puntos de la portada, desvanecida hacia la derecha */
.info-hero::before {
  content: ''; position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(rgba(4, 120, 87, .16) 1px, transparent 1.2px);
  background-size: 22px 22px;
  -webkit-mask-image: radial-gradient(ellipse 40% 70% at 88% 40%, #000 0%, transparent 75%);
  mask-image: radial-gradient(ellipse 40% 70% at 88% 40%, #000 0%, transparent 75%);
}
.info-hero > .info-wrap { position: relative; }
.info-page .info-back { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; margin-bottom: 24px; font-size: .85rem; text-decoration: none; font-weight: 600; }
.info-eyebrow { color: var(--c-primary); font-size: .75rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 14px; }
.info-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(2.1rem, 4.6vw, 3.8rem); line-height: 1.08; letter-spacing: -.035em; max-width: 850px; }
/* Subrayado tipo marcador, igual que en la portada */
.info-title em { font-style: normal; color: var(--c-primary); background: linear-gradient(transparent 64%, rgba(132, 204, 22, .38) 64%, rgba(132, 204, 22, .38) 92%, transparent 92%); -webkit-box-decoration-break: clone; box-decoration-break: clone; padding: 0 .04em; }
.info-lead { margin-top: 24px; font-size: 1.075rem; line-height: 1.75; color: #475569; max-width: 730px; }
.info-facts { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; }
.info-fact { padding: 10px 16px; border: 1px solid var(--c-border); border-radius: 12px; background: var(--c-surface); font-size: .85rem; color: var(--c-muted); }
.info-fact strong { color: var(--c-text); font-family: 'Poppins', sans-serif; }
.info-section { padding-top: 56px; padding-bottom: 56px; }
.info-section + .info-section { padding-top: 0; }
.info-section h2, .info-cta h2 { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.6rem, 3vw, 2.25rem); line-height: 1.15; letter-spacing: -.03em; }
.info-intro { max-width: 750px; color: var(--c-muted); margin-top: 16px; line-height: 1.8; }
.info-card { padding: 32px; border: 1px solid var(--c-border); border-radius: var(--r-card); background: white; min-width: 0; }
.info-card h3 { font-family: 'Poppins', sans-serif; font-size: 1.1rem; font-weight: 700; line-height: 1.5; margin-bottom: 12px; }
.info-card p, .info-copy { font-size: .95rem; color: var(--c-muted); line-height: 1.8; }
.info-step-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 28px; }
.info-step-number { display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; margin-bottom: 20px; border-radius: 50%; background: var(--c-surface); border: 1px solid var(--c-tint-border); color: var(--c-primary); font-family: 'Poppins', sans-serif; font-size: .85rem; font-weight: 700; }
.info-step-grid article:first-child .info-step-number { background: var(--c-primary); border-color: var(--c-primary); color: white; }
.info-note { border: 1px solid var(--c-tint-border); border-left: 4px solid var(--c-accent2); border-radius: var(--r-card); padding: 28px 32px; background: var(--c-tint); }
.info-note h3 { font-family: 'Poppins', sans-serif; font-size: 1rem; margin-bottom: 10px; }
.info-note p { font-size: .95rem; line-height: 1.8; color: var(--c-text-soft); }
.info-note a { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; margin-top: 12px; font-weight: 600; text-decoration: none; }
.info-faq { display: grid; gap: 12px; margin-top: 28px; }
.info-faq details { border: 1px solid var(--c-border); border-radius: 14px; background: white; padding: 0 24px; transition: border-color .2s; }
.info-faq details[open] { border-color: var(--c-tint-border); }
.info-faq summary { display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 64px; padding: 18px 0; font-weight: 600; cursor: pointer; list-style: none; }
.info-faq summary::-webkit-details-marker { display: none; }
.info-faq summary::after { content: '+'; flex: 0 0 28px; height: 28px; display: grid; place-items: center; border-radius: 50%; background: var(--c-tint); color: var(--c-primary); font-size: 1.1rem; font-weight: 600; }
.info-faq details[open] summary { color: var(--c-primary); }
.info-faq details[open] summary::after { content: '−'; }
.info-faq details p { padding-bottom: 22px; font-size: .95rem; color: var(--c-muted); line-height: 1.8; }
/* Bloque de cierre en verde profundo, como el registro de la portada */
.info-cta { position: relative; overflow: hidden; padding: 48px; border-radius: 24px; background: var(--c-deep); color: #ECFDF5; }
.info-cta::before { content: ''; position: absolute; width: 560px; height: 560px; right: -220px; bottom: -300px; border-radius: 50%; background: repeating-radial-gradient(circle, transparent 0 47px, rgba(167, 243, 208, .09) 47px 48px); pointer-events: none; }
.info-cta > * { position: relative; }
.info-cta h2 { color: white; }
.info-cta p { margin-top: 16px; max-width: 700px; color: #A7F3D0; line-height: 1.8; }
.info-cta > .info-eyebrow { color: #BEF264; margin-top: 0; }
.info-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px; }
.info-page .info-button {
  display: inline-flex; justify-content: center; align-items: center; gap: 8px;
  min-height: 48px; max-width: 100%; padding: 12px 24px; border-radius: 100px;
  color: white; background: var(--c-primary); font-weight: 600; font-size: .9rem;
  text-decoration: none; text-align: center; border: 1px solid transparent; transition: background-color .2s, border-color .2s, color .2s;
}
.info-page .info-button:hover { background: var(--c-primary-strong); }
.info-page .info-button--secondary { color: var(--c-text); background: white; border-color: var(--c-border); }
.info-page .info-button--secondary:hover { color: var(--c-primary); background: white; border-color: var(--c-primary); }
/* Sobre el bloque oscuro el botón principal pasa a blanco para destacar */
.info-page .info-cta .info-button { background: white; color: var(--c-deep); }
.info-page .info-cta .info-button:hover { background: var(--c-tint); }
.info-page .info-cta .info-button--secondary { background: transparent; color: white; border-color: rgba(167, 243, 208, .45); }
.info-page .info-cta .info-button--secondary:hover { color: white; background: rgba(255, 255, 255, .08); border-color: #A7F3D0; }
.info-dimension-nav { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 32px; }
.info-dimension-nav a { display: inline-flex; align-items: center; gap: 8px; min-height: 48px; padding: 10px 16px; border: 1px solid var(--c-border); border-radius: 100px; background: white; color: var(--c-text); text-decoration: none; font-size: .85rem; transition: border-color .2s; }
.info-dimension-nav a:hover { border-color: var(--dimension-color); }
.info-dimension-nav strong { color: var(--dimension-color); font-family: 'Poppins', sans-serif; font-size: 1rem; }
.info-traits { display: grid; gap: 24px; }
.info-trait { scroll-margin-top: 110px; border-top: 3px solid var(--dimension-color); }
.info-trait__header { display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }
.info-trait__letter { display: flex; align-items: center; justify-content: center; flex: 0 0 64px; height: 64px; border-radius: 16px; color: var(--dimension-color); background: var(--dimension-bg); font-family: 'Poppins', sans-serif; font-size: 2rem; font-weight: 800; }
.info-trait h2 { font-size: clamp(1.4rem, 2.8vw, 1.8rem); }
.info-trait__english { color: var(--c-muted); font-size: .8rem; margin-top: 3px; }
.info-trait__reading { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin: 24px 0; }
.info-trait__reading > div { padding: 20px; border-radius: 12px; background: var(--c-bg); border: 1px solid var(--c-border); }
.info-trait__reading h3 { font-family: 'Inter', sans-serif; font-size: .85rem; margin-bottom: 8px; }
.info-trait__example { border-left: 3px solid var(--dimension-color); padding-left: 16px; }
.info-trait__question { margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--c-border); font-weight: 500; color: var(--c-text) !important; }
.info-page .info-source { display: inline-flex; align-items: center; min-height: 44px; font-size: .8rem; margin-top: 12px; }
.info-reading-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; margin-top: 28px; }
.info-footer { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px; padding: 28px 48px; border-top: 1px solid var(--c-border); background: white; }
.info-footer p { color: var(--c-muted); font-size: .85rem; }
@media (max-width: 900px) {
  .info-nav { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; padding: 12px var(--page-gutter); background: white; backdrop-filter: none; }
  .info-nav__links { display: contents; }
  .info-nav__links a { font-size: .8rem; }
  .info-nav__links a:first-child { grid-row: 2; grid-column: 1; }
  .info-nav__links a:nth-child(2) { grid-row: 2; grid-column: 2; }
  .info-nav__links .info-nav__cta { grid-row: 1; grid-column: 2; padding: 8px 12px; }
  .info-page .info-wrap { padding-left: var(--page-gutter); padding-right: var(--page-gutter); }
  .info-hero { padding-top: 28px; padding-bottom: 40px; }
  .info-section { padding-top: 40px; padding-bottom: 40px; }
  .info-reading-grid { grid-template-columns: 1fr; }
  .info-trait { scroll-margin-top: 140px; }
  .info-footer { padding: 24px var(--page-gutter); flex-direction: column; text-align: center; gap: 12px; }
}
@media (max-width: 600px) {
  .info-step-grid, .info-trait__reading { grid-template-columns: 1fr; }
  .info-card, .info-note { padding: 24px 20px; }
  .info-cta { padding: 32px 20px; border-radius: 20px; }
  .info-faq details { padding-left: 20px; padding-right: 20px; }
  .info-trait__header { gap: 14px; }
  .info-trait__letter { flex-basis: 48px; height: 48px; font-size: 1.6rem; border-radius: 12px; }
  .info-actions { flex-direction: column; }
  .info-actions .info-button { width: 100%; }
  .info-dimension-nav { gap: 8px; }
  .info-dimension-nav a { padding: 10px 12px; }
  .info-lead { font-size: 1rem; }
}
@media (prefers-reduced-motion: reduce) {
  .info-faq details, .info-page .info-button, .info-nav__links .info-nav__cta, .info-dimension-nav a { transition: none; }
}
@media (max-width: 900px) and (max-height: 500px) {
  .info-nav { position: static; }
  .info-trait { scroll-margin-top: 24px; }
}
`````

### `src/views/AuthView.vue` (reemplazar completo, 675 líneas, hash `d5457f7487ac0d180d2da4e5f3d942afd849984f`)

`````vue
<template>
  <div class="auth-page">
    <aside class="auth-aside">
      <router-link to="/" class="auth-aside__brand" aria-label="Vócalis, volver al inicio">
        <span class="auth-logo-icon" aria-hidden="true">◈</span>
        <span>Vócalis</span>
      </router-link>
      <div class="auth-aside__body">
        <p class="auth-aside__eyebrow">Cuestionario BFI-44</p>
        <p class="auth-aside__title">Tu perfil, a tu ritmo.</p>
        <ul class="auth-aside__list">
          <li>44 afirmaciones, unos 8 minutos.</li>
          <li>Tus respuestas se guardan mientras avanzas.</li>
          <li>Tu orientador te acompaña en la lectura de resultados.</li>
        </ul>
      </div>
      <p class="auth-aside__foot">Proyecto de Título · Ingeniería en Informática · 2026</p>
    </aside>

    <div class="auth-panel">
    <router-link to="/" class="auth-back-btn">
      <span class="btn__arrow" aria-hidden="true">←</span> Volver al inicio
    </router-link>

    <main class="auth-container">
      <div class="auth-box">
        <div class="auth-logo">
          <span class="auth-logo-icon" aria-hidden="true">◈</span>
          <span class="auth-logo-text">Vócalis</span>
        </div>

        <div class="section__eyebrow">
          {{ isLogin ? 'Control de acceso' : 'Registro de nuevos usuarios' }}
        </div>
        <h1 class="auth-title">
          {{ isLogin ? 'Bienvenido de vuelta' : 'Crea tu cuenta' }}
        </h1>
        <p class="auth-sub">
          {{ isLogin ? 'Ingresa tus credenciales para acceder de forma segura.' : 'Únete a la plataforma para descubrir o guiar rutas vocacionales.' }}
        </p>

        <div v-if="errorMessage" class="auth-alert auth-alert--error" role="alert">
          <p class="auth-alert__text">{{ errorMessage }}</p>
        </div>

        <div v-if="successMessage" class="auth-alert auth-alert--success" role="status">
          <p class="auth-alert__text">{{ successMessage }}</p>
        </div>

        <form class="auth-form" :aria-busy="loading" @submit.prevent="handleSubmit">
          
          <fieldset v-if="!isLogin" class="role-fieldset" :disabled="loading">
            <legend>Tipo de cuenta</legend>
            <div class="role-selector">
            <button 
              type="button" 
              class="role-btn" 
              :class="{ 'role-btn--active': form.role === 'estudiante' }"
              :aria-pressed="form.role === 'estudiante'"
              @click="setRole('estudiante')"
            >
              Estudiante
            </button>
            <button 
              type="button" 
              class="role-btn" 
              :class="{ 'role-btn--active': form.role === 'orientador' }"
              :aria-pressed="form.role === 'orientador'"
              @click="setRole('orientador')"
            >
              Orientador Escolar
            </button>
            </div>
          </fieldset>

          <div v-if="!isLogin" class="input-group">
            <label for="nombre-completo">Nombre completo</label>
            <input
              id="nombre-completo"
              name="nombre_completo"
              autocomplete="name"
              v-model="form.name"
              class="register__input"
              type="text"
              placeholder="Nombre completo"
              :required="!isLogin"
            />
          </div>

          <div v-if="!isLogin && form.role === 'estudiante'" class="input-group">
            <label for="fecha-nacimiento">Fecha de nacimiento</label>
            <input id="fecha-nacimiento" v-model="form.fecha_nacimiento"
              class="register__input" name="fecha_nacimiento" autocomplete="bday" type="date" required />
          </div>

          <div v-if="!isLogin && form.role === 'estudiante'" class="form-row form-row--curso">
            <div class="input-group">
              <label for="nivel">Nivel</label>
              <select 
                id="nivel"
                name="nivel"
                v-model="form.nivel" 
                class="register__input register__select" 
                :required="!isLogin && form.role === 'estudiante'"
              >
                <option value="" disabled selected>Selecciona tu nivel</option>
                <option value="1° Medio">1° Medio</option>
                <option value="2° Medio">2° Medio</option>
                <option value="3° Medio">3° Medio</option>
                <option value="4° Medio">4° Medio</option>
              </select>
            </div>
            <div class="input-group input-group--letra">
              <label for="letra">Letra</label>
              <input 
                id="letra"
                name="letra"
                autocapitalize="characters"
                :spellcheck="false"
                v-model="form.letra" 
                class="register__input register__input--letra" 
                type="text" 
                placeholder="A" 
                maxlength="1"
                pattern="[A-La-l]"
                title="Debe ser una letra entre la A y la L"
                @input="form.letra = form.letra.toUpperCase().replace(/[^A-LA-L]/g, '')"
                :required="!isLogin && form.role === 'estudiante'" 
              />
            </div>
          </div>
          
          <div v-if="!isLogin" class="input-group">
            <label for="establecimiento">Establecimiento educacional</label>
            <input
              id="establecimiento"
              name="establecimiento"
              autocomplete="organization"
              v-model="form.establecimiento"
              class="register__input"
              type="text"
              placeholder="Establecimiento Educacional"
              maxlength="255"
              required
            />
          </div>

          <div v-if="!isLogin && form.role === 'orientador'" class="input-group">
            <label for="departamento">Departamento o unidad</label>
            <input
              id="departamento"
              name="departamento"
              v-model="form.departamento"
              class="register__input"
              type="text"
              placeholder="Departamento o Unidad (Ej: Convivencia Escolar)"
              :required="!isLogin && form.role === 'orientador'"
            />
          </div>

          <div v-if="!isLogin && form.role === 'orientador'" class="input-group">
            <label for="codigo-verificacion">Código privado de verificación</label>
            <input id="codigo-verificacion" name="codigo_verificacion" v-model="form.codigo_verificacion" class="register__input"
              type="password" autocomplete="off" placeholder="Código privado de verificación"
              aria-label="Código privado de verificación" required />
          </div>

          <div class="input-group">
            <label for="correo">Correo electrónico</label>
            <input
              id="correo"
              name="email"
              :autocomplete="isLogin ? 'username' : 'email'"
              inputmode="email"
              autocapitalize="none"
              :spellcheck="false"
              v-model="form.email"
              class="register__input"
              type="email"
              placeholder="tu@correo.cl"
              required
            />
          </div>
          
          <div class="input-group">
            <label for="contrasena">Contraseña</label>
            <input
              id="contrasena"
              name="password"
              :autocomplete="isLogin ? 'current-password' : 'new-password'"
              minlength="6"
              v-model="form.password"
              class="register__input"
              type="password"
              placeholder="Contraseña"
              required
            />
          </div>

          <button type="submit" class="btn btn--primary btn--full" :disabled="loading">
            {{ loading ? 'Procesando...' : (isLogin ? 'Iniciar Sesión' : 'Registrar mi cuenta gratis') }}
            <span v-if="!loading" class="btn__arrow" aria-hidden="true">→</span>
          </button>
        </form>

        <p class="auth-toggle-text">
          {{ isLogin ? '¿No tienes una cuenta académica?' : '¿Ya te encuentras registrado?' }}
          <button type="button" class="auth-toggle-btn" :disabled="loading" @click="toggleMode">
            {{ isLogin ? 'Regístrate aquí' : 'Inicia sesión aquí' }}
          </button>
        </p>
      </div>
    </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authService from '../services/authService'

const router = useRouter()
const route = useRoute()

// Estados reactivos de control
const isLogin = ref(true) // Parte por defecto en modo Login
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Formulario reactivo unificado
const form = ref({
  role: 'estudiante', // 'estudiante' o 'orientador'
  name: '',
  email: '',
  password: '',
  nivel: '',
  letra: '',
  establecimiento: '',
  departamento: '',
  fecha_nacimiento: '',
  codigo_verificacion: ''
})

// Si se llega desde la landing con datos precargados, abrir directo en modo registro
onMounted(() => {
  if (route.query.mode === 'register') {
    isLogin.value = false
  }
  if (route.query.name) form.value.name = String(route.query.name)
  if (route.query.email) form.value.email = String(route.query.email)
})

// Cambiar entre Login y Registro
function toggleMode() {
  isLogin.value = !isLogin.value
  errorMessage.value = ''
  successMessage.value = ''
  form.value.password = ''
  form.value.codigo_verificacion = ''
}

// Configurar rol seleccionado dinámicamente
function setRole(newRole) {
  form.value.role = newRole
  form.value.codigo_verificacion = ''
}

// Procesar el envío del formulario
async function handleSubmit() {
  if (loading.value) return
  errorMessage.value = ''
  successMessage.value = ''

  // Validación básica del lado del cliente antes de enviar
  if (!form.value.email.includes('@')) {
    errorMessage.value = 'Por favor, ingresa un correo electrónico institucional válido.'
    return
  }

  if (form.value.password.length < 6) {
    errorMessage.value = 'La contraseña debe contener al menos 6 caracteres por seguridad.'
    return
  }

  loading.value = true

  try {
    if (isLogin.value) {
      const { role } = await authService.login(form.value)
      router.push(role === 'orientador' ? '/orientador/dashboard' : '/estudiante/dashboard')
    } else {
      await authService.register(form.value)
      successMessage.value = 'Cuenta registrada con éxito. Ingresa tus credenciales para iniciar sesión.'
      isLogin.value = true
    }
  } catch (err) {
    errorMessage.value = err.message || 'Ocurrió un problema al procesar la solicitud. Intenta nuevamente.'
  } finally {
    form.value.codigo_verificacion = ''
    loading.value = false
  }
}
</script>


<style scoped>
/* Acceso: panel verde profundo + formulario, con los tokens globales de base.css */
.auth-page {
  min-height: 100vh;
  min-height: 100dvh;
  display: grid;
  grid-template-columns: minmax(360px, 0.8fr) minmax(0, 1fr);
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
}

/* ── Panel lateral ───────────────────────────────────────────────────────── */
.auth-aside {
  position: sticky;
  top: 0;
  height: 100vh;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 32px;
  padding: 40px 48px;
  background: var(--c-deep);
  color: #ECFDF5;
  overflow: hidden;
}

/* Anillos concéntricos que evocan el radar, muy tenues */
.auth-aside::before {
  content: '';
  position: absolute;
  width: 760px; height: 760px;
  left: -300px; bottom: -380px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 59px, rgba(167, 243, 208, 0.08) 59px 60px);
  pointer-events: none;
}

.auth-aside > * { position: relative; }

.auth-aside__brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
  align-self: flex-start;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  color: #FFFFFF;
  text-decoration: none;
}

.auth-aside__brand .auth-logo-icon { color: var(--c-accent2); }

.auth-aside__eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #BEF264;
  margin-bottom: 14px;
}

.auth-aside__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 3.2vw, 2.75rem);
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #FFFFFF;
  max-width: 340px;
}

.auth-aside__list {
  list-style: none;
  padding: 0;
  margin-top: 32px;
  display: grid;
  gap: 14px;
  max-width: 340px;
}

.auth-aside__list li {
  display: flex;
  align-items: baseline;
  gap: 12px;
  font-size: 0.95rem;
  line-height: 1.5;
  color: #D1FAE5;
}

.auth-aside__list li::before {
  content: '';
  flex: 0 0 8px;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-accent2);
  transform: translateY(-1px);
}

.auth-aside__foot {
  font-size: 0.8rem;
  color: #6EE7B7;
}

/* ── Columna del formulario ─────────────────────────────────────────────── */
.auth-panel {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 32px 48px 48px;
}

.auth-back-btn {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: color 0.2s;
}
.auth-back-btn:hover { color: var(--c-primary); }

.auth-container {
  width: 100%;
  max-width: 460px;
  margin: auto;
  min-width: 0;
}

.auth-box {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 44px 40px;
  box-shadow: var(--shadow-raised);
}

.auth-logo {
  display: none;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  color: var(--c-text);
  margin-bottom: 24px;
}
.auth-logo-icon { color: var(--c-primary); }

.section__eyebrow {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 10px;
}

.auth-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.9rem;
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 8px;
  color: var(--c-text);
}

.auth-sub {
  font-size: 0.92rem;
  line-height: 1.55;
  color: var(--c-muted);
  margin-bottom: 28px;
}

/* ── Formulario ──────────────────────────────────────────────────────────── */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.role-fieldset { border: 0; padding: 0; margin: 0; min-width: 0; }
.role-fieldset legend { margin-bottom: 8px; }

/* Selector segmentado */
.role-selector {
  display: flex;
  gap: 4px;
  padding: 4px;
  border-radius: 14px;
  background: #F1F5F9;
  border: 1px solid var(--c-border);
}

.role-btn {
  flex: 1;
  min-width: 0;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--c-muted);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
  font-family: 'Inter', sans-serif;
}
.role-btn:hover { color: var(--c-text); }
.role-btn--active {
  background: var(--c-surface);
  color: var(--c-primary);
  border-color: var(--c-border);
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}

.input-group { width: 100%; min-width: 0; display: flex; flex-direction: column; gap: 8px; }
.input-group label, .role-fieldset legend { font-size: 0.85rem; font-weight: 600; color: var(--c-text); }

.form-row { display: flex; gap: 12px; }
.form-row--curso .input-group:first-child { flex: 1; }
.form-row--curso .input-group--letra { flex: 0 0 72px; }

.register__input--letra {
  text-align: center;
  padding-left: 0;
  padding-right: 0;
}

.register__select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%2364748B%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 10px auto;
  cursor: pointer;
}

.register__input {
  background-color: var(--c-surface);
  border: 1px solid var(--c-border-strong);
  border-radius: 12px;
  padding: 13px 16px;
  box-sizing: border-box;
  font-size: 0.95rem;
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  width: 100%;
  min-height: 48px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}
.register__input::placeholder { color: #94A3B8; }
.register__input:focus {
  border-color: var(--c-primary);
  box-shadow: var(--ring);
}

/* ── Botón ───────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  margin-top: 4px;
  padding: 13px 26px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  border: none;
}
.btn--primary { background: var(--c-primary); color: #fff; }
.btn--primary:hover:not(:disabled) { background: var(--c-primary-strong); }
.btn--primary:disabled {
  background: var(--c-border);
  color: var(--c-muted);
  cursor: not-allowed;
}
.btn--full { width: 100%; justify-content: center; }
.btn__arrow { transition: transform 0.2s; }
.btn:hover .btn__arrow { transform: translateX(3px); }

/* ── Alertas ─────────────────────────────────────────────────────────────── */
.auth-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 20px;
  border: 1px solid;
  border-left-width: 4px;
}
.auth-alert--error { background: var(--c-danger-bg); border-color: var(--c-danger-border); border-left-color: var(--c-danger); }
.auth-alert--success { background: var(--c-tint); border-color: var(--c-tint-border); border-left-color: var(--c-primary); }
.auth-alert__text {
  font-size: 0.85rem;
  color: #991B1B;
  font-weight: 500;
  line-height: 1.45;
}
.auth-alert--success .auth-alert__text { color: var(--c-primary-strong); }

.auth-toggle-text {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  font-size: 0.875rem;
  color: var(--c-muted);
  text-align: center;
}
.auth-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  border: 0;
  padding: 8px 6px;
  background: transparent;
  color: var(--c-primary);
  font-weight: 600;
  cursor: pointer;
}
.auth-toggle-btn:hover { text-decoration: underline; text-underline-offset: 4px; }

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1080px) {
  .auth-aside { padding: 36px 32px; }
  .auth-panel { padding: 28px 32px 40px; }
}

@media (max-width: 900px) {
  .auth-page { display: flex; flex-direction: column; gap: 0; }
  .auth-aside { display: none; }
  .auth-panel { padding: 24px var(--page-gutter) 40px; background: linear-gradient(180deg, #F1F8F4 0%, var(--c-bg) 320px); flex: 1; }
  .auth-logo { display: flex; }
  .register__input { font-size: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  .auth-back-btn, .role-btn, .register__input, .btn, .btn__arrow { transition: none; }
}

@media (max-width: 600px) {
  .auth-panel { padding-top: 16px; padding-bottom: max(24px, env(safe-area-inset-bottom)); gap: 16px; }
  .auth-container { margin: 0 auto; }
  .auth-box { padding: 28px 20px; border-radius: 20px; }
  .auth-title { font-size: clamp(1.5rem, 6.5vw, 1.9rem); }
  .auth-logo { margin-bottom: 16px; }
  .auth-sub { margin-bottom: 24px; }
  .register__input { padding: 13px 12px; }
  .register__select { padding-right: 32px; }
  .form-row { gap: 10px; }
  .btn--full { padding: 13px 16px; }
}
</style>
`````

### `src/views/EvaluacionView.vue` (reemplazar completo, 645 líneas, hash `67d798ae4f82e7504b7865ca42f7dc95e38227db`)

`````vue
<template>
  <div class="test-layout">
    <main class="main-content">
      
      <div class="top-navigation">
        <router-link to="/estudiante/dashboard" class="back-btn">
          <span class="btn__arrow" aria-hidden="true">←</span> Volver a mi panel
        </router-link>
        <div class="brand">
          <span class="brand-icon" aria-hidden="true">◈</span>
          <span class="brand-text">Vócalis</span>
        </div>
      </div>
      
      <header class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Estado BPM registrado</span>
          <span class="bpm-status-text">Estado actual: <strong>{{ getBpmStatus(bpmState).label }}</strong></span>
        </div>
        
        <div class="bpm-steps">
          <div v-for="(step, index) in bpmStages" :key="step.state" class="bpm-step"
               :class="{ 'bpm-step--completed': index < bpmStageIndex, 'bpm-step--active': index === bpmStageIndex }">
            <div class="bpm-step__node">{{ index < bpmStageIndex ? '✓' : index + 1 }}</div>
            <span class="bpm-step__label">{{ step.label }}</span>
            <div v-if="index < bpmStages.length - 1" class="bpm-step__line"></div>
          </div>
        </div>
      </header>

      <section class="test-header-zone">
        <div class="test-title-container">
          <h1 class="test-title">Inventario Big Five (BFI-44)</h1>
          <div class="test-instructions-box">
            <p>
              Vas a responder 44 afirmaciones sobre cómo eres normalmente. No hay respuestas correctas o incorrectas. Responde con tu primera impresión — no lo pienses demasiado, ni te compares con lo que crees que "deberías" ser. <strong>Podrás enviar el cuestionario completo una sola vez</strong>; tus respuestas parciales se guardan para que puedas continuar después. Los resultados describen dimensiones de personalidad y no determinan una carrera.
            </p>
          </div>
        </div>
        
        <div class="progress-stats-box">
          <div class="progress-text">
            Bloque <strong>{{ currentPage + 1 }}</strong> de <strong>{{ totalPages }}</strong> 
            <span class="progress-count">({{ answeredCount }} de 44 respondidas)</span>
          </div>
          <div class="progress-bar-bg" role="progressbar" aria-label="Afirmaciones respondidas"
               :aria-valuenow="answeredCount" :aria-valuemax="questions.length || 44" :aria-valuemin="0">
            <div class="progress-bar-fill" :style="{ width: percentProgress + '%' }"></div>
          </div>
        </div>
      </section>

      <section class="test-card-container">
        <p v-if="loadingQuestions" class="loading-text">Cargando cuestionario…</p>
        <div v-else-if="loadError" role="alert">
          <p>{{ loadError }}</p>
          <button class="btn btn--primary" @click="loadQuestionnaire">Reintentar carga</button>
        </div>
        <div v-else-if="isCompleted" role="status">
          <p>Esta evaluación ya está completada y no se puede editar.</p>
          <router-link to="/estudiante/reporte" class="btn btn--primary">Ver reporte</router-link>
        </div>
        <template v-else>
        <div ref="questionnaireStatus" class="questionnaire-status">
          <div class="block-heading">
            <h2 id="questionnaire-block" tabindex="-1">Bloque {{ currentPage + 1 }} de {{ totalPages }}</h2>
            <span>{{ answeredCount }} de {{ questions.length }} respondidas</span>
          </div>
          <div class="save-status" :class="{ 'save-status--pending': hasUnsavedAnswers && !savingCount }">
            <p role="status" aria-live="polite" aria-atomic="true">{{ saveStatusText }}</p>
            <button v-if="hasUnsavedAnswers && !savingCount" type="button" class="btn btn--ghost" @click="retrySaving">Reintentar guardado</button>
          </div>
        </div>
        <div class="likert-table-wrapper">
          <table class="likert-table">
            <caption>Para cada afirmación: «Me considero una persona que…»</caption>
            <thead>
              <tr>
                <th class="col-question" scope="col">Afirmación</th>
                <th v-for="option in likertOptions" :key="option.value" class="col-option" scope="col">{{ option.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in paginatedQuestions" :id="'question-' + q.id" :key="q.id" class="likert-row"
                  :class="{ 'likert-row--invalid': invalidQuestionId === q.id }">
                <th class="question-text" scope="row">
                  <span :id="'question-text-' + q.id"><span class="question-number">{{ questionNumber(q.id) }}.</span> {{ q.text }}</span>
                  <span v-if="invalidQuestionId === q.id" :id="'question-error-' + q.id" class="question-error">Responde esta afirmación para continuar.</span>
                </th>
                <td v-for="option in likertOptions" :key="option.value" class="option-cell">
                  <label class="radio-container"
                         :class="{ 'radio-container--selected': answers[q.id] === option.value, 'radio-container--disabled': submitting }">
                    <input 
                      :id="'question-radio-' + q.id + '-' + option.value"
                      type="radio" 
                      :name="'q-' + q.id" 
                      :value="option.value"
                      :checked="answers[q.id] === option.value"
                      :aria-labelledby="'question-text-' + q.id + ' option-text-' + q.id + '-' + option.value"
                      :aria-invalid="invalidQuestionId === q.id"
                      :aria-describedby="invalidQuestionId === q.id ? 'question-error-' + q.id : null"
                      :disabled="submitting"
                      @change="selectAnswer(q.id, option.value)"
                    />
                    <span class="custom-radio" aria-hidden="true">
                      <span class="custom-radio__inner">{{ option.value }}</span>
                    </span>
                    <span :id="'option-text-' + q.id + '-' + option.value" class="option-label">{{ option.label }}</span>
                  </label>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="test-navigation-footer">
          <p v-if="validationMessage" class="validation-warning" role="alert">
            {{ validationMessage }}
          </p>
          <button 
            type="button"
            @click="prevPage" 
            class="btn btn--ghost" 
            :disabled="currentPage === 0 || submitting"
          >
            ← Bloque Anterior
          </button>
          
          <button 
            type="button"
            @click="nextPage" 
            class="btn btn--primary"
            :disabled="submitting"
          >
            {{ isLastPage ? (submitting ? 'Calculando perfil…' : 'Finalizar y Calcular Perfil') : 'Siguiente Bloque →' }}
          </button>
        </footer>
        </template>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import evaluacionService from '../services/evaluacionService'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()

const questions = ref([])
const loadingQuestions = ref(true)
const loadError = ref('')
const bpmState = ref(null)
const isCompleted = ref(false)
const bpmStageIndex = computed(() => bpmStages.findIndex(step => step.state === bpmState.value))

function applyEstado(estado) {
  bpmState.value = estado.bpm_estado ?? null
  isCompleted.value = ['completada', 'procesada'].includes(estado.estado)
}

async function refreshEstado() {
  try {
    applyEstado(await evaluacionService.getEstado())
  } catch {
    bpmState.value = null
  }
}

async function loadQuestionnaire() {
  loadingQuestions.value = true
  loadError.value = ''
  try {
    const [items, saved, estado] = await Promise.all([
      evaluacionService.getQuestions(),
      evaluacionService.getAnswers(),
      evaluacionService.getEstado()
    ])
    questions.value = items
    answers.value = Object.fromEntries(saved.map(answer => [answer.preguntaId, answer.valor]))
    savedAnswers.value = { ...answers.value }
    applyEstado(estado)
    const firstUnanswered = items.findIndex(q => !answers.value[q.id])
    currentPage.value = firstUnanswered < 0 ? Math.max(0, totalPages.value - 1) : Math.floor(firstUnanswered / itemsPerPage)
  } catch {
    bpmState.value = null
    loadError.value = 'No se pudo recuperar el cuestionario y su progreso. Reintenta antes de responder.'
  } finally {
    loadingQuestions.value = false
  }
}

onMounted(() => {
  window.addEventListener('beforeunload', warnUnsaved)
  loadQuestionnaire()
})
onUnmounted(() => window.removeEventListener('beforeunload', warnUnsaved))

// Paginación
const currentPage = ref(0)
const itemsPerPage = 10
const validationMessage = ref('')
const invalidQuestionId = ref(null)
const questionnaireStatus = ref(null)
const submitting = ref(false)
const likertOptions = [
  { value: 1, label: 'Totalmente en desacuerdo' },
  { value: 2, label: 'En desacuerdo' },
  { value: 3, label: 'Neutro' },
  { value: 4, label: 'De acuerdo' },
  { value: 5, label: 'Totalmente de acuerdo' },
]

// Estado de respuestas: clave es ID de pregunta, valor es puntaje Likert (1 a 5)
const answers = ref({})
const savedAnswers = ref({})
const savingCount = ref(0)
let saveQueue = Promise.resolve()
const hasUnsavedAnswers = computed(() => Object.entries(answers.value)
  .some(([id, value]) => savedAnswers.value[id] !== value))
const saveStatusText = computed(() => {
  if (savingCount.value) return 'Guardando respuestas…'
  if (hasUnsavedAnswers.value) return 'Hay respuestas sin guardar. Mantén esta página abierta y reintenta el guardado.'
  if (!answeredCount.value) return 'Tus respuestas se guardarán a medida que respondas.'
  return 'Todas las respuestas seleccionadas están guardadas.'
})

function warnUnsaved(event) {
  if (savingCount.value || hasUnsavedAnswers.value) {
    event.preventDefault()
    event.returnValue = ''
  }
}

onBeforeRouteLeave(async () => {
  if (submitting.value) return false
  while (savingCount.value) await saveQueue
  return !hasUnsavedAnswers.value || window.confirm('Hay respuestas sin guardar. Si sales, perderás esos cambios. ¿Salir de todos modos?')
})

const totalPages = computed(() => Math.ceil(questions.value.length / itemsPerPage))
const isLastPage = computed(() => currentPage.value === totalPages.value - 1)

// Segmentar las 10 preguntas correspondientes al bloque actual
const paginatedQuestions = computed(() => {
  const start = currentPage.value * itemsPerPage
  return questions.value.slice(start, start + itemsPerPage)
})

// Contadores de progreso analítico
const answeredCount = computed(() => Object.keys(answers.value).length)
const percentProgress = computed(() =>
  questions.value.length ? Math.round((answeredCount.value / questions.value.length) * 100) : 0
)

function queueSave(qId, val) {
  savingCount.value++
  // Guardado individual en orden: evita crear dos evaluaciones o sobrescribir
  // una selección reciente con una petición anterior que termine más tarde.
  saveQueue = saveQueue.then(async () => {
    try {
      if (isCompleted.value) return
      await evaluacionService.saveAnswer(qId, val)
      savedAnswers.value[qId] = val
      if (bpmState.value === null) await refreshEstado()
    } catch (error) {
      // La selección local permanece pendiente hasta un reintento exitoso.
      delete savedAnswers.value[qId]
      if (error.response?.status === 400) await refreshEstado()
    } finally {
      savingCount.value--
    }
  })
}

function selectAnswer(qId, val) {
  if (loadingQuestions.value || loadError.value || isCompleted.value || submitting.value) return
  if (answers.value[qId] === val) return
  answers.value[qId] = val
  validationMessage.value = ''
  invalidQuestionId.value = null
  queueSave(qId, val)
}

function retrySaving() {
  if (isCompleted.value || submitting.value || savingCount.value) return
  for (const [id, value] of Object.entries(answers.value)) {
    if (savedAnswers.value[id] !== value) queueSave(Number(id), value)
  }
}

function questionNumber(qId) {
  return questions.value.findIndex(q => q.id === qId) + 1
}

function scrollBehavior() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
}

function scrollToQuestion(qId) {
  const question = document.getElementById(`question-${qId}`)
  if (!question) return
  const status = questionnaireStatus.value
  const stickyHeight = status && window.getComputedStyle(status).position === 'sticky'
    ? status.getBoundingClientRect().height : 0
  window.scrollTo({ top: Math.max(0, window.scrollY + question.getBoundingClientRect().top - stickyHeight - 16), behavior: scrollBehavior() })
}

async function focusBlock() {
  await nextTick()
  const heading = document.getElementById('questionnaire-block')
  heading?.focus({ preventScroll: true })
  const firstQuestion = paginatedQuestions.value[0]
  scrollToQuestion(firstQuestion?.id)
}

async function showUnanswered(qId) {
  currentPage.value = Math.floor((questionNumber(qId) - 1) / itemsPerPage)
  invalidQuestionId.value = qId
  validationMessage.value = `Responde la afirmación ${questionNumber(qId)} antes de continuar.`
  await nextTick()
  document.getElementById(`question-radio-${qId}-1`)?.focus({ preventScroll: true })
  scrollToQuestion(qId)
}

async function prevPage() {
  if (currentPage.value > 0 && !submitting.value) {
    currentPage.value--
    validationMessage.value = ''
    invalidQuestionId.value = null
    await focusBlock()
  }
}

async function nextPage() {
  if (loadingQuestions.value || loadError.value || isCompleted.value || submitting.value) return
  // Validar si todas las preguntas del bloque actual fueron respondidas
  const unansweredQuestions = paginatedQuestions.value.filter(q => !answers.value[q.id])

  if (unansweredQuestions.length > 0) {
    await showUnanswered(unansweredQuestions[0].id)
    return
  }

  if (!isLastPage.value) {
    currentPage.value++
    validationMessage.value = ''
    invalidQuestionId.value = null
    await focusBlock()
    return
  }

  const firstUnanswered = questions.value.find(q => !answers.value[q.id])
  if (firstUnanswered) {
    await showUnanswered(firstUnanswered.id)
    return
  }

  submitting.value = true
  try {
    await saveQueue
    if (isCompleted.value) return
    if (hasUnsavedAnswers.value) {
      validationMessage.value = 'Reintenta el guardado de las respuestas pendientes antes de finalizar.'
      return
    }
    await evaluacionService.submitEvaluation(answers.value)
    isCompleted.value = true
    submitting.value = false
    await router.push('/estudiante/reporte')
  } catch {
    validationMessage.value = 'No se pudo finalizar la evaluación. Tus respuestas se conservan; puedes reintentar.'
    await refreshEstado()
  } finally {
    submitting.value = false
  }
}

</script>

<style scoped>
/* ── Infraestructura y Rejilla General ──────────────────────────────────── */
/* Usa los tokens globales de base.css */
.test-layout {
  min-height: 100vh;
  min-height: 100dvh;
  background: linear-gradient(180deg, #F1F8F4 0%, var(--c-bg) 360px);
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  display: flex;
  justify-content: center;
}

/* ── Navegación Superior Simplificada ───────────────────────────────────── */
.top-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}
.back-btn {
  min-height: 44px;
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
}
.back-btn:hover { color: var(--c-primary); }
.brand { display: flex; align-items: center; gap: 8px; font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.2rem; }
.brand-icon { color: var(--c-primary); }

/* ── Margen de contenido principal centrado ─────────────────────────────── */
.main-content {
  flex: 1;
  padding: 32px 24px;
  max-width: 1000px;
  width: 100%;
  min-width: 0;
}

/* ── Barra de Progreso Superior (BPM) ───────────────────────────────────── */
.bpm-progress-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 24px 28px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-card);
}
.bpm-header { display: flex; flex-wrap: wrap; gap: 8px 16px; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.bpm-badge { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; color: var(--c-primary); text-transform: uppercase; }
.bpm-status-text { font-size: 0.85rem; color: var(--c-muted); }
.bpm-status-text strong { color: var(--c-text); }
.bpm-steps { display: flex; justify-content: space-between; align-items: center; position: relative; }
.bpm-step { display: flex; flex-direction: column; align-items: center; position: relative; flex: 1; }
.bpm-step__node {
  width: 34px; height: 34px; border-radius: 50%; background: #FFFFFF; border: 1px solid var(--c-border-strong);
  display: flex; align-items: center; justify-content: center; font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.8rem; color: var(--c-muted); z-index: 2;
}
.bpm-step__label { margin-top: 8px; font-size: 0.8rem; font-weight: 600; color: var(--c-muted); text-align: center; }
.bpm-step__line { position: absolute; top: 17px; left: calc(50% + 22px); width: calc(100% - 44px); height: 1px; background: repeating-linear-gradient(90deg, var(--c-border-strong) 0 6px, transparent 6px 12px); z-index: 1; }

.bpm-step--completed .bpm-step__node { background: var(--c-tint); border-color: var(--c-tint-border); color: var(--c-primary); }
.bpm-step--completed .bpm-step__line { background: var(--c-tint-border); }
.bpm-step--active .bpm-step__node { background: var(--c-primary); border-color: var(--c-primary); color: #FFFFFF; box-shadow: 0 0 0 5px var(--c-tint); }
.bpm-step--active .bpm-step__label { color: var(--c-primary); font-weight: 700; }

/* ── Zona del Encabezado del Test e Indicador de Progreso ────────────────── */
.test-header-zone {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 24px;
  gap: 24px;
}
.test-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.6rem, 3vw, 2.1rem); line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 16px; text-align: left;}
.test-instructions-box {
  display: flex;
  gap: 16px;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-left: 4px solid var(--c-accent2);
  padding: 16px 20px;
  border-radius: 0 12px 12px 0;
  font-size: 0.92rem;
  color: var(--c-text-soft);
  line-height: 1.6;
  max-width: 600px;
  text-align: left;
}
.test-instructions-box p { margin: 0; }
.test-instructions-box strong { color: var(--c-text); }
.instructions-icon { font-size: 1.4rem; }

.progress-stats-box {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  padding: 16px 20px;
  border-radius: 14px;
  width: 340px;
  text-align: left;
  box-shadow: var(--shadow-card);
}
.progress-text { display: flex; flex-wrap: wrap; gap: 4px; font-size: 0.82rem; color: var(--c-text); margin-bottom: 8px; font-weight: 500; }
.progress-count { color: var(--c-muted); margin-left: auto; font-size: 0.8rem; }
.progress-bar-bg { width: 100%; height: 8px; background: #F1F5F9; border-radius: 100px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 100px; background: var(--c-primary); transition: width 0.4s ease; }

/* ── Matriz Likert (Tabla Estilizada) ────────────────────────────────────── */
.test-card-container {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 32px;
  box-shadow: var(--shadow-raised);
}
.likert-table-wrapper { overflow-x: auto; }
.questionnaire-status { background: var(--c-surface); padding-bottom: 20px; }
.block-heading { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 4px 16px; margin-bottom: 8px; }
.block-heading h2 { font-family: 'Poppins', sans-serif; font-size: 1.05rem; font-weight: 700; }
.block-heading > span { font-size: 0.8rem; color: var(--c-muted); }
.save-status { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; font-size: 0.85rem; color: var(--c-muted); }
.save-status--pending { color: var(--c-warning); }
.save-status .btn { font-size: 0.85rem; padding: 10px 16px; }
.likert-table caption { text-align: left; font-size: 0.9rem; color: var(--c-muted); padding-bottom: 16px; }
.likert-row { scroll-margin-top: 24px; }
.question-error { display: block; margin-top: 8px; font-size: 0.85rem; font-weight: 600; color: var(--c-danger); }
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.likert-table { width: 100%; border-collapse: collapse; text-align: left; }

.likert-table thead th {
  padding: 16px;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-muted);
  border-bottom: 1px solid var(--c-border);
  background: var(--c-bg);
}
.col-question { width: 45%; }
.col-option { width: 11%; text-align: center; }

.likert-row { border-bottom: 1px solid var(--c-border); transition: background 0.15s; }
.likert-row:hover { background: var(--c-bg); }

.question-text { padding: 20px 16px; font-size: 0.95rem; font-weight: 500; line-height: 1.5; color: var(--c-text); }
.question-number { color: var(--c-primary); font-family: 'Poppins', sans-serif; font-weight: 700; margin-right: 6px; }

.option-cell { text-align: center; padding: 8px 4px; }

/* Custom Radio Buttons redondos e interactivos */
.radio-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  min-width: 44px;
  min-height: 48px;
}
.radio-container input { position: absolute; width: 1px; height: 1px; margin: 0; opacity: 0; }
.radio-container:focus-within { outline: 3px solid var(--c-primary); outline-offset: 3px; border-radius: 8px; }
.radio-container--disabled { cursor: not-allowed; opacity: 0.6; }
.option-label { position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }

.custom-radio {
  width: 34px; height: 34px;
  border: 1px solid var(--c-border-strong);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
  background: #FFFFFF;
}
.custom-radio__inner { font-size: 0.85rem; font-weight: 700; color: #64748B; }

/* Estados dinámicos de selección de la escala Likert */
.radio-container input:checked ~ .custom-radio {
  border-color: var(--c-primary);
  background: var(--c-primary);
  box-shadow: 0 0 0 4px var(--c-tint);
}
.radio-container input:checked ~ .custom-radio .custom-radio__inner { color: #FFFFFF; }
.likert-row:hover .custom-radio { border-color: var(--c-tint-border); }
.radio-container:hover .custom-radio { border-color: var(--c-primary); }

/* ── Footer de Navegación ───────────────────────────────────────────────── */
.test-navigation-footer {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  margin-top: 32px;
  border-top: 1px solid var(--c-border);
  padding-top: 24px;
}
.test-navigation-footer .btn--ghost { justify-self: start; }
.test-navigation-footer .btn--primary { justify-self: end; }
.validation-warning { grid-column: 1 / -1; font-size: 0.85rem; color: var(--c-danger); font-weight: 600; background: var(--c-danger-bg); padding: 10px 16px; border-radius: 10px; border: 1px solid var(--c-danger-border); border-left: 4px solid var(--c-danger); }

/* Botones estructurados del Home */
.btn { display: inline-flex; align-items: center; gap: 8px; min-height: 48px; padding: 13px 26px; border-radius: 100px; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.92rem; text-decoration: none; cursor: pointer; transition: background-color 0.2s, border-color 0.2s, color 0.2s; border: 1px solid transparent; }
.btn--primary { background: var(--c-primary); color: #fff; }
.btn--primary:hover:not(:disabled) { background: var(--c-primary-strong); }
.btn--primary:disabled { background: var(--c-border); color: #475569; }
.btn--ghost { background: #FFFFFF; color: var(--c-text); border-color: var(--c-border); }
.btn--ghost:hover:not(:disabled) { border-color: var(--c-primary); color: var(--c-primary); }
.btn--ghost:disabled { color: #94A3B8; border-color: var(--c-border); cursor: not-allowed; }

@media (max-width: 900px) {
  .main-content { padding: 20px var(--page-gutter); }
  .test-card-container, .test-header-zone { min-width: 0; }
  .likert-table-wrapper { max-width: 100%; }
  .test-header-zone { flex-direction: column; align-items: flex-start; }
  .progress-stats-box { width: 100%; box-sizing: border-box; }
  .likert-table thead th:not(.col-question) { padding: 12px 4px; }
}

/* Una sola tabla y los mismos radios: las filas pasan a tarjetas al faltar espacio. */
@media (max-width: 700px) {
  .test-title { font-size: clamp(1.4rem, 5vw, 1.8rem); }
  .bpm-progress-card { padding: 16px; margin-bottom: 24px; }
  .bpm-step__label { font-size: 0.7rem; overflow-wrap: anywhere; }
  .test-instructions-box { padding: 16px; gap: 10px; }
  .test-card-container { padding: 16px; border-radius: 16px; }
  .questionnaire-status { position: sticky; top: 0; z-index: 5; padding: 12px 0; margin-bottom: 16px; border-bottom: 1px solid var(--c-border); }
  .save-status { gap: 8px; }
  .save-status .btn { width: 100%; }
  .likert-table-wrapper { overflow: visible; }
  .likert-table, .likert-table caption { display: block; width: 100%; }
  .likert-table thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
  .likert-table tbody { display: grid; gap: 20px; }
  .likert-row { display: grid; grid-template-columns: minmax(0, 1fr); gap: 8px; border: 1px solid var(--c-border); border-radius: 14px; padding: 16px; background: var(--c-bg); scroll-margin-top: 150px; }
  .likert-row:hover { background: var(--c-bg); }
  .likert-row--invalid { border-color: var(--c-danger); background: var(--c-danger-bg); }
  .question-text { width: auto; padding: 0 0 8px; font-size: 1rem; overflow-wrap: anywhere; }
  .option-cell { padding: 0; }
  .radio-container { display: flex; width: 100%; justify-content: flex-start; gap: 12px; min-height: 52px; padding: 10px 12px; border: 1px solid var(--c-border); border-radius: 12px; background: var(--c-surface); text-align: left; }
  .radio-container--selected { border-color: var(--c-primary); background: var(--c-tint); }
  .option-label { position: static; width: auto; height: auto; overflow: visible; clip-path: none; white-space: normal; font-size: 0.9rem; font-weight: 500; }
  .custom-radio { width: 30px; height: 30px; flex-shrink: 0; }
  .test-navigation-footer { grid-template-columns: minmax(0, 1fr); }
  .test-navigation-footer .btn { width: 100%; justify-self: stretch; border-radius: 12px; }
}

@media (max-height: 500px) and (max-width: 700px) {
  .questionnaire-status { position: static; }
  .likert-row { scroll-margin-top: 16px; }
}

@media (prefers-reduced-motion: reduce) {
  .progress-bar-fill, .custom-radio, .btn { transition: none; }
}
</style>
`````

### `src/views/OrientadorDashboardView.vue` (reemplazar completo, 432 líneas, hash `804bdd0a362d11feec23dc63b51ec1538b0d4915`)

`````vue
<template>
  <div class="dashboard-layout">
    
    <DashboardNavigation
      :items="[{ label: 'Panel de alumnos', to: '/orientador/dashboard', active: true }]"
      :user-name="userName"
      user-role="Orientador(a) escolar"
      label="Navegación del orientador"
      @logout="logout"
    />

    <main class="main-content">
      <section class="panel-header-zone">
        <div class="panel-title-container">
          <span class="panel-eyebrow">Unidad de Convivencia y Orientación Escolar</span>
          <h1 class="panel-title">Panel de Gestión y Monitoreo</h1>
          <p class="panel-sub">Consulta de los estados registrados de los procesos psicométricos y flujos BPM.</p>
        </div>
      </section>

      <section class="metrics-grid">
        <div class="metric-card metric-card--total">
          <div class="metric-card__data">
            <span class="metric-num">{{ totalAlumnos }}</span>
            <span class="metric-label">Alumnos Asignados</span>
          </div>
        </div>
        <div class="metric-card metric-card--progress">
          <div class="metric-card__data">
            <span class="metric-num">{{ flujosEnCurso }}</span>
            <span class="metric-label">Flujos en procesamiento</span>
          </div>
        </div>
        <div class="metric-card metric-card--ready">
          <div class="metric-card__data">
            <span class="metric-num metric-num--success">{{ reportesListos }}</span>
            <span class="metric-label">Reportes Listos</span>
          </div>
        </div>
      </section>

      <section class="course-assignment" aria-labelledby="course-assignment-title">
        <div class="course-assignment__header">
          <h2 id="course-assignment-title">Cursos sin orientador asignado</h2>
          <button type="button" class="btn-table btn-table--primary" :disabled="loadingCourses || assigningCourseId !== null" @click="loadCourses">Actualizar cursos</button>
        </div>
        <p>Si compartes colegio con otros orientadores, coordina qué cursos atenderá cada uno. Al tomar un curso a cargo, sus estudiantes actuales y los que se registren después aparecerán en tu panel. Se conservan los cursos que ya tienen responsable.</p>
        <p v-if="courseMessage" role="status">{{ courseMessage }}</p>
        <p v-if="assignmentError" role="alert">{{ assignmentError }}</p>
        <p v-if="loadingCourses" role="status">Consultando cursos de tu establecimiento…</p>
        <p v-else-if="coursesError" role="alert">{{ coursesError }} Usa «Actualizar cursos» para reintentar.</p>
        <p v-else-if="unassignedCourses.length === 0">No hay cursos sin asignar en tu establecimiento.</p>
        <ul v-else class="unassigned-courses">
          <li v-for="course in unassignedCourses" :key="course.id">
            <span><strong>{{ course.nombre }}</strong> · {{ course.total_estudiantes }} estudiantes</span>
            <button type="button" class="btn-table btn-table--primary" :disabled="assigningCourseId !== null" :aria-label="`Tomar a cargo ${course.nombre}`" @click="assignCourse(course)">
              {{ assigningCourseId === course.id ? 'Asignando…' : 'Tomar a cargo' }}
            </button>
          </li>
        </ul>
      </section>

      <section class="filters-card">
        <div class="filters-grid">
          <div class="filter-group">
            <label for="student-search">Buscar estudiante</label>
            <input 
              id="student-search"
              v-model="filters.search" 
              type="search"
              placeholder="Ej: José Miguel Piña..." 
              class="filter-input"
            />
          </div>
          <div class="filter-group">
            <label for="student-course">Curso</label>
            <select id="student-course" v-model="filters.course" class="filter-select">
              <option value="">Todos los cursos</option>
              <option v-for="course in availableCourses" :key="course" :value="course">{{ course }}</option>
            </select>
          </div>
          <div class="filter-group">
            <label for="student-status">Estado del Flujo Camunda</label>
            <select id="student-status" v-model="filters.status" class="filter-select">
              <option value="">Todos los estados</option>
              <option v-for="step in bpmStages" :key="step.state" :value="step.state">{{ step.label }}</option>
              <option value="unavailable">Estado no disponible</option>
            </select>
          </div>
        </div>
      </section>

      <section class="table-section">
        <p v-if="loadingStudents" class="loading-text" role="status">Cargando estudiantes…</p>
        <div v-else-if="studentsError" class="loading-text" role="alert">
          <p>{{ studentsError }}</p>
          <button class="btn-table btn-table--primary" @click="loadStudents">Reintentar</button>
        </div>
        <p v-else-if="studentsPool.length === 0" class="loading-text">Todavía no tienes estudiantes asignados.</p>
        <template v-else>
        <div class="table-container">
          <table class="students-table">
            <caption class="table-caption">Estudiantes asignados y estado de su proceso</caption>
            <thead>
              <tr>
                <th scope="col">Estudiante</th>
                <th scope="col">Curso</th>
                <th scope="col">Inicio de evaluación</th>
                <th scope="col">Estado Flujo BPM</th>
                <th scope="col" style="text-align: center;">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id" class="table-row">
                <td>
                  <div class="student-profile-cell">
                    <div class="student-initials" aria-hidden="true">{{ student.name.split(' ').map(n => n[0]).join('').substring(0,2) }}</div>
                    <div class="student-meta">
                      <strong class="student-name">{{ student.name }}</strong>
                      <span class="student-email">{{ student.email }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="cell-label" aria-hidden="true">Curso</span>
                  <span class="course-tag">{{ student.course }}</span>
                </td>
                <td>
                  <span class="cell-label" aria-hidden="true">Inicio de evaluación</span>
                  <span class="date-text">{{ student.lastUpdate }}</span>
                </td>
                <td>
                  <span class="cell-label" aria-hidden="true">Estado Flujo BPM</span>
                  <span class="bpm-tag" :class="'bpm-tag--' + getBpmStatus(student.bpm_estado).statusClass">
                    {{ getBpmStatus(student.bpm_estado).label }}
                  </span>
                  <span
                    v-if="student.estado_evaluacion === 'en_progreso' && !student.hasReport"
                    class="report-unavailable"
                  >Evaluación pendiente</span>
                </td>
                <td>
                  <div class="actions-cell-buttons">
                    <button 
                      @click="viewReport(student)" 
                      class="btn-table btn-table--primary"
                      :disabled="!student.hasReport"
                      :aria-label="`Ver reporte de ${student.name}`"
                    >
                      Ver Reporte
                    </button>
                  </div>
                  <span v-if="!student.hasReport" class="report-unavailable">Reporte no disponible</span>
                </td>
              </tr>
              <tr v-if="filteredStudents.length === 0">
                <td colspan="5" class="empty-table-msg">
                  No se encontraron estudiantes que coincidan con los criterios de búsqueda establecidos.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="table-pagination-footer">
          <span class="pagination-info" role="status" aria-live="polite" aria-atomic="true">Mostrando <strong>{{ filteredStudents.length }}</strong> de <strong>{{ studentsPool.length }}</strong> alumnos registrados</span>
        </footer>
        </template>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import orientadorService from '../services/orientadorService'
import authService from '../services/authService'
import DashboardNavigation from '../components/DashboardNavigation.vue'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()

const filters = ref({
  search: '',
  course: '',
  status: ''
})

const studentsPool = ref([])
const loadingStudents = ref(true)
const studentsError = ref('')
const userName = ref('Orientador')
const unassignedCourses = ref([])
const loadingCourses = ref(true)
const coursesError = ref('')
const assigningCourseId = ref(null)
const assignmentError = ref('')
const courseMessage = ref('')

async function loadCourses() {
  loadingCourses.value = true
  coursesError.value = ''
  try {
    unassignedCourses.value = await orientadorService.getUnassignedCourses()
  } catch {
    coursesError.value = 'No se pudieron consultar los cursos.'
  } finally {
    loadingCourses.value = false
  }
}

async function assignCourse(course) {
  if (assigningCourseId.value !== null) return
  assigningCourseId.value = course.id
  assignmentError.value = ''
  courseMessage.value = ''
  try {
    await orientadorService.assignCourse(course.id)
    courseMessage.value = `Ahora tienes a cargo el curso ${course.nombre}.`
    await Promise.all([loadCourses(), loadStudents()])
  } catch (error) {
    const messages = {
      401: 'Tu sesión no es válida. Vuelve a iniciar sesión.',
      403: 'No tienes permiso para asignar cursos.',
      404: 'El curso ya no está disponible en tu establecimiento.',
      409: 'Otro orientador ya tomó este curso a cargo. La lista se ha actualizado.',
    }
    assignmentError.value = messages[error.response?.status] || 'No se pudo confirmar la asignación. Actualiza los cursos e intenta nuevamente.'
    if ([404, 409].includes(error.response?.status)) await loadCourses()
  } finally {
    assigningCourseId.value = null
  }
}

// Métricas calculadas dinámicamente desde los datos reales
const totalAlumnos = computed(() => studentsPool.value.length)

const flujosEnCurso = computed(() => {
  return studentsPool.value.filter(s => 
    s.bpm_estado === 'calculando_ocean' || s.bpm_estado === 'generando_reporte'
  ).length
})

const reportesListos = computed(() => {
  return studentsPool.value.filter(s => s.hasReport).length
})

// Cursos disponibles extraídos dinámicamente de los estudiantes
const availableCourses = computed(() => {
  const courses = new Set(studentsPool.value.map(s => s.course))
  return [...courses].sort()
})

async function loadStudents() {
  loadingStudents.value = true
  studentsError.value = ''
  try {
    studentsPool.value = await orientadorService.getStudents()
  } catch {
    studentsError.value = 'No se pudieron cargar los estudiantes. Intenta nuevamente.'
  } finally {
    loadingStudents.value = false
  }
}

onMounted(() => {
  authService.getProfile().then(profile => {
    if (profile) userName.value = profile.name
  })
  loadStudents()
  loadCourses()
})

const filteredStudents = computed(() => {
  return studentsPool.value.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(filters.value.search.toLowerCase()) || 
                          student.email.toLowerCase().includes(filters.value.search.toLowerCase())
    const matchesCourse = filters.value.course === '' || student.course === filters.value.course
    const state = getBpmStatus(student.bpm_estado).state
    const matchesStatus = filters.value.status === '' ||
      (filters.value.status === 'unavailable' ? state === null : state === filters.value.status)
    
    return matchesSearch && matchesCourse && matchesStatus
  })
})

function viewReport(student) {
  if (student.hasReport) {
    router.push({ name: 'orientador-reporte', params: { studentId: student.id } })
  }
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
.course-assignment { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px 28px; margin-bottom: 24px; text-align: left; box-shadow: var(--shadow-card); }
.course-assignment__header { display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; align-items: center; }
.course-assignment h2 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.1rem; letter-spacing: -0.01em; }
.course-assignment p { color: var(--c-muted); font-size: 0.86rem; line-height: 1.6; margin-top: 12px; }
.course-assignment .btn-table { min-height: 44px; }
.unassigned-courses { list-style: none; padding: 0; margin-top: 16px; display: grid; gap: 12px; }
.unassigned-courses li { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; padding: 14px 16px; background: var(--c-bg); border: 1px solid var(--c-border); border-radius: 12px; font-size: 0.88rem; }
/* ── Encabezado ── */
.panel-header-zone { margin-bottom: 32px; text-align: left; }
.panel-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 10px; display: block; }
.panel-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.6rem, 3vw, 2.1rem); line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 6px; }
.panel-sub { font-size: 0.9rem; color: var(--c-muted); }

/* ── Tarjetas de Métricas ── */
.metrics-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin-bottom: 32px; }
.metric-card { position: relative; background: var(--c-surface); border: 1px solid var(--c-border); padding: 24px 24px 24px 28px; border-radius: var(--r-card); display: flex; align-items: center; box-shadow: var(--shadow-card); overflow: hidden; }
/* Franja de color que distingue cada métrica */
.metric-card::before { content: ''; position: absolute; left: 0; top: 18px; bottom: 18px; width: 3px; border-radius: 0 3px 3px 0; background: var(--c-border-strong); }
.metric-card--progress::before { background: #F59E0B; }
.metric-card--ready::before { background: var(--c-primary); }
.metric-card__data { display: flex; flex-direction: column; text-align: left; }
.metric-num { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 2rem; letter-spacing: -0.02em; color: var(--c-text); line-height: 1.05; }
.metric-num--success { color: var(--c-primary); }
.metric-label { font-size: 0.82rem; font-weight: 500; color: var(--c-muted); margin-top: 6px; }

/* ── Filtros ── */
.filters-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 24px 28px; margin-bottom: 24px; box-shadow: var(--shadow-card); }
.filters-grid { display: grid; grid-template-columns: minmax(0, 2fr) repeat(2, minmax(0, 1fr)); gap: 20px; }
.filter-group { display: flex; flex-direction: column; min-width: 0; text-align: left; gap: 6px; }
.filter-group label { font-size: 0.82rem; font-weight: 600; color: var(--c-text); }
.filter-input, .filter-select { width: 100%; min-height: 48px; background: var(--c-surface); border: 1px solid var(--c-border-strong); border-radius: 12px; padding: 12px 14px; font-size: 0.9rem; color: var(--c-text); outline: none; font-family: 'Inter', sans-serif; transition: border-color 0.2s, box-shadow 0.2s; }
.filter-input::placeholder { color: #94A3B8; }
.filter-input:focus, .filter-select:focus { border-color: var(--c-primary); box-shadow: var(--ring); }

/* ── Tabla (Bug Solucionado agregando padding exacto a las celdas td) ── */
.table-section { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); overflow: hidden; box-shadow: var(--shadow-card); }
.table-container { overflow-x: auto; }
.loading-text { padding: 40px 20px; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.loading-text .btn-table { margin-top: 16px; }
.table-caption { position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
.cell-label { display: none; }
.report-unavailable { display: block; margin-top: 6px; color: var(--c-muted); font-size: 0.78rem; }
.students-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left; }

.students-table th { 
  background: var(--c-bg); 
  padding: 14px 20px; 
  font-weight: 700; 
  color: var(--c-muted); 
  border-bottom: 1px solid var(--c-border); 
  font-size: 0.72rem; 
  text-transform: uppercase; 
  letter-spacing: 0.08em; 
}

/* El arreglo crítico de espacio se aplica aquí */
.students-table td { 
  padding: 16px 20px; 
  vertical-align: middle;
}

.table-row { border-bottom: 1px solid var(--c-border); transition: background 0.15s; }
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: var(--c-bg); }

/* Celda interna de perfil de estudiante */
.student-profile-cell { display: flex; align-items: center; gap: 14px; }
.student-initials { width: 38px; height: 38px; background: var(--c-tint); border: 1px solid var(--c-tint-border); color: var(--c-primary); font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.78rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.student-meta { display: flex; flex-direction: column; min-width: 0; text-align: left; overflow-wrap: anywhere; }
.student-name { font-size: 0.92rem; color: var(--c-text); }
.student-email { font-size: 0.78rem; color: var(--c-muted); }

.course-tag { display: inline-block; background: var(--c-bg); border: 1px solid var(--c-border); color: var(--c-text-soft); padding: 4px 10px; border-radius: 8px; font-weight: 600; font-size: 0.8rem; }
.date-text { color: var(--c-muted); font-size: 0.85rem; }

/* Estados del flujo */
/* Estado con punto de color: legible sin depender solo del fondo */
.bpm-tag { font-size: 0.78rem; font-weight: 600; padding: 5px 12px 5px 10px; border-radius: 100px; display: inline-flex; align-items: center; gap: 8px; overflow-wrap: anywhere; border: 1px solid; }
.bpm-tag::before { content: ''; flex: 0 0 7px; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.bpm-tag--success { background: var(--c-tint); color: var(--c-primary-strong); border-color: var(--c-tint-border); }
.bpm-tag--warning { background: var(--c-warning-bg); color: var(--c-warning); border-color: var(--c-warning-border); }
.bpm-tag--info { background: var(--c-info-bg); color: var(--c-info); border-color: var(--c-info-border); }
.bpm-tag--danger { background: var(--c-danger-bg); color: var(--c-danger); border-color: var(--c-danger-border); }

/* Botones de acción */
.actions-cell-buttons { display: flex; gap: 8px; }
.btn-table { padding: 8px 16px; border-radius: 100px; font-weight: 600; font-size: 0.82rem; cursor: pointer; border: 1px solid transparent; transition: background-color 0.2s; font-family: 'Inter', sans-serif; }
.btn-table--primary { background: var(--c-primary); color: #FFFFFF; }
.btn-table--primary:hover:not(:disabled) { background: var(--c-primary-strong); }
.btn-table--primary:disabled { background: #F1F5F9; border-color: var(--c-border); color: #94A3B8; cursor: not-allowed; }

/* Paginación de pie de tabla */
.table-pagination-footer { padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; background: var(--c-bg); border-top: 1px solid var(--c-border); }
.pagination-info { font-size: 0.82rem; color: var(--c-muted); }

.empty-table-msg { text-align: center; color: var(--c-muted); font-style: italic; padding: 40px !important; }

@media (max-width: 1200px) {
  .filters-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .filter-group:first-child { grid-column: 1 / -1; }
}
@media (max-width: 1100px) {
  .table-container { overflow: visible; padding: 16px; }
  .students-table { display: block; }
  .students-table thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
  .students-table tbody { display: grid; gap: 16px; }
  .students-table tr { display: block; min-width: 0; }
  .table-row, .table-row:last-child { padding: 16px; border: 1px solid var(--c-border); border-radius: 14px; }
  .students-table td { display: block; padding: 0; }
  .students-table td + td { margin-top: 12px; }
  .cell-label { display: block; margin-bottom: 4px; font-size: 0.75rem; font-weight: 700; color: var(--c-muted); }
  .actions-cell-buttons .btn-table { width: 100%; min-height: 48px; }
  .empty-table-msg { padding: 16px !important; }
}
@media (max-width: 900px) {
  .filter-input, .filter-select { font-size: 16px; }
}
@media (max-width: 600px) {
  .panel-title { font-size: 1.5rem; }
  .metrics-grid, .filters-grid { grid-template-columns: 1fr; gap: 12px; }
  .metric-card { padding: 16px 20px; }
  .metric-card__data { width: 100%; flex-direction: row; align-items: center; gap: 16px; }
  .metric-num { min-width: 2ch; }
  .metric-label { margin-top: 0; }
  .filters-card { padding: 20px; }
  .table-container, .table-pagination-footer { padding: 12px; }
  .table-pagination-footer { text-align: left; }
}
@media (prefers-reduced-motion: reduce) {
  .table-row, .btn-table, .filter-input, .filter-select { transition: none; }
}
</style>
`````

### `src/views/ReporteView.vue` (reemplazar completo, 573 líneas, hash `c5a0d8a993e1947f5f85fe9f39751a2a6fb74db4`)

`````vue
<template>
  <div class="dashboard-layout">
    
    <DashboardNavigation
      :items="navigationItems"
      :user-name="displayedStudentName"
      :user-role="isOrientador ? 'Estudiante evaluado' : 'Mi reporte'"
      label="Navegación del reporte"
      @logout="logout"
    />

    <main class="main-content">
      <p v-if="isOrientador" class="report-student">Consulta del reporte de {{ displayedStudentName }}</p>
      
      <header v-if="!errorMessage" class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Resultados BFI-44</span>
          <span class="bpm-status-text" role="status">{{ loading ? 'Consultando estado del proceso…' : 'Estado del proceso: ' + getBpmStatus(bpmState).label }}</span>
        </div>
      </header>

      <section class="report-header-zone">
        <div class="report-title-container">
          <span class="report-eyebrow">Resultados del cuestionario</span>
          <h1 class="report-title">{{ isOrientador ? 'Resultados BFI-44 del estudiante' : 'Tus resultados BFI-44' }}</h1>
          <p class="report-sub">Reporte generado el {{ evaluatedAt }}.</p>
        </div>
      </section>

      <p v-if="loading" class="loading-text" role="status">Cargando tu reporte…</p>
      <p v-else-if="errorMessage" role="alert">{{ errorMessage }}</p>

      <template v-else>
      <section class="profile-zone" aria-labelledby="profile-title">
        <header class="zone-head">
          <p class="zone-eyebrow">Tu perfil en cinco dimensiones</p>
          <h2 id="profile-title" class="zone-title">Cómo te describiste en el cuestionario</h2>
          <p class="zone-sub">Cada dimensión es un continuo entre dos extremos. El marcador indica hacia dónde se ubicaron tus respuestas; ningún punto de la escala es mejor que otro.</p>
        </header>

        <div class="report-grid">
          <aside class="report-visual-card">
            <h3 class="card-inner-title">Mapeo de Perfil de Personalidad</h3>
            <p class="card-inner-sub">Gráfico de los puntajes por dimensión incluidos en el reporte.</p>

            <div class="radar-container-box">
              <div v-for="dim in radarDimensions" :key="dim.letter"
                   class="radar__label-box" :class="'radar__label-box--' + dim.position">
                {{ dim.label }} <strong>{{ dim.score == null ? '—' : dim.score + '%' }}</strong>
              </div>

              <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg"
                   role="img" aria-labelledby="radar-title radar-description">
                <title id="radar-title">Puntajes de las cinco dimensiones BFI-44</title>
                <desc id="radar-description">Cada eje corresponde a una dimensión identificada con su nombre y porcentaje.</desc>
                <polygon v-for="(points, index) in radarGridPoints" :key="index" class="radar__grid" :points="points" />
                <line v-for="(point, index) in radarAxes" :key="index" class="radar__axis"
                      :x1="CENTER" :y1="CENTER" :x2="point.x" :y2="point.y" />
                <polygon v-if="hasRadarScores" class="radar__data" :points="radarPoints" />
                <circle v-for="(pt, i) in radarDots" :key="i" :cx="pt.x" :cy="pt.y" r="4.5" class="radar__dot" />
                <text v-for="axis in radarLabelPoints" :key="axis.letter" :x="axis.x" :y="axis.y"
                      class="radar__axis-letter" text-anchor="middle" dominant-baseline="middle" aria-hidden="true">{{ axis.letter }}</text>
              </svg>
            </div>
            <dl class="radar-legend" aria-label="Puntajes por dimensión">
              <div v-for="dim in radarDimensions" :key="dim.letter" class="radar-legend__item">
                <dt><span class="radar-legend__letter">{{ dim.letter }}</span> {{ dim.label }}</dt>
                <dd>{{ dim.score == null ? 'Sin puntaje' : dim.score + '%' }}</dd>
              </div>
            </dl>

            <div class="dominant-profile-badge">
              <div class="badge-info">
                <span class="badge-label">Dimensión con mayor puntaje:</span>
                <span class="badge-value">{{ dominantTraitLabel }}</span>
              </div>
            </div>

            <div class="reading-guide">
              <h4>Cómo leer tus porcentajes</h4>
              <ul>
                <li>Indican tu posición en la escala del cuestionario, no una nota.</li>
                <li>Un 70 % no significa que superes al 70 % de las personas.</li>
                <li>Mira las cinco dimensiones juntas: ninguna te resume por sí sola.</li>
              </ul>
            </div>
          </aside>

          <div class="report-text-card">
            <h3 class="card-inner-title">Interpretación de Dimensiones</h3>
            <p class="card-inner-sub">Selecciona una dimensión para abrir o cerrar su descripción.</p>

            <ol class="accordion-container">
              <li
                v-for="(dim, index) in dimensionsData"
                :key="dim.letter"
                class="accordion-item"
                :class="{ 'accordion-item--expanded': expandedIndexes.includes(index) }"
                :style="{ '--trait': dim.color }"
              >
                <button :id="`dimension-toggle-${dim.letter}`" type="button" class="accordion-header"
                        :aria-expanded="expandedIndexes.includes(index)"
                        :aria-controls="`dimension-content-${dim.letter}`" @click="toggleAccordion(index)">
                  <span class="accordion-header__left">
                    <span class="accordion-letter" aria-hidden="true">{{ dim.letter }}</span>
                    <span class="accordion-name">{{ dim.name }}</span>
                  </span>
                  <span class="accordion-header__right">
                    <span class="accordion-score-tag">Puntaje: {{ dim.score }}%</span>
                    <span class="accordion-arrow" aria-hidden="true"></span>
                  </span>
                </button>

                <div class="trait-scale" aria-hidden="true">
                  <span class="trait-scale__track">
                    <span class="trait-scale__fill" :style="{ width: (dim.pct ?? dim.score) + '%' }"></span>
                    <span class="trait-scale__marker" :style="{ left: (dim.pct ?? dim.score) + '%' }"></span>
                    <span class="trait-scale__ticks"><i></i><i></i><i></i></span>
                  </span>
                  <span v-if="dim.low" class="trait-scale__pole">{{ dim.low }}</span>
                  <span v-if="dim.high" class="trait-scale__pole trait-scale__pole--high">{{ dim.high }}</span>
                </div>

                <div v-show="expandedIndexes.includes(index)" :id="`dimension-content-${dim.letter}`"
                     class="accordion-content" role="region" :aria-labelledby="`dimension-toggle-${dim.letter}`">
                  <p class="accordion-text-desc">{{ dim.interpretation }}</p>
                  <div class="trait-impact-indicator">
                    <strong>Alcance del puntaje:</strong> {{ dim.vocationalImpact }}
                  </div>
                  <router-link v-if="dim.infoId" :to="`/el-test#${dim.infoId}`" class="trait-more">
                    Qué describe esta dimensión <span aria-hidden="true">→</span>
                  </router-link>
                </div>
              </li>
            </ol>
          </div>
        </div>
      </section>

      <section class="career-recommendations-zone" aria-labelledby="areas-title">
        <header class="zone-head">
          <p class="zone-eyebrow">Para seguir investigando</p>
          <h2 id="areas-title" class="section-title-secondary">Áreas profesionales para explorar</h2>
          <p class="section-sub-secondary">Referencias de las reglas actuales del prototipo; no acreditan afinidad ni aptitud profesional.</p>
        </header>

        <article v-for="(area, areaIndex) in careerAreas" :key="area.title" class="career-area-card">
          <header class="area-head" :class="{ 'area-head--image': area.info?.image }">
            <img v-if="area.info?.image" class="area-head__img" :src="area.info.image.src" alt="" loading="lazy" />
            <div class="area-head__body">
              <p class="area-head__index">Área {{ areaIndex + 1 }} de {{ careerAreas.length }}</p>
              <h3 class="career-card-title">{{ area.title }}</h3>
              <p class="career-card-desc">{{ area.desc }}</p>
            </div>
          </header>

          <div v-if="area.info" class="area-facts">
            <div class="area-fact">
              <h4>Qué se estudia</h4>
              <p>{{ area.info.queSeEstudia }}</p>
            </div>
            <div class="area-fact">
              <h4>Habilidades que se ponen en juego</h4>
              <ul class="area-chips">
                <li v-for="skill in area.info.habilidades" :key="skill">{{ skill }}</li>
              </ul>
            </div>
            <div class="area-fact">
              <h4>Dónde se trabaja</h4>
              <ul class="area-list">
                <li v-for="place in area.info.campoLaboral" :key="place">{{ place }}</li>
              </ul>
            </div>
          </div>

          <div class="career-list-box">
            <h5>Ejemplos de carreras:</h5>
            <ul class="career-grid">
              <li v-for="(carrera, i) in area.carreras" :key="carrera" class="career-item"
                  :class="{ 'career-item--rich': area.details?.[i] }">
                <figure v-if="area.details?.[i]?.image" class="career-item__media">
                  <img :src="area.details[i].image.src" :alt="area.details[i].image.alt" loading="lazy" />
                </figure>
                <div class="career-item__body">
                  <h6 class="career-item__name">{{ carrera.replace(/^[^:]+:\s*/, '') }}</h6>
                  <p v-if="area.details?.[i]?.descripcion" class="career-item__desc">{{ area.details[i].descripcion }}</p>
                  <a v-if="area.details?.[i]?.link" class="career-item__link" :href="area.details[i].link"
                     target="_blank" rel="noopener noreferrer">
                    Dónde se estudia <span class="visually-hidden">{{ carrera.replace(/^[^:]+:\s*/, '') }} (abre en otra pestaña)</span><span aria-hidden="true">↗</span>
                  </a>
                </div>
              </li>
            </ul>
          </div>

          <p v-if="area.credits?.length" class="area-credits">
            Imágenes de Wikimedia Commons:
            <template v-for="(credit, c) in area.credits" :key="credit.source">
              <a :href="credit.source" target="_blank" rel="noopener noreferrer">{{ credit.label }}</a>
              ({{ credit.author }}, <a v-if="credit.licenseUrl" :href="credit.licenseUrl" target="_blank" rel="noopener noreferrer">{{ credit.license }}</a><span v-else>{{ credit.license }}</span>){{ c < area.credits.length - 1 ? ' · ' : '.' }}
            </template>
          </p>
        </article>

        <div class="actionable-tips-card">
          <div class="tips-content">
            <h4>Resumen de resultados</h4>
            <p v-if="careerAreas.length">
              Áreas incluidas en este reporte: {{ careerAreas.map(area => area.title).join(', ') }}.
              Los puntajes y las interpretaciones por dimensión se presentan arriba.
            </p>
            <p v-else>Las reglas actuales no permiten sugerir un área para esta combinación. Los puntajes OCEAN siguen disponibles.</p>
            <p class="tips-note">Antes de decidir, conversa estas referencias con tu orientador y contrástalas con tus intereses, habilidades y experiencias.</p>
          </div>
        </div>
      </section>
      </template>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import reporteService from '../services/reporteService'
import orientadorService from '../services/orientadorService'
import authService from '../services/authService'
import DashboardNavigation from '../components/DashboardNavigation.vue'
import { getBpmStatus } from '../utils/bpmStatus'
import { enrichCareerArea } from '../data/areasEstudio'

const loading = ref(true)
const errorMessage = ref('')
const route = useRoute()
const isOrientador = computed(() => route.meta.role === 'orientador')
const navigationItems = computed(() => isOrientador.value
  ? [{ label: 'Panel de alumnos', to: '/orientador/dashboard', active: false }]
  : [
      { label: 'Panel principal', to: '/estudiante/dashboard', active: false },
      { label: 'Bitácora', to: '/estudiante/dashboard#history-section', active: false },
    ])
const studentName = ref('')
const displayedStudentName = computed(() => studentName.value || 'Nombre no disponible')

const evaluatedAt = ref('')
const dimensionsData = ref([])
const careerAreas = ref([])
const bpmState = ref(null)

watch([isOrientador, () => route.params.studentId], async ([orientador, studentId], _, onCleanup) => {
  let cancelled = false
  onCleanup(() => { cancelled = true })
  loading.value = true
  errorMessage.value = ''
  studentName.value = ''
  evaluatedAt.value = ''
  dimensionsData.value = []
  careerAreas.value = []
  bpmState.value = null
  try {
    if (orientador && (!/^\d+$/.test(studentId || '') || Number(studentId) < 1)) {
      errorMessage.value = 'Identificador de estudiante inválido.'
      return
    }
    const report = orientador
      ? await orientadorService.getStudentReport(studentId)
      : await reporteService.getLatestReport()
    if (cancelled) return
    studentName.value = typeof report.studentName === 'string' ? report.studentName.trim() : ''
    evaluatedAt.value = report.evaluatedAt
    dimensionsData.value = orderDimensions(report.dimensions)
    expandedIndexes.value = defaultExpanded(dimensionsData.value)
    careerAreas.value = (report.careerAreas || []).map(enrichCareerArea)
    bpmState.value = report.bpm_estado ?? null
  } catch (error) {
    if (cancelled) return
    const messages = {
      401: 'Tu sesión no es válida. Vuelve a iniciar sesión.',
      403: 'No tienes permiso para consultar el reporte de este estudiante.',
      404: 'No hay un reporte disponible.',
    }
    errorMessage.value = messages[error.response?.status] || 'No se pudo cargar el reporte. Intenta nuevamente.'
  } finally {
    if (!cancelled) loading.value = false
  }
}, { immediate: true })

// Lógica matemática nativa para construir el Gráfico de Radar SVG
const AXES = [
  { letter: 'O', label: 'Apertura', angle: -90, position: 'top' },
  { letter: 'C', label: 'Responsabilidad', angle: -18, position: 'tr' },
  { letter: 'E', label: 'Extraversión', angle: 54, position: 'br' },
  { letter: 'A', label: 'Amabilidad', angle: 126, position: 'bl' },
  { letter: 'N', label: 'Neuroticismo', angle: 198, position: 'tl' }
]
const CENTER = 160
const MAX_R = 120

function polarToXY(angleDeg, r) {
  const rad = (angleDeg * Math.PI) / 180
  return {
    x: CENTER + r * Math.cos(rad),
    y: CENTER + r * Math.sin(rad),
  }
}

// La identidad del eje depende de la letra, nunca del orden del JSON.
const radarDimensions = computed(() => AXES.map(axis => ({
  ...axis,
  score: dimensionsData.value.find(dim => dim.letter === axis.letter)?.score ?? null
})))
const hasRadarScores = computed(() => radarDimensions.value.every(dim => dim.score !== null))
const radarAxes = AXES.map(axis => polarToXY(axis.angle, MAX_R))
const radarLabelPoints = AXES.map(axis => ({ letter: axis.letter, ...polarToXY(axis.angle, MAX_R + 22) }))
const radarGridPoints = [1, 0.75, 0.5, 0.25].map(scale =>
  AXES.map(axis => {
    const point = polarToXY(axis.angle, MAX_R * scale)
    return `${point.x},${point.y}`
  }).join(' ')
)
const radarDots = computed(() => hasRadarScores.value
  ? radarDimensions.value.map(dim => polarToXY(dim.angle, dim.score / 100 * MAX_R))
  : []
)

const radarPoints = computed(() =>
  radarDots.value.map(p => `${p.x},${p.y}`).join(' ')
)

// El rasgo dominante se calcula a partir del puntaje más alto real,
// en vez de un texto fijo desconectado de los datos.
const dominantTraitLabel = computed(() => {
  if (!dimensionsData.value.length) return ''
  const top = dimensionsData.value.reduce((max, d) => (d.score > max.score ? d : max))
  return `${top.name} (${top.score}%)`
})

// Se abre por defecto la dimensión con mayor puntaje; el resto queda a un toque.
const expandedIndexes = ref([])

// Extremos de cada continuo y ancla en la página «El test».
const TRAIT_SCALE = {
  O: { low: 'Prefiere lo conocido', high: 'Busca lo nuevo', infoId: 'apertura' },
  C: { low: 'Flexible y espontáneo', high: 'Organizado y metódico', infoId: 'responsabilidad' },
  E: { low: 'Reservado', high: 'Sociable', infoId: 'extraversion' },
  A: { low: 'Directo y crítico', high: 'Cooperativo y empático', infoId: 'amabilidad' },
  N: { low: 'Emocionalmente estable', high: 'Más sensible al estrés', infoId: 'neuroticismo' },
}
const OCEAN_ORDER = ['O', 'C', 'E', 'A', 'N']

// Presenta las dimensiones siempre en orden OCEAN, sin depender del orden del JSON.
function orderDimensions(dimensions = []) {
  return [...dimensions]
    .sort((a, b) => OCEAN_ORDER.indexOf(a.letter) - OCEAN_ORDER.indexOf(b.letter))
    .map(dim => ({
      ...TRAIT_SCALE[dim.letter],
      ...dim,
      pct: Math.max(0, Math.min(100, Number(dim.score) || 0)),
    }))
}

function defaultExpanded(dimensions) {
  if (!dimensions.length) return []
  const top = dimensions.reduce((best, dim, i) => (dim.score > dimensions[best].score ? i : best), 0)
  return [top]
}

function toggleAccordion(index) {
  if (expandedIndexes.value.includes(index)) {
    expandedIndexes.value = expandedIndexes.value.filter(i => i !== index)
  } else {
    expandedIndexes.value.push(index)
  }
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
/* ── Estado del proceso ─────────────────────────────────────────────────── */
.bpm-progress-card { background: var(--c-surface); border: 1px solid var(--c-border); border-radius: var(--r-card); padding: 18px 24px; margin-bottom: 32px; box-shadow: var(--shadow-card); }
.bpm-header { display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; }
.bpm-badge { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--c-primary); }
.bpm-status-text { display: inline-flex; align-items: center; gap: 8px; font-size: 0.85rem; color: var(--c-text-soft); }
.bpm-status-text::before { content: ''; flex: 0 0 8px; width: 8px; height: 8px; border-radius: 50%; background: var(--c-primary); box-shadow: 0 0 0 4px var(--c-tint); }

/* ── Encabezado ─────────────────────────────────────────────────────────── */
.report-header-zone { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; gap: 24px; }
.report-title-container { text-align: left; min-width: 0; }
.report-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 10px; display: block; }
.report-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.7rem, 3.2vw, 2.4rem); line-height: 1.1; letter-spacing: -0.035em; margin-bottom: 8px; }
.report-sub { font-size: 0.9rem; color: var(--c-muted); }
.report-student {
  display: inline-flex; align-items: center; gap: 8px;
  margin-bottom: 16px; padding: 6px 14px;
  border: 1px solid var(--c-tint-border); border-radius: 100px;
  background: var(--c-tint); color: var(--c-primary-strong);
  font-size: 0.85rem; font-weight: 600; overflow-wrap: anywhere;
}
.loading-text { padding: 48px 0; text-align: center; color: var(--c-muted); font-size: 0.9rem; }
.visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }

/* Encabezado común de cada zona */
.zone-head { max-width: 720px; margin-bottom: 28px; text-align: left; }
.zone-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 10px; }
.zone-title, .section-title-secondary { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.4rem, 2.6vw, 1.85rem); line-height: 1.15; letter-spacing: -0.03em; margin-bottom: 10px; }
.zone-sub, .section-sub-secondary { font-size: 0.95rem; line-height: 1.65; color: var(--c-muted); }

/* ── Perfil: resumen fijo + escalas ─────────────────────────────────────── */
.report-grid { display: grid; grid-template-columns: minmax(300px, 0.8fr) minmax(0, 1.2fr); gap: 24px; align-items: start; }
.report-visual-card, .report-text-card { min-width: 0; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 24px; padding: 28px; text-align: left; overflow-wrap: anywhere; }
.report-visual-card { position: sticky; top: 24px; box-shadow: var(--shadow-raised); }
.report-text-card { padding: 28px 28px 12px; box-shadow: var(--shadow-card); }

.card-inner-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em; margin-bottom: 4px; }
.card-inner-sub { font-size: 0.85rem; color: var(--c-muted); margin-bottom: 8px; }

.radar-container-box { position: relative; display: flex; align-items: center; justify-content: center; height: 300px; margin: 8px 0 12px; }
.radar__svg { width: 220px; height: auto; overflow: visible; }
.radar__grid, .radar__axis { stroke: var(--c-border); stroke-width: 1; fill: none; }
.radar__grid:first-of-type { stroke: var(--c-border-strong); }
.radar__data { fill: rgba(4, 120, 87, 0.14); stroke: var(--c-primary); stroke-width: 2; stroke-linejoin: round; }
.radar__dot { fill: var(--c-surface); stroke: var(--c-primary); stroke-width: 2; }

.radar__label-box { position: absolute; display: flex; flex-direction: column; align-items: center; gap: 0; font-size: 0.7rem; font-weight: 500; line-height: 1.25; color: var(--c-muted); text-align: center; white-space: nowrap; }
.radar__label-box strong { font-family: 'Poppins', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--c-text); }
.radar__label-box--top { top: 0; left: 50%; transform: translateX(-50%); }
.radar__label-box--tr  { top: 30%; right: 0; }
.radar__label-box--br  { bottom: 4%; right: 10%; }
.radar__label-box--bl  { bottom: 4%; left: 10%; }
.radar__label-box--tl  { top: 30%; left: 0; }

.radar__axis-letter { display: none; font-family: 'Poppins', sans-serif; font-size: 16px; font-weight: 700; fill: var(--c-text); }
.radar-legend { display: none; gap: 8px; margin: 0; }
.radar-legend__item { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 8px 12px; background: var(--c-bg); border: 1px solid var(--c-border); border-radius: 10px; font-size: 0.85rem; }
.radar-legend dt { min-width: 0; display: flex; align-items: center; gap: 8px; }
.radar-legend dd { margin: 0; flex-shrink: 0; font-weight: 700; }
.radar-legend__letter { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 7px; background: var(--c-tint); color: var(--c-primary); font-family: 'Poppins', sans-serif; font-weight: 700; }

.dominant-profile-badge { display: flex; align-items: center; gap: 12px; background: var(--c-tint); border: 1px solid var(--c-tint-border); border-left: 4px solid var(--c-accent2); padding: 14px 16px; border-radius: 12px; margin-top: 8px; }
.badge-info { display: flex; flex-direction: column; gap: 2px; }
.badge-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; color: var(--c-primary); }
.badge-value { font-size: 0.95rem; font-weight: 700; color: var(--c-text); }

.reading-guide { margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--c-border); }
.reading-guide h4 { font-family: 'Poppins', sans-serif; font-size: 0.85rem; font-weight: 700; margin-bottom: 10px; }
.reading-guide ul { list-style: none; padding: 0; display: grid; gap: 8px; }
.reading-guide li { position: relative; padding-left: 16px; font-size: 0.82rem; line-height: 1.5; color: var(--c-text-soft); }
.reading-guide li::before { content: ''; position: absolute; left: 0; top: 0.55em; width: 6px; height: 6px; border-radius: 50%; background: var(--c-border-strong); }

/* Lista de dimensiones: cada una con su escala bipolar siempre visible */
.accordion-container { list-style: none; padding: 0; margin: 12px 0 0; display: flex; flex-direction: column; }
.accordion-item { --trait: var(--c-primary); border-top: 1px solid var(--c-border); padding: 4px 0 18px; }
.accordion-header { width: 100%; min-height: 56px; display: flex; flex-wrap: wrap; gap: 8px 12px; justify-content: space-between; align-items: center; padding: 12px 4px 8px; color: var(--c-text); text-align: left; border: none; border-radius: 10px; background: transparent; cursor: pointer; }
.accordion-header:hover .accordion-name { color: var(--c-primary); }
.accordion-header:focus-visible { outline-offset: 2px; }

.accordion-header__left { display: flex; min-width: 0; align-items: center; gap: 12px; }
.accordion-letter { display: inline-grid; place-items: center; width: 34px; height: 34px; flex-shrink: 0; border-radius: 10px; color: var(--trait); background: color-mix(in srgb, var(--trait) 10%, #FFFFFF); font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1rem; }
.accordion-name { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; letter-spacing: -0.01em; transition: color 0.15s; }
.accordion-header__right { display: flex; align-items: center; gap: 14px; }
.accordion-score-tag { font-size: 0.82rem; color: var(--c-text-soft); font-weight: 600; font-variant-numeric: tabular-nums; }
.accordion-arrow { width: 8px; height: 8px; border-right: 2px solid var(--c-muted); border-bottom: 2px solid var(--c-muted); transform: rotate(45deg) translateY(-2px); transition: transform 0.2s; margin-right: 6px; }
.accordion-item--expanded .accordion-arrow { transform: rotate(-135deg) translateY(-2px); border-color: var(--c-primary); }

.trait-scale { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-areas: "track track" "low high"; row-gap: 8px; column-gap: 12px; padding: 0 4px 0 50px; }
.trait-scale__track { grid-area: track; position: relative; height: 8px; border-radius: 8px; background: #F1F5F9; }
.trait-scale__fill { position: absolute; inset: 0 auto 0 0; border-radius: 8px; background: color-mix(in srgb, var(--trait) 28%, #FFFFFF); }
.trait-scale__marker { position: absolute; top: 50%; width: 16px; height: 16px; border-radius: 50%; transform: translate(-50%, -50%); background: var(--c-surface); border: 3px solid var(--trait); box-shadow: 0 1px 3px rgba(15, 23, 42, 0.18); z-index: 1; }
.trait-scale__ticks { position: absolute; inset: 0; display: flex; justify-content: space-evenly; pointer-events: none; }
.trait-scale__ticks i { width: 1px; height: 100%; background: rgba(255, 255, 255, 0.9); }
.trait-scale__pole { grid-area: low; font-size: 0.75rem; color: var(--c-muted); }
.trait-scale__pole--high { grid-area: high; text-align: right; }

.accordion-content { margin: 16px 4px 0 50px; padding: 16px 18px; background: var(--c-bg); border-radius: 12px; text-align: left; }
.accordion-text-desc { font-size: 0.92rem; line-height: 1.65; color: var(--c-text-soft); margin-bottom: 12px; }
.trait-impact-indicator { font-size: 0.84rem; line-height: 1.55; color: var(--c-text); background: #FFFFFF; border: 1px solid var(--c-border); border-left: 3px solid var(--c-accent1); padding: 10px 14px; border-radius: 10px; }
.trait-more { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; margin-top: 4px; font-size: 0.85rem; font-weight: 600; color: var(--c-primary); text-decoration: none; }
.trait-more:hover { text-decoration: underline; text-underline-offset: 4px; }

/* ── Áreas para explorar ────────────────────────────────────────────────── */
.career-recommendations-zone { text-align: left; margin-top: 56px; border-top: 1px solid var(--c-border); padding-top: 48px; }

.career-area-card { min-width: 0; overflow: hidden; overflow-wrap: anywhere; background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 24px; margin-bottom: 24px; box-shadow: var(--shadow-card); }

.area-head { position: relative; padding: 32px; background: var(--c-deep); color: #ECFDF5; }
.area-head--image { min-height: 240px; display: flex; align-items: flex-end; }
.area-head__img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
/* Velo para leer el texto sobre la fotografía */
.area-head--image::after { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(6, 78, 59, 0.15) 0%, rgba(6, 78, 59, 0.92) 78%); }
.area-head__body { position: relative; z-index: 1; max-width: 760px; }
.area-head__index { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #BEF264; margin-bottom: 8px; }
.career-card-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: clamp(1.25rem, 2.4vw, 1.6rem); line-height: 1.2; letter-spacing: -0.02em; color: #FFFFFF; margin-bottom: 10px; }
.career-card-desc { font-size: 0.92rem; line-height: 1.6; color: #D1FAE5; }

.area-facts { display: grid; grid-template-columns: 1.2fr 1fr 1fr; border-bottom: 1px solid var(--c-border); }
.area-fact { padding: 24px 28px; min-width: 0; }
.area-fact + .area-fact { border-left: 1px solid var(--c-border); }
.area-fact h4 { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--c-primary); margin-bottom: 12px; }
.area-fact p { font-size: 0.9rem; line-height: 1.6; color: var(--c-text-soft); }
.area-chips { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
.area-chips li { font-size: 0.8rem; font-weight: 500; color: var(--c-text-soft); background: var(--c-bg); border: 1px solid var(--c-border); padding: 4px 10px; border-radius: 100px; }
.area-list { list-style: none; padding: 0; display: grid; gap: 8px; }
.area-list li { position: relative; padding-left: 16px; font-size: 0.88rem; line-height: 1.45; color: var(--c-text-soft); }
.area-list li::before { content: ''; position: absolute; left: 0; top: 0.5em; width: 6px; height: 6px; border-radius: 50%; background: var(--c-primary); }

.career-list-box { padding: 24px 28px 28px; }
.career-list-box h5 { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; color: var(--c-muted); margin-bottom: 14px; }
.career-grid { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.career-item { min-width: 0; display: flex; flex-direction: column; border: 1px solid var(--c-border); border-radius: 16px; overflow: hidden; background: var(--c-surface); }
.career-item:not(.career-item--rich) { flex-direction: row; align-items: center; padding: 12px 16px; border-radius: 100px; background: var(--c-bg); }
.career-item__media { margin: 0; aspect-ratio: 4 / 3; background: #F1F5F9; overflow: hidden; }
.career-item__media img { width: 100%; height: 100%; object-fit: cover; display: block; }
.career-item__body { padding: 14px 16px 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; min-width: 0; }
.career-item:not(.career-item--rich) .career-item__body { padding: 0; }
.career-item__name { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.95rem; line-height: 1.3; color: var(--c-text); margin: 0; }
.career-item__desc { font-size: 0.84rem; line-height: 1.5; color: var(--c-muted); }
.career-item__link { margin-top: auto; display: inline-flex; align-items: center; gap: 6px; min-height: 44px; font-size: 0.82rem; font-weight: 600; color: var(--c-primary); text-decoration: none; }
.career-item__link:hover { text-decoration: underline; text-underline-offset: 4px; }

.area-credits { padding: 0 28px 20px; font-size: 0.7rem; line-height: 1.6; color: var(--c-muted); }
.area-credits a { color: inherit; }

.actionable-tips-card { display: flex; gap: 20px; background: var(--c-warning-bg); border: 1px solid var(--c-warning-border); border-left: 4px solid #F59E0B; border-radius: var(--r-card); padding: 24px 28px; align-items: flex-start; }
.tips-content h4 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1rem; color: var(--c-warning); margin-bottom: 6px; }
.tips-content p { font-size: 0.9rem; line-height: 1.6; color: #78350F; }
.tips-content .tips-note { margin-top: 8px; font-size: 0.85rem; }
.tips-content { min-width: 0; overflow-wrap: anywhere; }

@media (max-width: 1200px) {
  .report-grid { grid-template-columns: 1fr; }
  .report-visual-card { position: static; }
  .report-header-zone { flex-direction: column; align-items: flex-start; gap: 16px; }
  .area-facts { grid-template-columns: 1fr 1fr; }
  .area-fact:first-child { grid-column: 1 / -1; border-bottom: 1px solid var(--c-border); }
  .area-fact:nth-child(2) { border-left: none; }
}
@media (max-width: 600px) {
  .radar-container-box { height: auto; margin-bottom: 16px; }
  .radar__svg { width: 100%; max-width: 300px; }
  .radar__label-box { display: none; }
  .radar__axis-letter { display: block; }
  .radar-legend { display: grid; }
  .bpm-progress-card, .report-visual-card, .actionable-tips-card { padding: 20px; border-radius: var(--r-card); }
  .report-text-card { padding: 20px 16px 8px; border-radius: var(--r-card); }
  .accordion-header { padding: 12px 0 8px; }
  .accordion-header__left { gap: 10px; }
  .trait-scale { padding: 0; }
  .accordion-content { margin: 14px 0 0; padding: 14px; }
  .career-recommendations-zone { margin-top: 32px; padding-top: 32px; }
  .career-area-card { border-radius: 20px; }
  .area-head { padding: 24px 20px; }
  .area-head--image { min-height: 220px; }
  .area-facts { grid-template-columns: 1fr; }
  .area-fact { padding: 20px; }
  .area-fact + .area-fact { border-left: none; border-top: 1px solid var(--c-border); }
  .area-fact:first-child { border-bottom: none; }
  .career-list-box { padding: 20px; }
  .career-grid { grid-template-columns: 1fr; gap: 12px; }
  /* Fila compacta: miniatura a la izquierda para acortar la página */
  .career-item--rich { display: grid; grid-template-columns: 88px minmax(0, 1fr); align-items: start; }
  .career-item--rich .career-item__media { aspect-ratio: auto; height: 100%; min-height: 120px; }
  .career-item--rich .career-item__body { padding: 12px 14px; gap: 6px; }
  .career-item__desc { font-size: 0.82rem; }
  .area-credits { padding: 0 20px 16px; }
}
@media (prefers-reduced-motion: reduce) {
  .accordion-arrow, .accordion-name { transition: none; }
}
</style>
`````

### `src/views/StudentDashboardView.vue` (reemplazar completo, 634 líneas, hash `d24c5c8d4aa226a6ff68a9ae92395b001b5b0b91`)

`````vue
<template>
  <div class="dashboard-layout">
    
    <DashboardNavigation
      :items="navigationItems"
      :user-name="studentName || 'Estudiante'"
      user-role="Estudiante"
      label="Navegación del estudiante"
      @logout="logout"
    />

    <main class="main-content">
      <header class="bpm-progress-card">
        <div class="bpm-header">
          <span class="bpm-badge">Estado BPM registrado</span>
          <span class="bpm-status-text">Estado actual: <strong>{{ currentBpmStageText }}</strong></span>
        </div>
        
        <div class="bpm-steps">
          <div 
            v-for="(step, index) in bpmStages" 
            :key="index" 
            class="bpm-step"
            :class="{ 
              'bpm-step--completed': index < currentBpmStageIndex, 
              'bpm-step--active': index === currentBpmStageIndex 
            }"
            :aria-current="index === currentBpmStageIndex ? 'step' : undefined"
          >
            <div class="bpm-step__node">
              <span v-if="index < currentBpmStageIndex">✓</span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="bpm-step__label">{{ step.label }}</span>
            <div v-if="index < bpmStages.length - 1" class="bpm-step__line" aria-hidden="true"></div>
          </div>
        </div>
      </header>

      <section class="welcome-section">
        <h1 class="welcome-title">¡Hola de nuevo, {{ studentName || 'Estudiante' }}!</h1>
        <p class="welcome-sub">Estudiante · Plataforma Vócalis</p>
        <p v-if="orientadorName" class="welcome-orientador">Tu orientador/a: <strong>{{ orientadorName }}</strong></p>
      </section>

      <p v-if="!loading && loadError" class="action-card__desc" role="alert">{{ loadError }}</p>

      <div v-show="currentTab === 'dashboard'" class="dashboard-grid">
        
        <div v-if="loading" class="action-card">
          <div class="action-card__info">
            <p class="action-card__desc" role="status">Cargando tus datos…</p>
          </div>
        </div>

        <div v-else-if="!report && !hasPreviousTest && !loadError" class="action-card action-card--start">
          <div class="action-card__info">
            <span class="action-card__badge">{{ hasPendingTest ? 'Cuestionario pendiente' : 'Disponible ahora' }}</span>
            <h2 class="action-card__title">{{ hasPendingTest ? 'Tienes un cuestionario BFI-44 pendiente' : 'El cuestionario BFI-44 está disponible' }}</h2>
            <p v-if="hasPendingTest" class="action-card__desc">
              Dejaste tu cuestionario sin finalizar. Tus respuestas guardadas se conservan para que puedas retomarlo desde donde quedaste.
            </p>
            <p v-else class="action-card__desc">Aún no hay un reporte disponible.</p>
            <p v-if="!hasPendingTest" class="action-card__desc">
              Responde 44 afirmaciones sobre cómo te describes habitualmente. Los resultados muestran dimensiones de personalidad para apoyar tu reflexión.
            </p>
            <p class="action-card__warning">
              44 afirmaciones · sin límite de tiempo · un envío final
            </p>
            <button @click="startTest" class="btn btn--primary">
              {{ hasPendingTest ? 'Continuar cuestionario BFI-44' : 'Iniciar cuestionario BFI-44' }}
            </button>
          </div>
          <div class="action-card__visual" aria-hidden="true">
            <svg class="visual-radar" viewBox="0 0 120 120">
              <polygon points="60,10 107.6,44.5 89.4,100.5 30.6,100.5 12.4,44.5" />
              <polygon points="60,32.5 86.2,51.5 76.2,82.3 43.8,82.3 33.8,51.5" />
              <polygon class="visual-radar__data" points="60,18 98,47 80,90 38,86 26,49" />
            </svg>
          </div>
        </div>

        <div v-else-if="report" class="action-card action-card--report">
          <div class="action-card__info">
            <span class="action-card__badge action-card__badge--success">Reporte disponible</span>
            <h2 class="action-card__title">Reporte generado</h2>
            <p v-if="report.careerAreas.length" class="action-card__desc">
              Áreas para explorar incluidas en tu reporte:
              <strong>{{ report.careerAreas.map(area => area.title).join(', ') }}</strong>.
            </p>
            <p v-if="report.careerAreas.length" class="action-card__warning" role="note">
              Estas áreas son referencias exploratorias del prototipo; los resultados BFI-44 no evalúan tus aptitudes ni determinan una carrera.
            </p>
            <p v-else class="action-card__desc">El reporte no incluye áreas profesionales.</p>
            <div class="report-quick-stats">
              <div v-for="dimension in report.dimensions" :key="dimension.letter" class="q-stat">
                <span>{{ dimension.letter }}</span> {{ dimension.name }}: {{ dimension.score }}%
              </div>
            </div>
            <button @click="viewLatestReport" class="btn btn--primary">
              Ver Reporte Completo
            </button>
          </div>
        </div>

        <div v-else-if="!loadError" class="action-card action-card--report">
          <div class="action-card__info">
            <h2 class="action-card__title">Reporte no disponible</h2>
            <p class="action-card__desc">Tu cuestionario está completado, pero aún no hay un reporte disponible.</p>
          </div>
        </div>

        <div class="info-sidebar">
          <div class="info-mini-card">
            <div>
              <h4 class="mini-card__title">Antes de responder</h4>
              <p class="mini-card__desc">Responde con sinceridad. No hay respuestas correctas ni perfiles mejores que otros.</p>
            </div>
          </div>

          <div class="info-mini-card">
            <div>
              <h4 class="mini-card__title">Modelo Psicométrico</h4>
              <p class="mini-card__desc">
                El BFI-44 describe cinco dimensiones de personalidad. Sus puntajes no determinan aptitud, éxito académico ni una carrera adecuada.
              </p>
            </div>
          </div>
        </div>

      </div>

      <section v-show="currentTab === 'history'" class="history-section" id="history-section">
        <h3 class="history-title">Bitácora de mi Proceso</h3>
        <p v-if="loading" role="status">Cargando tu bitácora…</p>
        <p v-else-if="!loadError && !Object.values(timeline).some(Boolean)" class="action-card__desc">
          Aún no hay fechas registradas en tu bitácora.
        </p>
        
        <div class="timeline-container">
          <div v-if="timeline.registro" class="timeline-item">
            <div class="timeline-dot timeline-dot--completed"></div>
            <div class="timeline-content">
              <h4>Registro en plataforma</h4>
              <p>Te registraste el {{ formatDate(timeline.registro) }}</p>
            </div>
          </div>
          
          <div v-if="timeline.evaluacion" class="timeline-item">
            <div class="timeline-dot timeline-dot--completed"></div>
            <div class="timeline-content">
              <h4>Cuestionario finalizado</h4>
              <p>Completaste el cuestionario el {{ formatDate(timeline.evaluacion) }}</p>
            </div>
          </div>
          
          <div v-if="timeline.reporte" class="timeline-item">
            <div class="timeline-dot timeline-dot--completed"></div>
            <div class="timeline-content">
              <h4>Reporte generado</h4>
              <p>Tu reporte fue generado el {{ formatDate(timeline.reporte) }}</p>
            </div>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import authService from '../services/authService'
import DashboardNavigation from '../components/DashboardNavigation.vue'
import evaluacionService from '../services/evaluacionService'
import reporteService from '../services/reporteService'
import { bpmStages, getBpmStatus } from '../utils/bpmStatus'

const router = useRouter()
const route = useRoute()

// Pestaña actual de la interfaz
const currentTab = ref('dashboard')
const navigationItems = computed(() => [
  { label: 'Panel principal', to: '/estudiante/dashboard', active: currentTab.value === 'dashboard' },
  { label: 'Bitácora', to: '/estudiante/dashboard#history-section', active: currentTab.value === 'history' },
])
watch(() => route.hash, hash => {
  currentTab.value = hash === '#history-section' ? 'history' : 'dashboard'
}, { immediate: true })

// Estado de la evaluación desde backend
const hasPreviousTest = ref(false)
const hasPendingTest = ref(false)
const bpmState = ref(null)
const orientadorName = ref(null)
const studentName = ref('')

const report = ref(null)
const loading = ref(true)
const loadError = ref('')
const timeline = ref({
  registro: null,
  evaluacion: null,
  reporte: null
})

onMounted(async () => {
  const [profileResult, estadoResult, reportResult] = await Promise.allSettled([
    authService.getProfile(),
    evaluacionService.getEstado(),
    reporteService.getLatestReport()
  ])
  if (profileResult.status === 'fulfilled') {
    studentName.value = profileResult.value?.name?.trim() || ''
  }

  if (estadoResult.status === 'fulfilled') {
    const estado = estadoResult.value
    bpmState.value = estado.bpm_estado ?? null
    hasPreviousTest.value = estado.tiene_evaluacion && ['completada', 'procesada'].includes(estado.estado)
    hasPendingTest.value = estado.tiene_evaluacion && estado.estado === 'en_progreso'
    orientadorName.value = estado.orientador_nombre
    
    timeline.value.registro = estado.registro_fecha
    timeline.value.evaluacion = estado.evaluacion_fecha
    timeline.value.reporte = estado.reporte_fecha
  } else {
    loadError.value = 'No se pudo cargar el estado de tu evaluación. Intenta recargar la página.'
  }

  if (reportResult.status === 'fulfilled') {
    report.value = reportResult.value
  } else if (reportResult.reason.response?.status !== 404) {
    loadError.value = [loadError.value, 'No se pudo consultar tu reporte. Intenta recargar la página.'].filter(Boolean).join(' ')
  }
  loading.value = false
})

function formatDate(dateString) {
  if (!dateString) return ''
  const d = new Date(dateString)
  return d.toLocaleDateString('es-CL', {
    day: 'numeric', month: 'long', year: 'numeric',
    hour: '2-digit', minute:'2-digit'
  })
}

const currentBpmStageIndex = computed(() => {
  return bpmStages.findIndex(step => step.state === bpmState.value)
})

const currentBpmStageText = computed(() => {
  return getBpmStatus(bpmState.value).label
})

// Redirección hacia próximos mockups
function startTest() {
  router.push('/estudiante/evaluacion') // Redirección exacta
}

function viewLatestReport() {
  router.push('/estudiante/reporte')
}

function logout() {
  authService.logout()
}
</script>

<style scoped>
/* ── Progreso del proceso (BPM) ─────────────────────────────────────────── */
.bpm-progress-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 24px 28px;
  margin-bottom: 36px;
  box-shadow: var(--shadow-card);
}
.bpm-header {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.bpm-badge {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--c-primary);
}
.bpm-status-text { font-size: 0.85rem; color: var(--c-muted); }
.bpm-status-text strong { color: var(--c-text); }

.bpm-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}
.bpm-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
  min-width: 0;
}
.bpm-step__node {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: var(--c-surface);
  border: 1px solid var(--c-border-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.8rem;
  color: var(--c-muted);
  z-index: 2;
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}
.bpm-step__label {
  margin-top: 10px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-muted);
  text-align: center;
  overflow-wrap: anywhere;
}
.bpm-step__line {
  position: absolute;
  top: 17px;
  left: calc(50% + 22px);
  width: calc(100% - 44px);
  height: 1px;
  background: repeating-linear-gradient(90deg, var(--c-border-strong) 0 6px, transparent 6px 12px);
  z-index: 1;
}

.bpm-step--completed .bpm-step__node {
  background: var(--c-tint);
  border-color: var(--c-tint-border);
  color: var(--c-primary);
}
.bpm-step--completed .bpm-step__line { background: var(--c-tint-border); }
.bpm-step--completed .bpm-step__label { color: var(--c-text); }

.bpm-step--active .bpm-step__node {
  background: var(--c-primary);
  border-color: var(--c-primary);
  color: #FFFFFF;
  box-shadow: 0 0 0 5px var(--c-tint);
}
.bpm-step--active .bpm-step__label { color: var(--c-primary); font-weight: 700; }

/* ── Bienvenida ─────────────────────────────────────────────────────────── */
.welcome-section { text-align: left; margin-bottom: 32px; }
.welcome-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(1.6rem, 3vw, 2.1rem);
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 6px;
}
.welcome-sub { font-size: 0.9rem; color: var(--c-muted); margin-bottom: 12px; }
.welcome-orientador {
  display: inline-block;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--c-text-soft);
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  padding: 6px 14px;
  border-radius: 14px;
  overflow-wrap: anywhere;
}
.welcome-orientador::before {
  content: '';
  display: inline-block;
  vertical-align: middle;
  margin: -2px 8px 0 0;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-primary);
}
.welcome-orientador strong { color: var(--c-text); }

/* ── Tarjetas principales ───────────────────────────────────────────────── */
.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 24px;
  margin-bottom: 40px;
  align-items: stretch;
}

.action-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 40px;
  display: flex;
  gap: 24px;
  text-align: left;
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}
.action-card__info { flex: 1; min-width: 0; z-index: 2; overflow-wrap: anywhere; }
.action-card__badge {
  display: inline-block;
  font-size: 0.72rem;
  background: var(--c-tint);
  border: 1px solid var(--c-tint-border);
  color: var(--c-primary);
  padding: 4px 10px;
  border-radius: 100px;
  font-weight: 700;
  margin-bottom: 16px;
}
.action-card__badge--success {
  background: var(--c-tint);
  border-color: var(--c-tint-border);
  color: var(--c-primary-strong);
}
.action-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.55rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-bottom: 12px;
}
.action-card__desc { font-size: 0.95rem; line-height: 1.65; color: var(--c-muted); margin-bottom: 12px; }
.action-card__warning {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.5;
  color: var(--c-warning);
  background: var(--c-warning-bg);
  border: 1px solid var(--c-warning-border);
  padding: 8px 12px;
  border-radius: 10px;
  margin-bottom: 24px;
}

/* Tarjeta para comenzar: bloque verde profundo, igual que el cierre de la portada */
.action-card--start {
  background: var(--c-deep);
  border-color: var(--c-deep);
  color: #ECFDF5;
}
.action-card--start::before {
  content: '';
  position: absolute;
  width: 560px; height: 560px;
  right: -240px; bottom: -300px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 47px, rgba(167, 243, 208, 0.08) 47px 48px);
  pointer-events: none;
}
.action-card--start .action-card__badge { background: rgba(190, 242, 100, 0.12); border-color: rgba(190, 242, 100, 0.35); color: #BEF264; }
.action-card--start .action-card__title { color: #FFFFFF; }
.action-card--start .action-card__desc { color: #A7F3D0; }
.action-card--start .action-card__warning { color: #ECFDF5; background: rgba(255, 255, 255, 0.06); border-color: rgba(167, 243, 208, 0.25); }
.action-card--start .btn--primary { background: #FFFFFF; color: var(--c-deep); }
.action-card--start .btn--primary:hover { background: var(--c-tint); }

.action-card__visual {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 12px;
  z-index: 1;
}
.visual-radar { width: 150px; height: 150px; overflow: visible; }
.visual-radar polygon { fill: none; stroke: rgba(167, 243, 208, 0.3); stroke-width: 1; }
.visual-radar .visual-radar__data { fill: rgba(132, 204, 22, 0.22); stroke: var(--c-accent2); stroke-width: 2; stroke-linejoin: round; }

.report-quick-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}
.q-stat {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  padding: 6px 12px 6px 6px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--c-text-soft);
}
.q-stat span {
  display: inline-grid;
  place-items: center;
  width: 26px; height: 26px;
  border-radius: 7px;
  background: var(--c-tint);
  color: var(--c-primary);
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
}

/* ── Columna informativa ────────────────────────────────────────────────── */
.info-sidebar { display: flex; flex-direction: column; gap: 16px; height: 100%; }
.info-mini-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 22px;
  display: flex;
  gap: 16px;
  text-align: left;
}
.info-mini-card:first-child { background: var(--c-tint); border-color: var(--c-tint-border); }
.mini-card__icon { font-size: 1.5rem; line-height: 1; }
.mini-card__title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px; }
.mini-card__desc { font-size: 0.85rem; line-height: 1.55; color: var(--c-muted); }
.info-mini-card:first-child .mini-card__desc { color: var(--c-text-soft); }

/* ── Bitácora ───────────────────────────────────────────────────────────── */
.history-section { text-align: left; margin-top: 16px; }
.history-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.35rem;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
}

.timeline-container {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  box-shadow: var(--shadow-card);
}

.timeline-item { display: flex; gap: 20px; position: relative; }
.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 26px;
  bottom: -30px;
  width: 1px;
  background: repeating-linear-gradient(180deg, var(--c-tint-border) 0 6px, transparent 6px 12px);
}

.timeline-dot {
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--c-border);
  margin-top: 3px;
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}
.timeline-content { min-width: 0; overflow-wrap: anywhere; }
.timeline-dot--completed {
  background: var(--c-primary);
  box-shadow: 0 0 0 4px var(--c-tint);
}

.timeline-content h4 {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: var(--c-text);
  margin-bottom: 4px;
}
.timeline-content p { font-size: 0.875rem; color: var(--c-muted); }

/* ── Botón ──────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding: 12px 24px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  border: none;
}
.btn--primary { background: var(--c-primary); color: #fff; }
.btn--primary:hover { background: var(--c-primary-strong); }

/* ── Responsive ─────────────────────────────────────────────────────────── */
@media (max-width: 1200px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .info-sidebar { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); height: auto; }
}
@media (max-width: 600px) {
  .report-quick-stats { display: grid; grid-template-columns: 1fr; gap: 8px; }
  .bpm-progress-card, .action-card, .timeline-container { padding: 20px; }
  .bpm-progress-card, .welcome-section { margin-bottom: 24px; }
  .bpm-steps { flex-direction: column; align-items: stretch; gap: 16px; }
  .bpm-step { flex-direction: row; gap: 12px; }
  .bpm-step__node { flex-shrink: 0; }
  .bpm-step__label { margin-top: 0; text-align: left; }
  .bpm-step__line { left: 16px; top: 38px; width: 1px; height: calc(100% - 22px); background: repeating-linear-gradient(180deg, var(--c-border-strong) 0 6px, transparent 6px 12px); }
  .bpm-step--completed .bpm-step__line { background: var(--c-tint-border); }
  .action-card { flex-direction: column; border-radius: 20px; }
  .action-card__visual { display: none; }
  .action-card__title { font-size: 1.3rem; }
  .action-card .btn { width: 100%; justify-content: center; }
  .info-sidebar { grid-template-columns: 1fr; }
  .timeline-item { gap: 16px; }
}
@media (prefers-reduced-motion: reduce) {
  .bpm-step__node, .btn { transition: none; }
}
</style>
`````

### `src/views/homeview.vue` (reemplazar completo, 1651 líneas, hash `7ed9053a8d3993a54c39c574bfb8416f0c1b9855`)

`````vue
<template>
  <div class="landing">

    <nav class="nav" aria-label="Navegación de inicio">
      <div class="nav__logo">
        <span class="nav__logo-icon" aria-hidden="true">◈</span>
        <span class="nav__logo-text">Vócalis</span>
      </div>
      <div class="nav__links">
        <router-link to="/como-funciona">Cómo funciona</router-link>
        <router-link to="/el-test">El test</router-link>
        <router-link to="/auth" class="nav__cta">Comenzar gratis</router-link>
      </div>
    </nav>

    <main>
    <!-- ── Hero ─────────────────────────────────────────────────────────── -->
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__bg-glow" aria-hidden="true"></div>

      <div class="hero__inner wrap">
        <div class="hero__content">
          <p class="hero__eyebrow">Cuestionario BFI-44 · Modelo de los cinco grandes</p>

          <h1 id="hero-title" class="hero__title">
            Conoce más<br />
            <em>sobre</em> ti.
          </h1>

          <p class="hero__sub">
            Explora tus rasgos de personalidad con el BFI-44 y comparte tus resultados
            con tu orientador. Un apoyo para reflexionar sobre tu futuro, junto con tus intereses y experiencias.
          </p>

          <div class="hero__actions">
            <a href="#register" class="btn btn--primary">
              Descubrir mi perfil
              <span class="btn__arrow" aria-hidden="true">→</span>
            </a>
            <router-link to="/como-funciona" class="btn btn--ghost">Ver cómo funciona</router-link>
          </div>

          <div class="hero__stats">
            <div class="stat">
              <span class="stat__num">44</span>
              <span class="stat__label">afirmaciones</span>
            </div>
            <div class="stat__divider" aria-hidden="true"></div>
            <div class="stat">
              <span class="stat__num">5</span>
              <span class="stat__label">dimensiones</span>
            </div>
            <div class="stat__divider" aria-hidden="true"></div>
            <div class="stat">
              <span class="stat__num">~8</span>
              <span class="stat__label">minutos</span>
            </div>
          </div>
        </div>

        <div class="hero__visual">
          <div class="hero__visual-head">
            <span class="hero__visual-title">Perfil de ejemplo</span>
            <span class="hero__visual-tag">Datos ficticios</span>
          </div>

          <div ref="radarContainer" class="hero__radar-wrap">
            <div class="radar__label radar__label--top">Apertura</div>
            <div class="radar__label radar__label--tr">Responsabilidad</div>
            <div class="radar__label radar__label--br">Extraversión</div>
            <div class="radar__label radar__label--bl">Amabilidad</div>
            <div class="radar__label radar__label--tl">Neuroticismo</div>
            <svg class="radar__svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="landing-radar-title">
              <title id="landing-radar-title">Ejemplo de las cinco dimensiones OCEAN</title>
              <polygon v-for="(points, index) in radarGridPoints" :key="index"
                       class="radar__grid" :points="points" />
              <line v-for="(point, index) in radarAxes" :key="index" class="radar__axis"
                    :x1="CENTER" :y1="CENTER" :x2="point.x" :y2="point.y" />
              <polygon class="radar__data" :points="radarPoints" />
              <circle
                v-for="(pt, i) in radarDots"
                :key="i"
                :cx="pt.x"
                :cy="pt.y"
                r="4.5"
                class="radar__dot"
              />
            </svg>
          </div>

          <p class="hero__visual-note">
            Cada dimensión es un continuo. No hay perfiles mejores ni peores, solo formas distintas de ser.
          </p>
        </div>
      </div>
    </section>

    <!-- ── Para quién ───────────────────────────────────────────────────── -->
    <section class="audience" id="para-quien" aria-labelledby="audience-title">
      <div class="wrap">
        <header class="section__head">
          <p class="section__eyebrow">Para quién es</p>
          <h2 id="audience-title" class="section__title">Una herramienta,<br />dos miradas.</h2>
          <p class="section__lead">
            Vócalis conecta lo que cada estudiante descubre de sí mismo con el acompañamiento
            que ya ocurre en la orientación escolar.
          </p>
        </header>

        <div class="audience__grid">
          <article v-for="group in audiences" :key="group.title" class="audience-card" :class="`audience-card--${group.tone}`">
            <div class="audience-card__head">
              <span class="audience-card__icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path :d="group.icon" />
                </svg>
              </span>
              <div>
                <p class="audience-card__kicker">{{ group.kicker }}</p>
                <h3 class="audience-card__title">{{ group.title }}</h3>
              </div>
            </div>
            <ul class="audience-card__list">
              <li v-for="item in group.items" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <!-- ── Proceso ──────────────────────────────────────────────────────── -->
    <section class="steps" id="como-funciona" aria-labelledby="steps-title">
      <div class="wrap">
        <header class="section__head section__head--row">
          <div>
            <p class="section__eyebrow">El proceso</p>
            <h2 id="steps-title" class="section__title">Tres pasos para<br />conocerte mejor.</h2>
          </div>
          <router-link to="/como-funciona" class="text-link">
            Ver el recorrido completo <span aria-hidden="true">→</span>
          </router-link>
        </header>

        <ol class="steps__list">
          <li class="step-card" v-for="step in steps" :key="step.n">
            <span class="step-card__num" aria-hidden="true">{{ step.n }}</span>
            <h3 class="step-card__title">{{ step.title }}</h3>
            <p class="step-card__desc">{{ step.desc }}</p>
          </li>
        </ol>
      </div>
    </section>

    <!-- ── Dimensiones ──────────────────────────────────────────────────── -->
    <section class="ocean" id="dimensiones" aria-labelledby="ocean-title">
      <div class="ocean__inner wrap">
        <div class="ocean__left">
          <p class="section__eyebrow">Las dimensiones de personalidad</p>
          <h2 id="ocean-title" class="section__title">El Big Five<br />OCEAN.</h2>
          <p class="ocean__intro">
            El modelo Big Five describe cinco dimensiones de personalidad. En Vócalis,
            estos resultados aportan una perspectiva para conversar sobre cómo te describes y lo que te interesa.
          </p>
          <p class="ocean__hint">
            Cada rasgo va de un extremo a otro. Tu resultado indica hacia dónde tiendes,
            no si está bien o mal.
          </p>
          <router-link to="/el-test" class="text-link">
            Conocer cada dimensión en detalle <span aria-hidden="true">→</span>
          </router-link>
        </div>

        <ul class="ocean__cards">
          <li
            class="ocean-card"
            v-for="dim in dimensions"
            :key="dim.letter"
            :style="{ '--accent': dim.color }"
          >
            <span class="ocean-card__letter" aria-hidden="true">{{ dim.letter }}</span>
            <div class="ocean-card__body">
              <h3 class="ocean-card__name">{{ dim.name }}</h3>
              <p class="ocean-card__desc">{{ dim.desc }}</p>
              <p class="ocean-card__scale">
                <span class="visually-hidden">Va desde </span>
                <span class="ocean-card__pole">{{ dim.low }}</span>
                <span class="visually-hidden"> hasta </span>
                <span class="ocean-card__track" aria-hidden="true"></span>
                <span class="ocean-card__pole ocean-card__pole--high">{{ dim.high }}</span>
              </p>
            </div>
          </li>
        </ul>
      </div>
    </section>

    <!-- ── Reporte ──────────────────────────────────────────────────────── -->
    <section class="report-preview" aria-labelledby="report-title">
      <div class="report-preview__inner wrap">
        <header class="section__head">
          <p class="section__eyebrow">Tu reporte</p>
          <h2 id="report-title" class="section__title">Tus resultados.<br />Un punto de partida.</h2>
          <p class="section__lead">
            Al terminar el cuestionario recibes un reporte que puedes consultar desde tu cuenta
            y revisar junto a tu orientador.
          </p>
        </header>

        <div class="report-preview__grid">
          <article class="report-card" v-for="card in reportFeatures" :key="card.title">
            <span class="report-card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path :d="card.icon" />
              </svg>
            </span>
            <h3 class="report-card__title">{{ card.title }}</h3>
            <p class="report-card__desc">{{ card.desc }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ── Expectativas ─────────────────────────────────────────────────── -->
    <section class="scope" aria-labelledby="scope-title">
      <div class="wrap">
        <header class="section__head">
          <p class="section__eyebrow">Antes de empezar</p>
          <h2 id="scope-title" class="section__title">Qué es Vócalis,<br />y qué no es.</h2>
        </header>

        <div class="scope__grid">
          <div class="scope__col scope__col--is">
            <h3 class="scope__heading">Es</h3>
            <ul class="scope__list">
              <li v-for="item in scopeIs" :key="item">
                <svg class="scope__mark" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 10.5l3.2 3.2L15 6.8" /></svg>
                <span>{{ item }}</span>
              </li>
            </ul>
          </div>
          <div class="scope__col scope__col--not">
            <h3 class="scope__heading">No es</h3>
            <ul class="scope__list">
              <li v-for="item in scopeNot" :key="item">
                <svg class="scope__mark" viewBox="0 0 20 20" aria-hidden="true"><path d="M6 10h8" /></svg>
                <span>{{ item }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Registro ─────────────────────────────────────────────────────── -->
    <section class="register" id="register" aria-labelledby="register-title">
      <div class="register__inner wrap">
        <div class="register__copy">
          <p class="section__eyebrow section__eyebrow--on-dark">Empieza hoy</p>
          <h2 id="register-title" class="register__title">Tu perfil te está esperando.</h2>
          <p class="register__sub">
            Crea tu cuenta y responde 44 afirmaciones para empezar a reflexionar. Vócalis complementa el acompañamiento de tu orientador.
          </p>
          <ul class="register__facts">
            <li>Sin costo para estudiantes</li>
            <li>Desde tu computador o teléfono</li>
            <li>Tus respuestas se guardan mientras avanzas</li>
          </ul>
        </div>

        <div class="register__box">
          <form class="register__form" @submit.prevent="handleRegister">
            <div class="field">
              <label for="landing-name">Tu nombre</label>
              <input
                id="landing-name"
                name="nombre"
                autocomplete="name"
                v-model="form.name"
                class="register__input"
                type="text"
                placeholder="Ej.: Camila Rojas"
                required
              />
            </div>
            <div class="field">
              <label for="landing-email">Correo electrónico</label>
              <input
                id="landing-email"
                name="email"
                autocomplete="email"
                inputmode="email"
                autocapitalize="none"
                :spellcheck="false"
                v-model="form.email"
                class="register__input"
                type="email"
                placeholder="tu@correo.cl"
                required
              />
            </div>
            <button type="submit" class="btn btn--primary btn--full">
              Crear mi cuenta gratis
              <span class="btn__arrow" aria-hidden="true">→</span>
            </button>
            <p class="register__hint">En el siguiente paso eliges tu rol y completas tus datos.</p>
          </form>
          <p class="register__login">
            ¿Ya tienes cuenta?
            <router-link to="/auth">Inicia sesión aquí</router-link>
          </p>
        </div>
      </div>
    </section>
    </main>

    <footer class="footer">
      <div class="footer__inner wrap">
        <div class="footer__brand">
          <div class="footer__logo">
            <span class="nav__logo-icon" aria-hidden="true">◈</span>
            <span>Vócalis</span>
          </div>
          <p class="footer__copy">
            Proyecto de Título · Ingeniería en Informática · 2026
          </p>
        </div>
        <div class="footer__links">
          <router-link to="/como-funciona">Cómo funciona</router-link>
          <router-link to="/el-test">El test</router-link>
          <router-link to="/auth">Iniciar sesión</router-link>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

defineOptions({ name: 'HomeView' })

// ── Radar animation ──────────────────────────────────────────────────────────
const AXES = [
  { letter: 'O', angle: -90 },
  { letter: 'C', angle: -18 },
  { letter: 'E', angle: 54 },
  { letter: 'A', angle: 126 },
  { letter: 'N', angle: 198 },
]
const CENTER = 160
const MAX_R  = 120

const exampleValues = [0.85, 0.70, 0.60, 0.80, 0.45]
const targetValues = ref([...exampleValues])
const currentValues = ref(exampleValues.map(() => 0))
const radarContainer = ref(null)
let animFrame = null
let lastTimestamp = null
let targetElapsed = 0
let radarVisible = false
let observer

function polarToXY(angleDeg, r) {
  const rad = (angleDeg * Math.PI) / 180
  return {
    x: CENTER + r * Math.cos(rad),
    y: CENTER + r * Math.sin(rad),
  }
}

const radarAxes = AXES.map(axis => polarToXY(axis.angle, MAX_R))
const radarGridPoints = [1, 0.75, 0.5, 0.25].map(scale =>
  AXES.map(axis => {
    const point = polarToXY(axis.angle, MAX_R * scale)
    return `${point.x},${point.y}`
  }).join(' ')
)

function stopRadar() {
  if (animFrame !== null) cancelAnimationFrame(animFrame)
  animFrame = null
  lastTimestamp = null
}

function canAnimate() {
  return radarVisible && !document.hidden
}

// Conserva el movimiento continuo original y su velocidad en distintas pantallas.
function animateRadar(timestamp) {
  animFrame = null
  if (!canAnimate()) { stopRadar(); return }
  const elapsed = lastTimestamp === null ? 1000 / 60 : Math.min(timestamp - lastTimestamp, 100)
  lastTimestamp = timestamp
  targetElapsed += elapsed
  if (targetElapsed >= 3000) {
    targetElapsed %= 3000
    targetValues.value = targetValues.value.map(() => 0.35 + Math.random() * 0.60)
  }
  const blend = 1 - Math.pow(0.98, elapsed / (1000 / 60))
  currentValues.value = currentValues.value.map((value, index) =>
    value + (targetValues.value[index] - value) * blend
  )
  animFrame = requestAnimationFrame(animateRadar)
}

function syncRadar() {
  if (!canAnimate()) {
    stopRadar()
    return
  }
  if (animFrame === null) animFrame = requestAnimationFrame(animateRadar)
}

onMounted(() => {
  document.addEventListener('visibilitychange', syncRadar)
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(([entry]) => {
      radarVisible = entry.isIntersecting
      syncRadar()
    }, { threshold: 0.15 })
    observer.observe(radarContainer.value)
  } else {
    radarVisible = true
    syncRadar()
  }
})
onUnmounted(() => {
  stopRadar()
  observer?.disconnect()
  document.removeEventListener('visibilitychange', syncRadar)
})

const radarDots = computed(() =>
  AXES.map((ax, i) => polarToXY(ax.angle, currentValues.value[i] * MAX_R))
)

const radarPoints = computed(() =>
  radarDots.value.map(p => `${p.x},${p.y}`).join(' ')
)

// ── Content data ─────────────────────────────────────────────────────────────
const router = useRouter()

const audiences = [
  {
    tone: 'student',
    kicker: 'Si eres estudiante',
    title: 'Un espacio para mirarte con calma',
    icon: 'M12 12a4 4 0 1 0 0-8a4 4 0 1 0 0 8z M4.5 20.5c0-4 3.4-6.5 7.5-6.5s7.5 2.5 7.5 6.5',
    items: [
      'Respondes 44 afirmaciones a tu ritmo, desde tu computador o teléfono.',
      'Puedes pausar y continuar después: tus respuestas quedan guardadas.',
      'Recibes un reporte con tu perfil en las cinco dimensiones.',
    ],
  },
  {
    tone: 'counselor',
    kicker: 'Si eres orientador u orientadora',
    title: 'Contexto para cada conversación',
    icon: 'M9 11a3.5 3.5 0 1 0 0-7a3.5 3.5 0 1 0 0 7z M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6 M16 4.3a3.5 3.5 0 0 1 0 6.4 M18 14.4c2.1.7 3.5 2.7 3.5 5.6',
    items: [
      'Asignas los cursos que acompañas y ves a sus estudiantes en un solo panel.',
      'Sigues en qué etapa está cada estudiante: registro, cuestionario o reporte listo.',
      'Consultas los reportes para preparar entrevistas de orientación.',
    ],
  },
]

const steps = [
  { n: '01', title: 'Responde el test', desc: 'Contesta 44 afirmaciones simples sobre cómo piensas, sientes y actúas. Sin respuestas incorrectas.' },
  { n: '02', title: 'Conoce tu perfil', desc: 'El sistema calcula tus puntuaciones en las 5 dimensiones OCEAN y genera tu radar de personalidad.' },
  { n: '03', title: 'Reflexiona con tu orientador', desc: 'Revisa tus resultados y explora tus intereses junto con tu orientador. Elegir tu camino requiere también conocer tus habilidades, experiencias y opciones.' },
]

const dimensions = [
  { letter: 'O', name: 'Apertura', desc: 'Creatividad, curiosidad intelectual y gusto por las nuevas experiencias.', color: '#4F46E5', low: 'Prefiere lo conocido', high: 'Busca lo nuevo' },
  { letter: 'C', name: 'Responsabilidad', desc: 'Organización, disciplina y orientación al logro de metas.', color: '#10B981', low: 'Flexible y espontáneo', high: 'Organizado y metódico' },
  { letter: 'E', name: 'Extraversión', desc: 'Sociabilidad, energía y comodidad en entornos grupales.', color: '#F59E0B', low: 'Reservado', high: 'Sociable' },
  { letter: 'A', name: 'Amabilidad', desc: 'Empatía, cooperación y disposición a ayudar a los demás.', color: '#EC4899', low: 'Directo y crítico', high: 'Cooperativo y empático' },
  { letter: 'N', name: 'Neuroticismo', desc: 'Respuesta emocional y gestión del estrés y la ansiedad.', color: '#EF4444', low: 'Emocionalmente estable', high: 'Más sensible al estrés' },
]

const reportFeatures = [
  { title: 'Gráfico radar OCEAN', desc: 'Consulta tus puntajes en las cinco dimensiones de personalidad en un mismo gráfico.', icon: 'M12 3l8.5 6.2-3.2 10H6.7L3.5 9.2z M12 3v9 M20.5 9.2L12 12 M17.3 19.2L12 12 M6.7 19.2L12 12 M3.5 9.2L12 12' },
  { title: 'Texto interpretativo', desc: 'Lee descripciones de las tendencias que reflejan tus respuestas para apoyar tu reflexión.', icon: 'M4 6h16 M4 10h16 M4 14h11 M4 18h7' },
  { title: 'Áreas para explorar', desc: 'Referencias exploratorias del prototipo para investigar y conversar. No son una medida de afinidad profesional.', icon: 'M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18z M15.5 8.5l-2 5-5 2 2-5z' },
  { title: 'Acompañamiento del orientador', desc: 'Tu orientador asignado puede consultar tu avance y tus resultados para apoyar el seguimiento.', icon: 'M9 11a3.5 3.5 0 1 0 0-7a3.5 3.5 0 1 0 0 7z M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6 M16 4.3a3.5 3.5 0 0 1 0 6.4 M18 14.4c2.1.7 3.5 2.7 3.5 5.6' },
]

const scopeIs = [
  'Un cuestionario de autoconocimiento basado en el modelo de los cinco grandes rasgos.',
  'Una descripción de tendencias en tu forma habitual de pensar, sentir y actuar.',
  'Un punto de partida para conversar con tu orientador sobre tus intereses.',
]

const scopeNot = [
  'Un test que te diga qué carrera estudiar.',
  'Una evaluación con nota, puntaje ideal o respuestas correctas.',
  'Un diagnóstico psicológico ni clínico.',
]

// ── Form ──────────────────────────────────────────────────────────────────────
// Este formulario solo captura el nombre y correo como puerta de entrada;
// el registro completo (contraseña, rol) se termina en /auth para no
// duplicar la lógica de creación de cuenta en dos lugares distintos.
const form = ref({ name: '', email: '' })
function handleRegister() {
  router.push({
    path: '/auth',
    query: { mode: 'register', name: form.value.name, email: form.value.email },
  })
}
</script>

<style scoped>
/* ── Tokens de la portada ───────────────────────────────────────────────── */

.landing {
  --c-bg:             #F8FAFC; /* Slate 50 - Fondo general */
  --c-surface:        #FFFFFF; /* Blanco para tarjetas */
  --c-primary:        #047857; /* Verde esmeralda oscuro (Emerald 700) */
  --c-primary-strong: #065F46; /* Emerald 800 - Hover */
  --c-deep:           #064E3B; /* Emerald 900 - Bloque de registro */
  --c-accent1:        #0D9488; /* Teal 600 */
  --c-accent2:        #84CC16; /* Lima (Lime 500) */
  --c-tint:           #ECFDF5; /* Emerald 50 - Fondos suaves */
  --c-tint-border:    #A7F3D0; /* Emerald 200 - Bordes suaves */
  --c-text:           #0F172A; /* Slate 900 - Texto principal */
  --c-muted:          #64748B; /* Slate 500 - Texto secundario */
  --c-border:         #E2E8F0; /* Slate 200 - Bordes sutiles */
  --r-card:           16px;
  --wrap-pad:         48px;

  font-family: 'Inter', sans-serif;
  background: var(--c-bg);
  color: var(--c-text);
}
.landing section[id] { scroll-margin-top: 100px; }

.wrap {
  max-width: 1180px;
  margin: 0 auto;
  padding-left: var(--wrap-pad);
  padding-right: var(--wrap-pad);
}

.visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

/* ── Nav ─────────────────────────────────────────────────────────────────── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 48px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--c-border);
}

.nav__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.25rem;
  letter-spacing: -0.01em;
  color: var(--c-text);
}

.nav__logo-icon {
  color: var(--c-primary);
  font-size: 1.4rem;
}

.nav__links {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav__links a {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--c-muted);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s;
}

.nav__links a:hover { color: var(--c-primary); }

.nav__cta {
  background: var(--c-primary) !important;
  color: #FFFFFF !important;
  padding: 8px 20px;
  border-radius: 100px;
  font-size: 0.875rem !important;
  font-weight: 600;
  transition: background-color 0.2s;
}

.nav__cta:hover { background: var(--c-primary-strong) !important; }

/* ── Hero ────────────────────────────────────────────────────────────────── */
.hero {
  position: relative;
  overflow: hidden;
  padding: 136px 0 96px;
  background: linear-gradient(180deg, #F1F8F4 0%, var(--c-bg) 100%);
  border-bottom: 1px solid var(--c-border);
}

/* Trama de puntos que se desvanece detrás del gráfico */
.hero__bg-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: radial-gradient(rgba(4, 120, 87, 0.16) 1px, transparent 1.2px);
  background-size: 22px 22px;
  -webkit-mask-image: radial-gradient(ellipse 45% 60% at 76% 50%, #000 0%, transparent 75%);
  mask-image: radial-gradient(ellipse 45% 60% at 76% 50%, #000 0%, transparent 75%);
}

.hero__inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
  align-items: center;
  gap: 64px;
}

.hero__content { min-width: 0; }

.hero__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--c-primary);
  margin-bottom: 24px;
}

.hero__eyebrow::before {
  content: '';
  width: 24px;
  height: 2px;
  border-radius: 2px;
  background: var(--c-primary);
}

.hero__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2.8rem, 5.4vw, 4.6rem);
  line-height: 1.04;
  letter-spacing: -0.035em;
  margin-bottom: 24px;
  color: var(--c-text);
}

/* Subrayado tipo marcador en lugar de texto degradado */
.hero__title em {
  font-style: normal;
  color: var(--c-primary);
  background: linear-gradient(transparent 64%, rgba(132, 204, 22, 0.38) 64%, rgba(132, 204, 22, 0.38) 92%, transparent 92%);
  padding: 0 0.04em;
}

.hero__sub {
  font-size: 1.075rem;
  line-height: 1.7;
  color: #475569; /* Slate 600: más contraste para el párrafo principal */
  max-width: 470px;
  margin-bottom: 36px;
}

.hero__actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 44px;
}

.hero__stats {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-top: 28px;
  border-top: 1px solid var(--c-border);
  max-width: 470px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.stat__num {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.75rem;
  color: var(--c-text);
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat__label {
  font-size: 0.8rem;
  color: var(--c-muted);
  font-weight: 500;
}

.stat__divider {
  width: 1px;
  height: 36px;
  background: var(--c-border);
}

/* ── Tarjeta del radar ───────────────────────────────────────────────────── */
.hero__visual {
  position: relative;
  min-width: 0;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 24px;
  padding: 22px 24px 24px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 24px 48px -24px rgba(6, 78, 59, 0.22);
}

.hero__visual-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--c-border);
}

.hero__visual-title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
}

.hero__visual-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-muted);
  background: var(--c-bg);
  border: 1px solid var(--c-border);
  padding: 4px 10px;
  border-radius: 100px;
  white-space: nowrap;
}

.hero__visual-note {
  margin-top: 4px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--c-muted);
}

/* ── Radar ───────────────────────────────────────────────────────────────── */
/* El contenedor mide exactamente lo mismo que el SVG para que los
   rótulos se anclen a cada vértice con porcentajes del viewBox. */
.hero__radar-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: min(340px, 100%);
  margin: 44px auto 40px;
}

.radar__svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

.radar__grid {
  fill: none;
  stroke: #E2E8F0;
  stroke-width: 1;
}

.radar__grid:first-of-type { stroke: #CBD5E1; }

.radar__axis {
  stroke: #E2E8F0;
  stroke-width: 1;
}

.radar__data {
  fill: rgba(4, 120, 87, 0.14);
  stroke: var(--c-primary);
  stroke-width: 2;
  stroke-linejoin: round;
}

.radar__dot {
  fill: var(--c-surface);
  stroke: var(--c-primary);
  stroke-width: 2;
}

.radar__label {
  position: absolute;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-text);
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.9);
  padding: 2px 6px;
  border-radius: 6px;
}

/* Vértices en el viewBox 320×320: O(50%,12.5%) C(85.6%,38.4%)
   E(72%,80.3%) A(28%,80.3%) N(14.4%,38.4%) */
.radar__label--top { left: 50%;   top: calc(12.5% - 10px); transform: translate(-50%, -100%); }
.radar__label--tr  { left: 85.6%; top: calc(38.4% - 10px); transform: translate(-50%, -100%); }
.radar__label--br  { left: 72%;   top: calc(80.3% + 10px); transform: translateX(-50%); }
.radar__label--bl  { left: 28%;   top: calc(80.3% + 10px); transform: translateX(-50%); }
.radar__label--tl  { left: 14.4%; top: calc(38.4% - 10px); transform: translate(-50%, -100%); }

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 13px 26px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
  border: 1px solid transparent;
}

.btn--primary {
  background: var(--c-primary);
  color: #fff;
}

.btn--primary:hover { background: var(--c-primary-strong); }

.btn--ghost {
  background: var(--c-surface);
  color: var(--c-text);
  border-color: var(--c-border);
}

.btn--ghost:hover {
  border-color: var(--c-primary);
  color: var(--c-primary);
}

.btn--full { width: 100%; justify-content: center; }

.btn__arrow {
  font-size: 1rem;
  transition: transform 0.2s;
}

.btn:hover .btn__arrow { transform: translateX(3px); }

.text-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 44px;
  color: var(--c-primary);
  font-weight: 600;
  font-size: 0.9rem;
  text-decoration: none;
  white-space: nowrap;
}

.text-link span { transition: transform 0.2s; }
.text-link:hover { text-decoration: underline; text-underline-offset: 4px; }
.text-link:hover span { transform: translateX(3px); }

/* ── Section shared ──────────────────────────────────────────────────────── */
.section__head {
  max-width: 640px;
  margin-bottom: 48px;
}

.section__head--row {
  max-width: none;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.section__eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--c-primary);
  margin-bottom: 14px;
}

.section__eyebrow--on-dark { color: #BEF264; } /* Lime 300 sobre verde profundo */

.section__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(1.9rem, 3.4vw, 2.75rem);
  line-height: 1.12;
  letter-spacing: -0.03em;
  color: var(--c-text);
}

.section__lead {
  margin-top: 18px;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--c-muted);
}

/* ── Para quién ──────────────────────────────────────────────────────────── */
.audience {
  padding: 112px 0;
  background: var(--c-surface);
}

.audience__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.audience-card {
  border-radius: 20px;
  padding: 36px;
  border: 1px solid var(--c-border);
}

.audience-card--student { background: var(--c-tint); border-color: var(--c-tint-border); }
.audience-card--counselor { background: var(--c-bg); }

.audience-card__head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}

.audience-card__head > div { min-width: 0; }

.audience-card__icon {
  flex: 0 0 48px;
  width: 48px; height: 48px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: var(--c-surface);
  color: var(--c-primary);
  border: 1px solid var(--c-border);
}

.audience-card--student .audience-card__icon { border-color: var(--c-tint-border); }
.audience-card__icon svg { width: 24px; height: 24px; }

.audience-card__kicker {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-primary);
  margin-bottom: 2px;
}

.audience-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.2rem;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.audience-card__list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 0;
}

.audience-card__list li {
  position: relative;
  padding: 14px 0 14px 22px;
  font-size: 0.95rem;
  line-height: 1.55;
  color: #334155; /* Slate 700 */
  border-top: 1px solid rgba(15, 23, 42, 0.07);
}

.audience-card__list li::before {
  content: '';
  position: absolute;
  left: 2px; top: 23px;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--c-primary);
}

/* ── Steps ───────────────────────────────────────────────────────────────── */
.steps {
  padding: 112px 0;
  background: var(--c-bg);
  border-top: 1px solid var(--c-border);
}

.steps__list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 40px;
  counter-reset: step;
}

.step-card {
  position: relative;
  min-width: 0;
}

/* Línea que une cada paso con el siguiente */
.step-card:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 24px;
  left: 64px;
  right: -28px;
  height: 1px;
  background: repeating-linear-gradient(90deg, var(--c-tint-border) 0 6px, transparent 6px 12px);
}

.step-card__num {
  display: grid;
  place-items: center;
  width: 48px; height: 48px;
  margin-bottom: 24px;
  border-radius: 50%;
  background: var(--c-surface);
  border: 1px solid var(--c-tint-border);
  font-family: 'Poppins', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--c-primary);
}

.step-card:first-child .step-card__num {
  background: var(--c-primary);
  border-color: var(--c-primary);
  color: #fff;
}

.step-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1.15rem;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
}

.step-card__desc {
  font-size: 0.95rem;
  line-height: 1.65;
  color: var(--c-muted);
  max-width: 340px;
}

/* ── Ocean ───────────────────────────────────────────────────────────────── */
.ocean {
  padding: 112px 0;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.ocean__inner {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.3fr);
  gap: 72px;
  align-items: start;
}

.ocean__left {
  position: sticky;
  top: 112px;
  min-width: 0;
}

.ocean__intro {
  margin-top: 20px;
  font-size: 1rem;
  line-height: 1.7;
  color: var(--c-muted);
  max-width: 400px;
}

.ocean__hint {
  margin: 20px 0 12px;
  padding: 16px 18px;
  max-width: 400px;
  border-left: 3px solid var(--c-accent2);
  background: var(--c-bg);
  border-radius: 0 12px 12px 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #334155;
}

.ocean__cards {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ocean-card {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr);
  gap: 20px;
  align-items: start;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 22px 24px;
}

.ocean-card__letter {
  display: grid;
  place-items: center;
  width: 52px; height: 52px;
  border-radius: 14px;
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: 1.5rem;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 10%, #FFFFFF);
}

.ocean-card__body { min-width: 0; }

.ocean-card__name {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 4px;
}

.ocean-card__desc {
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--c-muted);
}

.ocean-card__scale {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  grid-template-areas: "track track" "low high";
  row-gap: 8px;
  column-gap: 12px;
  margin-top: 16px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #475569;
}

.ocean-card__pole { grid-area: low; }
.ocean-card__pole--high { grid-area: high; text-align: right; }

.ocean-card__track {
  grid-area: track;
  position: relative;
  height: 4px;
  border-radius: 4px;
  background: linear-gradient(90deg, #E2E8F0 0%, var(--accent) 100%);
}

.ocean-card__track::before,
.ocean-card__track::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 10px; height: 10px;
  border-radius: 50%;
  transform: translateY(-50%);
  background: var(--c-surface);
  border: 2px solid #CBD5E1;
}

.ocean-card__track::before { left: -1px; }
.ocean-card__track::after  { right: -1px; border-color: var(--accent); }

/* ── Report preview ──────────────────────────────────────────────────────── */
.report-preview {
  padding: 112px 0;
  background: var(--c-bg);
  border-top: 1px solid var(--c-border);
}

.report-preview__inner {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.3fr);
  gap: 72px;
  align-items: start;
}

.report-preview__inner .section__head { margin-bottom: 0; }

.report-preview__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.report-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  padding: 26px 24px;
  min-width: 0;
}

.report-card__icon {
  display: grid;
  place-items: center;
  width: 44px; height: 44px;
  margin-bottom: 18px;
  border-radius: 12px;
  background: var(--c-tint);
  color: var(--c-primary);
}

.report-card__icon svg { width: 22px; height: 22px; }

.report-card__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 8px;
  color: var(--c-text);
}

.report-card__desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--c-muted);
}

/* ── Qué es / qué no es ──────────────────────────────────────────────────── */
.scope {
  padding: 112px 0;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.scope__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  border: 1px solid var(--c-border);
  border-radius: 20px;
  overflow: hidden;
}

.scope__col {
  padding: 36px 40px;
  min-width: 0;
}

.scope__col--is { background: var(--c-tint); }
.scope__col--not { background: var(--c-surface); border-left: 1px solid var(--c-border); }

.scope__heading {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.scope__col--is .scope__heading { color: var(--c-primary); }
.scope__col--not .scope__heading { color: var(--c-muted); }

.scope__list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 16px;
}

.scope__list li {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  gap: 12px;
  align-items: start;
  font-size: 0.98rem;
  line-height: 1.55;
  color: #334155;
}

.scope__mark {
  width: 24px; height: 24px;
  padding: 3px;
  border-radius: 50%;
  fill: none;
  stroke-width: 2.2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.scope__col--is .scope__mark { background: var(--c-primary); stroke: #FFFFFF; }
.scope__col--not .scope__mark { background: #F1F5F9; stroke: #64748B; }

/* ── Register ────────────────────────────────────────────────────────────── */
.register {
  position: relative;
  padding: 112px 0;
  background: var(--c-deep);
  color: #ECFDF5;
  overflow: hidden;
}

/* Anillos concéntricos que evocan el radar, muy tenues */
.register::before {
  content: '';
  position: absolute;
  width: 720px; height: 720px;
  left: -260px; bottom: -380px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, transparent 0 59px, rgba(167, 243, 208, 0.08) 59px 60px);
  pointer-events: none;
}

.register__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 440px);
  gap: 72px;
  align-items: center;
}

.register__copy { min-width: 0; }

.register__title {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #FFFFFF;
  margin-bottom: 18px;
}

.register__sub {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #A7F3D0;
  max-width: 480px;
}

.register__facts {
  list-style: none;
  padding: 0;
  margin-top: 32px;
  display: grid;
  gap: 12px;
}

.register__facts li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.95rem;
  color: #ECFDF5;
}

.register__facts li::before {
  content: '';
  flex: 0 0 8px;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--c-accent2);
}

.register__box {
  background: var(--c-surface);
  color: var(--c-text);
  border-radius: 24px;
  padding: 36px;
  box-shadow: 0 30px 60px -30px rgba(0, 0, 0, 0.5);
  min-width: 0;
}

.register__form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--c-text);
}

.register__input {
  background: var(--c-surface);
  border: 1px solid #CBD5E1;
  border-radius: 12px;
  padding: 13px 16px;
  font-size: 0.95rem;
  color: var(--c-text);
  font-family: 'Inter', sans-serif;
  width: 100%;
  min-height: 48px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.register__input::placeholder { color: #94A3B8; }

.register__input:focus {
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(4, 120, 87, 0.18);
}

.register__form .btn { margin-top: 6px; }

.register__hint {
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--c-muted);
  text-align: center;
}

.register__login {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--c-border);
  font-size: 0.875rem;
  color: var(--c-muted);
  text-align: center;
}

.register__login a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 4px 6px;
  color: var(--c-primary);
  text-decoration: none;
  font-weight: 600;
}

.register__login a:hover { text-decoration: underline; text-underline-offset: 4px; }

/* ── Footer ──────────────────────────────────────────────────────────────── */
.footer {
  padding: 40px 0;
  background: var(--c-surface);
  border-top: 1px solid var(--c-border);
}

.footer__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.footer__logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 4px;
}

.footer__copy {
  font-size: 0.85rem;
  color: var(--c-muted);
}

.footer__links {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 24px;
}

.footer__links a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--c-muted);
  text-decoration: none;
}

.footer__links a:hover { color: var(--c-primary); }

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1080px) {
  .hero__inner,
  .ocean__inner,
  .report-preview__inner,
  .register__inner { gap: 48px; }
}

@media (max-width: 900px) {
  .landing { --wrap-pad: var(--page-gutter); }
  .landing section[id] { scroll-margin-top: 140px; }

  .nav { position: sticky; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; padding: 12px var(--page-gutter); background: var(--c-surface); backdrop-filter: none; }
  .nav__logo { min-width: 0; }
  .nav__links { display: contents; }
  .nav__links a { font-size: 0.8rem; text-align: center; }
  .nav__links a:first-child { grid-row: 2; grid-column: 1; }
  .nav__links a:nth-child(2) { grid-row: 2; grid-column: 2; }
  .nav__cta { grid-row: 1; grid-column: 2; padding: 8px 12px; }

  .hero { padding: 28px 0 56px; }
  .hero__bg-glow { display: none; }
  .hero__inner { grid-template-columns: 1fr; gap: 36px; }
  .hero__content { text-align: center; }
  .hero__eyebrow { justify-content: center; }
  .hero__eyebrow::before { display: none; }
  .hero__sub { margin-left: auto; margin-right: auto; }
  .hero__actions { justify-content: center; }
  .hero__stats { justify-content: center; margin: 0 auto; }

  .hero__visual { order: -1; width: 100%; max-width: 400px; margin: 0 auto; padding: 16px; border-radius: 20px; }
  .hero__visual-head { padding-bottom: 12px; }
  .hero__visual-note { display: none; }
  .hero__radar-wrap { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 6px; width: 100%; margin: 4px 0 0; }
  .radar__svg { grid-row: 1; grid-column: 1 / -1; width: 100%; max-width: 210px; margin: -6px auto 0; }
  .radar__label { position: static; transform: none; white-space: normal; overflow-wrap: anywhere; text-align: center; font-size: 0.7rem; background: var(--c-bg); padding: 6px 4px; grid-column: span 2; }
  .radar__label--bl,
  .radar__label--tl { grid-column: span 3; }

  .audience,
  .steps,
  .ocean,
  .report-preview,
  .scope,
  .register { padding: 64px 0; }

  .section__head { margin-bottom: 32px; }
  .section__head--row { flex-direction: column; align-items: flex-start; gap: 8px; }

  .audience__grid { grid-template-columns: 1fr; gap: 16px; }
  .audience-card { padding: 28px 24px; }

  .steps__list { grid-template-columns: 1fr; gap: 0; }
  .step-card { display: grid; grid-template-columns: 48px minmax(0, 1fr); column-gap: 20px; padding-bottom: 32px; }
  .step-card:last-child { padding-bottom: 0; }
  .step-card__num { grid-row: 1 / span 2; margin-bottom: 0; }
  .step-card__title { align-self: center; margin: 12px 0 6px; }
  .step-card__desc { grid-column: 2; max-width: none; }
  .step-card:not(:last-child)::after { top: 56px; bottom: 8px; left: 24px; right: auto; width: 1px; height: auto; background: repeating-linear-gradient(180deg, var(--c-tint-border) 0 6px, transparent 6px 12px); }

  .ocean__inner { grid-template-columns: 1fr; gap: 32px; }
  .ocean__left { position: static; }

  .report-preview__inner { grid-template-columns: 1fr; gap: 32px; }

  .scope__grid { grid-template-columns: 1fr; }
  .scope__col { padding: 28px 24px; }
  .scope__col--not { border-left: none; border-top: 1px solid var(--c-border); }

  .register__inner { grid-template-columns: 1fr; gap: 36px; }
  .register__box { padding: 28px 24px; }
  .register__input { font-size: 16px; }

  .footer { padding: 28px 0; }
  .footer__inner { flex-direction: column; text-align: center; gap: 12px; }
  .footer__logo { justify-content: center; }
  .footer__links { justify-content: center; }
}

@media (max-width: 600px) {
  .report-preview__grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .hero__title { font-size: clamp(2.2rem, 11vw, 2.8rem); }
  .hero__eyebrow { font-size: 0.75rem; }
  .hero__actions { flex-direction: column; }
  .hero__actions .btn { width: 100%; justify-content: center; }
  .hero__stats { gap: 14px; }
  .stat__num { font-size: 1.5rem; }
  .stat__label { font-size: 0.72rem; }
  .audience-card { padding: 24px 20px; }
  .audience-card__head { align-items: flex-start; }
  .ocean-card { grid-template-columns: 40px minmax(0, 1fr); gap: 14px; padding: 18px 16px; }
  .ocean-card__letter { width: 40px; height: 40px; border-radius: 12px; font-size: 1.2rem; }
  .report-card { padding: 22px 20px; }
  .register__box { padding: 24px 20px; }
}

@media (max-height: 500px) and (max-width: 900px) {
  .nav { position: static; }
  .landing section[id] { scroll-margin-top: 24px; }
}

/* ── Reduced motion ──────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .btn, .btn__arrow, .text-link span, .nav__links a, .nav__cta { transition: none; }
}
</style>
`````

