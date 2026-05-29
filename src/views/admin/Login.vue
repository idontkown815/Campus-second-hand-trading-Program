<template>
  <div class="admin-login-container">
    <el-card class="admin-login-card">
      <template #header>
        <h2>校园二手交易平台</h2>
        <p>管理员登录</p>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="form.student_id" placeholder="请输入管理员学号" maxlength="8" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">
            登录
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="primary" @click="$router.push('/login')">返回用户登录</el-link>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  student_id: '',
  password: ''
})

const rules = {
  student_id: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { min: 8, max: 8, message: '学号必须为8位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const loading = ref(false)

const handleLogin = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const response = await userStore.login(form.value.student_id, form.value.password)
    const isAdmin = response.data?.is_admin

    if (!isAdmin) {
      userStore.logout()
      ElMessage.error('您不是管理员，无权访问后台管理系统')
      return
    }

    ElMessage.success('管理员登录成功')
    router.push('/admin')
  } catch (error) {
    console.error(error)
    ElMessage.error('学号或密码错误，请检查后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('/uploads/materials/background.jpg') no-repeat center center fixed;
  background-size: cover;
}

.admin-login-card {
  width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.admin-login-card h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

.admin-login-card p {
  text-align: center;
  color: #666;
}
</style>
