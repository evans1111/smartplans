<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/common/Navbar.vue'
import Footer from './components/common/Footer.vue'
</script>

<template>
  <div class="app-wrapper">
    <Navbar />
    <main class="container">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<style>
:root {
  --dark-bg: #121212;
  --darker-bg: #0a0a0a;
  --dark-card: #1e1e1e;
  --dark-border: #333;
  --dark-text: #e1e1e1;
  --dark-secondary: #888;
  --primary: #4F46E5;
  --primary-hover: #4338CA;
  --primary-light: rgba(79, 70, 229, 0.1);
  --success: #059669;
  --danger: #DC2626;
}

/* Global styles */
html, body {
  background-color: var(--dark-bg);
  color: var(--dark-text);
  min-height: 100vh;
}

/* Bulma overrides for dark mode */
.section {
  background-color: var(--dark-bg);
  padding: 3rem 1.5rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.box {
  background-color: var(--dark-card);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
}

.title {
  color: var(--dark-text) !important;
}

.subtitle {
  color: var(--dark-secondary) !important;
}

/* Button styles */
.button {
  background-color: var(--dark-card);
  border-color: var(--dark-border);
  color: var(--dark-text);
  transition: all 0.3s ease;
  height: auto;
  padding: 1rem 1.5rem;
}

.button:hover {
  border-color: var(--primary);
  color: var(--dark-text);
}

.button.is-primary {
  background-color: var(--primary);
  border-color: transparent;
  color: white;
}

.button.is-primary:hover {
  background-color: var(--primary-hover);
}

/* Form elements */
.input, 
.textarea, 
.select select,
.select:not(.is-multiple):not(.is-loading)::after {
  background-color: var(--darker-bg);
  border-color: var(--dark-border);
  color: var(--dark-text);
  min-height: 3rem;
  padding: 0.75rem 1rem;
  width: 100%;
  border-radius: 8px;
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: var(--dark-text);
}

.input:focus, 
.textarea:focus, 
.select select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.125em rgba(79, 70, 229, 0.25);
}

.select:not(.is-multiple):not(.is-loading):hover::after {
  border-color: var(--primary);
}

/* Card styles */
.card {
  background-color: var(--dark-card);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-header {
  border-bottom: 1px solid var(--dark-border);
  padding-bottom: 1rem;
}

.card-content {
  padding: 1.5rem 0;
}

/* Navigation */
.navbar {
  background-color: var(--darker-bg) !important;
  border-bottom: 1px solid var(--dark-border);
}

.navbar-item {
  color: var(--dark-text) !important;
}

.navbar-item:hover {
  background-color: var(--primary-light) !important;
  color: var(--primary) !important;
}

.navbar-link {
  color: var(--dark-text) !important;
  background-color: var(--darker-bg) !important;
}

.navbar-link:hover {
  color: var(--primary) !important;
}

.navbar-dropdown {
  background-color: var(--dark-card) !important;
  border: 1px solid var(--dark-border) !important;
  border-radius: 6px !important;
}

/* Tags */
.tags .tag {
  background-color: var(--dark-card);
  color: var(--dark-text);
  border: 1px solid var(--dark-border);
  padding: 0.75rem 1rem;
  height: auto;
  font-size: 0.9rem;
}

.tags .tag.is-primary {
  background-color: var(--primary);
  color: white;
  border: none;
}

/* Tables */
.table {
  background-color: var(--dark-card);
  color: var(--dark-text);
}

.table th,
.table td {
  border-color: var(--dark-border);
}

.table.is-striped tbody tr:not(.is-selected):nth-child(even) {
  background-color: var(--darker-bg);
}

/* Notifications */
.notification {
  background-color: var(--dark-card);
  color: var(--dark-text);
}

/* Menu lists */
.menu-list a {
  color: var(--dark-text);
}

.menu-list a:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}

/* Pagination */
.pagination-link {
  background-color: var(--dark-card);
  border-color: var(--dark-border);
  color: var(--dark-text);
}

.pagination-link.is-current {
  background-color: var(--primary);
  border-color: var(--primary);
}

/* Modal */
.modal-card {
  background-color: var(--dark-card);
}

.modal-card-head,
.modal-card-foot {
  background-color: var(--darker-bg);
  border-color: var(--dark-border);
}

/* Dropdown */
.dropdown-content {
  background-color: var(--dark-card);
  border: 1px solid var(--dark-border);
}

.dropdown-item {
  color: var(--dark-text);
}

.dropdown-item:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}

.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 2rem;
}

/* Form improvements */
.input::placeholder,
.textarea::placeholder,
.select select::placeholder {
  color: var(--dark-secondary);
  opacity: 0.7;
}

.label {
  color: var(--dark-text);
  margin-bottom: 0.5rem;
}
</style>
