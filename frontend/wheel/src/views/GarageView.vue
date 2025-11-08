<template>
  <div class="page-container">
    <h2>My Garage</h2>
    <div v-if="store.likedCars.length === 0" class="empty-state">
      <p>You haven't liked any cars yet.</p>
      <router-link to="/swipe" class="cta-button">Start Swiping</router-link>
    </div>
    <div v-else class="garage-grid">
      <router-link 
        v-for="car in store.likedCars" 
        :key="car.id" 
        :to="'/details/' + car.id" 
        class="car-card"
      >
        <img :src="car.img" class="car-image" />
        <div class="car-info">
          <strong>{{ car.year }} {{ car.model }}</strong>
          <span>${{ car.price.toLocaleString() }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useCarStore } from '@/store'
const store = useCarStore()
</script>

<style scoped>
.page-container {
  padding: 1rem;
  text-align: center;
}
.empty-state {
  margin-top: 5rem;
}
.cta-button {
  display: inline-block;
  background-color: #EB0A1E; /* Toyota Red */
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  margin-top: 1rem;
}
.garage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.car-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  text-decoration: none;
  color: #333;
}
.car-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
.car-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.car-info strong {
  font-size: 1.1rem;
}
</style>