<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
    <div class="bg-white rounded-2xl p-8 w-full max-w-md shadow-2xl">
      <h2 class="text-2xl font-bold mb-6 text-center text-primary">{{ isLogin ? '登录' : '注册' }}</h2>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-bold mb-2">用户名</label>
          <input v-model="username" type="text" required class="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none" />
        </div>
        
        <div>
          <label class="block text-sm font-bold mb-2">密码</label>
          <input v-model="password" type="password" required class="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none" />
        </div>
        
        <div v-if="error" class="text-red-500 text-sm text-center">{{ error }}</div>
        
        <button type="submit" class="w-full py-3 rounded-xl bg-primary text-white font-bold hover:bg-primary/90 transition-all">
          {{ isLogin ? '登录' : '注册' }}
        </button>
      </form>
      
      <div class="mt-4 text-center text-sm text-gray-500">
        {{ isLogin ? '还没有账号？' : '已有账号？' }}
        <button @click="toggleMode" class="text-primary font-bold hover:underline">
          {{ isLogin ? '去注册' : '去登录' }}
        </button>
      </div>
      
      <button @click="$emit('close')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">✕</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps(['isOpen'])
const emit = defineEmits(['close', 'login-success'])

const isLogin = ref(true)
const username = ref('')
const password = ref('')
const error = ref('')

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
}

const handleSubmit = async () => {
  error.value = ''
  try {
    if (isLogin.value) {
      const formData = new FormData()
      formData.append('username', username.value)
      formData.append('password', password.value)
      
      const res = await axios.post('/api/token', formData)
      localStorage.setItem('token', res.data.access_token)
      emit('login-success')
      emit('close')
    } else {
      await axios.post('/api/register', {
        username: username.value,
        password: password.value
      })
      // Auto login or switch to login
      isLogin.value = true
      error.value = '注册成功，请登录'
    }
  } catch (e) {
    error.value = e.response?.data?.detail || '操作失败'
  }
}
</script>
