<template>
  <div class="admin-container">
    <el-container>
      <el-aside width="200px" class="admin-aside">
        <div class="logo">
          <h3>管理员后台</h3>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="admin-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <span>首页概览</span>
          </el-menu-item>
          <el-menu-item index="products">
            <span>商品管理</span>
          </el-menu-item>
          <el-menu-item index="users">
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="admin-header">
          <div class="header-left">
            <h2>校园二手交易平台 - 管理后台</h2>
          </div>
          <div class="header-right">
            <span>欢迎，{{ userStore.user?.name || '管理员' }}</span>
            <el-button @click="handleLogout">退出登录</el-button>
          </div>
        </el-header>
        <el-main class="admin-main">
          <div v-if="activeMenu === 'dashboard'" class="dashboard-content">
            <el-row :gutter="20">
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-value">{{ stats.totalUsers }}</div>
                  <div class="stat-label">用户总数</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-value">{{ stats.totalProducts }}</div>
                  <div class="stat-label">商品总数</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-value">{{ stats.pendingProducts }}</div>
                  <div class="stat-label">待审核商品</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-value">{{ stats.totalTransactions }}</div>
                  <div class="stat-label">交易总数</div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <div v-if="activeMenu === 'products'" class="products-content">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>商品列表</span>
                  <el-button type="primary" @click="loadProducts">刷新</el-button>
                </div>
              </template>
              <el-table :data="products" style="width: 100%">
                <el-table-column prop="id" label="ID" width="60" />
                <el-table-column prop="title" label="商品名称" min-width="150" />
                <el-table-column prop="price" label="价格" width="100" />
                <el-table-column prop="status" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="seller_name" label="卖家" width="100" />
                <el-table-column prop="created_at" label="发布时间" width="180" />
                <el-table-column label="操作" width="200">
                  <template #default="{ row }">
                    <el-button size="small" type="danger" @click="handleProductAction(row, 'remove')">违规下架</el-button>
                    <el-button size="small" type="success" @click="handleProductAction(row, 'approve')">审核通过</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>

          <div v-if="activeMenu === 'users'" class="users-content">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>用户列表</span>
                  <div class="card-actions">
                    <el-input 
                      v-model="searchKeyword" 
                      placeholder="搜索姓名、学号或专业" 
                      style="width: 250px; margin-right: 10px;"
                      @keyup.enter="loadUsers"
                    >
                      <template #append>
                        <el-button @click="loadUsers">搜索</el-button>
                      </template>
                    </el-input>
                    <el-button type="primary" @click="loadUsers">刷新</el-button>
                  </div>
                </div>
              </template>
              <el-table :data="users" style="width: 100%">
                <el-table-column prop="id" label="ID" width="60" />
                <el-table-column prop="name" label="姓名" width="100" />
                <el-table-column prop="student_id" label="学号" width="120" />
                <el-table-column prop="grade" label="年级" width="100" />
                <el-table-column prop="major" label="专业" min-width="150" />
                <el-table-column prop="is_superuser" label="角色" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.is_superuser ? 'danger' : 'info'">
                      {{ row.is_superuser ? '管理员' : '普通用户' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="is_active" label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.is_active ? 'success' : 'warning'">
                      {{ row.is_active ? '正常' : '禁用' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="250">
                  <template #default="{ row }">
                    <el-button size="small" type="primary" @click="handleEditUser(row)">编辑</el-button>
                    <el-button 
                      size="small" 
                      :type="row.is_active ? 'warning' : 'success'" 
                      @click="handleToggleActive(row)"
                    >
                      {{ row.is_active ? '禁用' : '启用' }}
                    </el-button>
                    <el-button 
                      size="small" 
                      type="danger" 
                      @click="handleDeleteUser(row)"
                      :disabled="row.id === userStore.user?.id"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </el-main>
      </el-container>
    </el-container>

    <!-- 编辑用户弹窗 -->
    <el-dialog title="编辑用户" v-model="editDialogVisible" width="450px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="学号">
          <el-input v-model="editForm.student_id" disabled />
        </el-form-item>
        <el-form-item label="年级">
          <el-input v-model="editForm.grade" />
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="editForm.major" />
        </el-form-item>
        <el-form-item label="角色">
          <el-switch v-model="editForm.is_superuser" active-text="管理员" inactive-text="普通用户" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="editForm.is_active" active-text="正常" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const activeMenu = ref('dashboard')
const products = ref([])
const users = ref([])
const stats = ref({
  totalUsers: 0,
  totalProducts: 0,
  pendingProducts: 0,
  totalTransactions: 0
})
const searchKeyword = ref('')
const editDialogVisible = ref(false)
const editForm = ref({
  id: '',
  name: '',
  student_id: '',
  grade: '',
  major: '',
  is_superuser: false,
  is_active: true
})

const handleMenuSelect = (index) => {
  activeMenu.value = index
  if (index === 'dashboard') {
    loadStats()
  }
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/admin/login')
}

const loadStats = async () => {
  try {
    const response = await api.getAdminStats()
    if (response.data.code === 200) {
      stats.value = response.data.data
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('获取统计数据失败')
  }
}

const loadProducts = async () => {
  try {
    const response = await api.getAdminProducts()
    products.value = response.data.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('获取商品列表失败')
  }
}

const loadUsers = async () => {
  try {
    const params = searchKeyword.value ? { search: searchKeyword.value } : {}
    const response = await api.getUsers(params)
    users.value = response.data.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('获取用户列表失败')
  }
}

const handleEditUser = (user) => {
  editForm.value = {
    id: user.id,
    name: user.name || '',
    student_id: user.student_id || '',
    grade: user.grade || '',
    major: user.major || '',
    is_superuser: user.is_superuser || false,
    is_active: user.is_active || true
  }
  editDialogVisible.value = true
}

const handleSaveEdit = async () => {
  try {
    await api.updateUser(editForm.value.id, editForm.value)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadUsers()
  } catch (error) {
    console.error(error)
    ElMessage.error('更新失败')
  }
}

const handleToggleActive = async (user) => {
  try {
    const action = user.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(`确定要${action}该用户吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await api.updateUser(user.id, { is_active: !user.is_active })
    ElMessage.success(`${action}成功`)
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('操作失败')
    }
  }
}

const handleDeleteUser = async (user) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？此操作不可恢复！', '警告', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'danger'
    })
    await api.deleteUser(user.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('删除失败')
    }
  }
}

const getStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'available': 'success',
    'locked': 'info',
    'sold': 'primary',
    'violation': 'danger',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    'pending': '待审核',
    'available': '在售',
    'locked': '锁定中',
    'sold': '已售出',
    'violation': '违规下架',
    'rejected': '已下架'
  }
  return textMap[status] || status
}

const handleProductAction = async (product, action) => {
  try {
    if (action === 'remove') {
      await ElMessageBox.confirm('确定要下架该商品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await api.adminTakeDownProduct(product.id)
      ElMessage.success('商品已下架')
      loadProducts()
      loadStats()
    } else if (action === 'approve') {
      await api.approveProduct(product.id)
      ElMessage.success('商品已审核通过')
      loadProducts()
      loadStats()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  if (!userStore.isLoggedIn || !userStore.user?.is_superuser) {
    ElMessage.error('请先以管理员身份登录')
    router.push('/admin/login')
    return
  }
  loadStats()
  loadProducts()
  loadUsers()
})
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
}

.admin-aside {
  background: #304156;
  color: #fff;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #3f4a5a;
}

.logo h3 {
  color: #fff;
  font-size: 18px;
}

.admin-menu {
  border: none;
  background: #304156;
}

.admin-menu :deep(.el-menu-item) {
  color: #bfcbd9;
}

.admin-menu :deep(.el-menu-item:hover),
.admin-menu :deep(.el-menu-item.is-active) {
  background: #263445;
  color: #409eff;
}

.admin-header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left h2 {
  font-size: 18px;
  color: #333;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.admin-main {
  background: #f0f2f5;
  padding: 20px;
}

.dashboard-content {
  padding: 20px 0;
}

.stat-card {
  text-align: center;
  padding: 20px 0;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  margin-top: 10px;
  color: #666;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-actions {
  display: flex;
  align-items: center;
}

.el-form-item {
  margin-bottom: 15px;
}
</style>