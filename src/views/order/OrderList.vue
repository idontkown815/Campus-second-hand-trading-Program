<template>
  <div class="order-container">
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
        <div v-if="!userStore.isLoggedIn" class="login-prompt">
          <el-empty description="请先登录查看订单" />
          <el-button type="primary" @click="goToLogin">立即登录</el-button>
        </div>
        <div v-else>
          <el-tabs v-model="activeTab" type="card" class="order-tabs">
            <el-tab-pane label="待付款" name="pending">
              <div v-if="pendingOrders.length === 0" class="empty-state">
                <el-empty description="暂无待付款订单" />
              </div>
              <div v-else>
                <el-card v-for="order in pendingOrders" :key="order.id" class="order-card">
                  <div class="order-header">
                    <span class="order-id">订单号：{{ order.id }}</span>
                    <span class="order-time">{{ formatDate(order.created_at) }}</span>
                  </div>
                  <div class="order-content">
                    <div class="product-info">
                      <img :src="getProductImage(order.product_images)" class="product-image" />
                      <div class="product-detail">
                        <h4>{{ order.product_title }}</h4>
                        <p>价格：¥{{ order.product_price }}</p>
                        <p>卖家：{{ order.seller }}</p>
                      </div>
                    </div>
                    <div class="order-actions">
                      <div class="lock-time" v-if="order.locked_remaining_seconds > 0">
                        <el-alert type="warning" :closable="false" :title="'剩余付款时间：' + formatLockTime(order.locked_remaining_seconds)"></el-alert>
                      </div>
                      <div class="action-buttons" v-if="isBuyer(order)">
                        <el-button type="primary" @click="handlePay(order.id)">立即付款</el-button>
                        <el-button @click="handleCancel(order.id)">取消订单</el-button>
                      </div>
                      <div class="status-display" v-else>
                        <span class="status-text">买家未付款</span>
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>

            <el-tab-pane label="待发货" name="paid">
              <div v-if="paidOrders.length === 0" class="empty-state">
                <el-empty description="暂无待发货订单" />
              </div>
              <div v-else>
                <el-card v-for="order in paidOrders" :key="order.id" class="order-card">
                  <div class="order-header">
                    <span class="order-id">订单号：{{ order.id }}</span>
                    <span class="order-time">{{ formatDate(order.created_at) }}</span>
                  </div>
                  <div class="order-content">
                    <div class="product-info">
                      <img :src="getProductImage(order.product_images)" class="product-image" />
                      <div class="product-detail">
                        <h4>{{ order.product_title }}</h4>
                        <p>价格：¥{{ order.product_price }}</p>
                        <p>买家：{{ order.buyer }}</p>
                      </div>
                    </div>
                    <div class="order-actions">
                      <div class="action-buttons" v-if="isSeller(order)">
                        <el-button type="primary" @click="handleShip(order.id)">确认发货</el-button>
                      </div>
                      <div class="action-buttons" v-else-if="isBuyer(order)">
                        <el-button type="danger" @click="handleRefund(order.id)">申请退款</el-button>
                      </div>
                      <div v-else>
                        <el-alert type="info" :closable="false" title="等待卖家发货"></el-alert>
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>

            <el-tab-pane label="待收货" name="shipped">
              <div v-if="shippedOrders.length === 0" class="empty-state">
                <el-empty description="暂无待收货订单" />
              </div>
              <div v-else>
                <el-card v-for="order in shippedOrders" :key="order.id" class="order-card">
                  <div class="order-header">
                    <span class="order-id">订单号：{{ order.id }}</span>
                    <span class="order-time">{{ formatDate(order.created_at) }}</span>
                  </div>
                  <div class="order-content">
                    <div class="product-info">
                      <img :src="getProductImage(order.product_images)" class="product-image" />
                      <div class="product-detail">
                        <h4>{{ order.product_title }}</h4>
                        <p>价格：¥{{ order.product_price }}</p>
                        <p>卖家：{{ order.seller }}</p>
                      </div>
                    </div>
                    <div class="order-actions">
                      <div class="action-buttons" v-if="isBuyer(order)">
                        <el-button type="primary" @click="handleComplete(order.id)">确认收货</el-button>
                      </div>
                      <div v-else>
                        <el-alert type="info" :closable="false" title="等待买家确认收货"></el-alert>
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>

            <el-tab-pane label="已完成" name="completed">
              <div v-if="completedOrders.length === 0" class="empty-state">
                <el-empty description="暂无已完成订单" />
              </div>
              <div v-else>
                <el-card v-for="order in completedOrders" :key="order.id" class="order-card">
                  <div class="order-header">
                    <span class="order-id">订单号：{{ order.id }}</span>
                    <span class="order-time">{{ formatDate(order.created_at) }}</span>
                    <el-tag type="success">交易完成</el-tag>
                  </div>
                  <div class="order-content">
                    <div class="product-info">
                      <img :src="getProductImage(order.product_images)" class="product-image" />
                      <div class="product-detail">
                        <h4>{{ order.product_title }}</h4>
                        <p>价格：¥{{ order.product_price }}</p>
                        <p>卖家：{{ order.seller }}</p>
                        <p>买家：{{ order.buyer }}</p>
                      </div>
                    </div>
                    <div class="order-actions">
                      <el-button type="default" @click="goToProduct(order.product_id)">查看商品</el-button>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const activeTab = ref('pending')
