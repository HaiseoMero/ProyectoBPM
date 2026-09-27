// Estados persistidos por el servicio BPM y los workers, en orden de avance.
export const bpmStages = [
  { state: 'registro', label: 'Registro', statusClass: 'info' },
  { state: 'calculando_ocean', label: 'Calculando perfil', statusClass: 'warning' },
  { state: 'generando_reporte', label: 'Generando reporte', statusClass: 'warning' },
  { state: 'reporte_listo', label: 'Reporte disponible', statusClass: 'success' }
]

export function getBpmStatus(state) {
  return bpmStages.find(step => step.state === state) ?? {
    state: null,
    label: 'Estado no disponible',
    statusClass: 'info'
  }
}
