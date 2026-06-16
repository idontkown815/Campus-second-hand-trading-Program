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
          <el-tabs v-model="activeTab" type="card" class="order-tabs" v-loading="loading">
            <template #loading>
              <div class="loading-spinner">
                <el-icon class="is-loading" :size="40"><Loading /></el-icon>
                <p style="margin-top: 10px; color: #666;">正在加载订单...</p>
              </div>
            </template>
            <el-tab-pane label="待付款" name="pending">
              <div v-if="pendingOrders.length === 0" class="empty-state">
                <el-empty description="暂无待付款订单">
                  <template #image>
                    <el-icon size="80" style="color: #e6a23c"><ShoppingCart /></el-icon>
                  </template>
                  <template #description>
                    <span>暂无待付款订单</span>
                    <p style="color: #909399; font-size: 14px; margin-top: 8px;">您可以去商品详情页创建订单</p>
                  </template>
                  <el-button type="primary" @click="router.push('/')">去逛逛</el-button>
                </el-empty>
              </div>
              <div v-else>
                <el-card v-for="order in pendingOrders" :key="order.id" class="order-card pending-card">
                  <div class="order-header">
                    <div class="header-left">
                      <el-tag type="warning">待付款</el-tag>
                      <span class="order-id">订单号：{{ order.id }}</span>
                    </div>
                    <span class="order-time">{{ formatDate(order.created_at) }}</span>
                  </div>
                  <div class="order-content">
                    <div class="product-info">
                      <img :src="getProductImage(order.product_images)" class="product-image" />
                      <div class="product-detail">
                        <h4>{{ order.product_title }}</h4>
                        <p class="price">价格：<span class="price-num">¥{{ order.product_price }}</span></p>
                        <p>卖家：{{ order.seller }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <el-divider></el-divider>
                  
                  <div v-if="isBuyer(order)" class="shipping-section">
                    <el-alert 
                      type="warning" 
                      :closable="false" 
                      class="shipping-alert"
                      show-icon
                    >
                      <template #title>
                        <div class="alert-title">请先填写收货信息，再付款！</div>
                      </template>
                    </el-alert>
                    <div class="section-title">
                      <el-icon><Document /></el-icon>
                      填写收货信息
                    </div>
                    <el-form :model="orderShippingInfo[order.id]" label-width="80px" class="shipping-form">
                      <el-form-item label="收件人">
                        <el-input 
                          v-model="orderShippingInfo[order.id].recipient_name" 
                          placeholder="请输入收件人姓名" 
                          clearable
                          size="large"
                        />
                      </el-form-item>
                      <el-form-item label="手机号">
                        <el-input 
                          v-model="orderShippingInfo[order.id].recipient_phone" 
                          placeholder="请输入手机号码" 
                          clearable
                          size="large"
                        />
                      </el-form-item>
                      <el-form-item label="收货地址">
                        <el-input 
                          v-model="orderShippingInfo[order.id].shipping_address" 
                          type="textarea" 
                          :rows="3" 
                          placeholder="请输入详细收货地址（省市区街道门牌号等）" 
                          size="large"
                        />
                      </el-form-item>
                    </el-form>
                  </div>
                  
                  <div class="order-footer">
                    <div class="lock-time" v-if="order.locked_remaining_seconds > 0">
                      <el-icon class="time-icon"><Timer /></el-icon>
                      <span>剩余付款时间：{{ formatLockTime(order.locked_remaining_seconds) }}</span>
                    </div>
                    <div class="action-buttons" v-if="isBuyer(order)">
                      <el-button @click="handleCancel(order.id)">取消订单</el-button>
                      <el-button type="primary" @click="handlePay(order.id)" size="large">立即付款</el-button>
                    </div>
                    <div class="status-display" v-else>
                      <span class="status-text">买家未付款</span>
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
                        <div v-if="order.recipient_name" class="shipping-info">
                          <p class="info-title">收货信息：</p>
                          <p>收件人：{{ order.recipient_name }}</p>
                          <p>电话：{{ order.recipient_phone }}</p>
                          <p>地址：{{ order.shipping_address }}</p>
                        </div>
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
                        <p v-if="isSeller(order)">买家：{{ order.buyer }}</p>
                        <p v-else>卖家：{{ order.seller }}</p>
                        <div v-if="order.recipient_name" class="shipping-info">
                          <p class="info-title">收货信息：</p>
                          <p>收件人：{{ order.recipient_name }}</p>
                          <p>电话：{{ order.recipient_phone }}</p>
                          <p>地址：{{ order.shipping_address }}</p>
                        </div>
                      </div>
                    </div>
                    <div class="order-actions">
                      <div class="action-buttons" v-if="isSeller(order)">
                        <el-button type="primary" @click="handleArrive(order.id)">确认到货</el-button>
                      </div>
                      <div class="action-buttons" v-else-if="isBuyer(order)">
                        <el-button type="primary" @click="handleComplete(order.id)">确认收货</el-button>
                      </div>
                      <div v-else>
                        <el-alert type="info" :closable="false" title="等待确认"></el-alert>
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
import { ref, computed, onMounted, onUnmounted, watch, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Timer, ShoppingCart, Loading } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const activeTab = ref('pending')
const orders = ref([])
const loading = ref(false)
let refreshTimer = null

// 收货信息表单数据（每个订单独立的收货信息）
const orderShippingInfo = reactive({})

// 初始化收货信息
const initOrderShippingInfo = (order) => {
  if (!orderShippingInfo[order.id]) {
    orderShippingInfo[order.id] = {
      recipient_name: '',
      recipient_phone: '',
      shipping_address: ''
    }
  }
}

// 根据URL参数设置标签页
const setActiveTabFromQuery = () => {
  const tab = route.query.tab
  if (['pending', 'paid', 'shipped', 'completed'].includes(tab)) {
    activeTab.value = tab
  }
}

// 监听URL参数变化，重新加载订单
watch(() => route.query.tab, () => {
  setActiveTabFromQuery()
  loadOrders()
})

// 监听路由变化（进入该页面时重新加载订单）
watch(() => route.path, (newPath) => {
  if (newPath === '/orders') {
    setActiveTabFromQuery()
    loadOrders()
  }
})

const pendingOrders = computed(() => orders.value.filter(o => o.status === 'pending'))
const paidOrders = computed(() => orders.value.filter(o => o.status === 'paid'))
const shippedOrders = computed(() => orders.value.filter(o => o.status === 'shipped'))
const completedOrders = computed(() => orders.value.filter(o => o.status === 'completed'))

const loadOrders = async () => {
  if (!userStore.isLoggedIn) return
  
  loading.value = true
  try {
    if (!userStore.user) {
      await userStore.getProfile()
    }
    const response = await api.getTransactions()
    orders.value = response.data.data || []
    // 初始化所有订单的收货信息
    orders.value.forEach(order => initOrderShippingInfo(order))
  } catch (error) {
    console.error('加载订单失败:', error)
    let errorMsg = error.response?.data?.message || '加载订单失败'
    if (error.response?.status === 401) {
      errorMsg = '登录已过期，请重新登录'
    }
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
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
  if (!images) {
    return '/placeholder.png'
  }
  
  let imageArray = []
  
  // 处理字符串格式（可能是 JSON 字符串或逗号分隔的字符串）
  if (typeof images === 'string') {
    try {
      // 尝试解析 JSON 字符串
      imageArray = JSON.parse(images)
    } catch (e) {
      // 如果不是有效 JSON，尝试按逗号分割
      imageArray = images.split(',')
    }
  } else if (Array.isArray(images)) {
    imageArray = images
  }
  
  if (!imageArray || imageArray.length === 0) {
    return '/placeholder.png'
  }
  
  let imgPath = imageArray[0].trim()
  
  // 如果路径不包含完整 URL 且不包含 /uploads/ 前缀，则添加前缀
  if (imgPath && !imgPath.startsWith('http') && !imgPath.startsWith('/uploads/')) {
    // 如果路径不包含 商品/ 前缀，则添加
    if (!imgPath.startsWith('商品/')) {
      imgPath = '商品/' + imgPath
    }
    imgPath = '/uploads/' + imgPath
  }
  
  return imgPath || '/placeholder.png'
}

const isBuyer = (order) => {
  return order.buyer_id === userStore.user?.id
}

const isSeller = (order) => {
  return order.seller_id === userStore.user?.id
}

const handlePay = async (orderId) => {
  // 确保订单有收货信息对象
  if (!orderShippingInfo[orderId]) {
    orderShippingInfo[orderId] = {
      recipient_name: '',
      recipient_phone: '',
      shipping_address: ''
    }
  }
  
  const shippingInfo = orderShippingInfo[orderId]
  
  // 简单的本地验证
  if (!shippingInfo.recipient_name || !shippingInfo.recipient_name.trim()) {
    ElMessage.warning('请输入收件人姓名')
    return
  }
  if (!shippingInfo.recipient_phone || !shippingInfo.recipient_phone.trim()) {
    ElMessage.warning('请输入手机号码')
    return
  }
  if (!shippingInfo.shipping_address || !shippingInfo.shipping_address.trim()) {
    ElMessage.warning('请输入收货地址')
    return
  }
  
  try {
    const response = await api.payTransaction(orderId, {
      recipient_name: shippingInfo.recipient_name.trim(),
      recipient_phone: shippingInfo.recipient_phone.trim(),
      shipping_address: shippingInfo.shipping_address.trim()
    })
    if (response.data.code === 200) {
      ElMessage.success('付款成功')
      // 清空表单
      orderShippingInfo[orderId] = {
        recipient_name: '',
        recipient_phone: '',
        shipping_address: ''
      }
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
  background: #f5f7fa;
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
  padding-top: 20px;
}

.empty-state {
  padding: 60px 20px;
}

.order-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
}

.pending-card {
  border: 2px solid #e6a23c;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-id {
  color: #666;
  font-size: 14px;
}

.order-time {
  color: #999;
  font-size: 14px;
}

.order-content {
  padding: 15px 0;
}

.product-info {
  display: flex;
  gap: 15px;
  flex: 1;
}

.product-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid #eee;
}

.product-detail {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.product-detail h4 {
  margin: 0 0 12px 0;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.product-detail .price {
  margin: 8px 0;
  color: #666;
  font-size: 15px;
}

.product-detail .price-num {
  color: #e6a23c;
  font-weight: bold;
  font-size: 20px;
}

.product-detail p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}

.shipping-info {
  margin-top: 10px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
}

.shipping-info .info-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 15px;
}

.shipping-info p {
  margin: 4px 0;
  font-size: 14px;
  color: #666;
}

.shipping-section {
  background: linear-gradient(135deg, #fff7e6 0%, #fff 100%);
  padding: 20px;
  border-radius: 10px;
  margin: 10px 0;
}

.shipping-alert {
  margin-bottom: 20px;
}

.shipping-alert .alert-title {
  font-weight: 600;
  font-size: 15px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #e6a23c;
  margin-bottom: 15px;
}

.shipping-form {
  max-width: 600px;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
  margin-top: 10px;
}

.lock-time {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #e6a23c;
  font-size: 14px;
  background: #fff7e6;
  padding: 8px 15px;
  border-radius: 20px;
}

.time-icon {
  font-size: 16px;
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