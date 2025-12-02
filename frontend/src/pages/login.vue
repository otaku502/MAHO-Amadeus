<template>
  <div class="login">
    <h1>Login Page</h1>
    <input type="text" v-model="username" placeholder="用户名" />
    <input type="password" v-model="password" placeholder="密码" />
    <button @click="login">登录</button>
    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMsg = ref('')

async function login() {
  try {
    const response = await fetch('http://localhost:8080/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('token', data.token)
      localStorage.setItem('username', data.username)
      console.log('登录成功')
      router.push({ name: 'Home' })
    } else {
      const error = await response.json()
      errorMsg.value = error.detail || '登录失败'
    }
  } catch (e) {
    console.error('登录请求失败', e)
    errorMsg.value = '网络错误，请稍后重试'
  }
}
</script>

<style scoped></style>