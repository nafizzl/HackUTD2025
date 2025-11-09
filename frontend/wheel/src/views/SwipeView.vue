<template>
  <div class="swipe-wrapper">
    <div class="header-bar">
      <router-link to="/" class="header-link">Filters</router-link>
      <router-link to="/garage" class="header-link garage">My Garage</router-link>
    </div>
    
    <div class="tinder-container">
      <FlashCards
        :cards="cars"
        @approve="onLike"
        @reject="onNope"
      >
        <template #default="{ item }">
          <div class="swipe-card">
            <img :src="item.img" class="card-image" />
            <div class="card-info">
              <h3>{{ item.year }} {{ item.make }} {{ item.model }}</h3>
              <p>${{ item.price.toLocaleString() }}</p>
            </div>
          </div>
        </template>

        <template #approve>
          <div class="tinder-label like">LIKE</div>
        </template>
        <template #reject>
          <div class="tinder-label nope">NOPE</div>
        </template>

        <template #empty>
           <div class="no-cars">
            <h3>All out of cars!</h3>
            <p>Try adjusting your budget or filters.</p>
            <router-link to="/" class="cta-button">Edit Filters</router-link>
          </div>
        </template>
      </FlashCards>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCarStore } from '@/store'

const store = useCarStore()

// Get the reactive list of cars from the store
const cars = computed(() => store.carsForSwiping)

// These event handlers are called by the FlashCards component
function onLike(item) {
  store.likeCar(item)
}
function onNope(item) {
  store.nopeCar(item)
}
</script>

<style>
/* We make these global so the FlashCards component can be styled */
.swipe-wrapper {
  padding: 1rem;
  box-sizing: border-box;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.header-link {
  display: inline-block;
  background-color: #eee;
  color: #333;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
}
.header-link.garage {
  background-color: #333;
  color: white;
}

.tinder-container {
  flex-grow: 1;
  position: relative;
  width: 100%;
  max-width: 450px;
  margin: 0 auto;
}

/* This targets the vue3-flashcards component */
.flash-cards {
  width: 100%;
  height: 100%;
}

.swipe-card {
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.card-image {
  width: 100%;
  height: 75%;
  object-fit: cover;
  flex-shrink: 0;
  pointer-events: none; /* Prevents image dragging */
}
.card-info {
  padding: 1rem;
  text-align: left;
}
.card-info h3 {
  margin: 0 0 0.5rem;
}
.card-info p {
  margin: 0;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
}
.tinder-label {
  position: absolute;
  top: 30px;
  font-size: 2rem;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  color: white;
  z-index: 10;
}
.tinder-label.like {
  left: 20px;
  background-color: rgba(0, 128, 0, 0.7);
  transform: rotate(-15deg);
}
.tinder-label.nope {
  right: 20px;
  background-color: rgba(235, 10, 30, 0.7); /* Toyota Red */
  transform: rotate(15deg);
}
.no-cars {
  padding-top: 50%;
  text-align: center;
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
</style>