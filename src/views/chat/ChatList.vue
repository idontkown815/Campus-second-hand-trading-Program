<template>
  <div class="chat-list-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>校园二手交易平台</h1>
          <div class="header-nav">
            <el-button type="text" @click="$router.push('/')">首页</el-button>
            <el-button type="text" @click="$router.push('/products')">商品</el-button>
            <el-button type="text" @click="$router.push('/messages')" v-if="userStore.isLoggedIn">消息</el-button>
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
        <div class="chat-list-section">
          <div class="section-title-row">
            <h2>我的消息</h2>
            <div class="unread-info" v-if="totalUnreadCount > 0">
              <el-badge :value="totalUnreadCount" type="danger" />
              <span class="unread-text">条未读消息</span>
            </div>
          </div>
          <div v-if="loading" class="loading-container">
            <el-icon class="is-loading"><Loading /></el-icon>
            加载中...
          </div>
          <div v-else-if="conversations.length === 0" class="empty-container">
            <el-empty description="暂无消息">
              <el-button type="primary" @click="$router.push('/products')">去逛逛商品</el-button>
            </el-empty>
          </div>
          <div v-else class="conversation-list">
            <el-card
              v-for="conv in conversations"
              :key="conv.id"
              class="conversation-card"
              @click="openChat(conv)"
            >
              <div class="conversation-content">
                <div class="product-image">
                  <img v-if="conv.product_images && conv.product_images.length" :src="conv.product_images[0]" />
                  <div v-else class="image-placeholder">暂无图片</div>
                </div>
                <div class="conversation-info">
                  <div class="product-title">{{ conv.product_title || '商品' }}</div>
                  <div class="last-message" :class="{ 'unread': conv.unread_count > 0 }">
                    {{ conv.last_message_content || '暂无消息' }}
                  </div>
                  <div class="conversation-meta">
                    <span class="participants">{{ conv.other_participant }}</span>
                    <span class="time">{{ formatTime(conv.updated_at) }}</span>
                  </div>
                </div>
                <div v-if="conv.unread_count > 0" class="conversation-unread">
                  <el-badge :value="conv.unread_count > 99 ? '99+' : conv.unread_count" type="danger" />
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-main>
    </el-container>

    <ChatWindow
      v-model="chatWindowVisible"
      :conversation-id="currentConversationId"
      :product="currentProduct"
      :seller-id="currentSellerId"
      :seller-name="currentSellerName"
      @closed="refreshUnreadCount"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import ChatWindow from './ChatWindow.vue'
import api from '../../api'

const router = useRouter()
const userStore = useUserStore()

const conversations = ref([])
const loading = ref(false)
const totalUnreadCount = ref(0)
const chatWindowVisible = ref(false)
const currentConversationId = ref(null)
const currentProduct = ref(null)
const currentSellerId = ref(null)
const currentSellerName = ref('')

const loadUnreadCount = async () => {
  if (!userStore.isLoggedIn) return
  
  try {
    const response = await api.getUnreadCount()
    if (response.data.code === 200) {
      totalUnreadCount.value = response.data.data.unread_count
      console.log('未读消息数:', totalUnreadCount.value)
    }
  } catch (error) {
    console.error('加载未读消息数失败:', error)
  }
}

// 刷新未读消息数（在查看消息后调用）
const refreshUnreadCount = () => {
  loadUnreadCount()
  loadConversations()
}

const loadConversations = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  loading.value = true
  try {
    const response = await api.getConversations()
    if (response.data.code === 200) {
      conversations.value = response.data.data.map(conv => {
        const otherParticipant = conv.participants.find(p => p.id !== userStore.user?.id)
        return {
          ...conv,
          other_participant: otherParticipant?.name || otherParticipant?.username || '未知用户',
          product_title: conv.product?.title || '',
          product_images: conv.product?.images || [],
          last_message_content: conv.last_message?.content || ''
        }
      })
    }
  } catch (error) {
    console.error('加载会话列表失败:', error)
    ElMessage.error('加载会话列表失败')
  } finally {
    loading.value = false
  }
}

const openChat = (conv) => {
  currentConversationId.value = conv.id
  currentProduct.value = {
    id: conv.product?.id,
    title: conv.product?.title,
    price: conv.product?.price,
    images: conv.product?.images || []
  }
  const otherParticipant = conv.participants.find(p => p.id !== userStore.user?.id)
  currentSellerId.value = otherParticipant?.id
  currentSellerName.value = otherParticipant?.name || otherParticipant?.username || '未知用户'
  chatWindowVisible.value = true
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`

  return date.toLocaleDateString()
}

const goToMy = () => {
  router.push('/my')
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

onMounted(() => {
  loadConversations()
  loadUnreadCount()
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

.chat-list-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.chat-list-section {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.chat-list-section h2 {
  margin-bottom: 20px;
  color: #333;
}

.section-title-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.section-title-row h2 {
  margin-bottom: 0;
}

.unread-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: #fef0f0;
  border-radius: 20px;
  border: 1px solid #fde2e2;
}

.unread-text {
  font-size: 14px;
  color: #f56c6c;
  font-weight: 500;
}

.unread-badge {
  font-size: 14px;
}

.loading-container, .empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.conversation-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.conversation-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.conversation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.conversation-content {
  display: flex;
  gap: 15px;
  align-items: center;
}

.conversation-unread {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 30px;
}

.last-message.unread {
  color: #f56c6c;
  font-weight: 500;
}

.product-image {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 12px;
  border-radius: 4px;
}

.conversation-info {
  flex: 1;
  overflow: hidden;
}

.product-title {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.last-message {
  color: #666;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 5px;
}

.conversation-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.unread-badge {
  background: #f56c6c;
  color: white;
  border-radius: 50%;
  min-width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  padding: 0 6px;
}
</style>
