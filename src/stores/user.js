import { defineStore } from 'pinia'
import api from '../api'

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

    async getProfile() {
      const response = await api.getProfile()
      this.user = response.data.data
      return this.user
    },

    logout() {
      this.token = null
      this.user = null
      this.isLoggedIn = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
})
