import axios from 'axios'
import router from '@/router'

// Create axios instance with default config
const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})

// Add token if it exists
const token = localStorage.getItem('token')
if (token) {
  instance.defaults.headers.common['Authorization'] = `Token ${token}`
}

// Function to get CSRF token from cookies
function getCsrfToken() {
  const name = 'csrftoken'
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

// Add request interceptor
instance.interceptors.request.use(
  config => {
    // Get token from localStorage
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    
    // Add CSRF token for non-GET requests
    if (config.method !== 'get') {
      const csrfToken = getCsrfToken()
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }
    
    // Don't set Content-Type for FormData
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    
    // Log the full URL being requested
    console.log('Making request to:', `${config.baseURL}${config.url}`)
    return config
  },
  error => Promise.reject(error)
)

// Add response interceptor for debugging
instance.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      headers: error.config?.headers
    })
    return Promise.reject(error)
  }
)

// Add response interceptor
instance.interceptors.response.use(
  response => response,
  async error => {
    console.error('Response Error:', error.response) // Debug log
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Clear auth data
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete instance.defaults.headers.common['Authorization']
      
      // Only redirect to login if not already there
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default instance
