import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/user/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/user/Register.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/user/Profile.vue')
  },
  {
    path: '/my',
    name: 'My',
    component: () => import('../views/My.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/product/ProductList.vue')
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('../views/product/ProductDetail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
