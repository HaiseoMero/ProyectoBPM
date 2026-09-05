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
      component: StudentDashboardView,
      meta: { requiresAuth: true, role: 'estudiante' }
    },
    {
      path: '/estudiante/evaluacion',
      name: 'estudiante-evaluacion',
      component: EvaluacionView,
      meta: { requiresAuth: true, role: 'estudiante' }
    },
    {
      path: '/estudiante/reporte',
      name: 'estudiante-reporte',
      component: ReporteView,
      meta: { requiresAuth: true, role: 'estudiante' }
    },
    {
      path: '/orientador/dashboard',
      name: 'orientador-dashboard',
      component: OrientadorDashboardView,
      meta: { requiresAuth: true, role: 'orientador' }
    }
  ]
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('vocalis_token')
  let userRole = null

  if (token) {
    try {
      const payloadBase64 = token.split('.')[1]
      const decodedJson = atob(payloadBase64)
      const payload = JSON.parse(decodedJson)
      userRole = payload.role
      
      // Check if token expired
      if (payload.exp * 1000 < Date.now()) {
        localStorage.removeItem('vocalis_token')
        userRole = null
      }
    } catch (e) {
      localStorage.removeItem('vocalis_token')
    }
  }

  // Si trata de ir a /auth y ya está logueado, redirigir a su dashboard
  if (to.path === '/auth' && userRole) {
    if (userRole === 'orientador') return next('/orientador/dashboard')
    else return next('/estudiante/dashboard')
  }

  // Proteger rutas
  if (to.meta.requiresAuth) {
    if (!userRole) {
      return next('/auth')
    }
    if (to.meta.role && to.meta.role !== userRole) {
      return next('/') // Unauthorized para ese rol
    }
  }

  next()
})

export default router