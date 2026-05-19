<template>
  <div class="my-container">
    <div class="my-header">
      <div class="user-info">
        <div class="avatar-wrapper" @click="goToProfile">
          <img v-if="userStore.user?.avatar" :src="userStore.user.avatar" class="avatar-img" />
          <div v-else class="avatar-placeholder">{{ userStore.user?.name?.charAt(0) || 'U' }}</div>
          <div class="edit-icon">
            <el-icon><Edit /></el-icon>
          </div>
        </div>
        <div class="user-details">
          <h2 class="user-name">{{ userStore.user?.name || '未登录' }}</h2>
          <p class="user-id">学号：{{ userStore.user?.student_id || '-' }}</p>
          <p class="user-meta">{{ userStore.user?.major || '未设置专业' }} · {{ userStore.user?.grade || '未设置年级' }}</p>
        </div>
      </div>
    </div>

    <div class="order-section">
      <div class="section-header">
        <span class="section-title">我的订单</span>
        <span class="see-all" @click="goToOrders">查看全部 <el-icon><ArrowRight /></el-icon></span>
      </div>
      <div class="order-icons">
        <div class="order-item" @click="goToOrders('pending_payment')">
          <el-icon class="order-icon"><Wallet /></el-icon>
          <span>待付款</span>
          <el-badge v-if="orderCounts.pending_payment" :value="orderCounts.pending_payment" class="badge" />
        </div>
        <div class="order-item" @click="goToOrders('pending_shipment')">
          <el-icon class="order-icon"><Sell /></el-icon>
          <span>待发货</span>
          <el-badge v-if="orderCounts.pending_shipment" :value="orderCounts.pending_shipment" class="badge" />
        </div>
        <div class="order-item" @click="goToOrders('pending_receipt')">
          <el-icon class="order-icon"><Box /></el-icon>
          <span>待收货</span>
          <el-badge v-if="orderCounts.pending_receipt" :value="orderCounts.pending_receipt" class="badge" />
        </div>
        <div class="order-item" @click="goToOrders('completed')">
          <el-icon class="order-icon"><CircleCheck /></el-icon>
          <span>已完成</span>
          <el-badge v-if="orderCounts.completed" :value="orderCounts.completed" class="badge" />
        </div>
      </div>
    </div>

    <div class="tool-section">
      <div class="tool-item" @click="goToProfile">
        <el-icon class="tool-icon"><User /></el-icon>
        <span>个人资料</span>
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
      <div class="tool-item" @click="goToMyProducts">
        <el-icon class="tool-icon"><Goods /></el-icon>
        <span>我的发布</span>
        <el-badge v-if="productCount" :value="productCount" class="badge" />
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
      <div class="tool-item" @click="goToFavorites">
        <el-icon class="tool-icon"><Star /></el-icon>
        <span>我的收藏</span>
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
      <div class="tool-item" @click="goToFootprint">
        <el-icon class="tool-icon"><Clock /></el-icon>
        <span>我的足迹</span>
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
    </div>

    <div class="tool-section">
      <div class="tool-item" @click="goToSettings">
        <el-icon class="tool-icon"><Setting /></el-icon>
        <span>设置</span>
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
      <div class="tool-item" @click="goToHelp">
        <el-icon class="tool-icon"><QuestionFilled /></el-icon>
        <span>帮助与反馈</span>
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
      <div class="tool-item" @click="goToAbout">
        <el-icon class="tool-icon"><InfoFilled /></el-icon>
        <span>关于平台</span>
        <el-icon class="arrow"><ArrowRight /></el-icon>
      </div>
    </div>

    <!-- 管理员功能区 -->
    <div v-if="userStore.user?.is_superuser" class="admin-section">
      <el-card class="admin-card">
        <div class="admin-item">
          <div class="admin-header">
            <el-icon class="admin-icon"><Monitor /></el-icon>
            <span class="admin-title">管理员功能</span>
          </div>
          <p class="admin-desc">释放所有被锁定的商品，并将待付款交易设为过期</p>
        </div>
        <el-button 
          type="danger" 
          @click="handleAdminReleaseAll"
          :loading="adminLoading"
          class="admin-btn">
          <el-icon><Refresh /></el-icon>
          一键释放锁定商品
        </el-button>
      </el-card>
    </div>

    <div class="logout-section">
      <el-button v-if="userStore.isLoggedIn" type="danger" plain class="logout-btn" @click="handleLogout">
        退出登录
      </el-button>
      <el-button v-else type="primary" class="login-btn" @click="goToLogin">
        立即登录
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import api from '../api'
import {
  Edit,
  ArrowRight,
  Wallet,
  Sell,
  Box,
  CircleCheck,
  User,
  Goods,
  Star,
  Clock,
  Setting,
  QuestionFilled,
  InfoFilled,
  Monitor,
  Refresh
} from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const adminLoading = ref(false)

const orderCounts = ref({
  pending_payment: 0,
  pending_shipment: 0,
  pending_receipt: 0,
  completed: 0
})

