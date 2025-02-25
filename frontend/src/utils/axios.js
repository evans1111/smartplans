import axios from 'axios'

// Create axios instance with default config
const axiosInstance = axios.create({
  baseURL: '/api/',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCookie('csrftoken')
  },
  withCredentials: true
})

// Function to get CSRF cookie
function getCookie(name) {
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

// Add request interceptor to update CSRF token before each request
axiosInstance.interceptors.request.use(config => {
  config.headers['X-CSRFToken'] = getCookie('csrftoken')
  return config
})

export default axiosInstance
