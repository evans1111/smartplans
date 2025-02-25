<template>
  <div class="section">
    <div class="container">
      <!-- Loading State -->
      <div v-if="isLoading" class="loading-container">
        <div class="loader"></div>
        <p>Loading plan details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <div class="icon">
          <i class="fas fa-exclamation-circle"></i>
        </div>
        <p>{{ error }}</p>
        <div class="buttons is-centered mt-4">
          <button class="button is-primary" @click="fetchPlanDetails">Try Again</button>
          <router-link to="/plans" class="button is-light">Back to Plans</router-link>
        </div>
      </div>

      <!-- Plan Details -->
      <div v-else-if="plan" class="plan-details-container">
        <!-- Header with Actions -->
        <div class="plan-header">
          <div class="plan-header-left">
            <router-link to="/plans" class="back-link">
              <span class="icon">
                <i class="fas fa-arrow-left"></i>
              </span>
              <span>Back to Plans</span>
            </router-link>
            <div class="plan-type-badge" :class="plan.plan_type">
              {{ getPlanTypeLabel(plan.plan_type) }}
            </div>
          </div>
          <div class="plan-header-actions">
            <button class="button is-light" @click="copyPlanToClipboard">
              <span class="icon">
                <i class="fas fa-copy"></i>
              </span>
              <span>Copy</span>
            </button>
            
            <button class="button is-danger is-outlined" @click="confirmDelete">
              <span class="icon">
                <i class="fas fa-trash"></i>
              </span>
              <span>Delete</span>
            </button>
          </div>
        </div>

        <!-- Plan Title Section -->
        <div class="plan-title-section">
          <h1 class="title is-1">{{ plan.title }}</h1>
          <div class="plan-meta">
            <div class="plan-meta-item">
              <span class="icon"><i class="fas fa-calendar"></i></span>
              <span>{{ getTimelineLabel(plan.timeline) }}</span>
            </div>
            <div class="plan-meta-item">
              <span class="icon"><i class="fas fa-clock"></i></span>
              <span>Created {{ formatDate(plan.created_at) }}</span>
            </div>
            <div class="plan-meta-item">
              <span class="tag" :class="getStatusClass(plan.status)">
                {{ plan.status.charAt(0).toUpperCase() + plan.status.slice(1) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Channel Pills Section -->
        <div class="channels-section">
          <h3 class="subtitle is-5">Marketing Channels</h3>
          <div class="channels-list">
            <div v-for="channel in plan.channels" :key="channel" class="channel-pill">
              <span class="icon">
                <i :class="getChannelIcon(channel)"></i>
              </span>
              <span>{{ getChannelLabel(channel) }}</span>
            </div>
          </div>
        </div>

        <!-- Plan Content Sections -->
        <div v-if="plan.content" class="plan-content">
          <div v-for="(section, index) in parsedContent" :key="index" class="content-section">
            <h2 class="section-title">{{ section.title }}</h2>
            <div class="section-content" v-html="formatContent(section.content)"></div>
          </div>
        </div>
        
        <!-- If plan is still generating -->
        <div v-else-if="plan.status === 'generating'" class="generating-state">
          <div class="generating-animation">
            <div class="generating-pulse"></div>
          </div>
          <h3>Your marketing plan is being generated</h3>
          <p>This typically takes 1-2 minutes. The page will refresh automatically when it's ready.</p>
        </div>
        
        <!-- If plan is in error state -->
        <div v-else-if="plan.status === 'failed'" class="failed-state">
          <div class="icon">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <h3>There was a problem generating your plan</h3>
          <p>Please try creating a new plan or contact support if the issue persists.</p>
          <router-link to="/dashboard" class="button is-primary mt-4">Create New Plan</router-link>
        </div>
        
        <!-- If no content but not generating or failed -->
        <div v-else class="empty-content">
          <div class="icon">
            <i class="fas fa-file-alt"></i>
          </div>
          <h3>No content available</h3>
          <p>This plan doesn't have any content yet.</p>
        </div>
      </div>

      <!-- If no plan found -->
      <div v-else class="no-plan-state">
        <div class="icon">
          <i class="fas fa-search"></i>
        </div>
        <h3>Plan Not Found</h3>
        <p>The requested plan could not be found.</p>
        <router-link to="/plans" class="button is-primary mt-4">View All Plans</router-link>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background" @click="cancelDelete"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirm Deletion</p>
          <button class="delete" aria-label="close" @click="cancelDelete"></button>
        </header>
        <section class="modal-card-body">
          <p>Are you sure you want to delete this plan: <strong>{{ plan?.title }}</strong>?</p>
          <p class="has-text-danger">This action cannot be undone.</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="deletePlan" :class="{'is-loading': isDeleting}">Delete</button>
          <button class="button" @click="cancelDelete">Cancel</button>
        </footer>
      </div>
    </div>
    
    <!-- Toast for copy notification -->
    <div class="toast" :class="{ 'is-active': showToast }">
      <div class="notification is-success">
        <span class="icon">
          <i class="fas fa-check"></i>
        </span>
        <span>Plan content copied to clipboard!</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePlansStore } from '@/stores/plans'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const plansStore = usePlansStore()
const toast = useToast()

const plan = computed(() => plansStore.currentPlan)
const isLoading = computed(() => plansStore.isLoading)
const error = computed(() => plansStore.error)

const showDeleteModal = ref(false)
const isDeleting = ref(false)
const showToast = ref(false)

const poller = ref(null)

onMounted(async () => {
  try {
    await fetchPlanDetails()
    
    // If plan is in 'generating' status, poll for updates
    if (plan.value && plan.value.status === 'generating') {
      startPolling()
    }
  } catch (error) {
    console.error('Error loading plan details:', error)
  }
})

onUnmounted(() => {
  if (poller.value) {
    clearInterval(poller.value)
  }
})

async function fetchPlanDetails() {
  try {
    const planId = route.params.id
    if (!planId) {
      throw new Error('No plan ID provided')
    }
    await plansStore.getPlan(planId)
  } catch (error) {
    console.error('Error fetching plan details:', error)
  }
}

// Polling function to check for updates if plan is generating
function startPolling() {
  poller.value = setInterval(async () => {
    try {
      await fetchPlanDetails()
      
      // If plan is no longer generating, stop polling
      if (plan.value && plan.value.status !== 'generating') {
        clearInterval(poller.value)
      }
    } catch (error) {
      console.error('Error while polling for plan updates:', error)
      clearInterval(poller.value)
    }
  }, 10000) // Poll every 10 seconds
}

// Parse the plan content from JSON string if needed
const parsedContent = computed(() => {
  if (!plan.value || !plan.value.content) return []
  
  try {
    // If the content is a string (JSON), parse it
    if (typeof plan.value.content === 'string') {
      return JSON.parse(plan.value.content)
    } 
    // If it's already an object, return it
    return Array.isArray(plan.value.content) ? plan.value.content : [plan.value.content]
  } catch (error) {
    console.error('Error parsing plan content:', error)
    // If parsing fails, return content as a single section
    return [{
      title: 'Plan Details',
      content: plan.value.content
    }]
  }
})

// Format content for display (convert newlines to <br>, etc)
function formatContent(content) {
  if (!content) return ''
  
  // Replace newlines with <br> tags
  let formatted = content.replace(/\n/g, '<br>')
  
  // Convert markdown-like formatting to HTML
  // Bold: **text** to <strong>text</strong>
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // Italic: *text* to <em>text</em>
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Handle lists: - item to <li>item</li>
  if (formatted.includes('\n- ')) {
    formatted = formatted.replace(/\n- (.*?)(?=\n|$)/g, '\n<li>$1</li>')
    formatted = formatted.replace(/(<li>.*?<\/li>)+/g, '<ul>$&</ul>')
  }
  
  return formatted
}

// Delete plan
function confirmDelete() {
  showDeleteModal.value = true
}

function cancelDelete() {
  showDeleteModal.value = false
}

async function deletePlan() {
  if (!plan.value) return
  
  isDeleting.value = true
  try {
    await plansStore.deletePlan(plan.value.id)
    toast.success('Plan deleted successfully')
    router.push('/plans')
  } catch (error) {
    console.error('Error deleting plan:', error)
    toast.error('Failed to delete plan: ' + (error.message || 'Unknown error'))
  } finally {
    isDeleting.value = false
    showDeleteModal.value = false
  }
}

// Copy plan content to clipboard
function copyPlanToClipboard() {
  if (!plan.value) return
  
  let textContent = `${plan.value.title}\n\n`
  
  if (parsedContent.value.length > 0) {
    parsedContent.value.forEach(section => {
      textContent += `${section.title}\n${'='.repeat(section.title.length)}\n\n`
      textContent += `${section.content.replace(/<br\s*\/?>/g, '\n')}\n\n`
    })
  } else if (plan.value.content) {
    textContent += plan.value.content
  }
  
  navigator.clipboard.writeText(textContent)
    .then(() => {
      toast.success('Plan copied to clipboard')
    })
    .catch(err => {
      console.error('Error copying text: ', err)
      toast.error('Failed to copy to clipboard')
    })
}

// Helper functions for display formatting
function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  }).format(date)
}

