import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
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
        ElMessage.error('登录已过期，请重新登录')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
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
    return api.post('/users/register/', data)
  },
  login(data) {
    return api.post('/users/login/', data)
  },
  getProfile() {
    return api.get('/users/profile/')
  },
  updateProfile(data) {
    return api.put('/users/profile/', data)
  },
  getProducts(params) {
    return api.get('/products/', { params })
  },
  getProduct(id) {
    return api.get(`/products/${id}/`)
  },
  createProduct(data) {
    return api.post('/products/', data)
  },
  getCategories() {
    return api.get('/products/categories/')
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
  getTransactions() {
    return api.get('/transactions/')
  },
  createTransaction(productId) {
    return api.post('/transactions/', { product_id: productId })
  },
  payTransaction(id) {
    return api.post(`/transactions/${id}/pay/`)
  },
  cancelTransaction(id) {
    return api.post(`/transactions/${id}/cancel/`)
  },
  shipTransaction(id) {
    return api.post(`/transactions/${id}/ship/`)
  },
  completeTransaction(id) {
    return api.post(`/transactions/${id}/complete/`)
  },
  refundTransaction(id) {
    return api.post(`/transactions/${id}/refund/`)
  }
}
