<template>
    <div class="section">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-4">
            <div class="box">
              <!-- Success message after registration -->
              <div v-if="justRegistered" class="notification is-success">
                Registration successful! Please log in.
              </div>

              <!-- Error message -->
              <div v-if="error" class="notification is-danger">
                <button class="delete" @click="error = ''"></button>
                {{ error }}
              </div>

              <h1 class="title has-text-centered">Sign In</h1>
              <form @submit.prevent="handleLogin">
                <div class="field">
                  <label class="label">Email</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="form.email" 
                      class="input" 
                      :class="{ 'is-danger': errors.email }"
                      type="email" 
                      placeholder="your@email.com"
                      required
                    >
                    <span class="icon is-small is-left">
                      <i class="fas fa-envelope"></i>
                    </span>
                  </div>
                  <p v-if="errors.email" class="help is-danger">{{ errors.email }}</p>
                </div>
                
                <div class="field">
                  <label class="label">Password</label>
                  <div class="control has-icons-left">
                    <input 
                      v-model="form.password" 
                      class="input" 
                      :class="{ 'is-danger': errors.password }"
                      type="password" 
                      placeholder="••••••••"
                      required
                    >
                    <span class="icon is-small is-left">
                      <i class="fas fa-lock"></i>
                    </span>
                  </div>
                  <p v-if="errors.password" class="help is-danger">{{ errors.password }}</p>
                </div>
  
                <div class="field">
                  <div class="control">
                    <button 
                      type="submit"
                      class="button is-primary is-fullwidth"
                      :class="{ 'is-loading': isLoading }"
                      :disabled="isLoading"
                    >
                      Sign In
                    </button>
                  </div>
                </div>
  
                <div class="has-text-centered mt-4">
                  <router-link to="/register">Need an account? Sign up</router-link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  
  const router = useRouter()
  const route = useRoute()
  const authStore = useAuthStore()
  
  const isLoading = ref(false)
  const error = ref('')
  const errors = ref({})
  const justRegistered = ref(false)
  
  const form = ref({
    email: '',
    password: ''
  })
  
  onMounted(() => {
    // Check if user just registered
    justRegistered.value = route.query.registered === 'true'
  })
  
  const validateForm = () => {
    errors.value = {}
    let isValid = true
    
    if (!form.value.email) {
      errors.value.email = 'Email is required'
      isValid = false
    }
    
    if (!form.value.password) {
      errors.value.password = 'Password is required'
      isValid = false
    }
    
    return isValid
  }
  
  const handleLogin = async () => {
    error.value = ''
    if (!validateForm()) return
    
    isLoading.value = true
    try {
      // Debug log
      console.log('Login attempt with:', {
        email: form.value.email,
        password: form.value.password
      })
      
      await authStore.login({
        email: form.value.email,
        password: form.value.password
      })
      
      // If successful, router.push will happen automatically via navigation guard
    } catch (err) {
      console.error('Login error:', err)
      // More specific error handling
      if (err.response?.status === 401) {
        error.value = 'Invalid email or password'
      } else if (err.response?.data?.error) {
        error.value = err.response.data.error
      } else {
        error.value = 'An error occurred during login. Please try again.'
      }
    } finally {
      isLoading.value = false
    }
  }
  </script>