function getPlanTypeLabel(type) {
  const labels = {
    'past-clients': 'Past Clients',
    'open-house': 'Open House'
  }
  return labels[type] || type
}

function getTimelineLabel(timeline) {
  const labels = {
    '30days': '30 Days',
    '60days': '60 Days',
    '90days': '90 Days'
  }
  return labels[timeline] || timeline
}

function getStatusClass(status) {
  const classes = {
    'draft': 'is-light',
    'generating': 'is-warning',
    'completed': 'is-success',
    'failed': 'is-danger'
  }
  return classes[status] || 'is-light'
}

function getChannelIcon(channel) {
  const icons = {
    'email': 'fas fa-envelope',
    'social': 'fas fa-hashtag',
    'video': 'fas fa-video',
    'text': 'fas fa-comment-alt',
    'voicemail': 'fas fa-phone'
  }
  return icons[channel] || 'fas fa-bullhorn'
}

function getChannelLabel(channel) {
  const labels = {
    'email': 'Email',
    'social': 'Social Media',
    'video': 'Video',
    'text': 'Text',
    'voicemail': 'Voicemail'
  }
  return labels[channel] || channel.charAt(0).toUpperCase() + channel.slice(1)
}
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.loader {
  border: 4px solid rgba(79, 70, 229, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.plan-header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--dark-secondary);
  transition: color 0.2s ease;
}

