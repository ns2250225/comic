<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
    <div class="bg-white rounded-2xl p-6 w-full max-w-4xl shadow-2xl h-[80vh] flex flex-col">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-primary">用户管理</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">✕</button>
      </div>
      
      <div class="overflow-auto flex-1">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-gray-100">
              <th class="p-4 font-bold text-gray-600">ID</th>
              <th class="p-4 font-bold text-gray-600">用户名</th>
              <th class="p-4 font-bold text-gray-600">积分</th>
              <th class="p-4 font-bold text-gray-600">IP</th>
              <th class="p-4 font-bold text-gray-600">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="border-b border-gray-50 hover:bg-gray-50">
              <td class="p-4">{{ user.id }}</td>
              <td class="p-4">
                {{ user.username }}
                <span v-if="user.is_admin" class="ml-2 px-2 py-0.5 bg-purple-100 text-purple-600 text-xs rounded-full">管理员</span>
              </td>
              <td class="p-4">{{ user.points }}</td>
              <td class="p-4 text-gray-400 text-sm">{{ user.registration_ip }}</td>
              <td class="p-4">
                <button @click="editPoints(user)" class="text-primary font-bold hover:underline">修改积分</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Edit Points Modal -->
    <div v-if="editingUser" class="fixed inset-0 bg-black/20 flex items-center justify-center z-[60]">
      <div class="bg-white rounded-xl p-6 w-80 shadow-xl">
        <h3 class="font-bold mb-4">修改 {{ editingUser.username }} 的积分</h3>
        <input v-model.number="newPoints" type="number" class="w-full p-2 border rounded mb-4" />
        <div class="flex justify-end gap-2">
          <button @click="editingUser = null" class="px-4 py-2 text-gray-500">取消</button>
          <button @click="savePoints" class="px-4 py-2 bg-primary text-white rounded">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps(['isOpen'])
const emit = defineEmits(['close'])

const users = ref([])
const editingUser = ref(null)
const newPoints = ref(0)

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/admin/users', {
      headers: { Authorization: `Bearer ${token}` }
    })
    users.value = res.data
  } catch (e) {
    alert('获取用户列表失败')
  }
}

const editPoints = (user) => {
  editingUser.value = user
  newPoints.value = user.points
}

const savePoints = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.post(`/api/admin/users/${editingUser.value.id}/points`, 
      { points: newPoints.value },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    editingUser.value = null
    fetchUsers()
  } catch (e) {
    alert('修改失败')
  }
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) fetchUsers()
})
</script>
