<template>
  <div class="my-favorites-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <div class="back-btn" @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回</span>
          </div>
          <h1>我的收藏</h1>
          <div class="placeholder"></div>
        </div>
      </el-header>
      <el-main>
        <div class="favorites-section">
          <el-row :gutter="20">
            <el-col :span="8" v-for="favorite in favorites" :key="favorite.id">
              <el-card class="product-card" @click="goToDetail(favorite.product.id)">
                <div class="favorite-badge" @click.stop="handleRemoveFavorite(favorite)">
                  <el-icon class="remove-icon"><Delete /></el-icon>
                </div>
                <img v-if="favorite.product.images && favorite.product.images.length" :src="favorite.product.images[0]" class="product-image" />
                <div v-else class="product-image placeholder">暂无图片</div>
                <h3>{{ favorite.product.title }}</h3>
                <p class="price">¥{{ favorite.product.price }}</p>
                <p class="favorited-time">收藏于 {{ formatDate(favorite.created_at) }}</p>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="!favorites.length" description="暂无收藏商品">
            <template #image>
              <el-icon class="empty-icon"><Star /></el-icon>
            </template>
            <el-button type="primary" @click="$router.push('/products')">去逛逛</el-button>
          </el-empty>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Star, Delete } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const favorites = ref([])

const loadFavorites = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    const response = await api.getFavorites()
    if (response.data.code === 200) {
      favorites.value = response.data.data || []
    }
  } catch (error) {
    console.error('加载收藏失败:', error)
    ElMessage.error('加载收藏失败')
  }
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

const handleRemoveFavorite = async (favorite) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏此商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.removeFavorite(favorite.id)
    ElMessage.success('已取消收藏')
    favorites.value = favorites.value.filter(f => f.id !== favorite.id)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消收藏失败')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

onMounted(() => {
  loadFavorites()
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

.back-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  color: #667eea;
  font-size: 16px;
}

.back-btn:hover {
  color: #764ba2;
}

.header-content h1 {
  font-size: 20px;
  color: #333;
}

.placeholder {
  width: 60px;
}

.my-favorites-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.favorites-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.product-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
  position: relative;
}

.product-card:hover {
  transform: translateY(-5px);
}

.favorite-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.product-card:hover .favorite-badge {
  opacity: 1;
}

.remove-icon {
  color: #fff;
  font-size: 16px;
}

.favorite-badge:hover {
  background: #f56c6c;
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

.favorited-time {
  color: #999;
  font-size: 12px;
  margin: 0;
}

.empty-icon {
  font-size: 48px;
  color: #ccc;
}
</style>