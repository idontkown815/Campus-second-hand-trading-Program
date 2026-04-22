import { defineStore } from 'pinia'
import api from '../api'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    currentProduct: null,
    categories: []
  }),

  actions: {
    async fetchProducts(params = {}) {
      const response = await api.getProducts(params)
      this.products = response.data.data
      return this.products
    },

    async fetchProduct(id) {
      const response = await api.getProduct(id)
      this.currentProduct = response.data.data
      return this.currentProduct
    },

    async createProduct(data) {
      const response = await api.createProduct(data)
      return response.data
    },

    async fetchCategories() {
      const response = await api.getCategories()
      this.categories = response.data.data
      return this.categories
    },

    async getMyProducts() {
      const response = await api.getMyProducts()
      this.products = response.data.data
      return response.data
    },

    async takeDownProduct(id) {
      const response = await api.takeDownProduct(id)
      return response.data
    }
  }
})
