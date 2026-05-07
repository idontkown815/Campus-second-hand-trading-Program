<template>
  <div class="publish-container">
    <el-card class="publish-card">
      <template #header>
        <div class="header-content">
          <h2>{{ isEditMode ? '编辑商品' : '发布商品' }}</h2>
          <el-steps :active="activeStep" process-status="wait" align-center>
            <el-step title="基本信息" />
            <el-step title="商品图片" />
            <el-step title="价格与库存" />
            <el-step title="发布确认" />
          </el-steps>
        </div>
      </template>
      <div v-if="!userStore.isLoggedIn" class="login-prompt">
        <el-empty description="请先登录后发布商品" />
        <el-button type="primary" @click="goToLogin">立即登录</el-button>
      </div>
      <div v-else>
        <!-- 步骤1：基本信息 -->
        <div v-show="activeStep === 0">
          <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
            <el-form-item label="商品标题" prop="title">
              <el-input v-model="form.title" placeholder="请输入商品标题" maxlength="100" show-word-limit />
              <div class="form-tip">建议标题简洁明了，突出商品特点</div>
            </el-form-item>
            <el-form-item label="商品描述" prop="description">
              <el-input v-model="form.description" type="textarea" :rows="6" placeholder="请输入商品描述" maxlength="2000" show-word-limit />
              <div class="form-tip">详细描述商品的成色、使用情况、优缺点等信息</div>
            </el-form-item>
            <el-form-item label="商品分类" prop="category">
              <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
                <el-option label="学习用具" value="学习用具" />
                <el-option label="数码产品" value="数码产品" />
                <el-option label="生活日用" value="生活日用" />
                <el-option label="服饰美妆" value="服饰美妆" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
            <el-form-item label="校区位置" prop="campus_location">
              <el-select v-model="form.campus_location" placeholder="请选择校区位置" style="width: 100%">
                <el-option label="成都校区" value="成都校区" />
                <el-option label="什邡校区" value="什邡校区" />
              </el-select>
            </el-form-item>
            <el-form-item label="楼栋位置" prop="building_location">
              <el-input v-model="form.building_location" placeholder="请输入楼栋位置" />
              <div class="form-tip">如：1栋、2栋等，方便买家取货</div>
            </el-form-item>
          </el-form>
          <div class="step-actions">
            <el-button @click="$router.back()">取消</el-button>
            <el-button type="primary" @click="nextStep">下一步</el-button>
          </div>
        </div>

        <!-- 步骤2：商品图片 -->
        <div v-show="activeStep === 1">
          <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
            <el-form-item label="商品图片" prop="images">
              <div class="image-upload">
                <div class="main-image-tip">
                  <el-icon><Picture /></el-icon>
                  <span>第一张图片将作为商品主图</span>
                </div>
                <el-upload
                  class="upload-demo"
                  action="/api/v1/products/upload/"
                  :headers="{ Authorization: `Bearer ${userStore.token}` }"
                  :on-success="handleUploadSuccess"
                  :on-error="handleUploadError"
                  :before-upload="beforeUpload"
                  :file-list="uploadedFiles"
                  multiple
                  :limit="9"
                  :on-exceed="handleExceed"
                  list-type="picture-card"
                  :auto-upload="true"
                >
                  <template #default>
                    <el-icon class="avatar-uploader-icon"><Plus /></el-icon>
                    <div class="el-upload__text">上传图片</div>
                  </template>
                  <template #file="{ file }">
                    <div class="image-item">
                      <img :src="file.url" alt="商品图片" />
                      <el-icon class="delete-icon" @click.stop="removeImage(file)"><Delete /></el-icon>
                    </div>
                  </template>
                </el-upload>
                <div v-if="form.image_list.length === 0" class="image-tip">请上传商品图片，最多9张</div>
                <div v-else class="image-count">{{ form.image_list.length }}/9</div>
              </div>
            </el-form-item>
          </el-form>
          <div class="step-actions">
            <el-button @click="prevStep">上一步</el-button>
            <el-button type="primary" @click="nextStep">下一步</el-button>
          </div>
        </div>

        <!-- 步骤3：价格与库存 -->
        <div v-show="activeStep === 2">
          <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
            <el-form-item label="商品价格" prop="price">
              <el-input v-model="form.price" placeholder="请输入价格" type="number" min="0" step="0.01">
                <template #prefix>¥</template>
              </el-input>
              <div class="form-tip">请输入合理的价格</div>
            </el-form-item>
            <el-form-item label="商品库存" prop="stock">
              <el-input v-model="form.stock" placeholder="请输入库存" type="number" min="1" />
              <div class="form-tip">默认为1，适用于二手商品</div>
            </el-form-item>
          </el-form>
          <div class="step-actions">
            <el-button @click="prevStep">上一步</el-button>
            <el-button type="primary" @click="nextStep">下一步</el-button>
          </div>
        </div>

        <!-- 步骤4：发布确认 -->
        <div v-show="activeStep === 3">
          <div class="confirm-section">
            <h3>发布确认</h3>
            <el-divider />
            <div class="confirm-item">
              <span class="label">商品标题：</span>
              <span class="value">{{ form.title }}</span>
            </div>
            <div class="confirm-item">
              <span class="label">商品分类：</span>
              <span class="value">{{ form.category }}</span>
            </div>
            <div class="confirm-item">
              <span class="label">商品价格：</span>
              <span class="value">¥{{ form.price }}</span>
            </div>
            <div class="confirm-item">
              <span class="label">校区位置：</span>
              <span class="value">{{ form.campus_location }} - {{ form.building_location }}</span>
            </div>
            <div class="confirm-item">
              <span class="label">商品图片：</span>
              <div class="image-preview">
                <img v-for="(img, index) in form.image_list" :key="index" :src="'/uploads/' + img" alt="预览图片" />
              </div>
            </div>
            <el-divider />
            <div class="publish-tip">
              <el-icon><Warning /></el-icon>
              <span>发布后，商品将在平台上展示，您可以在"我的发布"中管理商品</span>
            </div>
          </div>
          <div class="step-actions">
            <el-button @click="prevStep">上一步</el-button>
            <el-button type="primary" @click="handlePublish" :loading="loading">发布商品</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useProductStore } from '../../stores/product'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'
