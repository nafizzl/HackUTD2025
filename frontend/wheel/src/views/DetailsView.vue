<template>
  <div class="page-container" v-if="car">
    <router-link to="/garage" class="back-link">&lt; Back to Garage</router-link>
    <img :src="car.img" class="hero-image" />
    <h1>{{ car.year }} {{ car.make }} {{ car.model }}</h1>
    <div class="price-tag">${{ car.price.toLocaleString() }}</div>
    <p class="description">{{ car.description }}</p>
    <h3>Key Features</h3>
    <ul class="features-list">
      <li v-for="feature in car.features" :key="feature">{{ feature }}</li>
    </ul>
    <a href="#" class="cta-button">Check Financing</a>
  </div>
  <div v-else class="page-container">
    <h2>Car not found.</h2>
    <router-link to="/garage" class="back-link">Back to Garage</router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCarStore } from '@/store'
import { useRoute } from 'vue-router'

const store = useCarStore()
const route = useRoute()

// Get the car ID from the URL and find the car in the store
const car = computed(() => {
  return store.getCarById(parseInt(route.params.id, 10))
})
</script>

<style scoped>
.page-container {
  padding: 1rem;
}
.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #0066cc;
  text-decoration: none;
  font-weight: 500;
}
.hero-image {
  width: 100%;
  border-radius: 8px;
}
h1 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}
.price-tag {
  font-size: 1.5rem;
  font-weight: bold;
  color: #EB0A1E; /* Toyota Red */
  margin-bottom: 1rem;
}
.description {
  font-size: 1.1rem;
  line-height: 1.6;
}
.features-list {
  padding-left: 20px;
}
.features-list li {
  margin-bottom: 0.5rem;
}
.cta-button {
  display: block;
  width: 100%;
  background-color: #EB0A1E; /* Toyota Red */
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  text-align: center;
  margin-top: 2rem;
  box-sizing: border-box;
}
</style>