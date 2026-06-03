<template>
  <div class="product-detail-container">
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
              <div class="product-status-badge">
                <el-tag v-if="product.status === 'available'" type="success" size="large">在售</el-tag>
                <el-tag v-else-if="product.status === 'locked'" type="warning" size="large">锁定中</el-tag>
                <el-tag v-else-if="product.status === 'sold'" type="danger" size="large">已售出</el-tag>
                <el-tag v-else-if="product.status === 'pending'" type="info" size="large">待审核</el-tag>
                <el-tag v-else type="info" size="large">{{ product.status }}</el-tag>
              </div>
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
              <template v-if="product.status === 'available'">
                <el-button type="primary" @click="handleBuy" style="width: 100%" size="large">
                  立即购买
                </el-button>
              </template>
              <template v-else-if="product.status === 'locked'">
                <div class="lock-info">
                  <el-alert type="warning" :closable="false">
                    <template #title>
                      <p>该商品已被其他用户锁定</p>
                      <p v-if="lockRemainingTime">剩余锁定时间：{{ lockRemainingTime }}</p>
                    </template>
                  </el-alert>
                </div>
              </template>
              <template v-else-if="product.status === 'sold'">
                <el-alert type="info" :closable="false" title="该商品已售出"></el-alert>
              </template>
              <template v-if="currentTransaction && currentTransaction.status === 'pending'">
                <el-divider></el-divider>
                <div class="transaction-panel">
                  <h4>您的购买意向</h4>
                  <el-alert type="warning" :closable="false">
                    <template #title>
                      <p>请在 {{ lockRemainingTime }} 内完成付款</p>
                    </template>
                  </el-alert>
                  <div class="transaction-actions">
                    <el-button type="primary" @click="goToOrder" size="large">去订单页面付款</el-button>
                    <el-button @click="handleCancelTransaction" size="large">取消意向</el-button>
                  </div>
                </div>
              </template>
              <el-button type="default" @click="contactSeller" style="width: 100%; margin-top: 10px">
                联系卖家
              </el-button>
            </el-col>
          </el-row>
          <el-card class="description-card" style="margin-top: 20px;">
            <template #header>
              <div class="description-header">
                <h3>商品描述</h3>
                <el-button 
                  v-if="userStore.isLoggedIn"
                  @click="handleFavorite" 
                  :type="isFavorited ? 'primary' : 'default'"
                  class="favorite-btn"
                  :loading="favoriteLoading">
                  <el-icon><Star :filled="isFavorited" /></el-icon>
                  {{ isFavorited ? '已收藏' : '收藏' }}
                </el-button>
              </div>
            </template>
            <p>{{ product.description }}</p>
          </el-card>
          <ProductComment
            v-if="product.id && product.seller_id"
            :product-id="product.id"
            :product-owner-id="product.seller_id"
          />
        </div>
        <el-empty v-else description="商品不存在"></el-empty>
      </el-main>
    </el-container>

    <ChatWindow
      v-model="chatWindowVisible"
      :conversation-id="chatConversationId"
      :product="product"
      :seller-id="product?.seller_id"
      :seller-name="product?.seller"
      :is-new-conversation="isNewConversation"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import ProductComment from './ProductComment.vue'
import ChatWindow from '../chat/ChatWindow.vue'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const product = ref(null)
const currentTransaction = ref(null)
const lockRemainingTime = ref('')
const chatWindowVisible = ref(false)
const chatConversationId = ref(null)
const isNewConversation = ref(false)
const isFavorited = ref(false)
const favoriteLoading = ref(false)
const favoriteId = ref(null)
let lockTimer = null

const loadProduct = async () => {
  const id = route.params.id
  try {
    const response = await api.getProduct(id)
    product.value = response.data.data
  } catch (error) {
    console.error(error)
  }
}

const loadMyTransaction = async () => {
  if (!userStore.isLoggedIn) return

  try {
    const response = await api.getTransactions()
    const transactions = response.data.data || []
    currentTransaction.value = transactions.find(
      t => t.product_id === product.value?.id && ['pending', 'paid', 'shipped'].includes(t.status)
    )
    updateLockTime()
  } catch (error) {
    console.error('加载交易信息失败:', error)
  }
}

