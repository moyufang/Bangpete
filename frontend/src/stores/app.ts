import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {

  const theme = ref<'light' | 'dark'>('light')
  const sidebarCollapsed = ref(false)

  const isDark = computed(() => theme.value === 'dark')

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  //State
  return {theme, isDark, toggleTheme}
})