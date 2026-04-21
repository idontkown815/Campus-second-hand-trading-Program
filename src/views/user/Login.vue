<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>校园二手交易平台</h2>
        <p>用户登录</p>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="form.student_id" placeholder="请输入学号" maxlength="8" />
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
          <el-link type="primary" @click="$router.push('/register')">没有账号？去注册</el-link>
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
    { len: 8, message: '学号必须为8位', trigger: 'blur' }
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
    await userStore.login(form.value.student_id, form.value.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error(error)
    ElMessage.error('学号或密码错误，请检查后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
}

.login-card h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

.login-card p {
  text-align: center;
  color: #666;
}
</style>
