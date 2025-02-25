import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: true
  }),

  actions: {
    async login(email, password) {
      try {
        console.log('Attempting login for:', email)  // Debug log
        
        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          credentials: 'include',
          body: JSON.stringify({ email, password })
        })

        const data = await response.json()
        console.log('Login response:', data)  // Debug log

        if (!response.ok) {
          throw new Error(data.message || 'Login failed')
        }

        this.user = data.user
        this.isAuthenticated = true
        return true
      } catch (error) {
        console.error('Login error:', error)  // Debug log
        throw error
      }
    },

    async logout() {
      try {
        const response = await fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          credentials: 'include'
        })

        if (!response.ok) {
          throw new Error('Logout failed')
        }

        // Clear user data regardless of response
        this.user = null
        this.isAuthenticated = false
      } catch (error) {
        console.error('Logout error:', error)
        // Still clear user data even if the request fails
        this.user = null
        this.isAuthenticated = false
        throw error
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
