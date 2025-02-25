import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

// Remove or comment out this line if it exists
// import 'bulma/css/bulma.min.css'

// Remove or comment out this line since we don't have this file yet
// import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast, {
  position: "top-right",
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false
})

app.mount('#app')
