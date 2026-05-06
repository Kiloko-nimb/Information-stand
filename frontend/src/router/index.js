import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Schedule from '../views/Schedule.vue'
import Staff from '../views/Staff.vue'
import Map from '../views/Map.vue'
import Quiz from '../views/Quiz.vue'
import Faq from '../views/Faq.vue'
import AdminLogin from '../views/admin/Login.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'

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
    path: '/faq',
    name: 'Faq',
    component: Faq
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
