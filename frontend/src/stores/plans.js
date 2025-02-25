import { defineStore } from 'pinia'
import axios from 'axios'

export const usePlansStore = defineStore('plans', {
  state: () => ({
    plans: [],
    currentPlan: null,
    isLoading: false,
    error: null
  }),

  actions: {
    async fetchPlans() {
      this.isLoading = true
      try {
        const response = await fetch('/api/plans/', {
          credentials: 'include'
        })
        if (!response.ok) throw new Error('Failed to fetch plans')
        const data = await response.json()
        this.plans = data
      } catch (error) {
        console.error('Fetch plans error:', error)
        this.error = error.message
      } finally {
        this.isLoading = false
      }
    },

    async createPlan(planData) {
      try {
        const response = await axios.post('/api/plans/', planData)
        return response.data
      } catch (error) {
        console.error('Error creating plan:', error)
        throw error
      }
    },

    async getPlan(planId) {
      this.isLoading = true
      try {
        const response = await fetch(`/api/plans/${planId}/`, {
          credentials: 'include'
        })
        if (!response.ok) throw new Error('Failed to fetch plan')
        const data = await response.json()
        this.currentPlan = data
        return data
      } catch (error) {
        console.error('Get plan error:', error)
        this.error = error.message
        throw error
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
