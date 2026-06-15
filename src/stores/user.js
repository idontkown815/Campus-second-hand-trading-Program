import { defineStore } from 'pinia'
import api from '../api'
import router from '../router'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isLoggedIn: !!localStorage.getItem('access_token'),
    isAdmin: localStorage.getItem('is_admin') === 'true',
    initialized: false
  }),

  actions: {
    async init() {
      if (this.initialized) return
      
      const token = localStorage.getItem('access_token')
      const isAdminStr = localStorage.getItem('is_admin')
      
      if (token) {
        this.token = token
        this.isLoggedIn = true
        this.isAdmin = isAdminStr === 'true'
        
        try {
          await this.getProfile()
        } catch (error) {
          this.logout()
          return
        }
      }
      
      this.initialized = true
    },
    async register(data) {
      const response = await api.register(data)
      return response.data
    },

    async login(student_id, password) {
      const response = await api.login({ student_id, password })
      const { access, refresh, user, is_admin } = response.data.data
      this.token = access
      this.user = user
      this.isAdmin = is_admin
      this.isLoggedIn = true
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('is_admin', is_admin ? 'true' : 'false')
      return response.data
    },

    async getProfile() {
      const response = await api.getProfile()
      this.user = response.data.data
      this.isAdmin = response.data.data.is_superuser
      localStorage.setItem('is_admin', this.isAdmin ? 'true' : 'false')
      return this.user
    },

    async updateProfile(data) {
      const response = await api.updateProfile({
        grade: data.grade,
        major: data.major
      })
      this.user = response.data.data
      return this.user
    },

    logout() {
      this.token = null
      this.user = null
      this.isLoggedIn = false
      this.isAdmin = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('is_admin')
      router.push('/')
    }
  }
})