.back-link:hover {
  color: var(--primary);
}

.plan-type-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.plan-type-badge.past-clients {
  background-color: rgba(79, 70, 229, 0.2);
  color: var(--primary);
}

.plan-type-badge.open-house {
  background-color: rgba(5, 150, 105, 0.2);
  color: var(--success);
}

.plan-header-actions {
  display: flex;
  gap: 0.75rem;
}

.plan-title-section {
  margin-bottom: 2.5rem;
}

.plan-meta {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.75rem;
  align-items: center;
}

.plan-meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--dark-secondary);
}

.plan-meta-item .icon {
  color: var(--primary);
}

.channels-section {
  margin-bottom: 2.5rem;
}

.channels-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.channel-pill {
  background-color: var(--dark-card);
  border-radius: 25px;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.channel-pill .icon {
  color: var(--primary);
}

.plan-content {
  margin-top: 3rem;
}

.content-section {
  background-color: var(--dark-card);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--dark-text);
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--dark-border);
}

.section-content {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--dark-secondary);
}

.generating-state, .failed-state, .empty-content, .no-plan-state, .error-message {
  text-align: center;
  padding: 4rem 2rem;
  background-color: var(--dark-card);
  border-radius: 12px;
  margin-top: 2rem;
}

.generating-animation {
  margin-bottom: 1.5rem;
}

.generating-pulse {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(79, 70, 229, 0.2);
  position: relative;
  margin: 0 auto;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4);
  }
  
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 15px rgba(79, 70, 229, 0);
  }
  
  100% {
    transform: scale(0.95);
  }
}

.failed-state .icon, .empty-content .icon, .no-plan-state .icon, .error-message .icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.failed-state .icon {
  color: var(--danger);
}

.empty-content .icon, .no-plan-state .icon {
  color: var(--dark-secondary);
}

.error-message .icon {
  color: var(--danger);
}

.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  opacity: 0;
  transform: translateY(1rem);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.toast.is-active {
  opacity: 1;
  transform: translateY(0);
}

/* Modal styling */
.modal-card {
  background-color: var(--dark-card);
  color: var(--dark-text);
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-card-head {
  background-color: var(--darker-bg);
  border-bottom: 1px solid var(--dark-border);
  color: var(--dark-text);
}

.modal-card-title {
  color: var(--dark-text);
  font-weight: 600;
}

.modal-card-body {
  background-color: var(--dark-card);
  color: var(--dark-text);
  padding: 1.5rem;
}

.modal-card-foot {
  background-color: var(--darker-bg);
  border-top: 1px solid var(--dark-border);
  justify-content: flex-end;
}

.has-text-danger {
  color: var(--danger) !important;
  margin-top: 0.75rem;
  font-size: 0.9rem;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .plan-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .plan-header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .plan-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .content-section {
    padding: 1.5rem;
  }
}
</style> 