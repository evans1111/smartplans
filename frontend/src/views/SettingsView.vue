<template>
  <div class="settings">
    <div class="section">
      <div class="settings-content">
        <h1 class="title is-2 mb-6">Settings</h1>

        <div class="tabs-wrapper">
          <div class="tabs is-boxed is-left mb-5">
            <ul>
              <li :class="{ 'is-active': activeTab === 'profile' }">
                <a @click="setActiveTab('profile')">
                  <span class="icon"><i class="fas fa-user"></i></span>
                  <span>Profile</span>
                </a>
              </li>
              <li :class="{ 'is-active': activeTab === 'business' }">
                <a @click="setActiveTab('business')">
                  <span class="icon"><i class="fas fa-building"></i></span>
                  <span>Business Info</span>
                </a>
              </li>
              <li :class="{ 'is-active': activeTab === 'social' }">
                <a @click="setActiveTab('social')">
                  <span class="icon"><i class="fas fa-share-alt"></i></span>
                  <span>Social Media</span>
                </a>
              </li>
              <li :class="{ 'is-active': activeTab === 'branding' }">
                <a @click="setActiveTab('branding')">
                  <span class="icon"><i class="fas fa-paint-brush"></i></span>
                  <span>Branding</span>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Profile Tab -->
        <div v-show="activeTab === 'profile'" class="box settings-box">
          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input 
                class="input" 
                type="email" 
                v-model="profileData.email" 
                placeholder="Your email"
              >
            </div>
          </div>

          <div class="field">
            <label class="label">Current Password</label>
            <div class="control">
              <input 
                class="input" 
                type="password" 
                v-model="profileData.currentPassword"
                placeholder="Enter current password"
              >
            </div>
          </div>

          <div class="field">
            <label class="label">New Password</label>
            <div class="control">
              <input 
                class="input" 
                type="password" 
                v-model="profileData.newPassword"
                placeholder="Enter new password"
              >
            </div>
          </div>

          <div class="field mt-5">
            <div class="control">
              <button 
                class="button is-primary" 
                @click="saveProfile"
                :class="{ 'is-loading': isLoading }"
              >
                Save Profile Changes
              </button>
            </div>
          </div>
        </div>

        <!-- Business Info Tab -->
        <div v-show="activeTab === 'business'" class="box settings-box">
          <div class="field">
            <label class="label">Business Name</label>
            <div class="control">
              <input 
                class="input" 
                type="text" 
                v-model="businessData.name"
                placeholder="Your business name"
              >
            </div>
          </div>

          <div class="field">
            <label class="label">Business Phone</label>
            <div class="control">
              <input 
                class="input" 
                type="tel" 
                v-model="businessData.phone"
                placeholder="Your business phone number"
              >
            </div>
          </div>

          <div class="field">
            <label class="label">Business Address</label>
            <div class="control">
              <input 
                class="input mb-2" 
                type="text" 
                v-model="businessData.address.street"
                placeholder="Street address"
              >
              <div class="columns is-mobile">
                <div class="column is-6">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="businessData.address.city"
                    placeholder="City"
                  >
                </div>
                <div class="column is-3">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="businessData.address.state"
                    placeholder="State"
                  >
                </div>
                <div class="column is-3">
                  <input 
                    class="input" 
                    type="text" 
                    v-model="businessData.address.zip"
                    placeholder="ZIP"
                  >
                </div>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Target Market</label>
            <div class="control">
              <textarea 
                class="textarea" 
                v-model="businessData.targetMarket"
                placeholder="Describe your ideal clients and target market (e.g., first-time homebuyers, luxury property investors, etc.)"
              ></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Unique Value Proposition</label>
            <div class="control">
              <textarea 
                class="textarea" 
                v-model="businessData.valueProposition"
                placeholder="What makes your real estate services unique? What special value do you provide to clients?"
              ></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Additional Context</label>
            <div class="control">
              <textarea 
                class="textarea" 
                v-model="businessData.additionalContext"
                placeholder="Any additional information about your business that would help in creating marketing plans (e.g., specialties, achievements, preferred marketing approaches)"
              ></textarea>
            </div>
          </div>

          <div class="field mt-5">
            <div class="control">
              <button 
                class="button is-primary" 
                @click="saveBusinessInfo"
                :class="{ 'is-loading': isLoading }"
              >
                Save Business Info
              </button>
            </div>
          </div>
        </div>

        <!-- Social Media Tab -->
        <div v-show="activeTab === 'social'" class="box settings-box">
          <div class="field">
            <label class="label">Instagram</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.instagram"
                placeholder="Your Instagram profile URL"
              >
              <span class="icon is-left">
                <i class="fab fa-instagram"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">Facebook</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.facebook"
                placeholder="Your Facebook profile or page URL"
              >
              <span class="icon is-left">
                <i class="fab fa-facebook"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">TikTok</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.tiktok"
                placeholder="Your TikTok profile URL"
              >
              <span class="icon is-left">
                <i class="fab fa-tiktok"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">LinkedIn</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.linkedin"
                placeholder="Your LinkedIn profile URL"
              >
              <span class="icon is-left">
                <i class="fab fa-linkedin"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">YouTube</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.youtube"
                placeholder="Your YouTube channel URL"
              >
              <span class="icon is-left">
                <i class="fab fa-youtube"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">X (Twitter)</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.twitter"
                placeholder="Your X (Twitter) profile URL"
              >
              <span class="icon is-left">
                <i class="fab fa-x-twitter"></i>
              </span>
            </div>
          </div>

          <div class="field">
            <label class="label">Threads</label>
            <div class="control has-icons-left">
              <input 
                class="input" 
                type="text" 
                v-model="socialData.threads"
                placeholder="Your Threads profile URL"
              >
              <span class="icon is-left">
                <i class="fab fa-threads"></i>
              </span>
            </div>
          </div>

          <div class="field mt-5">
            <div class="control">
              <button 
                class="button is-primary" 
                @click="saveSocialMedia"
                :class="{ 'is-loading': isLoading }"
              >
                Save Social Media
              </button>
            </div>
          </div>
        </div>

        <!-- Branding Tab -->
        <div v-show="activeTab === 'branding'" class="box settings-box">
          <h2 class="title is-4 mb-4">Brand Identity</h2>

          <div class="field">
            <label class="label">Brand Colors</label>
            <div class="columns">
              <div class="column is-6">
                <div class="color-field">
                  <label class="sublabel">Primary Color</label>
                  <div class="color-picker-wrapper">
                    <input 
                      type="color" 
                      v-model="brandingData.primaryColor"
                      class="color-input"
                    >
                    <input 
                      type="text" 
                      v-model="brandingData.primaryColor"
                      class="input color-text"
                      placeholder="#000000"
                    >
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="color-field">
                  <label class="sublabel">Secondary Color</label>
                  <div class="color-picker-wrapper">
                    <input 
                      type="color" 
                      v-model="brandingData.secondaryColor"
                      class="color-input"
                    >
                    <input 
                      type="text" 
                      v-model="brandingData.secondaryColor"
                      class="input color-text"
                      placeholder="#FFFFFF"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Brand Voice</label>
            <div class="control">
              <div class="select is-fullwidth">
                <select v-model="brandingData.brandVoice">
                  <option value="professional">Professional & Formal</option>
                  <option value="friendly">Friendly & Approachable</option>
                  <option value="luxury">Luxury & Sophisticated</option>
                  <option value="modern">Modern & Dynamic</option>
                  <option value="traditional">Traditional & Trustworthy</option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Brand Description</label>
            <div class="control">
              <textarea 
                class="textarea" 
                v-model="brandingData.brandDescription"
                placeholder="Describe your brand's personality, values, and the impression you want to make"
                rows="4"
              ></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Logo</label>
            <div class="file has-name is-fullwidth">
              <label class="file-label">
                <input class="file-input" type="file" @change="handleLogoUpload" accept="image/*">
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label">
                    Choose a file...
                  </span>
                </span>
                <span class="file-name">
                  {{ logoFileName || 'No file selected' }}
                </span>
              </label>
            </div>
          </div>

          <div class="field mt-5">
            <div class="control">
              <button 
                class="button is-primary" 
                @click="saveBranding"
                :class="{ 'is-loading': isLoading }"
              >
                Save Brand Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import axios from '@/utils/axios'

