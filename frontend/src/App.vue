
<template>
  <div id="app">
    <!-- 背景组件 -->
    <AppBackground
      :image-url="`/src/assets/imgs/app_background.jpg`"
      :fog-intensity="50"
      :whiten-intensity="0"
      :blur="0"
      :brightness="50"
      :gradient-overlay="true"
      :gradient-colors="['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.4)']"
      :parallax="true"
    />
    
    <!-- 应用内容 -->
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import AppBackground from '@/components/AppBackground.vue'

// 视差滚动效果
const handleScroll = () => {
  const scrollY = window.scrollY || window.pageYOffset
  document.documentElement.style.setProperty('--scroll-y', `${scrollY}`)
}

onMounted(() => {
  // 添加滚动监听（用于视差效果）
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  // 移除滚动监听
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss">
// 导入 SCSS 变量
@import '@/styles/variables';

#app {
  position: relative;
  min-height: 100vh;
  height: 100vh;
  width: 100vw;
  
  .app-content {
    position: relative;
    z-index: 1; // 确保内容在背景之上
  }
}

// 全局滚动条样式
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  
  &:hover {
    background: rgba(255, 255, 255, 0.5);
  }
}
</style>