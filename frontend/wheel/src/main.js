import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router' // Our router

// --- New Imports ---
import { FlashCardsPlugin } from 'vue3-flashcards'
// -------------------

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(FlashCardsPlugin) // Plug in the new flashcards component

app.mount('#app')