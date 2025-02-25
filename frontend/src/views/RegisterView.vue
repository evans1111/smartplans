<template>
  <div class="section">
    <div class="container">
      <div class="columns is-centered">
        <div class="column is-6">
          <div class="box">
            <h1 class="title has-text-centered">Create Your Account</h1>
            
            <!-- Error Alert -->
            <div v-if="error" class="notification is-danger">
              <button class="delete" @click="error = ''"></button>
              {{ error }}
            </div>

            <form @submit.prevent="handleRegister">
              <div class="field">
                <label class="label">Full Name</label>
                <div class="control">
                  <input 
                    v-model="form.fullName" 
                    class="input" 
                    :class="{ 'is-danger': errors.fullName }"
                    type="text" 
                    required
                  >
                </div>
                <p v-if="errors.fullName" class="help is-danger">{{ errors.fullName }}</p>
              </div>

              <div class="field">
                <label class="label">Email</label>
                <div class="control">
                  <input 
                    v-model="form.email" 
                    class="input"
                    :class="{ 'is-danger': errors.email }"
                    type="email" 
                    required
                  >
                </div>
                <p v-if="errors.email" class="help is-danger">{{ errors.email }}</p>
              </div>

              <div class="field">
                <label class="label">Password</label>
                <div class="control">
                  <input 
                    v-model="form.password" 
                    class="input"
                    :class="{ 'is-danger': errors.password }"
                    type="password" 
                    required
                  >
                </div>
                <p v-if="errors.password" class="help is-danger">{{ errors.password }}</p>
              </div>

              <div class="field">
                <label class="label">Confirm Password</label>
                <div class="control">
                  <input 
                    v-model="form.passwordConfirm" 
                    class="input"
                    :class="{ 'is-danger': errors.passwordConfirm }"
                    type="password" 
                    required
                  >
                </div>
                <p v-if="errors.passwordConfirm" class="help is-danger">{{ errors.passwordConfirm }}</p>
              </div>

              <div class="field">
                <div class="control">
                  <button 
                    type="submit"
                    class="button is-primary is-fullwidth"
                    :class="{ 'is-loading': isLoading }"
                    :disabled="isLoading"
                  >
                    Create Account
                  </button>
                </div>
              </div>

              <div class="has-text-centered mt-4">
                Already have an account? 
                <router-link to="/login">Sign in</router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)
const error = ref('')
const errors = ref({})

const form = ref({
  fullName: '',
  email: '',
  password: '',
  passwordConfirm: ''
})

const validateForm = () => {
  errors.value = {}
  let isValid = true
  
  if (!form.value.fullName) {
    errors.value.fullName = 'Name is required'
    isValid = false
  }
  
  if (!form.value.email) {
    errors.value.email = 'Email is required'
    isValid = false
  }
  
  if (form.value.password.length < 8) {
    errors.value.password = 'Password must be at least 8 characters'
    isValid = false
  }
  
  if (form.value.password !== form.value.passwordConfirm) {
    errors.value.passwordConfirm = 'Passwords do not match'
    isValid = false
  }
  
  return isValid
}

const handleRegister = async () => {
  error.value = ''
  if (!validateForm()) return
  
  isLoading.value = true
  try {
    console.log('Sending registration request...')  // Debug log
    
    const response = await fetch('/api/auth/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': authStore.getCookie('csrftoken')
      },
      credentials: 'include',
      body: JSON.stringify({
        name: form.value.fullName,
        email: form.value.email,
        password: form.value.password,
      }),
    })

    const data = await response.json()
    console.log('Registration response:', response.status)  // Debug log
    
    if (response.ok) {
      // Update auth store and redirect
      authStore.user = data.user
      authStore.isAuthenticated = true
      console.log('Registration successful, redirecting to dashboard')  // Debug log
      router.push('/dashboard')
    } else {
      error.value = data.message || 'Registration failed. Please try again.'
    }
  } catch (err) {
    console.error('Registration error:', err)
    error.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
