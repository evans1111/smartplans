import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  const isLoading = ref(true)

  const checkAuth = async () => {
    try {
      if (!authStore.isAuthenticated) {
        await authStore.init()
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      if (router.currentRoute.value.meta.requiresAuth) {
        router.push('/login')
      }
    } finally {
      isLoading.value = false
    }
  }

  onMounted(() => {
    checkAuth()
  })

  return {
    isLoading,
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user
  }
} 