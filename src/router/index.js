import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/homeview.vue' 
import AuthView from '../views/AuthView.vue'
import StudentDashboardView from '../views/StudentDashboardView.vue'
import EvaluacionView from '../views/EvaluacionView.vue'
import ReporteView from '../views/ReporteView.vue'
import OrientadorDashboardView from '../views/OrientadorDashboardView.vue' // Importación del Mockup 5

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/auth',
      name: 'authentication',
      component: AuthView
    },
    {
      path: '/estudiante/dashboard',
      name: 'estudiante-dashboard',
      component: StudentDashboardView
    },
    {
      path: '/estudiante/evaluacion',
      name: 'estudiante-evaluacion',
      component: EvaluacionView
    },
    {
      path: '/estudiante/reporte',
      name: 'estudiante-reporte',
      component: ReporteView
    },
    {
      path: '/orientador/dashboard',
      name: 'orientador-dashboard',
      component: OrientadorDashboardView // Ruta enlazada al Mockup 5
    }
  ]
})

export default router