const authStore = useAuthStore()
const toast = useToast()
const activeTab = ref('profile')
const isLoading = ref(false)
const logoFileName = ref('')

// Initialize all data objects with default values
const profileData = ref({
  email: '',
  currentPassword: '',
  newPassword: ''
})

const businessData = ref({
  name: '',
  phone: '',
  address: {
    street: '',
    city: '',
    state: '',
    zip: ''
  },
  targetMarket: '',
  valueProposition: '',
  additionalContext: ''
})

const socialData = ref({
  instagram: '',
  facebook: '',
  tiktok: '',
  linkedin: '',
  youtube: '',
  twitter: '',
  threads: ''
})

const brandingData = ref({
  primaryColor: '#000000',
  secondaryColor: '#ffffff',
  brandVoice: 'professional',
  brandDescription: '',
  logo: null
})

const setActiveTab = (tab) => {
  activeTab.value = tab
}

const handleLogoUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    logoFileName.value = file.name
    brandingData.value.logo = file
  }
}

const loadUserData = async () => {
  try {
    const response = await axios.get('/api/users/settings/')
    const data = response.data
    console.log('Loaded user data:', data)
    
    // Profile data
    profileData.value = {
      email: data.email || '',
      currentPassword: '',
      newPassword: ''
    }
    
    // Business data
    businessData.value = {
      name: data.business_info?.name || '',
      phone: data.business_info?.phone || '',
      address: data.business_info?.address || {
        street: '',
        city: '',
        state: '',
        zip: ''
      },
      targetMarket: data.business_info?.target_market || '',
      valueProposition: data.business_info?.value_proposition || '',
      additionalContext: data.business_info?.additional_context || ''
    }
    
    // Social media data
    socialData.value = {
      instagram: data.social_media?.instagram || '',
      facebook: data.social_media?.facebook || '',
      tiktok: data.social_media?.tiktok || '',
      linkedin: data.social_media?.linkedin || '',
      youtube: data.social_media?.youtube || '',
      twitter: data.social_media?.twitter || '',
      threads: data.social_media?.threads || ''
    }
    
    // Branding data
    brandingData.value = {
      primaryColor: data.branding?.primary_color || '#000000',
      secondaryColor: data.branding?.secondary_color || '#ffffff',
      brandVoice: data.branding?.brand_voice || 'professional',
      brandDescription: data.branding?.brand_description || '',
      logo: data.branding?.logo || null
    }
  } catch (error) {
    console.error('Error loading user data:', error)
    toast.error('Failed to load user data')
  }
}

