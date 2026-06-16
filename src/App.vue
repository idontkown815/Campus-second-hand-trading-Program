<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()

// 应用加载时，如果有 token 但没有用户信息，自动获取用户信息
onMounted(async () => {
  if (userStore.isLoggedIn && !userStore.user) {
    try {
      await userStore.getProfile()
    } catch (error) {
      console.error('自动获取用户信息失败:', error)
    }
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  min-height: 100vh;
}
</style>
