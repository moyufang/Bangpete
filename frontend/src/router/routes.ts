import { RouteRecordRaw } from 'vue-router'

// 路由定义
export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: {
      title: 'Bangpete',
      requiresAuth: false
    }
  },
]