const saveProfile = async () => {
  isLoading.value = true
  try {
    await axios.put('/api/users/profile/', profileData.value)
    toast.success('Profile updated successfully')
  } catch (error) {
    console.error('Error saving profile:', error)
    toast.error('Failed to update profile')
  } finally {
    isLoading.value = false
  }
}

const saveBusinessInfo = async () => {
  isLoading.value = true
  try {
    const response = await axios.put('/api/users/settings/', {
      business: {
        name: businessData.value.name,
        phone: businessData.value.phone,
        address: businessData.value.address,
        target_market: businessData.value.targetMarket,
        value_proposition: businessData.value.valueProposition,
        additional_context: businessData.value.additionalContext
      }
    })
    console.log('Business info saved:', response.data)
    toast.success('Business information updated successfully')
    await loadUserData()
  } catch (error) {
    console.error('Error saving business info:', error)
    toast.error('Failed to update business information')
  } finally {
    isLoading.value = false
  }
}

const saveSocialMedia = async () => {
  isLoading.value = true
  try {
    const response = await axios.put('/api/users/settings/', {
      social: socialData.value
    })
    console.log('Social media saved:', response.data)
    toast.success('Social media links updated successfully')
    await loadUserData()
  } catch (error) {
    console.error('Error saving social media:', error)
    toast.error('Failed to update social media links')
  } finally {
    isLoading.value = false
  }
}

