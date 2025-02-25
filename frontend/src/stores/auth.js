import { defineStore } from 'pinia'
import axios, { updateAuthToken, authRequest } from '@/utils/axios'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
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
        
        console.log('Login successful, token received:', token ? 'Yes' : 'No')
        
        // Update state and localStorage
        this.setAuthData(token, user)
        
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
        const response = await axios.post('/api/auth/register/', credentials)
        const { token, user } = response.data
        
        console.log('Registration successful, token received:', token ? 'Yes' : 'No')
        
        // Update state and localStorage
        this.setAuthData(token, user)
        
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
        await axios.post('/api/auth/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearAuthData()
        await router.push('/login')
      }
    },

    setAuthData(token, user) {
      if (!token) {
        console.error('Attempted to set auth data with null/empty token');
        return;
      }
      
      // Update state
      this.token = token
      this.user = user
      this.isAuthenticated = true
      
      // Update localStorage
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
      
      // Update axios defaults using our utility function
      updateAuthToken(token)
      
      console.log('Auth data set successfully')
    },

    clearAuthData() {
      // Clear state
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      // Clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // Clear axios defaults using our utility function
      updateAuthToken(null)
      
      console.log('Auth data cleared')
    },

    async checkAuth() {
      if (!this.token) {
        console.log('No token available, skipping auth check')
        this.isAuthenticated = false
        return false
      }
      
      try {
        console.log('Checking authentication with token')
        const response = await authRequest('get', '/api/auth/user/')
        
        if (response.status === 200) {
          const { user } = response.data
          this.user = user
          this.isAuthenticated = true
          localStorage.setItem('user', JSON.stringify(user))
          console.log('Authentication verified successfully')
          return true
        } else {
          console.warn('Auth check returned non-200 status:', response.status)
          this.clearAuthData()
          return false
        }
      } catch (error) {
        console.error('Authentication check failed:', error.response?.status)
        this.clearAuthData()
        return false
      } finally {
        this.isLoading = false
      }
    },

    async init() {
      console.log('Initializing auth store')
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')
      
      if (token && user) {
        console.log('Found stored credentials, initializing auth state')
        this.token = token
        this.user = JSON.parse(user)
        this.isAuthenticated = true
        
        // Ensure token is in axios headers
        updateAuthToken(token)
        
        // Verify token is still valid (but don't await it)
        this.checkAuth()
      } else {
        console.log('No stored credentials found')
        this.clearAuthData()
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
