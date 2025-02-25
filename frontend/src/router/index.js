import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import PlanCreateView from '@/views/PlanCreateView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/plan/create/:type',
    name: 'plan-create',
    component: PlanCreateView,
    props: true,
    meta: { requiresAuth: true }
  }
  // We'll add these back later when we create the components
  // {
  //   path: '/templates',
  //   name: 'templates',
  //   component: TemplatesView,
  //   meta: { requiresAuth: true }
  // },
  // {
  //   path: '/generator/:templateId?',
  //   name: 'generator',
  //   component: GeneratorView,
  //   meta: { requiresAuth: true }
  // }
]

const router = createRouter({
  history: createWebHistory('/'),  // Simplified base URL
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path)
  console.log('Route params:', to.params)
  
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
