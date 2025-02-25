<template>
  <div class="section">
    <div class="container">
      <div class="has-text-centered mb-6">
        <h1 class="title is-2">{{ planType === 'past-clients' ? 'Past Clients Plan' : 'Open House Plan' }}</h1>
        <p class="subtitle is-5">Create your customized marketing plan</p>
      </div>

      <div class="columns is-centered">
        <div class="column is-8">
          <!-- Progress Steps -->
          <div class="steps mb-6">
            <div 
              v-for="step in totalSteps" 
              :key="step"
              class="step-item"
              :class="{
                'is-active': currentStep === step,
                'is-completed': currentStep > step
              }"
            >
              <div class="step-marker">{{ step }}</div>
              <div class="step-details">
                <p class="step-title">{{ ['Channels', 'Timeline', 'Review'][step-1] }}</p>
              </div>
            </div>
          </div>

          <!-- Content Box -->
          <div class="box p-6">
            <!-- Step 1: Channels -->
            <div v-if="currentStep === 1">
              <h2 class="title is-4 mb-4">Select Marketing Channels</h2>
              <p class="subtitle is-6 mb-5">Choose the channels you want to include in your campaign</p>
              
              <div class="options-grid">
                <div
                  v-for="channel in channels"
                  :key="channel.value"
                  class="option-card"
                  :class="{ 'is-selected': selectedChannels.includes(channel.value) }"
                  @click="toggleChannel(channel.value)"
                >
                  <span class="icon is-large">
                    <i :class="channel.icon"></i>
                  </span>
                  <h3 class="option-title">{{ channel.label }}</h3>
                  <p class="option-description">{{ channel.description }}</p>
                </div>
              </div>
            </div>

            <!-- Step 2: Timeline -->
            <div v-if="currentStep === 2">
              <h2 class="title is-4 mb-4">Choose Campaign Timeline</h2>
              <p class="subtitle is-6 mb-5">Select the duration for your marketing campaign</p>
              
              <div class="options-grid">
                <div
                  v-for="option in timelineOptions"
                  :key="option.value"
                  class="option-card"
                  :class="{ 'is-selected': selectedTimeline === option.value }"
                  @click="selectedTimeline = option.value"
                >
                  <span class="icon is-large">
                    <i :class="option.icon"></i>
                  </span>
                  <h3 class="option-title">{{ option.label }}</h3>
                  <p class="option-description">{{ option.description }}</p>
                </div>
              </div>
            </div>

            <!-- Step 3: Review -->
            <div v-if="currentStep === 3" class="review-section">
              <h3 class="has-text-weight-bold mb-4">Campaign Overview</h3>
              
              <div class="review-item">
                <span class="icon">
                  <i class="fas fa-bullseye"></i>
                </span>
                <div class="review-item-content">
                  <div class="review-item-title">Campaign Type</div>
                  <div class="review-item-description">
                    {{ planType === 'past-clients' ? 'Past Clients Re-engagement' : 'Open House Marketing' }}
                  </div>
                </div>
              </div>

              <div class="review-item">
                <span class="icon">
                  <i class="fas fa-broadcast-tower"></i>
                </span>
                <div class="review-item-content">
                  <div class="review-item-title">Selected Channels</div>
                  <div class="review-item-description">
                    <div class="tags">
                      <span v-for="channel in selectedChannels" :key="channel" class="tag is-primary is-medium">
                        <span class="icon">
                          <i :class="channels.find(c => c.value === channel).icon"></i>
                        </span>
                        <span>{{ channels.find(c => c.value === channel).label }}</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="review-item">
                <span class="icon">
                  <i class="fas fa-calendar-alt"></i>
                </span>
                <div class="review-item-content">
                  <div class="review-item-title">Campaign Timeline</div>
                  <div class="review-item-description">
                    {{ timelineOptions.find(t => t.value === selectedTimeline).label }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Navigation Buttons -->
            <div class="navigation-buttons">
              <button 
                class="button is-medium" 
                @click="prevStep" 
                v-if="currentStep > 1"
              >
                <span class="icon">
                  <i class="fas fa-arrow-left"></i>
                </span>
                <span>Previous</span>
              </button>
              
              <button 
                class="button is-primary is-medium" 
                @click="nextStep"
                :disabled="!canProceed"
                :class="{ 'is-loading': isLoading }"
              >
                <span>{{ currentStep === totalSteps ? 'Create Plan' : 'Next' }}</span>
                <span class="icon">
                  <i class="fas fa-arrow-right"></i>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePlansStore } from '@/stores/plans'