const orders = ref([])
let refreshTimer = null

// 根据URL参数设置标签页
const setActiveTabFromQuery = () => {
  const tab = route.query.tab
  if (['pending', 'paid', 'shipped', 'completed'].includes(tab)) {
    activeTab.value = tab
  }
}

// 监听URL参数变化
watch(() => route.query.tab, () => {
  setActiveTabFromQuery()
})

const pendingOrders = computed(() => orders.value.filter(o => o.status === 'pending'))
const paidOrders = computed(() => orders.value.filter(o => o.status === 'paid'))
const shippedOrders = computed(() => orders.value.filter(o => o.status === 'shipped'))
const completedOrders = computed(() => orders.value.filter(o => o.status === 'completed'))

const loadOrders = async () => {
  if (!userStore.isLoggedIn) return
  
  try {
    if (!userStore.user) {
      await userStore.getProfile()
    }
    const response = await api.getTransactions()
    orders.value = response.data.data || []
  } catch (error) {
    console.error('加载订单失败:', error)
    ElMessage.error(error.response?.data?.message || '加载订单失败')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const formatLockTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours}小时${minutes}分${secs}秒`
}

const getProductImage = (images) => {
  if (!images || !Array.isArray(images)) {
    return '/placeholder.png'
  }
  return images[0] || '/placeholder.png'
}

const isBuyer = (order) => {
  return order.buyer_id === userStore.user?.id
}

const isSeller = (order) => {
  return order.seller_id === userStore.user?.id
}

const handlePay = async (orderId) => {
  try {
    const response = await api.payTransaction(orderId)
    if (response.data.code === 200) {
      ElMessage.success('付款成功')
      await loadOrders()
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '付款失败')
  }
}

const handleCancel = async (orderId) => {
  try {
    await ElMessageBox.confirm('确定要取消订单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await api.cancelTransaction(orderId)
    if (response.data.code === 200) {
      ElMessage.success('订单已取消')
      await loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '取消失败')
    }
  }
}

const handleShip = async (orderId) => {
  try {
    const response = await api.shipTransaction(orderId)
    if (response.data.code === 200) {
      ElMessage.success('发货成功')
      await loadOrders()
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '发货失败')
  }
}

const handleRefund = async (orderId) => {
  try {
    await ElMessageBox.confirm('确定要申请退款吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await api.refundTransaction(orderId)
    if (response.data.code === 200) {
      ElMessage.success('退款申请已提交')
      await loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '退款失败')
    }
  }
}

const handleComplete = async (orderId) => {
  try {
    await ElMessageBox.confirm('确定已收到商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await api.completeTransaction(orderId)
    if (response.data.code === 200) {
      ElMessage.success('交易完成')
      await loadOrders()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.message || '确认失败')
    }
  }
}

const goToLogin = () => {
  router.push('/login')
}

const goToProduct = (productId) => {
  router.push(`/product/${productId}`)
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

onMounted(async () => {
  setActiveTabFromQuery()
  await loadOrders()
  // 每分钟刷新一次订单状态
  refreshTimer = setInterval(loadOrders, 60000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.order-container {
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

.header-content h1 {
  font-size: 24px;
  color: #667eea;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.login-prompt {
  text-align: center;
  padding: 100px 20px;
}

.login-prompt .el-button {
  margin-top: 20px;
}

.order-tabs {
  max-width: 1200px;
  margin: 0 auto;
}

.empty-state {
  padding: 60px 20px;
}

.order-card {
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.order-id {
  font-weight: bold;
  color: #333;
}

.order-time {
  color: #999;
  font-size: 14px;
}

.order-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.product-info {
  display: flex;
  gap: 15px;
  flex: 1;
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.product-detail {
  flex: 1;
}

.product-detail h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.product-detail p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}

.order-actions {
  text-align: right;
}

.lock-time {
  margin-bottom: 15px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.status-display {
  padding: 10px 20px;
  background-color: #fff7e6;
  border-radius: 4px;
  display: inline-block;
}

.status-text {
  color: #faad14;
  font-size: 14px;
  font-weight: 500;
}
</style>