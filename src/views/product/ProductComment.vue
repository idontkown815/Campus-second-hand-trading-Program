<template>
  <div class="comments-section">
    <h3>商品评论</h3>

    <div class="comment-input" v-if="userStore.isLoggedIn">
      <el-input
        v-model="newComment"
        type="textarea"
        placeholder="请输入评论内容..."
        :rows="3"
        maxlength="500"
        show-word-limit
      />
      <el-button type="primary" @click="submitComment" :loading="submitting" class="submit-btn">
        发布评论
      </el-button>
    </div>

    <div v-else class="login-tip">
      <el-link type="primary" @click="$router.push('/login')">登录</el-link>后可发表评论
    </div>

    <div class="comments-list" v-if="comments.length > 0">
      <div class="comment-item" v-for="comment in comments" :key="comment.id">
        <div class="comment-header">
          <div class="comment-user">
            <span class="user-name">{{ comment.user }}</span>
            <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
          </div>
          <div class="comment-actions" v-if="canDelete(comment)">
            <el-button type="danger" size="small" link @click="handleDelete(comment.id)">
              删除
            </el-button>
          </div>
        </div>
        <div class="comment-content">{{ comment.content }}</div>
      </div>
    </div>

    <el-empty v-else description="暂无评论，快来抢沙发吧~" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import api from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  productId: {
    type: Number,
    required: true
  },
  productOwnerId: {
    type: Number,
    required: true
  }
})

const userStore = useUserStore()
const comments = ref([])
const newComment = ref('')
const submitting = ref(false)

// 调试信息 - 组件初始化时打印
console.log('ProductComment 组件初始化:', {
  productId: props.productId,
  productOwnerId: props.productOwnerId,
  userStoreIsLoggedIn: userStore.isLoggedIn,
  userStoreUser: userStore.user
})

const loadComments = async () => {
  try {
    console.log('开始加载评论，productId:', props.productId)
    const response = await api.getComments(props.productId)
    console.log('评论接口响应:', response.data)
    if (response.data.code === 200) {
      comments.value = response.data.data || []
      console.log('评论数据:', comments.value)
    }
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  if (newComment.value.length > 500) {
    ElMessage.warning('评论内容不能超过500字')
    return
  }

  submitting.value = true
  try {
    const response = await api.addComment({
      product: props.productId,
      content: newComment.value.trim()
    })

    if (response.data.code === 200) {
      ElMessage.success('评论成功')
      newComment.value = ''
      await loadComments()
    }
  } catch (error) {
    console.error('评论失败:', error)
    const errorMsg = error.response?.data?.message || error.response?.data?.errors || '评论失败，请稍后重试'
    ElMessage.error(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg))
  } finally {
    submitting.value = false
  }
}

const canDelete = (comment) => {
  if (!userStore.isLoggedIn) return false
  const currentUserId = Number(userStore.user?.id)
  const commentUserId = Number(comment.user_id)
  const productOwnerId = Number(props.productOwnerId)
  const isCommentOwner = currentUserId === commentUserId
  const isProductOwner = currentUserId === productOwnerId
  
  // 调试信息
  console.log('删除权限检查:', {
    currentUserId,
    commentUserId,
    productOwnerId,
    isCommentOwner,
    isProductOwner
  })
  
  return isCommentOwner || isProductOwner
}

const handleDelete = async (commentId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await api.deleteComment(commentId)
    if (response.data.code === 200) {
      ElMessage.success('删除成功')
      await loadComments()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除评论失败:', error)
    }
  }
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
  if (diff < 604800000) return Math.floor(diff / 86400000) + '天前'

  return date.toLocaleDateString()
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.comments-section {
  margin-top: 30px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}

.comments-section h3 {
  margin-bottom: 20px;
  color: #333;
  font-size: 18px;
}

.comment-input {
  margin-bottom: 20px;
}

.submit-btn {
  margin-top: 10px;
  float: right;
}

.login-tip {
  text-align: center;
  padding: 20px;
  color: #999;
  background: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 20px;
}

.comments-list {
  clear: both;
}

.comment-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-name {
  font-weight: bold;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-content {
  color: #666;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>
