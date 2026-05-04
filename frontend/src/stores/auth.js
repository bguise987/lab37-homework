import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userId = ref(Number(localStorage.getItem('userId')) || null)

  async function login(username, password) {
    const { data } = await axios.post('/api/auth/login', { username, password })
    token.value = data.token
    userId.value = data.user_id
    localStorage.setItem('token', data.token)
    localStorage.setItem('userId', data.user_id)
  }

  async function logout() {
    try {
      await axios.post('/api/auth/logout', null, { headers: authHeaders() })
    } finally {
      token.value = ''
      userId.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
    }
  }

  function authHeaders() {
    return { Authorization: `Bearer ${token.value}` }
  }

  return { token, userId, login, logout, authHeaders }
})
