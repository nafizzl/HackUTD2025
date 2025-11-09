<template>
  <div class="onboarding-container">
    <h2>What are your 'must-haves'?</h2>
    <div class="toggle-list">
      <div class="toggle-item" @click="store.toggleMustHave('heatedSeats')">
        <label>Heated Seats</label>
        <div :class="['toggle-switch', { active: store.mustHaves.heatedSeats }]">
          <div class="toggle-knob"></div>
        </div>
      </div>
      <div class="toggle-item" @click="store.toggleMustHave('pushToStart')">
        <label>Push to Start</label>
        <div :class="['toggle-switch', { active: store.mustHaves.pushToStart }]">
          <div class="toggle-knob"></div>
        </div>
      </div>
      <div class="toggle-item" @click="store.toggleMustHave('appleCarPlay')">
        <label>Apple CarPlay</label>
        <div :class="['toggle-switch', { active: store.mustHaves.appleCarPlay }]">
          <div class="toggle-knob"></div>
        </div>
      </div>
      <div class="toggle-item" @click="store.toggleMustHave('awd')">
        <label>All-Wheel Drive (AWD)</label>
        <div :class="['toggle-switch', { active: store.mustHaves.awd }]">
          <div class="toggle-knob"></div>
        </div>
      </div>
    </div>
    <router-link to="/swipe" class="next-button">Find My Cars</router-link>
  </div>
</template>

<script setup>
import { useCarStore } from '@/store'
const store = useCarStore()
</script>

<style scoped>
.onboarding-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  box-sizing: border-box;
  text-align: center;
  height: 100vh;
}
.toggle-list {
  width: 100%;
  max-width: 400px;
  margin-top: 2rem;
}
.toggle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 1rem;
  cursor: pointer;
}
.toggle-item label {
  font-weight: 500;
}
.toggle-switch {
  width: 50px;
  height: 28px;
  background-color: #ccc;
  border-radius: 14px;
  position: relative;
  transition: background-color 0.2s;
}
.toggle-switch.active {
  background-color: #EB0A1E; /* Toyota Red */
}
.toggle-knob {
  width: 24px;
  height: 24px;
  background-color: white;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.2s;
}
.toggle-switch.active .toggle-knob {
  transform: translateX(22px);
}
.next-button {
  display: inline-block;
  background-color: #EB0A1E; /* Toyota Red */
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  margin-top: 2rem;
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
  position: absolute;
  bottom: 2rem;
}
</style>