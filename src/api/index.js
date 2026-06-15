import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  console.log("=== 请求拦截器 ===")
  console.log(`请求URL: ${config.url}`)
  console.log(`请求方法: ${config.method}`)
  console.log(`Token存在: ${!!token}`)
  console.log(`跳过认证: ${config.skipAuth}`)
  
  // 跳过登录和注册请求的token添加
  if (token && !config.skipAuth) {
    config.headers.Authorization = `Bearer ${token}`
    console.log("已添加Authorization头")
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      const { status, data } = error.response
      const message = data?.message || '请求失败'
      if (status === 401) {
        // 获取当前是否为管理员
        const isAdmin = localStorage.getItem('is_admin') === 'true'
        const adminLoginPath = '/admin/login'
        const userLoginPath = '/login'
        
        // 获取当前路径
        const currentPath = window.location.pathname
        
        // 判断应该跳转到哪个登录页
        const targetLoginPath = isAdmin ? adminLoginPath : userLoginPath
        
        // 如果当前已经在正确的登录页面，不进行重定向
        if (currentPath !== targetLoginPath) {
          ElMessage.error('登录已过期，请重新登录')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('is_admin')
          window.location.href = targetLoginPath
        } else {
          // 在登录页面，直接返回错误，让登录页面处理
          return Promise.reject(error)
        }
      } else {
        ElMessage.error(message)
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default {
  register(data) {
    return api.post('/users/register/', data, { skipAuth: true })
  },
  login(data) {
    return api.post('/users/login/', data, { skipAuth: true })
  },
  getProfile() {
    return api.get('/users/profile/')
  },
  updateProfile(data) {
    return api.put('/users/profile/', data)
  },
  getUsers(params) {
    return api.get('/users/', { params })
  },
  getUser(id) {
    return api.get(`/users/${id}/`)
  },
  updateUser(id, data) {
    return api.put(`/users/${id}/`, data)
  },
  deleteUser(id) {
    return api.delete(`/users/${id}/`)
  },
  getProducts(params) {
    return api.get('/products/', { params, skipAuth: true })
  },
  getProduct(id) {
    return api.get(`/products/${id}/`, { skipAuth: true })
  },
  createProduct(data) {
    return api.post('/products/', data)
  },
  getCategories() {
    return api.get('/products/categories/', { skipAuth: true })
  },
  getMyProducts() {
    return api.get('/products/my_products/')
  },
  takeDownProduct(id) {
    return api.post(`/products/${id}/take_down/`)
  },
  putOnShelf(id) {
    return api.post(`/products/${id}/put_on_shelf/`)
  },
  updateProduct(id, data) {
    return api.put(`/products/${id}/`, data)
  },
  getComments(productId) {
    return api.get('/communications/comments/', { params: { product_id: productId } })
  },
  addComment(data) {
    return api.post('/communications/comments/', data)
  },
  deleteComment(id) {
    return api.delete(`/communications/comments/${id}/`)
  },
  getMessages(conversationId) {
    return api.get('/communications/messages/', { params: { conversation_id: conversationId } })
  },
  sendMessage(conversationId, content) {
    return api.post('/communications/messages/', { conversation_id: conversationId, content })
  },
  getConversations() {
    return api.get('/communications/conversations/')
  },
  createConversation(productId, sellerId, content) {
    return api.post('/communications/conversations/', {
      product_id: productId,
      participant_ids: [sellerId],
      initial_message: content
    })
  },
  markMessagesAsRead(conversationId) {
    return api.post('/communications/messages/mark_read/', { conversation_id: conversationId })
  },
  getUnreadCount() {
    return api.get('/communications/conversations/unread_count/')
  },
  getTransactions() {
    return api.get('/transactions/')
  },
  createTransaction(productId) {
    return api.post('/transactions/', { product_id: productId })
  },
  payTransaction(id, shippingInfo) {
    return api.post(`/transactions/${id}/pay/`, shippingInfo)
  },
  cancelTransaction(id) {
    return api.post(`/transactions/${id}/cancel/`)
  },
  shipTransaction(id) {
    return api.post(`/transactions/${id}/ship/`)
  },
  arriveTransaction(id) {
    return api.post(`/transactions/${id}/arrive/`)
  },
  completeTransaction(id) {
    return api.post(`/transactions/${id}/complete/`)
  },
  refundTransaction(id) {
    return api.post(`/transactions/${id}/refund/`)
  },
  adminReleaseAll() {
    return api.post('/products/admin_release_all/')
  },
  approveProduct(id) {
    return api.post(`/products/${id}/approve/`)
  },
  rejectProduct(id) {
    return api.post(`/products/${id}/reject/`)
  },
  adminTakeDownProduct(id) {
    return api.post(`/products/${id}/admin_take_down/`)
  },
  getAdminProducts() {
    return api.get('/products/admin_products/')
  },
  getAdminStats() {
    return api.get('/products/admin_stats/')
  },
  // 收藏相关API
  getFavorites() {
    return api.get('/communications/favorites/')
  },
  addFavorite(productId) {
    return api.post('/communications/favorites/', { product_id: productId })
  },
  removeFavorite(favoriteId) {
    return api.delete(`/communications/favorites/${favoriteId}/`)
  },
  checkFavorite(productId) {
    return api.get('/communications/favorites/check/', { params: { product_id: productId } })
  },
  // 浏览历史相关API
  getViewHistory() {
    return api.get('/communications/view_history/')
  },
  addViewHistory(productId) {
    return api.post('/communications/view_history/', { product_id: productId })
  },
  deleteViewHistory(id) {
    return api.delete(`/communications/view_history/${id}/`)
  },
  clearViewHistory() {
    return api.delete('/communications/view_history/clear/')
  }
}
