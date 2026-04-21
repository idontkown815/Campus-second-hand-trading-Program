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
      // 401错误由页面自己处理，不显示全局错误
      if (status !== 401) {
        const message = data?.message || '请求失败'
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
  }
}
