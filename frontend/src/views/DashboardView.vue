<template>
  <div class="dashboard">
    <div class="section">
      <div class="dashboard-content">
        <h1 class="title is-2 mb-6">Welcome to SmartPlan</h1>
        <p class="subtitle is-5 mb-6">Choose a marketing plan to get started</p>

        <div class="plan-cards">
          <div class="card plan-card" @click="createPlan('open-house')">
            <div class="card-content">
              <div class="icon-wrapper">
                <span class="icon">
                  <i class="fas fa-home"></i>
                </span>
              </div>
              <h3 class="plan-title">Open House Plan</h3>
              <p class="plan-description">
                Create a comprehensive marketing strategy for your next open house event
              </p>
            </div>
          </div>

          <div class="card plan-card" @click="createPlan('past-clients')">
            <div class="card-content">
              <div class="icon-wrapper">
                <span class="icon">
                  <i class="fas fa-users"></i>
                </span>
              </div>
              <h3 class="plan-title">Past Clients Plan</h3>
              <p class="plan-description">
                Re-engage with past clients and generate referrals through targeted marketing
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const createPlan = (type) => {
  router.push(`/plan/create/${type}`)
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: var(--dark-bg);
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.plan-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.plan-card {
  background-color: var(--dark-card);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.plan-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border-color: var(--primary);
}

.card-content {
  padding: 2.5rem 2rem;
  text-align: center;
}

.icon-wrapper {
  background-color: var(--primary-light);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.icon-wrapper .icon {
  font-size: 2rem;
  color: var(--primary);
}

.plan-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--dark-text);
  margin-bottom: 1rem;
}

.plan-description {
  color: var(--dark-secondary);
  line-height: 1.6;
}

@media screen and (max-width: 768px) {
  .plan-cards {
    grid-template-columns: 1fr;
  }
}
</style>
