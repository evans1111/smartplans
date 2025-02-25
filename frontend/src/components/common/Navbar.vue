<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-content">
      <div class="navbar-brand">
        <router-link class="navbar-item brand" to="/">
          <span class="icon">
            <i class="fas fa-chart-line"></i>
          </span>
          <strong>SmartPlan</strong>
        </router-link>

        <a role="button" 
           class="navbar-burger" 
           aria-label="menu" 
           aria-expanded="false" 
           :class="{ 'is-active': isMenuOpen }" 
           @click="toggleMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" :class="{ 'is-active': isMenuOpen }">
        <div class="navbar-start">
          <template v-if="authStore.isAuthenticated">
            <router-link class="navbar-item nav-link" to="/dashboard">
              Dashboard
            </router-link>
          </template>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="!authStore.isAuthenticated">
                <router-link to="/register" class="button is-primary">
                  <strong>Sign up</strong>
                </router-link>
                <router-link to="/login" class="button">
                  Log in
                </router-link>
              </template>
              <template v-else>
                <div class="navbar-item has-dropdown is-hoverable">
                  <a class="navbar-link">
                    {{ authStore.user?.email }}
                  </a>
                  <div class="navbar-dropdown is-right">
                    <router-link to="/settings" class="navbar-item">
                      <span class="icon">
                        <i class="fas fa-cog"></i>
                      </span>
                      <span>Settings</span>
                    </router-link>
                    <hr class="navbar-divider">
                    <a class="navbar-item" @click="handleLogout">
                      <span class="icon">
                        <i class="fas fa-sign-out-alt"></i>
                      </span>
                      <span>Log out</span>
                    </a>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/')
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>

<style scoped>
.navbar {
  background-color: var(--darker-bg);
  border-bottom: 1px solid var(--dark-border);
  padding: 1rem 0;
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  width: 100%;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  color: var(--dark-text) !important;
}

.brand:hover {
  color: var(--primary) !important;
}

.brand .icon {
  color: var(--primary);
}

.navbar-menu {
  background-color: var(--darker-bg);
}

.navbar-menu.is-active {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid var(--dark-border);
}

.navbar-item {
  color: var(--dark-text);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-item:hover {
  background-color: var(--dark-card) !important;
  color: var(--primary) !important;
}

.navbar-link {
  color: var(--dark-text) !important;
  background-color: transparent !important;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.navbar-link:hover {
  color: var(--primary) !important;
  background-color: var(--dark-card) !important;
}

.navbar-dropdown {
  background-color: var(--dark-card);
  border: 1px solid var(--dark-border);
  border-radius: 8px;
  padding: 0.5rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.navbar-dropdown .navbar-item {
  padding: 0.75rem 1rem;
  border-radius: 6px;
}

.navbar-divider {
  background-color: var(--dark-border);
  margin: 0.5rem 0;
}

.button {
  background-color: var(--dark-card);
  border-color: var(--dark-border);
  color: var(--dark-text);
  transition: all 0.3s ease;
}

.button:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.button.is-primary {
  background-color: var(--primary);
  border-color: transparent;
  color: white;
}

.button.is-primary:hover {
  background-color: var(--primary-hover);
  color: white;
}

.navbar-burger {
  color: var(--dark-text);
}

.navbar-burger:hover {
  background-color: var(--dark-card);
}

.navbar-burger span {
  background-color: currentColor;
}

@media screen and (max-width: 1023px) {
  .navbar-menu {
    padding: 1rem;
  }
  
  .navbar-item {
    padding: 0.75rem;
  }
  
  .buttons {
    padding: 0.5rem 0;
  }
}

.nav-link {
  color: var(--dark-text);
  background: none !important;
  padding: 0.5rem 1rem;
}

.nav-link:hover {
  color: var(--primary) !important;
  background: none !important;
}
</style>
