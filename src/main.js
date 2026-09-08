import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')

// Evitar vulnerabilidad de bfcache: forzar recarga si se vuelve atrás tras logout
window.addEventListener('pageshow', (event) => {
  if (event.persisted && !localStorage.getItem('vocalis_token')) {
    window.location.reload()
  }
})
