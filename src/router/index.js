import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

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
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue')
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAdmin: true }
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
  },
  {
    path: '/product/publish',
    name: 'ProductPublish',
    component: () => import('../views/product/ProductPublish.vue')
  },
  {
    path: '/my/products',
    name: 'MyProducts',
    component: () => import('../views/product/MyProducts.vue')
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: () => import('../views/order/OrderList.vue')
  },
  {
    path: '/messages',
    name: 'ChatList',
    component: () => import('../views/chat/ChatList.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAdmin) {
    if (!userStore.isLoggedIn) {
      next('/admin/login')
      return
    }
    if (!userStore.isAdmin) {
      next('/admin/login')
      return
    }
  }

  next()
})

export default router
