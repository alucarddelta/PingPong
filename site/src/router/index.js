import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/service/:id',
    name: 'Service',
    component: () => import(/* webpackChunkName: "Service" */ '../views/Service.vue')
  },
  {
    path: '/config/services',
    name: 'Config_Services',
    component: () => import(/* webpackChunkName: "Config_Service" */ '../views/Config_services.vue')
  },
  {
    path: '/config/heartbeat',
    name: 'Config_Heartbeat',
    component: () => import(/* webpackChunkName: "Config_Service" */ '../views/Config_heartbeat.vue')
  },
  {
    path: '/config/server',
    name: 'Config_server',
    component: () => import(/* webpackChunkName: "Config_Service" */ '../views/Config_server.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

