import { createRouter, createWebHistory } from 'vue-router'
import index from '../pages/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: index,
    },
    {
      path: '/main',
      name: 'main',
      component: () => import('../pages/main.vue'),
    },
    {
      path: '/introduce',
      name: 'introduce',
      component: () => import('../pages/introduce.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../pages/chat.vue'),
    }
  ],
})

export default router