const updateLockTime = () => {
  if (!currentTransaction.value?.locked_until) {
    lockRemainingTime.value = ''
    return
  }

  const remaining = currentTransaction.value.locked_remaining_seconds
  if (remaining <= 0) {
    lockRemainingTime.value = '已过期'
    return
  }

  const hours = Math.floor(remaining / 3600)
  const minutes = Math.floor((remaining % 3600) / 60)
  const seconds = remaining % 60
  lockRemainingTime.value = `${hours}小时${minutes}分${seconds}秒`
}

const startLockTimer = () => {
  if (lockTimer) clearInterval(lockTimer)
  lockTimer = setInterval(() => {
    if (currentTransaction.value) {
      currentTransaction.value.locked_remaining_seconds--
      updateLockTime()
    }
  }, 1000)
}

const contactSeller = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  if (!product.value) {
    ElMessage.error('商品信息未加载')
    return
  }

  if (product.value.seller_id === userStore.user.id) {
    ElMessage.warning('这是您发布的商品')
    return
  }

  try {
    console.log('创建会话参数:', {
      productId: product.value.id,
      sellerId: product.value.seller_id,
      title: product.value.title
    })
    
    const response = await api.createConversation(
      product.value.id,
      product.value.seller_id,
      `您好，我想咨询关于"${product.value.title}"的商品`
    )
    
    console.log('创建会话响应:', response)
    
    if (response.data && (response.data.code === 200 || response.data.code === 201)) {
      chatConversationId.value = response.data.data.id
      isNewConversation.value = true
      chatWindowVisible.value = true
    } else {
      ElMessage.error('创建会话失败: ' + (response.data?.message || '未知错误'))
    }
  } catch (error) {
    console.error('创建会话失败详情:', error)
    const errorMsg = error.response?.data?.message || error.message || '创建会话失败，请稍后重试'
    ElMessage.error(errorMsg)
  }
}

const handleBuy = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    const response = await api.createTransaction(product.value.id)
    if (response.data.code === 200) {
      ElMessage.success('购买意向已创建，请在3小时内完成付款')
      currentTransaction.value = response.data.data
      product.value.status = 'locked'
      startLockTimer()
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '创建购买意向失败')
  }
}

const goToOrder = () => {
  router.push('/orders?tab=pending')
}

const handleCancelTransaction = async () => {
  try {
    await ElMessageBox.confirm('确定要取消购买意向吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await api.cancelTransaction(currentTransaction.value.id)
    if (response.data.code === 200) {
      ElMessage.success('已取消购买意向')
      currentTransaction.value = null
      product.value.status = 'available'
      if (lockTimer) {
        clearInterval(lockTimer)
        lockTimer = null
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '取消失败')
    }
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

const goToMy = () => {
  router.push('/my')
}

const checkFavoriteStatus = async () => {
  if (!userStore.isLoggedIn || !product.value?.id) return
  
  try {
    const response = await api.checkFavorite(product.value.id)
    if (response.data.code === 200) {
      isFavorited.value = response.data.data.is_favorited
    }
  } catch (error) {
    console.error('检查收藏状态失败:', error)
  }
}

const handleFavorite = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  if (!product.value?.id) {
    ElMessage.error('商品信息未加载')
    return
  }

  favoriteLoading.value = true

  try {
    if (isFavorited.value) {
      // 取消收藏
      await api.removeFavorite(favoriteId.value)
      ElMessage.success('已取消收藏')
      isFavorited.value = false
      favoriteId.value = null
    } else {
      // 添加收藏
      const response = await api.addFavorite(product.value.id)
      if (response.data.code === 200) {
        ElMessage.success('收藏成功')
        isFavorited.value = true
        favoriteId.value = response.data.data.id
      }
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '操作失败')
  } finally {
    favoriteLoading.value = false
  }
}

onMounted(async () => {
  await loadProduct()
  if (userStore.isLoggedIn) {
    await loadMyTransaction()
    await checkFavoriteStatus()
    if (currentTransaction.value?.status === 'pending') {
      startLockTimer()
    }
  }
})

onUnmounted(() => {
  if (lockTimer) {
    clearInterval(lockTimer)
  }
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

.product-status-badge {
  margin-bottom: 10px;
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

.description-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.favorite-btn {
  display: flex;
  align-items: center;
  gap: 5px;
}

.lock-info {
  margin-top: 10px;
}

.transaction-panel {
  margin-top: 20px;
  padding: 15px;
  background: #f0f9ff;
  border-radius: 8px;
}

.transaction-panel h4 {
  margin-bottom: 10px;
  color: #303133;
}

.transaction-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}
</style>
