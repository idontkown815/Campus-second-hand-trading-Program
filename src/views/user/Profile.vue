<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <h2>个人信息</h2>
      </template>
      <div v-if="!userStore.isLoggedIn" class="login-prompt">
        <el-empty description="请先登录" />
        <el-button type="primary" @click="goToLogin">立即登录</el-button>
      </div>
      <el-form v-else :model="form" :rules="rules" ref="formRef" label-width="100px" :disabled="!isEditing">
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="form.student_id" disabled />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" disabled />
        </el-form-item>
        <el-form-item label="年级" prop="grade">
          <el-input v-model="form.grade" placeholder="请输入年级" />
        </el-form-item>
        <el-form-item label="专业" prop="major">
          <el-input v-model="form.major" placeholder="请输入专业" />
        </el-form-item>
        <el-form-item>
          <el-button v-if="!isEditing" type="primary" @click="isEditing = true">
            编辑资料
          </el-button>
          <template v-else>
            <el-button type="primary" @click="handleSave" :loading="loading">
              保存
            </el-button>
            <el-button @click="handleCancel">
              取消
            </el-button>
          </template>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  student_id: '',
  name: '',
  grade: '',
  major: ''
})

const originalForm = ref({})

const rules = {
  name: [{ required: false, message: '请输入姓名', trigger: 'blur' }],
  grade: [{ required: false, message: '请输入年级', trigger: 'blur' }],
  major: [{ required: false, message: '请输入专业', trigger: 'blur' }]
}

const formRef = ref(null)
const loading = ref(false)
const isEditing = ref(false)

const goToLogin = () => {
  router.push('/login')
}

const fetchProfile = async () => {
  if (userStore.isLoggedIn) {
    try {
      const user = await userStore.getProfile()
      form.value = {
        student_id: user.student_id || '',
        name: user.name || '',
        grade: user.grade || '',
        major: user.major || ''
      }
      originalForm.value = { ...form.value }
    } catch (error) {
      console.error(error)
      ElMessage.error('获取个人信息失败')
    }
  }
}

const handleSave = async () => {
  loading.value = true
  try {
    await userStore.updateProfile({
      name: form.value.name,
      grade: form.value.grade,
      major: form.value.major
    })
    ElMessage.success('更新成功')
    isEditing.value = false
    originalForm.value = { ...form.value }
  } catch (error) {
    console.error(error)
    ElMessage.error('更新失败')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  form.value = { ...originalForm.value }
  isEditing.value = false
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.profile-card {
  width: 500px;
}

.profile-card h2 {
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
</style>