const route = useRoute()
const router = useRouter()
const plansStore = usePlansStore()

// Add debug logging
console.log('Route params:', route.params)
console.log('Current route:', route.path)

const planType = computed(() => {
  console.log('Plan type:', route.params.type)
  return route.params.type
})
const currentStep = ref(1)
const totalSteps = 3
const isLoaded = ref(false)

const selectedChannels = ref([])
const selectedTimeline = ref('')

const channels = [
  { value: 'email', label: 'Email Campaigns', icon: 'fas fa-envelope', description: 'Automated email sequences' },
  { value: 'voicemail', label: 'Voicemail Drops', icon: 'fas fa-phone', description: 'Personalized voice messages' },
  { value: 'video', label: 'Video Messages', icon: 'fas fa-video', description: 'Engaging video content' },
  { value: 'text', label: 'Text Messages', icon: 'fas fa-comment', description: 'Direct SMS communication' }
]

const timelineOptions = [
  { value: '30days', label: '30-Day Campaign', icon: 'fas fa-calendar-alt', description: 'Short campaign' },
  { value: '60days', label: '60-Day Campaign', icon: 'fas fa-calendar-week', description: 'Medium campaign' },
  { value: '90days', label: '90-Day Campaign', icon: 'fas fa-calendar', description: 'Long campaign' }
]

const canProceed = computed(() => {
  if (currentStep.value === 1) return selectedChannels.value.length > 0
  if (currentStep.value === 2) return selectedTimeline.value !== ''
  return true
})

const toggleChannel = (value) => {
  const index = selectedChannels.value.indexOf(value)
  if (index === -1) {
    selectedChannels.value.push(value)
  } else {
    selectedChannels.value.splice(index, 1)
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const nextStep = async () => {
  if (currentStep.value === totalSteps) {
    try {
      await plansStore.createPlan({
        plan_type: planType.value,
        channels: selectedChannels.value,
        timeline: selectedTimeline.value
      })
      router.push('/dashboard')
    } catch (error) {
      console.error('Failed to create plan:', error)
    }
  } else {
    currentStep.value++
  }
}

onMounted(() => {
  console.log('PlanCreateView mounted')
  // Validate plan type
  const validTypes = ['past-clients', 'open-house']
  if (!validTypes.includes(route.params.type)) {
    console.error('Invalid plan type:', route.params.type)
    router.push('/dashboard')
    return
  }
  isLoaded.value = true
})
</script>

<style scoped>
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.option-card {
  background-color: var(--dark-card);
  padding: 2rem;
  border: 2px solid var(--dark-border);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  height: 100%;
  min-height: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.option-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.option-card.is-selected {
  border-color: var(--primary);
  background-color: var(--primary-light);
}

.option-card .icon {
  font-size: 2.5rem;
  color: var(--primary);
}

.option-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--dark-text);
  margin: 0;
}

.option-description {
  font-size: 0.95rem;
  color: var(--dark-secondary);
  line-height: 1.5;
  margin: 0;
}

/* Progress Steps */
.steps {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin: 3rem 0;
}

.steps::before {
  content: '';
  position: absolute;
  top: 15px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--dark-border);
  z-index: 0;
}

.step-item {
  flex: 1;
  text-align: center;
  position: relative;
}

.step-marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--dark-card);
  border: 2px solid var(--dark-border);
  color: var(--dark-text);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  position: relative;
  z-index: 1;
  font-weight: 600;
}

.step-title {
  font-size: 1rem;
  color: var(--dark-secondary);
  margin-top: 0.5rem;
}

.step-item.is-active .step-marker {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.step-item.is-completed .step-marker {
  background: var(--success);
  border-color: var(--success);
  color: white;
}

/* Review Step */
.review-section {
  background-color: var(--dark-card);
  border-radius: 12px;
  padding: 2rem;
  margin: 1.5rem 0;
}

.review-section h3 {
  color: var(--dark-text);
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--dark-border);
  padding-bottom: 0.5rem;
}

.review-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
}

.review-item .icon {
  color: var(--primary);
  font-size: 1.5rem;
}

.review-item-content {
  flex: 1;
}

.review-item-title {
  font-weight: 600;
  color: var(--dark-text);
  margin-bottom: 0.25rem;
}

.review-item-description {
  color: var(--dark-secondary);
  font-size: 0.95rem;
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--dark-border);
}

.button {
  min-width: 120px;
}
</style>