const productCount = ref(0)

const loadOrderCounts = async () => {
  if (!userStore.isLoggedIn || !userStore.user) return
  
  try {
    const response = await api.getTransactions()
    const orders = response.data.data || []
    
    orderCounts.value = {
      pending_payment: 0,
      pending_shipment: 0,
      pending_receipt: 0,
      completed: 0
    }
    
    const userId = userStore.user.id
    
    orders.forEach(order => {
      const isBuyer = order.buyer_id === userId
      const isSeller = order.seller_id === userId
      
      if (order.status === 'pending' && isBuyer) {
        orderCounts.value.pending_payment++
      } else if (order.status === 'paid' && isSeller) {
        orderCounts.value.pending_shipment++
      } else if (['shipped', 'arrived'].includes(order.status) && isBuyer) {
        orderCounts.value.pending_receipt++
      } else if (order.status === 'completed') {
        orderCounts.value.completed++
      }
    })
  } catch (error) {
    console.error('加载订单计数失败:', error)
  }
}

const goToProfile = () => {
  router.push('/profile')
}

const goToOrders = (type) => {
  const tabMap = {
    pending_payment: 'pending',
    pending_shipment: 'paid',
    pending_receipt: 'shipped',
    completed: 'completed'
  }
  const tab = tabMap[type] || 'pending'
  router.push({ path: '/orders', query: { tab } })
}

const goToMyProducts = () => {
  router.push('/my/products')
}

const goToFavorites = () => {
  ElMessage.info('我的收藏功能即将上线')
}

const goToFootprint = () => {
  ElMessage.info('我的足迹功能即将上线')
}

const goToSettings = () => {
  ElMessage.info('设置功能即将上线')
}

const goToHelp = () => {
  ElMessage.info('帮助与反馈功能即将上线')
}

const goToAbout = () => {
  ElMessage.info('关于平台功能即将上线')
}

const goToLogin = () => {
  router.push('/login')
}

const handleAdminReleaseAll = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要释放所有被锁定的商品吗？\n此操作将：\n 1. 把所有锁定商品恢复为在售状态\n 2. 把所有待付款交易设为过期',
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    adminLoading.value = true
    const response = await api.adminReleaseAll()
    
    if (response.data.code === 200) {
      const data = response.data.data
      ElMessage.success(
        `释放成功！\n释放锁定商品: ${data.locked_released} 个\n过期待付款交易: ${data.pending_expired} 个`
      )
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  } finally {
    adminLoading.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

const fetchData = async () => {
  if (userStore.isLoggedIn) {
    try {
      await userStore.getProfile()
      await loadOrderCounts()
    } catch (error) {
      console.error(error)
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.my-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.my-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px 20px;
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
}

.avatar-img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.5);
}

.avatar-placeholder {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: bold;
  border: 3px solid rgba(255, 255, 255, 0.5);
}

.edit-icon {
  position: absolute;
  bottom: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
}

.user-details {
  margin-left: 20px;
  flex: 1;
}

.user-name {
  font-size: 22px;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.user-id {
  font-size: 14px;
  margin: 0 0 5px 0;
  opacity: 0.9;
}

.user-meta {
  font-size: 13px;
  margin: 0;
  opacity: 0.8;
}

.order-section {
  background: white;
  margin: 12px;
  border-radius: 12px;
  padding: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.see-all {
  font-size: 13px;
  color: #999;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.order-icons {
  display: flex;
  justify-content: space-around;
}

.order-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  cursor: pointer;
  flex: 1;
}

.order-icon {
  font-size: 28px;
  color: #667eea;
  margin-bottom: 8px;
}

.order-item span {
  font-size: 13px;
  color: #666;
}

.badge {
  position: absolute;
  top: -5px;
  right: 10px;
}

.tool-section {
  background: white;
  margin: 12px;
  border-radius: 12px;
  overflow: hidden;
}

.tool-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
}

.tool-item:hover {
  background: #f9f9f9;
}

.tool-item + .tool-item {
  border-top: 1px solid #f0f0f0;
}

.tool-icon {
  font-size: 22px;
  color: #667eea;
  margin-right: 15px;
}

.tool-item span {
  flex: 1;
  font-size: 15px;
  color: #333;
}

.arrow {
  color: #ccc;
  font-size: 14px;
}

.logout-section {
  padding: 20px 12px;
}

.logout-btn,
.login-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  border-radius: 22px;
}

.admin-section {
  padding: 0 12px;
  margin-bottom: 12px;
}

.admin-card {
  background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
  border: 2px solid #fde2e2;
}

.admin-item {
  margin-bottom: 15px;
}

.admin-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.admin-icon {
  font-size: 20px;
  color: #f56c6c;
}

.admin-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.admin-desc {
  margin: 0;
  font-size: 13px;
  color: #999;
  padding-left: 28px;
}

.admin-btn {
  width: 100%;
  height: 44px;
  font-size: 15px;
  border-radius: 22px;
}
</style>
