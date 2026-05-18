<template>
  <div class="my-products-container">
    <el-card class="my-products-card">
      <template #header>
        <h2>我的发布</h2>
      </template>
      <div v-if="!userStore.isLoggedIn" class="login-prompt">
        <el-empty description="请先登录" />
        <el-button type="primary" @click="goToLogin">立即登录</el-button>
      </div>
      <div v-else>
        <el-table :data="products" style="width: 100%" v-loading="loading">
          <el-table-column prop="title" label="商品标题" width="200">
            <template #default="scope">
              <el-link type="primary" @click="goToDetail(scope.row.id)">{{ scope.row.title }}</el-link>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="价格" width="100">
            <template #default="scope">
              ¥{{ scope.row.price }}
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="120" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row)" :disable-transitions="true">
                {{ getStatusText(scope.row) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="发布时间" width="180" />
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <template v-if="canOperate(scope.row)">
                <el-button type="primary" size="small" @click="editProduct(scope.row.id)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="takeDownProduct(scope.row.id)" v-if="scope.row.status === 'available'">
                  下架
                </el-button>
                <el-button type="success" size="small" @click="putOnShelf(scope.row.id)" v-if="scope.row.status === 'rejected'">
                  上架
                </el-button>
              </template>
              <span v-else class="status-hint">
                {{ getStatusHint(scope.row) }}
              </span>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="!loading && products.length === 0" description="暂无发布商品" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '../../stores/product'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const productStore = useProductStore()
const userStore = useUserStore()
const products = ref([])
const loading = ref(false)

const goToLogin = () => {
  router.push('/login')
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

const getStatusType = (product) => {
  const status = product.status
  const txStatus = product.transaction_status

  if (status === 'available' && !txStatus) return 'success'
  if (status === 'locked' && txStatus === 'pending') return 'warning'
  if (status === 'sold' && txStatus === 'paid') return 'warning'
  if (status === 'sold' && txStatus === 'shipped') return 'primary'
  if (status === 'sold' && txStatus === 'completed') return 'success'
  if (status === 'rejected') return 'danger'
  if (status === 'pending') return 'info'

  return 'info'
}

const getStatusText = (product) => {
  const status = product.status
  const txStatus = product.transaction_status

  if (status === 'available' && !txStatus) return '在售'
  if (status === 'locked' && txStatus === 'pending') return '待付款'
  if (status === 'sold' && txStatus === 'paid') return '待发货'
  if (status === 'sold' && txStatus === 'shipped') return '待收货'
  if (status === 'sold' && txStatus === 'completed') return '已完成'
  if (status === 'rejected') return '已下架'
  if (status === 'pending') return '待审核'

  return status
}

const canOperate = (product) => {
  const status = product.status
  const txStatus = product.transaction_status

  if (status === 'available' && !txStatus) return true
  if (status === 'rejected') return true
  if (status === 'pending') return true

  return false
}

const getStatusHint = (product) => {
  const status = product.status
  const txStatus = product.transaction_status

  if (status === 'locked' && txStatus === 'pending') return '买家待付款'
  if (status === 'sold' && txStatus === 'paid') return '待发货'
  if (status === 'sold' && txStatus === 'shipped') return '买家待收货'
  if (status === 'sold' && txStatus === 'completed') return '交易完成'

  return ''
}

const loadMyProducts = async () => {
  if (!userStore.isLoggedIn) return

  loading.value = true
  try {
    const response = await productStore.getMyProducts()
    products.value = response.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('获取商品失败')
  } finally {
    loading.value = false
  }
}

const takeDownProduct = async (id) => {
  try {
    await productStore.takeDownProduct(id)
    ElMessage.success('商品已下架')
    await loadMyProducts()
  } catch (error) {
    console.error(error)
    ElMessage.error('下架失败')
  }
}

const putOnShelf = async (id) => {
  try {
    await productStore.putOnShelf(id)
    ElMessage.success('商品已上架')
    await loadMyProducts()
  } catch (error) {
    console.error(error)
    ElMessage.error('上架失败')
  }
}

const editProduct = (id) => {
  router.push(`/product/publish?id=${id}`)
}

onMounted(() => {
  loadMyProducts()
})
</script>

<style scoped>
.my-products-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.my-products-card {
  width: 100%;
  max-width: 1000px;
}

.my-products-card h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

.login-prompt {
  text-align: center;
  padding: 40px 20px;
}

.login-prompt .el-button {
  margin-top: 20px;
}

.status-hint {
  color: #909399;
  font-size: 12px;
}
</style>