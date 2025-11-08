<template>
  <div class="onboarding-container">
    <h2>What's your monthly budget?</h2>
    <div class="budget-display">${{ budget }}</div>
    <div class="slider-container">
      <span>$200/mo</span>
      <input
        type="range"
        min="200"
        max="1000"
        :value="budget"
        @input="updateBudget"
        class="slider"
      />
      <span>$1,000/mo</span>
    </div>
    <router-link to="/musthaves" class="next-button">Next</router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCarStore } from '@/store'

const store = useCarStore()

// Use computed property to get and set budget from store
const budget = computed(() => store.budget)

function updateBudget(event) {
  store.setBudget(parseInt(event.target.value, 10))
}
</script>

<style scoped>
.onboarding-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  box-sizing: border-box;
  text-align: center;
}
.budget-display {
  font-size: 3rem;
  font-weight: bold;
  color: #EB0A1E; /* Toyota Red */
  margin: 1rem 0 2rem;
}
.slider-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 400px;
}
.slider-container span {
  font-size: 0.9rem;
  color: #666;
}
.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 10px;
  background: #ddd;
  outline: none;
  border-radius: 5px;
  margin: 0 1rem;
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  background: #EB0A1E; /* Toyota Red */
  cursor: pointer;
  border-radius: 50%;
}
.next-button {
  display: inline-block;
  background-color: #EB0A1E; /* Toyota Red */
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  margin-top: 3rem;
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
}
</style>