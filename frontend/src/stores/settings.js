import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    profile: null,
    isLoading: false,
    error: null
  }),

  actions: {
    async fetchSettings() {
      this.isLoading = true
      try {
        const response = await fetch('/api/auth/settings/', {
          credentials: 'include'
        })
        if (!response.ok) throw new Error('Failed to fetch settings')
        const data = await response.json()
        this.profile = data
      } catch (error) {
        console.error('Fetch settings error:', error)
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },

    async saveSettings(settings) {
      this.isLoading = true
      try {
        const response = await fetch('/api/auth/settings/', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          credentials: 'include',
          body: JSON.stringify(settings)
        })
        
        if (!response.ok) throw new Error('Failed to save settings')
        const data = await response.json()
        this.profile = data
        return data
      } catch (error) {
        console.error('Save settings error:', error)
        this.error = error.message
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async uploadLogo(file) {
      const formData = new FormData()
      formData.append('logo', file)

      try {
        const response = await fetch('/api/auth/settings/', {
          method: 'PUT',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          credentials: 'include',
          body: formData
        })
        
        if (!response.ok) throw new Error('Failed to upload logo')
        const data = await response.json()
        this.profile = data
        return data
      } catch (error) {
        console.error('Logo upload error:', error)
        throw error
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
