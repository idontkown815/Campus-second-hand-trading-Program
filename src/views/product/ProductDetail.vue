<template>
  <div class="product-detail-container">
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
        <div class="product-detail" v-if="product">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-carousel :interval="5000" type="card" height="400px">
                <el-carousel-item v-for="(image, index) in product.images" :key="index">
                  <img :src="image" class="carousel-image" />
                </el-carousel-item>
              </el-carousel>
            </el-col>
            <el-col :span="12">
              <h2>{{ product.title }}</h2>
              <p class="price">¥{{ product.price }}</p>
              <el-divider></el-divider>
              <div class="info-item">
                <span class="label">分类：</span>
                <span>{{ product.category }}</span>
              </div>
              <div class="info-item">
                <span class="label">校区：</span>
                <span>{{ product.campus_location }}</span>
              </div>
              <div class="info-item">
                <span class="label">楼栋：</span>
                <span>{{ product.building_location }}</span>
              </div>
              <div class="info-item">
                <span class="label">卖家：</span>
                <span>{{ product.seller }}</span>
              </div>
              <div class="info-item">
                <span class="label">发布时间：</span>
                <span>{{ formatDate(product.created_at) }}</span>
              </div>
              <el-divider></el-divider>
              <el-button type="primary" @click="contactSeller" style="width: 100%">
                联系卖家
              </el-button>
            </el-col>
          </el-row>
          <el-card class="description-card" style="margin-top: 20px;">
            <template #header>
              <h3>商品描述</h3>
            </template>
            <p>{{ product.description }}</p>
          </el-card>
        </div>
        <el-empty v-else description="商品不存在"></el-empty>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const product = ref(null)

const loadProduct = async () => {
  const id = route.params.id
  try {
    const response = await api.getProduct(id)
    product.value = response.data.data
  } catch (error) {
    console.error(error)
  }
}

const contactSeller = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  console.log('联系卖家', product.value.seller)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
}

onMounted(() => {
  loadProduct()
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

.product-detail-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.product-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.carousel-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.price {
  color: #f56c6c;
  font-size: 28px;
  font-weight: bold;
  margin: 20px 0;
}

.info-item {
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  margin-right: 10px;
}

.description-card {
  margin-top: 20px;
}
</style>
