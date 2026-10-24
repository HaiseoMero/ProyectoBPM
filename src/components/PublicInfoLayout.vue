<template>
  <div class="info-page">
    <a class="info-skip" href="#contenido">Ir al contenido</a>
    <nav class="info-nav" aria-label="Navegación principal">
      <router-link to="/" class="info-brand" aria-label="Vócalis, volver al inicio">
        <span class="info-brand__icon" aria-hidden="true">◈</span>
        <span>Vócalis</span>
      </router-link>
      <div class="info-nav__links">
        <router-link to="/como-funciona" :aria-current="route.name === 'como-funciona' ? 'page' : undefined">Cómo funciona</router-link>
        <router-link to="/el-test" :aria-current="route.name === 'el-test' ? 'page' : undefined">El test</router-link>
        <router-link to="/auth" class="info-nav__cta">Comenzar gratis</router-link>
      </div>
    </nav>

    <main id="contenido" tabindex="-1">
      <slot />
    </main>

    <footer class="info-footer">
      <router-link to="/" class="info-brand" aria-label="Vócalis, volver al inicio">
        <span class="info-brand__icon" aria-hidden="true">◈</span>
        <span>Vócalis</span>
      </router-link>
      <p>Proyecto de Título · Ingeniería en Informática · 2026</p>
    </footer>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style src="../styles/public-info.css"></style>
