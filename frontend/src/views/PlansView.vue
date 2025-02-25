<template>
  <div class="section">
    <div class="container">
      <div class="plans-header">
        <h1 class="title is-2">My Plans</h1>
        <router-link to="/dashboard" class="button is-primary">
          <span class="icon">
            <i class="fas fa-plus"></i>
          </span>
          <span>Create New Plan</span>
        </router-link>
      </div>

      <div v-if="isLoading" class="loading-container">
        <div class="loader"></div>
        <p>Loading your plans...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <div class="icon">
          <i class="fas fa-exclamation-circle"></i>
        </div>
        <p>{{ error }}</p>
        <button class="button is-primary mt-4" @click="fetchPlans">Try Again</button>
      </div>

      <div v-else-if="plans.length === 0" class="empty-state">
        <div class="icon">
          <i class="fas fa-clipboard"></i>
        </div>
        <h2>No Plans Yet</h2>
        <p>You haven't created any marketing plans yet. Get started by creating your first plan!</p>
        <router-link to="/dashboard" class="button is-primary mt-4">Create Your First Plan</router-link>
      </div>

      <div v-else class="plans-grid">
        <div v-for="plan in plans" :key="plan.id" class="plan-card">
          <div class="plan-card-content">
            <div class="plan-type-badge" :class="plan.plan_type">
              {{ getPlanTypeLabel(plan.plan_type) }}
            </div>
            
            <h3 class="plan-title">{{ plan.title }}</h3>
            
            <div class="plan-details">
              <div class="detail">
                <span class="icon"><i class="fas fa-calendar"></i></span>
                <span>{{ getTimelineLabel(plan.timeline) }}</span>
              </div>
              
              <div class="detail">
                <span class="icon"><i class="fas fa-chart-line"></i></span>
                <span>{{ plan.channels.length }} channels</span>
              </div>
              
              <div class="detail">
                <span class="icon"><i class="fas fa-clock"></i></span>
                <span>Created {{ formatDate(plan.created_at) }}</span>
              </div>
              
              <div class="plan-status">
                <span class="tag" :class="getStatusClass(plan.status)">
                  {{ plan.status.charAt(0).toUpperCase() + plan.status.slice(1) }}
                </span>
              </div>
            </div>
            
            <div class="channels-preview">
              <div v-for="channel in plan.channels" :key="channel" class="channel-tag">
                <span class="icon">
                  <i :class="getChannelIcon(channel)"></i>
                </span>
                <span>{{ getChannelLabel(channel) }}</span>
              </div>
            </div>
          </div>
          
          <div class="plan-actions">
            <button 
              class="button is-info is-outlined" 
              @click="viewPlan(plan.id)"
              :disabled="plan.status === 'generating'"
            >
              <span class="icon">
                <i class="fas fa-eye"></i>
              </span>
              <span>View</span>
            </button>
            
            <button 
              class="button is-danger is-outlined" 
              @click="confirmDelete(plan)"
            >
              <span class="icon">
                <i class="fas fa-trash"></i>
              </span>
              <span>Delete</span>
            </button>
          </div>
        </div>
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
          <p>Are you sure you want to delete the plan: <strong>{{ planToDelete?.title }}</strong>?</p>
          <p class="has-text-danger">This action cannot be undone.</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="deletePlan" :class="{'is-loading': isDeleting}">Delete</button>
          <button class="button" @click="cancelDelete">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePlansStore } from '@/stores/plans'

const router = useRouter()
const plansStore = usePlansStore()

const plans = computed(() => plansStore.plans)
const isLoading = computed(() => plansStore.isLoading)
const error = computed(() => plansStore.error)

const showDeleteModal = ref(false)
const planToDelete = ref(null)
const isDeleting = ref(false)

// Fetch plans on component mount
onMounted(async () => {
  try {
    await fetchPlans()
  } catch (error) {
    console.error('Error fetching plans:', error)
  }
})

async function fetchPlans() {
  try {
    await plansStore.fetchPlans()
  } catch (error) {
    console.error('Error fetching plans:', error)
  }
}

// Navigation
function viewPlan(planId) {
  router.push(`/plans/${planId}`)
}

// Delete functionality
function confirmDelete(plan) {
  planToDelete.value = plan
  showDeleteModal.value = true
}

function cancelDelete() {
  planToDelete.value = null
  showDeleteModal.value = false
}

async function deletePlan() {
  if (!planToDelete.value) return
  
  isDeleting.value = true
  try {
    await plansStore.deletePlan(planToDelete.value.id)
    showDeleteModal.value = false
    planToDelete.value = null
  } catch (error) {
    console.error('Error deleting plan:', error)
  } finally {
    isDeleting.value = false
  }
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
.plans-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.plan-card {
  background-color: var(--dark-card);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.plan-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  border-color: var(--primary);
}

.plan-card-content {
  padding: 1.5rem;
  flex: 1;
}

.plan-type-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.plan-type-badge.past-clients {
  background-color: rgba(79, 70, 229, 0.2);
  color: var(--primary);
}

.plan-type-badge.open-house {
  background-color: rgba(5, 150, 105, 0.2);
  color: var(--success);
}

.plan-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--dark-text);
}

.plan-details {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.detail {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--dark-secondary);
  font-size: 0.9rem;
}

.detail .icon {
  color: var(--primary);
  font-size: 0.9rem;
}

.plan-status {
  margin-left: auto;
}

.channels-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.channel-tag {
  background-color: var(--darker-bg);
  border-radius: 20px;
  padding: 0.3rem 0.75rem;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.channel-tag .icon {
  font-size: 0.8rem;
  color: var(--primary);
}

.plan-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background-color: var(--darker-bg);
  border-top: 1px solid var(--dark-border);
}

/* Loading state */
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

/* Empty state */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background-color: var(--dark-card);
  border-radius: 12px;
  border: 1px dashed var(--dark-border);
}

.empty-state .icon {
  font-size: 3rem;
  color: var(--dark-secondary);
  margin-bottom: 1rem;
}

.empty-state h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--dark-text);
}

.empty-state p {
  color: var(--dark-secondary);
  max-width: 500px;
  margin: 0 auto;
}

/* Error state */
.error-message {
  text-align: center;
  padding: 3rem 2rem;
  background-color: var(--dark-card);
  border-radius: 12px;
  border: 1px solid var(--danger);
}

.error-message .icon {
  font-size: 2.5rem;
  color: var(--danger);
  margin-bottom: 1rem;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .plans-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .plans-grid {
    grid-template-columns: 1fr;
  }
  
  .plan-details {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .plan-status {
    margin-left: 0;
    margin-top: 0.5rem;
  }
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
</style> 