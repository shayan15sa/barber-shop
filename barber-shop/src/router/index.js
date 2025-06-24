import { createRouter, createWebHistory } from 'vue-router'

// Import your components/views
import Home from '../views/Home.vue'
import Barbers from '../views/Barbers.vue'
import Hairstyles from '../views/Hairstyles.vue'
import Examples from '../views/Examples.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/barbers', name: 'Barbers', component: Barbers },
  { path: '/hairstyles', name: 'Hairstyles', component: Hairstyles },
  { path: '/examples', name: 'Examples', component: Examples },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
