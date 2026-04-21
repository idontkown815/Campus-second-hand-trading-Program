import { defineStore } from 'pinia'
import api from '../api'
import router from '../router'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isLoggedIn: !!localStorage.getItem('access_token')
  }),

  actions: {
    async register(data) {
      const response = await api.register(data)
      return response.data
    },

    async login(student_id, password) {
      const response = await api.login({ student_id, password })
      const { access, refresh, user } = response.data.data
      this.token = access
      this.user = user
      this.isLoggedIn = true
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      return response.data
    },

    async getProfile() {
      const response = await api.getProfile()
      this.user = response.data.data
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
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/')
    }
  }
})
