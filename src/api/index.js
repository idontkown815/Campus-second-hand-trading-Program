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
      const { code, message } = error.response.data
      ElMessage.error(message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default {
  register(data) {
    return api.post('/users/register/', data)
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
  }
}
