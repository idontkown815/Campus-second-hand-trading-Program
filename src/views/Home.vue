<template>
  <div class="home-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>校园二手交易平台</h1>
          <div class="header-actions">
            <template v-if="userStore.isLoggedIn">
              <span>欢迎，{{ userStore.user?.name }}</span>
              <div class="avatar" @click="goToMy">
                <img v-if="userStore.user?.avatar" :src="userStore.user.avatar" class="avatar-img" />
                <div v-else class="avatar-placeholder">{{ userStore.user?.name?.charAt(0) || 'U' }}</div>
              </div>
              <el-button @click="handleLogout">退出</el-button>
            </template>
            <template v-else>
              <el-button @click="$router.push('/login')">登录</el-button>
              <el-button type="primary" @click="$router.push('/register')">注册</el-button>
              <div class="avatar" @click="$router.push('/my')">
                <div class="avatar-placeholder">U</div>
              </div>
            </template>
          </div>
        </div>
      </el-header>
      <el-main>
        <div class="product-section">
          <h2>最新商品</h2>
          <el-row :gutter="20">
            <el-col :span="8" v-for="product in products" :key="product.id">
              <el-card class="product-card" @click="goToDetail(product.id)">
                <img v-if="product.images && product.images.length" :src="product.images[0]" class="product-image" />
                <div v-else class="product-image placeholder">暂无图片</div>
                <h3>{{ product.title }}</h3>
                <p class="price">¥{{ product.price }}</p>
                <p class="location">{{ product.campus_location }} - {{ product.building_location }}</p>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="!products.length" description="暂无商品"></el-empty>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const products = ref([])

const loadProducts = async () => {
  try {
    const response = await api.getProducts()
    products.value = response.data.data || []
  } catch (error) {
    console.error(error)
  }
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
}

const goToMy = () => {
  router.push('/my')
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-content h1 {
  font-size: 24px;
  color: #667eea;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.avatar {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #667eea;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
}

.home-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.product-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.product-section h2 {
  margin-bottom: 20px;
  color: #333;
}

.product-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.product-image.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eee;
  color: #999;
}

.product-card h3 {
  margin: 10px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
  margin: 5px 0;
}

.location {
  color: #999;
  font-size: 12px;
}
</style>