const saveBranding = async () => {
  isLoading.value = true
  try {
    const formData = new FormData()
    formData.append('branding', JSON.stringify({
      primaryColor: brandingData.value.primaryColor,
      secondaryColor: brandingData.value.secondaryColor,
      brandVoice: brandingData.value.brandVoice,
      brandDescription: brandingData.value.brandDescription
    }))
    
    if (brandingData.value.logo instanceof File) {
      formData.append('logo', brandingData.value.logo)
    }
    
    const response = await axios.put('/api/users/settings/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log('Branding saved:', response.data)
    toast.success('Branding updated successfully')
    await loadUserData()
  } catch (error) {
    console.error('Error saving branding:', error)
    toast.error('Failed to update branding')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.settings {
  min-height: 100vh;
  background-color: var(--dark-bg);
}

.settings-content {
  max-width: 800px;
  margin: 0 auto;
}

.settings-box {
  position: relative;
  overflow: visible;
  border: 1px solid var(--dark-border);
  background-color: var(--dark-card);
}

.tabs-wrapper {
  border-bottom: none;
}

.tabs.is-boxed {
  margin-bottom: 2rem;
}

.tabs.is-left ul {
  justify-content: flex-start;
  border-bottom-color: var(--dark-border);
}

.tabs.is-boxed li.is-active a {
  background-color: var(--dark-card);
  border-color: var(--dark-border);
  border-bottom-color: transparent;
  color: var(--primary);
}

.tabs.is-boxed a {
  border-color: var(--dark-border);
  color: var(--dark-text);
}

.tabs.is-boxed a:hover {
  background-color: var(--dark-card);
  border-color: var(--dark-border);
  color: var(--primary);
}

.label {
  color: var(--dark-text);
  margin-bottom: 0.5rem;
}

.input,
.textarea {
  background-color: var(--darker-bg);
  border-color: var(--dark-border);
  color: var(--dark-text);
}

.input::placeholder,
.textarea::placeholder {
  color: var(--dark-secondary);
  opacity: 0.7;
}

.icon.is-left {
  color: var(--dark-secondary);
}

.field {
  margin-bottom: 1.5rem;
}

@media screen and (max-width: 768px) {
  .settings-content {
    padding: 0 1rem;
  }
  
  .tabs ul {
    flex-wrap: wrap;
  }
}

.color-field {
  margin-bottom: 1.5rem;
}

.sublabel {
  display: block;
  font-size: 0.875rem;
  color: var(--dark-text);
  margin-bottom: 0.5rem;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.color-input {
  width: 50px;
  height: 40px;
  padding: 0;
  border: 1px solid var(--dark-border);
  border-radius: 6px;
  cursor: pointer;
}

.color-text {
  flex: 1;
  text-transform: uppercase;
}

.select select {
  background-color: var(--darker-bg);
  color: var(--dark-text);
  border-color: var(--dark-border);
  height: 2.5rem;
}

.select:not(.is-multiple):not(.is-loading)::after {
  border-color: var(--dark-text);
}

.textarea {
  min-height: 120px;
}

.field:not(:last-child) {
  margin-bottom: 1.5rem;
}

.title {
  color: var(--dark-text);
}

/* Ensure no overflow from input elements */
.input,
.textarea,
.select,
.color-input {
  z-index: 1;
  position: relative;
}

/* Remove any potential pseudo-elements */
*::before,
*::after {
  display: none !important;
}

.file-cta {
  background-color: var(--dark-card);
  color: var(--dark-text);
  border-color: var(--dark-border);
}

.file-name {
  background-color: var(--darker-bg);
  color: var(--dark-text);
  border-color: var(--dark-border);
}
</style>
