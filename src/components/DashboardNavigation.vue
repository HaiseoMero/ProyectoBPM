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
