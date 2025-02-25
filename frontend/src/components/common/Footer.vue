<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="columns">
        <div class="column is-4">
          <div class="brand-section">
            <h3 class="footer-title">
              <span class="icon">
                <i class="fas fa-chart-line"></i>
              </span>
              SmartPlan
            </h3>
            <p class="footer-description">
              AI-Powered Real Estate Marketing Plans that help you grow your business and connect with clients.
            </p>
            <div class="social-links">
              <a href="#" class="social-link" aria-label="Twitter">
                <i class="fab fa-twitter"></i>
              </a>
              <a href="#" class="social-link" aria-label="LinkedIn">
                <i class="fab fa-linkedin"></i>
              </a>
              <a href="#" class="social-link" aria-label="Instagram">
                <i class="fab fa-instagram"></i>
              </a>
            </div>
          </div>
        </div>

        <div class="column is-2">
          <h4 class="footer-subtitle">Product</h4>
          <ul class="footer-links">
            <li><router-link to="/features">Features</router-link></li>
            <li><router-link to="/pricing">Pricing</router-link></li>
            <li><a href="#" @click.prevent="openDocs">Documentation</a></li>
            <li><a href="#" @click.prevent="openGuides">Guides</a></li>
          </ul>
        </div>

        <div class="column is-2">
          <h4 class="footer-subtitle">Company</h4>
          <ul class="footer-links">
            <li><router-link to="/about">About Us</router-link></li>
            <li><router-link to="/contact">Contact</router-link></li>
            <li><a href="#" @click.prevent="openCareers">Careers</a></li>
            <li><a href="#" @click.prevent="openBlog">Blog</a></li>
          </ul>
        </div>

        <div class="column is-4">
          <h4 class="footer-subtitle">Stay Updated</h4>
          <p class="newsletter-text">Get the latest updates and marketing tips straight to your inbox.</p>
          <div class="newsletter-form">
            <div class="field has-addons">
              <div class="control is-expanded">
                <input 
                  class="input" 
                  type="email" 
                  placeholder="Enter your email"
                  v-model="emailInput"
                >
              </div>
              <div class="control">
                <button 
                  class="button is-primary"
                  @click="subscribeNewsletter"
                  :class="{ 'is-loading': isSubscribing }"
                >
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="legal-links">
          <a href="#" @click.prevent="openPrivacy">Privacy Policy</a>
          <span class="separator">•</span>
          <a href="#" @click.prevent="openTerms">Terms of Service</a>
          <span class="separator">•</span>
          <a href="#" @click.prevent="openCookies">Cookie Policy</a>
        </div>
        <p class="copyright">
          © {{ new Date().getFullYear() }} SmartPlan. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const emailInput = ref('')
const isSubscribing = ref(false)

const subscribeNewsletter = async () => {
  if (!emailInput.value) return
  
  isSubscribing.value = true
  try {
    // Implement newsletter subscription
    await new Promise(resolve => setTimeout(resolve, 1000))
    emailInput.value = ''
    // Show success message
  } catch (error) {
    // Handle error
  } finally {
    isSubscribing.value = false
  }
}

// Placeholder functions for footer links
const openDocs = () => console.log('Open docs')
const openGuides = () => console.log('Open guides')
const openCareers = () => console.log('Open careers')
const openBlog = () => console.log('Open blog')
const openPrivacy = () => console.log('Open privacy')
const openTerms = () => console.log('Open terms')
const openCookies = () => console.log('Open cookies')
</script>

<style scoped>
.footer {
  background-color: var(--darker-bg);
  border-top: 1px solid var(--dark-border);
  padding: 4rem 1.5rem 2rem;
  color: var(--dark-text);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
}

.brand-section {
  margin-bottom: 2rem;
}

.footer-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--dark-text);
}

.footer-title .icon {
  color: var(--primary);
}

.footer-description {
  color: var(--dark-secondary);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  color: var(--dark-secondary);
  font-size: 1.25rem;
  transition: color 0.2s ease;
}

.social-link:hover {
  color: var(--primary);
}

.footer-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  color: var(--dark-text);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-links a {
  color: var(--dark-secondary);
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: var(--primary);
}

.newsletter-text {
  color: var(--dark-secondary);
  margin-bottom: 1rem;
}

.newsletter-form .input {
  background-color: var(--dark-bg);
  border-color: var(--dark-border);
  color: var(--dark-text);
}

.newsletter-form .input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.125em rgba(79, 70, 229, 0.25);
}

.newsletter-form .button {
  border-color: var(--primary);
}

.footer-bottom {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid var(--dark-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.legal-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.legal-links a {
  color: var(--dark-secondary);
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.legal-links a:hover {
  color: var(--primary);
}

.separator {
  color: var(--dark-border);
}

.copyright {
  color: var(--dark-secondary);
  font-size: 0.9rem;
}

@media screen and (max-width: 768px) {
  .footer {
    padding: 3rem 1rem 1.5rem;
  }

  .footer-bottom {
    flex-direction: column-reverse;
    text-align: center;
  }

  .legal-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .columns {
    margin: 0;
  }

  .column {
    padding: 1rem;
  }
}
</style>
