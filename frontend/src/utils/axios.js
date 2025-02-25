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

// Initialize with token from localStorage (at module load time)
const initToken = localStorage.getItem('token')
if (initToken) {
  instance.defaults.headers.common['Authorization'] = `Token ${initToken}`
  console.log('Initialized axios with token from localStorage')
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

// Function to make authenticated requests - use this instead of axios directly
export async function authRequest(method, url, data = null) {
  // Get the latest token
  const token = localStorage.getItem('token')
  if (!token) {
    console.error('No token available for auth request')
    throw new Error('Authentication required')
  }
  
  // Prepare headers with token
  const headers = {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  }
  
  // Add CSRF token for non-GET requests
  if (method.toLowerCase() !== 'get') {
    const csrfToken = getCsrfToken()
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken
    }
  }
  
  console.log(`Making authenticated ${method.toUpperCase()} request to ${url} with token`)
  
  try {
    // Use axios instance but with explicit headers
    const response = await instance({
      method,
      url,
      data,
      headers
    })
    return response
  } catch (error) {
    console.error('Auth request failed:', {
      url,
      status: error.response?.status,
      data: error.response?.data
    })
    
    // Handle auth errors
    if (error.response?.status === 401 || error.response?.status === 403) {
      console.error('Authentication failed, redirecting to login')
      // Only redirect if not already at login
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
    }
    
    throw error
  }
}

// Add request interceptor
instance.interceptors.request.use(
  config => {
    // Get token from localStorage (in case it changed after module initialization)
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
      console.log('Adding token to request:', config.url)
    } else {
      console.warn('No token found for request:', config.url)
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
    
    // Log the full request
    console.log('Request details:', {
      url: `${config.baseURL}${config.url}`,
      method: config.method,
      headers: config.headers,
      withCredentials: config.withCredentials
    })
    
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

// Utility function to help debugging
export function updateAuthToken(token) {
  if (token) {
    instance.defaults.headers.common['Authorization'] = `Token ${token}`
    console.log('Token updated in axios instance')
  } else {
    delete instance.defaults.headers.common['Authorization']
    console.log('Token removed from axios instance')
  }
}

export default instance
