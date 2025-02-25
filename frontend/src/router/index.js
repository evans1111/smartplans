import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import PlanCreateView from '@/views/PlanCreateView.vue'
import SettingsView from '../views/SettingsView.vue'
import PlansView from '@/views/PlansView.vue'
import PlanDetailView from '@/views/PlanDetailView.vue'

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
    path: '/plans',
    name: 'plans',
    component: PlansView,
    meta: { requiresAuth: true }
  },
  {
    path: '/plans/:id',
    name: 'plan-detail',
    component: PlanDetailView,
    props: true,
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
  history: createWebHistory(),  // Remove the base path
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth store if needed
  if (!authStore.initialized) {
    await authStore.init()
  }

  // Handle protected routes
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Handle guest-only routes (login, register)
  if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }

  next()
})

export default router
