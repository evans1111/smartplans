import { defineStore } from 'pinia'
import axios, { authRequest } from '@/utils/axios'
import { useAuthStore } from './auth'

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
        console.log('Fetching plans...')
        const response = await authRequest('get', '/api/plans/')
        this.plans = response.data
        console.log('Plans fetched successfully:', this.plans.length)
        return this.plans
      } catch (error) {
        console.error('Fetch plans error:', error.response?.data || error.message)
        this.error = error.message || 'Failed to fetch plans'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async createPlan(planData) {
      this.isLoading = true
      const authStore = useAuthStore()
      
      try {
        if (!authStore.isAuthenticated) {
          console.error('Authentication check failed - user not authenticated')
          throw new Error('User not authenticated')
        }
        
        if (!authStore.token) {
          console.error('No auth token available')
          throw new Error('Authentication token not found')
        }
        
        console.log('Creating plan with data:', planData)
        console.log('Auth status:', {
          isAuthenticated: authStore.isAuthenticated,
          hasToken: !!authStore.token,
          tokenFirstChars: authStore.token ? authStore.token.substring(0, 5) + '...' : 'none'
        })
        
        const response = await authRequest('post', '/api/plans/', planData)
        console.log('Plan created successfully:', response.data)
        
        // Add the new plan to the plans array
        this.plans.unshift(response.data)
        
        return response.data
      } catch (error) {
        console.error('Error creating plan:', error)
        console.error('Error details:', {
          status: error.response?.status,
          data: error.response?.data,
          headers: error.config?.headers
        })
        
        this.error = error.response?.data?.error || error.message || 'Failed to create plan'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async getPlan(planId) {
      this.isLoading = true
      try {
        console.log('Fetching plan details for ID:', planId)
        const response = await authRequest('get', `/api/plans/${planId}/`)
        this.currentPlan = response.data
        console.log('Plan details fetched successfully')
        return response.data
      } catch (error) {
        console.error('Get plan error:', error.response?.data || error.message)
        this.error = error.message || 'Failed to fetch plan details'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async deletePlan(planId) {
      this.isLoading = true
      try {
        console.log('Deleting plan with ID:', planId)
        await authRequest('delete', `/api/plans/${planId}/`)
        
        // Remove the deleted plan from the plans array
        this.plans = this.plans.filter(plan => plan.id !== planId)
        
        // Clear currentPlan if it was the deleted plan
        if (this.currentPlan && this.currentPlan.id === planId) {
          this.currentPlan = null
        }
        
        console.log('Plan deleted successfully')
        return true
      } catch (error) {
        console.error('Delete plan error:', error.response?.data || error.message)
        this.error = error.message || 'Failed to delete the plan'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // Helper method to check authentication before making requests
    checkAuth() {
      const authStore = useAuthStore()
      if (!authStore.isAuthenticated || !authStore.token) {
        console.error('Authentication check failed', {
          isAuthenticated: authStore.isAuthenticated,
          hasToken: !!authStore.token
        })
        
        // Force navigation to login
        throw new Error('Authentication required')
      }
      
      return true
    }
  }
})
