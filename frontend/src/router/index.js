import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Schedule from '../views/Schedule.vue'
import Staff from '../views/Staff.vue'
import Map from '../views/Map.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule
  },
  {
    path: '/staff',
    name: 'Staff',
    component: Staff
  },
  {
    path: '/map',
    name: 'Map',
    component: Map
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
