import { defineStore } from 'pinia'
import axios from '@/utils/axios'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false,
    isLoading: false
  }),

  actions: {
    async login(credentials) {
      this.isLoading = true
      try {
        // First, get CSRF token
        await axios.get('/api/auth/csrf/')
        
        // Then login
        const response = await axios.post('/api/auth/login/', credentials)
        const { token, user } = response.data
        
        this.token = token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        
        await router.push('/dashboard')
        return response.data
      } catch (error) {
        console.error('Login error:', error.response?.data || error.message)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async register(credentials) {
      this.isLoading = true
      try {
        const response = await axios.post('/auth/register/', credentials)
        const { token, user } = response.data
        
        this.token = token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        
        await router.push('/dashboard')
        return response.data
      } catch (error) {
        console.error('Registration error:', error.response?.data || error.message)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      try {
        await axios.post('/auth/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = null
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
        await router.push('/login')
      }
    },

    init() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
      }
    },

    async checkAuth() {
      try {
        const response = await fetch('/api/auth/user/', {
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          this.user = data.user
          this.isAuthenticated = true
        } else {
          this.user = null
          this.isAuthenticated = false
        }
      } catch (error) {
        console.error('Check auth error:', error)  // Debug log
        this.user = null
        this.isAuthenticated = false
      } finally {
        this.isLoading = false
      }
    },

    getCookie(name) {
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    }
  }
})
