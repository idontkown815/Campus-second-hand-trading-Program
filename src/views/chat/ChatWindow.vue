<template>
  <el-drawer
    v-model="visible"
    title="联系卖家"
    direction="rtl"
    size="400px"
    :before-close="handleClose"
  >
    <div class="chat-container">
      <div class="product-info" v-if="product">
        <el-card shadow="hover">
          <div class="product-brief">
            <img v-if="product.images && product.images.length" :src="product.images[0]" class="product-image" />
            <div class="product-details">
              <h4>{{ product.title }}</h4>
              <p class="price">¥{{ product.price }}</p>
              <p class="seller">卖家：{{ sellerName }}</p>
            </div>
          </div>
        </el-card>
      </div>

      <div class="messages-container" ref="messagesContainer">
        <div v-if="loading" class="loading">
          <el-icon class="is-loading"><Loading /></el-icon>
          加载中...
        </div>
        <div v-else-if="messages.length === 0" class="no-messages">
          暂无消息，开始对话吧！
        </div>
        <div v-else class="message-list">
          <div
            v-for="msg in messages"
            :key="msg.id"
            :class="['message-item', msg.is_self ? 'self' : 'other']"
          >
            <div class="message-content">
              <div class="message-text">{{ msg.content }}</div>
              <div class="message-time">{{ formatTime(msg.created_at) }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <el-input
          v-model="messageContent"
          type="textarea"
          :rows="2"
          placeholder="输入消息..."
          @keyup.enter.ctrl="handleSend"
        />
        <el-button type="primary" @click="handleSend" :disabled="!messageContent.trim() || sending">
          发送
        </el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import api from '../../api'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  conversationId: {
    type: [Number, String],
    default: null
  },
  product: {
    type: Object,
    default: null
  },
  sellerId: {
    type: [Number, String],
    default: null
  },
  sellerName: {
    type: String,
    default: ''
  },
  isNewConversation: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'conversation-created'])

const visible = ref(false)
const messages = ref([])
const messageContent = ref('')
const loading = ref(false)
const sending = ref(false)
const messagesContainer = ref(null)
let refreshTimer = null

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    if (props.isNewConversation && props.conversationId) {
      loadMessages()
      startRefresh()
    } else if (props.conversationId) {
      loadMessages()
      startRefresh()
    }
  } else {
    stopRefresh()
  }
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const loadMessages = async () => {
  if (!props.conversationId) return

  loading.value = true
  try {
    const response = await api.getMessages(props.conversationId)
    if (response.data.code === 200) {
      messages.value = response.data.data.map(msg => ({
        ...msg,
        is_self: String(msg.sender_id) !== String(props.sellerId)
      }))
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载消息失败:', error)
    ElMessage.error('加载消息失败')
  } finally {
    loading.value = false
  }
}

const handleSend = async () => {
  const content = messageContent.value.trim()
  if (!content) return

  if (!props.conversationId) {
    ElMessage.warning('请先创建会话')
    return
  }

  sending.value = true
  try {
    const response = await api.sendMessage(props.conversationId, content)
    if (response.data.code === 200 || response.data.code === 201) {
      messageContent.value = ''
      await loadMessages()
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送消息失败')
  } finally {
    sending.value = false
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`

  return date.toLocaleString()
}

const startRefresh = () => {
  stopRefresh()
  refreshTimer = setInterval(() => {
    if (props.conversationId && visible.value) {
      loadMessages()
    }
  }, 5000)
}

const stopRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

const handleClose = () => {
  visible.value = false
  stopRefresh()
}

onUnmounted(() => {
  stopRefresh()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-info {
  margin-bottom: 15px;
}

.product-brief {
  display: flex;
  gap: 10px;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.product-details {
  flex: 1;
}

.product-details h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-details .price {
  color: #f56c6c;
  font-weight: bold;
  margin: 5px 0;
}

.product-details .seller {
  color: #666;
  font-size: 12px;
  margin: 0;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 8px;
  min-height: 300px;
  max-height: 400px;
}

.loading, .no-messages {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #999;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message-item {
  display: flex;
  max-width: 80%;
}

.message-item.self {
  align-self: flex-end;
}

.message-item.other {
  align-self: flex-start;
}

.message-content {
  padding: 10px 15px;
  border-radius: 12px;
  position: relative;
}

.message-item.self .message-content {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-item.other .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-text {
  word-break: break-word;
}

.message-time {
  font-size: 10px;
  margin-top: 5px;
  opacity: 0.7;
}

.input-container {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-container .el-textarea {
  flex: 1;
}
</style>