import { Delete, Plus, Picture, Warning } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const productStore = useProductStore()
const userStore = useUserStore()

const productId = computed(() => route.query.id)
const isEditMode = computed(() => !!productId.value)

const activeStep = ref(0)

const form = ref({
  title: '',
  description: '',
  price: '',
  stock: 1,
  category: null,
  campus_location: '',
  building_location: '',
  image_list: []
})

const rules = {
  title: [
    { required: true, message: '请输入商品标题', trigger: 'blur' },
    { max: 100, message: '标题最多100个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入商品描述', trigger: 'blur' },
    { max: 2000, message: '描述最多2000个字符', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存', trigger: 'blur' },
    { type: 'number', min: 1, message: '库存至少为1', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  campus_location: [
    { required: true, message: '请输入校区位置', trigger: 'blur' }
  ],
  building_location: [
    { required: true, message: '请输入楼栋位置', trigger: 'blur' }
  ],
  image_list: [
    { required: true, message: '请上传商品图片', trigger: 'change' }
  ]
}

const formRef = ref(null)
const loading = ref(false)
const uploadedFiles = ref([])

const loadProductDetail = async () => {
  if (!isEditMode.value) return
  
  try {
    const product = await productStore.fetchProduct(productId.value)
    // 提取文件名列表（不带 /uploads/ 前缀）
    const imageNames = (product.images || []).map(url => url.split('/').pop())
    form.value = {
      title: product.title,
      description: product.description,
      category: product.category,
      campus_location: product.campus_location,
      building_location: product.building_location,
      price: product.price,
      stock: product.stock,
      image_list: imageNames
    }
    // 转换图片路径为上传组件需要的格式
    uploadedFiles.value = (product.images || []).map(url => {
      return {
        name: url.split('/').pop(),
        url: url
      }
    })
  } catch (error) {
    console.error(error)
    ElMessage.error('加载商品信息失败')
  }
}

const handleUploadSuccess = (response, uploadFile) => {
  if (response && response.data && response.data.url) {
    // 存储相对路径到form.image_list
    form.value.image_list.push(response.data.url)
    // 为el-upload组件设置完整的预览路径
    uploadFile.url = '/uploads/' + response.data.url
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error('图片上传失败')
  }
}

const handleUploadError = (error) => {
  console.error(error)
  ElMessage.error('图片上传失败')
}

const beforeUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('只能上传JPG、PNG、GIF格式的图片')
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB')
  }
  return isJPG && isLt2M
}

const handleExceed = () => {
  ElMessage.warning('最多只能添加9张图片')
}

const removeImage = (file) => {
  let filename = file.name
  // 如果是编辑模式已有图片，form.image_list中存储的是完整路径
  // 需要从file.url中提取文件名
  if (isEditMode.value && file.url && file.url.includes('/uploads/')) {
    filename = file.url.split('/uploads/').pop()
  }
  
  // 从form.image_list中删除
  const fullPath = '/uploads/' + filename
  const index = form.value.image_list.indexOf(filename)
  const fullPathIndex = form.value.image_list.indexOf(fullPath)
  
  if (index !== -1) {
    form.value.image_list.splice(index, 1)
  } else if (fullPathIndex !== -1) {
    form.value.image_list.splice(fullPathIndex, 1)
  }
  
  // 从uploadedFiles中删除
  const uploadedIndex = uploadedFiles.value.findIndex(f => f.name === filename || f.url === file.url)
  if (uploadedIndex !== -1) {
    uploadedFiles.value.splice(uploadedIndex, 1)
  }
}

const goToLogin = () => {
  router.push('/login')
}

const nextStep = async () => {
  // 验证当前步骤的必填字段
  if (activeStep.value === 0) {
    const valid = await formRef.value.validateField(['title', 'description', 'category', 'campus_location', 'building_location']).catch(() => false)
    if (!valid) return
  } else if (activeStep.value === 1) {
    const valid = await formRef.value.validateField('image_list').catch(() => false)
    if (!valid) return
  } else if (activeStep.value === 2) {
    const valid = await formRef.value.validateField(['price', 'stock']).catch(() => false)
    if (!valid) return
  }
  
  activeStep.value++
}

const prevStep = () => {
  if (activeStep.value > 0) {
    activeStep.value--
  }
}

const handlePublish = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    ElMessage.error('表单验证失败，请检查填写的信息')
    return
  }

  loading.value = true
  try {
    const productData = {
      title: form.value.title,
      description: form.value.description,
      price: parseFloat(form.value.price),
      stock: parseInt(form.value.stock),
      category: form.value.category,
      image_list: form.value.image_list,
      campus_location: form.value.campus_location,
      building_location: form.value.building_location
    }
    
    console.log('准备发送的商品数据:', productData)
    
    if (isEditMode.value) {
      await productStore.updateProduct(productId.value, productData)
      ElMessage.success('修改成功')
    } else {
      await productStore.createProduct(productData)
      ElMessage.success('发布成功')
    }
    router.push('/my/products')
  } catch (error) {
    console.error('发布失败详情:', error)
    console.error('错误响应:', error.response?.data)
    const errorMsg = error.response?.data?.message || (isEditMode.value ? '修改失败' : '发布失败')
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 无需获取分类，使用固定分类选项
  if (isEditMode.value) {
    loadProductDetail()
  }
})
</script>

