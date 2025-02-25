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
        <div class="navbar-end">
          <template v-if="authStore.isAuthenticated">
            <router-link class="navbar-item" to="/dashboard">
              <span class="icon">
                <i class="fas fa-th-large"></i>
              </span>
              <span>Dashboard</span>
            </router-link>
            
            <router-link class="navbar-item" to="/plans">
              <span class="icon">
                <i class="fas fa-clipboard-list"></i>
              </span>
              <span>My Plans</span>
            </router-link>
            
            <router-link class="navbar-item" to="/settings">
              <span class="icon">
                <i class="fas fa-cog"></i>
              </span>
              <span>Settings</span>
            </router-link>
            
            <a class="navbar-item logout" @click="handleLogout">
              <span class="icon">
                <i class="fas fa-sign-out-alt"></i>
              </span>
              <span>Log out</span>
            </a>
            
            <div class="navbar-item user-email">
              <span class="icon">
                <i class="fas fa-user-circle"></i>
              </span>
              <span>{{ authStore.user?.email }}</span>
            </div>
          </template>
          
          <template v-else>
            <router-link to="/login" class="navbar-item">
              <span class="icon">
                <i class="fas fa-sign-in-alt"></i>
              </span>
              <span>Log in</span>
            </router-link>
            
            <router-link to="/register" class="navbar-item sign-up">
              <span class="icon">
                <i class="fas fa-user-plus"></i>
              </span>
              <span>Sign up</span>
            </router-link>
          </template>
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
  padding: 0.5rem 0;
  height: auto;
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  color: var(--dark-text) !important;
  padding: 0.5rem 0;
}

.brand:hover {
  color: var(--primary) !important;
}

.brand .icon {
  color: var(--primary);
  font-size: 1.4rem;
}

/* Menu styles */
.navbar-menu {
  display: flex;
  align-items: center;
}

.navbar-end {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-item {
  color: var(--dark-text);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.navbar-item .icon {
  color: var(--primary);
  font-size: 1.1rem;
}

.navbar-item:hover {
  background-color: var(--dark-card);
  color: var(--primary);
}

/* Special styling for sign-up button */
.sign-up {
  background-color: var(--primary);
  color: white;
}

.sign-up:hover {
  background-color: var(--primary-hover);
  color: white;
}

.sign-up .icon {
  color: white;
}

/* User email display */
.user-email {
  color: var(--dark-secondary);
  font-size: 0.9rem;
  border-left: 1px solid var(--dark-border);
  margin-left: 0.5rem;
  padding-left: 1rem;
}

.logout {
  cursor: pointer;
}

/* Mobile styles */
@media screen and (max-width: 1023px) {
  .navbar-menu.is-active {
    position: absolute;
    left: 0;
    right: 0;
    top: 100%;
    background-color: var(--darker-bg);
    padding: 1rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    border-bottom: 1px solid var(--dark-border);
  }

  .navbar-end {
    flex-direction: column;
    width: 100%;
  }

  .navbar-item {
    width: 100%;
    justify-content: flex-start;
  }

  .user-email {
    border-left: none;
    border-top: 1px solid var(--dark-border);
    margin: 0.5rem 0 0 0;
    padding: 0.5rem 0 0 0;
    width: 100%;
  }
}

/* Burger menu */
.navbar-burger {
  color: var(--dark-text);
  height: 3.5rem;
  width: 3.5rem;
  display: none;
}

@media screen and (max-width: 1023px) {
  .navbar-burger {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 0.3rem;
  }
}

.navbar-burger:hover {
  background-color: var(--dark-card);
}

.navbar-burger span {
  height: 2px;
  width: 16px;
  background-color: currentColor;
  display: block;
}
</style>
