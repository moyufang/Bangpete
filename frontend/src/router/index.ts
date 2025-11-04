// src/router/index.ts
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

// 定义路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Lobby',
    component: () => import('@/pages/Lobby.vue') // 懒加载
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router