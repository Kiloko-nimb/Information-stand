import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Schedule from '../views/Schedule.vue'
import Staff from '../views/Staff.vue'
import Map from '../views/Map.vue'
import Quiz from '../views/Quiz.vue'
import Honor from '../views/Honor.vue'
import Faq from '../views/Faq.vue'

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
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: Quiz
  },
  {
    path: '/honor',
    name: 'Honor',
    component: Honor
  },
  {
    path: '/faq',
    name: 'Faq',
    component: Faq
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
