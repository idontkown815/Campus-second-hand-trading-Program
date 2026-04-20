<template>
  <div class="product-list-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>校园二手交易平台</h1>
          <div class="header-actions">
            <template v-if="userStore.isLoggedIn">
              <span>欢迎，{{ userStore.user?.name }}</span>
              <el-button @click="handleLogout">退出</el-button>
            </template>
            <template v-else>
              <el-button @click="$router.push('/login')">登录</el-button>
              <el-button type="primary" @click="$router.push('/register')">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>
      <el-main>
        <div class="search-bar">
          <el-input v-model="searchKeyword" placeholder="搜索商品" style="width: 300px" @change="handleSearch">
            <template #append>
              <el-button icon="Search" @click="handleSearch"></el-button>
            </template>
          </el-input>
          <el-button type="primary" @click="goToPublish">发布商品</el-button>
        </div>
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
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const products = ref([])
const searchKeyword = ref('')

const loadProducts = async () => {
  try {
    const response = await api.getProducts()
    products.value = response.data.data || []
  } catch (error) {
    console.error(error)
  }
}

const handleSearch = () => {
  console.log('搜索:', searchKeyword.value)
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

const goToPublish = () => {
  router.push('/product/publish')
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
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

.product-list-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto 20px;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
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
