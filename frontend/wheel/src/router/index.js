import { createRouter, createWebHistory } from 'vue-router'
import BudgetView from '../views/BudgetView.vue'
import MustHavesView from '../views/MustHavesView.vue'
import SwipeView from '../views/SwipeView.vue'
import GarageView from '../views/GarageView.vue'
import DetailsView from '../views/DetailsView.vue'

const routes = [
  {
    path: '/',
    name: 'Budget',
    component: BudgetView
  },
  {
    path: '/musthaves',
    name: 'MustHaves',
    component: MustHavesView
  },
  {
    path: '/swipe',
    name: 'Swipe',
    component: SwipeView
  },
  {
    path: '/garage',
    name: 'Garage',
    component: GarageView
  },
  {
    // The :id part is dynamic, so /details/1 or /details/2 will work
    path: '/details/:id',
    name: 'Details',
    component: DetailsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router