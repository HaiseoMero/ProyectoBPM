/**
 * Divide un texto con marcas **palabra clave** en segmentos para renderizar
 * destacados (<strong class="kw">) sin usar v-html y conservando intacto el
 * texto plano para lectores de pantalla y pruebas automatizadas.
 */
export function parseHighlights(text = '') {
  return String(text)
    .split(/(\*\*[^*]+\*\*)/g)
    .filter(Boolean)
    .map((part) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return { text: part.slice(2, -2), kw: true }
      }
      return { text: part, kw: false }
    })
}
