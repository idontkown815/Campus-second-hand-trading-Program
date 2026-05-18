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
                    <el-button type="primary" @click="handlePay" size="large">确认付款</el-button>
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
              <h3>商品描述</h3>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import ProductComment from './ProductComment.vue'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const product = ref(null)
const currentTransaction = ref(null)
const lockRemainingTime = ref('')
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

const contactSeller = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  console.log('联系卖家', product.value.seller)
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

const handlePay = async () => {
  try {
    const response = await api.payTransaction(currentTransaction.value.id)
    if (response.data.code === 200) {
      ElMessage.success('付款成功，等待卖家发货')
      currentTransaction.value = response.data.data
      product.value.status = 'sold'
      if (lockTimer) {
        clearInterval(lockTimer)
        lockTimer = null
      }
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '付款失败')
  }
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

onMounted(async () => {
  await loadProduct()
  if (userStore.isLoggedIn) {
    await loadMyTransaction()
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