<style scoped>
.publish-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.publish-card {
  width: 800px;
  max-width: 100%;
}

.header-content {
  text-align: center;
  margin-bottom: 20px;
}

.header-content h2 {
  margin-bottom: 20px;
  color: #333;
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.image-upload {
  width: 100%;
}

.main-image-tip {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.main-image-tip el-icon {
  margin-right: 5px;
}

.image-item {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ddd;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-item .delete-icon {
  position: absolute;
  top: 2px;
  right: 2px;
  font-size: 16px;
  color: #fff;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  padding: 2px;
  cursor: pointer;
}

.image-tip {
  color: #999;
  font-size: 14px;
  text-align: center;
  padding: 20px;
  border: 1px dashed #ddd;
  border-radius: 8px;
}

.image-count {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

.step-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.confirm-section {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.confirm-section h3 {
  margin-bottom: 15px;
  color: #333;
}

.confirm-item {
  margin-bottom: 15px;
  display: flex;
  align-items: flex-start;
}

.confirm-item .label {
  width: 100px;
  font-weight: bold;
  color: #666;
}

.confirm-item .value {
  flex: 1;
  color: #333;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 5px;
}

.image-preview img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.publish-tip {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  color: #856404;
  margin-top: 10px;
}

.publish-tip el-icon {
  margin-right: 10px;
}

.login-prompt {
  text-align: center;
  padding: 40px 20px;
}

.login-prompt .el-button {
  margin-top: 20px;
}
</style>
