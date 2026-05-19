<template>
  <div class="product-list-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>校园二手交易平台</h1>
          <div class="header-nav">
            <el-button type="text" @click="$router.push('/')">首页</el-button>
            <el-button type="text" @click="$router.push('/products')">商品</el-button>
          </div>
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
        <div class="product-section">
          <div class="filter-header">
            <div class="search-controls">
              <el-input v-model="searchKeyword" placeholder="搜索商品" style="width: 300px" clearable @keyup.enter="handleSearch" @clear="handleSearch">
                <template #append>
                  <el-button icon="Search" @click="handleSearch"></el-button>
                </template>
              </el-input>
            </div>
            <div class="filter-actions">
              <el-button size="small" @click="handleClearFilters" type="info" plain>
                <el-icon><RefreshLeft /></el-icon>
                清除筛选
              </el-button>
              <el-dropdown trigger="click" @command="handleSortCommand">
                <span class="filter-item">
                  综合
                  <el-icon><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="default">默认排序</el-dropdown-item>
                    <el-dropdown-item command="price_asc">价格从低到高</el-dropdown-item>
                    <el-dropdown-item command="price_desc">价格从高到低</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-dropdown trigger="click" @command="handleCategoryCommand">
                <span class="filter-item">
                  {{ selectedCategoryName || '全部分类' }}
                  <el-icon><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="">全部分类</el-dropdown-item>
                    <el-dropdown-item v-for="cat in categories" :key="cat.id" :command="cat.name">{{ cat.name }}</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-dropdown trigger="click" @command="handleCampusCommand">
                <span class="filter-item">
                  {{ selectedCampus || '全部校区' }}
                  <el-icon><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="">全部校区</el-dropdown-item>
                    <el-dropdown-item command="成都校区">成都校区</el-dropdown-item>
                    <el-dropdown-item command="什邡校区">什邡校区</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <div class="price-filter">
                <span class="filter-label">价格：</span>
                <span class="price-prefix">¥</span>
                <el-input-number v-model="minPrice" :min="0" :max="9999999" placeholder="最低" style="width: 100px" size="small" />
                <span class="price-separator">-</span>
                <span class="price-prefix">¥</span>
                <el-input-number v-model="maxPrice" :min="0" :max="9999999" placeholder="最高" style="width: 100px" size="small" />
                <el-button size="small" @click="handlePriceFilter">确定</el-button>
              </div>
            </div>
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
import { ElMessage } from 'element-plus'
import { ArrowDown, RefreshLeft } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const products = ref([])
const searchKeyword = ref('')
const categories = ref([
  { id: 1, name: '学习用具' },
  { id: 2, name: '数码产品' },
  { id: 3, name: '生活日用' },
  { id: 4, name: '服饰美妆' },
  { id: 5, name: '其他' }
])
const selectedCategoryName = ref('')
const selectedCampus = ref('')
const sortOrder = ref('default')
const minPrice = ref('')
const maxPrice = ref('')

const loadProducts = async () => {
  try {
    const params = {}
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }
    if (selectedCategoryName.value) {
      params.category = selectedCategoryName.value
    }
    if (minPrice.value) {
      params.min_price = minPrice.value
    }
    if (maxPrice.value) {
      params.max_price = maxPrice.value
    }
    if (selectedCampus.value) {
      params.campus = selectedCampus.value
    }
    if (sortOrder.value !== 'default') {
      params.sort = sortOrder.value
    }
    const response = await api.getProducts(params)
    products.value = response.data.data || []
  } catch (error) {
    console.error('加载商品失败:', error)
    ElMessage.error('加载商品失败')
  }
}

const handleSearch = () => {
  loadProducts()
}

const handleSortCommand = (command) => {
  sortOrder.value = command
  loadProducts()
}

const handleCategoryCommand = (command) => {
  selectedCategoryName.value = command || ''
  loadProducts()
}

const handleCampusCommand = (command) => {
  selectedCampus.value = command || ''
  loadProducts()
}

const handlePriceFilter = () => {
  loadProducts()
}

const handleClearFilters = () => {
  searchKeyword.value = ''
  selectedCategoryName.value = ''
  selectedCampus.value = ''
  sortOrder.value = 'default'
  minPrice.value = ''
  maxPrice.value = ''
  loadProducts()
  ElMessage.success('已清除所有筛选条件')
}

const goToDetail = (id) => {
  router.push(`/product/${id}`)
}

const goToMy = () => {
  router.push('/my')
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
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

.header-nav {
  display: flex;
  gap: 20px;
  margin: 0 20px;
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

.product-list-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.product-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-controls {
  display: flex;
  align-items: center;
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.price-filter {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  padding: 4px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: all 0.3s;
  white-space: nowrap;
}

.filter-item:hover {
  border-color: #667eea;
  color: #667eea;
}

.price-separator {
  margin: 0 3px;
  color: #999;
}

.price-prefix {
  color: #667eea;
  font-weight: 500;
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