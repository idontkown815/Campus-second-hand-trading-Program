<template>
  <div class="footprint-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <div class="back-btn" @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回</span>
          </div>
          <h1>我的足迹</h1>
          <div class="header-right">
            <el-button 
              v-if="viewHistory.length" 
              type="text" 
              @click="handleClear"
              class="clear-btn">
              清空足迹
            </el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <div v-if="viewHistory.length" class="footprint-list">
          <div class="timeline">
            <div 
              v-for="item in viewHistory" 
              :key="item.id" 
              class="timeline-item"
              @click="goToDetail(item.product.id)"
            >
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <div class="product-card">
                  <img 
                    v-if="item.product.images && item.product.images.length" 
                    :src="item.product.images[0]" 
                    class="product-image" 
                  />
                  <div v-else class="product-image placeholder">暂无图片</div>
                  <div class="product-info">
                    <h3>{{ item.product.title }}</h3>
                    <p class="price">¥{{ item.product.price }}</p>
                    <p class="view-time">{{ formatTime(item.viewed_at) }}</p>
                  </div>
                  <div class="delete-btn" @click.stop="handleDelete(item.id)">
                    <el-icon><Delete /></el-icon>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <el-empty 
          v-else 
          description="暂无浏览记录"
          class="empty-state">
          <template #image>
            <el-icon class="empty-icon"><Clock /></el-icon>
          </template>
          <template #description>
            <p>还没有浏览过商品</p>
            <p class="empty-hint">去逛逛，发现心仪的商品吧</p>
          </template>
          <el-button type="primary" @click="$router.push('/products')">去逛逛</el-button>
        </el-empty>
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
import { ArrowLeft, Delete, Clock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const viewHistory = ref([])
const loading = ref(false)

const loadViewHistory = async () => {
  if (!userStore.isLoggedIn) return
  
  loading.value = true
  try {
    const response = await api.getViewHistory()
    viewHistory.value = response.data.data || []
  } catch (error) {
    console.error('加载浏览历史失败:', error)
  } finally {
    loading.value = false
  }
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条浏览记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await api.deleteViewHistory(id)
    if (response.data.code === 200) {
      ElMessage.success('删除成功')
      viewHistory.value = viewHistory.value.filter(item => item.id !== id)
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '删除失败')
    }
  }
}

const handleClear = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有浏览记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await api.clearViewHistory()
    if (response.data.code === 200) {
      ElMessage.success('清空成功')
      viewHistory.value = []
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '清空失败')
    }
  }
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor(diff / (1000 * 60))
  
  if (minutes < 1) {
    return '刚刚'
  } else if (minutes < 60) {
    return `${minutes}分钟前`
  } else if (hours < 24) {
    return `${hours}小时前`
  } else if (days < 7) {
    return `${days}天前`
  } else {
    return date.toLocaleDateString()
  }
}

onMounted(() => {
  loadViewHistory()
})
</script>

<style scoped>
.footprint-container {
  min-height: 100vh;
  background: #f5f5f5;
}

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
  color: #667eea;
  cursor: pointer;
  font-size: 15px;
}

.header-content h1 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.clear-btn {
  color: #f56c6c;
  font-size: 14px;
}

.timeline {
  padding: 20px;
}

.timeline-item {
  display: flex;
  position: relative;
  padding-bottom: 20px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-dot {
  width: 10px;
  height: 10px;
  background: #667eea;
  border-radius: 50%;
  margin-right: 15px;
  margin-top: 20px;
  flex-shrink: 0;
}

.timeline-content {
  flex: 1;
}

.product-card {
  background: #fff;
  border-radius: 12px;
  padding: 15px;
  display: flex;
  gap: 15px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.product-image.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #999;
  font-size: 12px;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-info h3 {
  margin: 0;
  font-size: 15px;
  font-weight: bold;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price {
  margin: 5px 0;
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}

.view-time {
  margin: 0;
  font-size: 13px;
  color: #999;
}

.delete-btn {
  padding: 8px;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;
}

.delete-btn:hover {
  color: #f56c6c;
}

.empty-state {
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  color: #ccc;
}

.empty-hint {
  font-size: 13px;
  color: #999;
  margin-top: 5px;
}
</style>