import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userId = ref(Number(localStorage.getItem('userId')) || null)
  const username = ref(localStorage.getItem('username') || '')
  const companies = ref(JSON.parse(localStorage.getItem('companies') || '[]'))
  const selectedCompanyId = ref(Number(localStorage.getItem('selectedCompanyId')) || null)

  const selectedCompany = computed(() =>
    companies.value.find(c => c.id === selectedCompanyId.value) ?? null
  )

  async function login(usernameInput, passwordInput) {
    const { data } = await axios.post('/api/auth/login', { username: usernameInput, password: passwordInput })
    token.value = data.token
    userId.value = data.user_id
    username.value = data.username
    companies.value = data.companies
    localStorage.setItem('token', data.token)
    localStorage.setItem('userId', data.user_id)
    localStorage.setItem('username', data.username)
    localStorage.setItem('companies', JSON.stringify(data.companies))

    // Auto-select if only one company
    if (data.companies.length === 1) {
      selectCompany(data.companies[0].id)
    } else {
      selectedCompanyId.value = null
      localStorage.removeItem('selectedCompanyId')
    }
  }

  function selectCompany(id) {
    selectedCompanyId.value = id
    localStorage.setItem('selectedCompanyId', id)
  }

  async function logout() {
    try {
      await axios.post('/api/auth/logout', null, { headers: authHeaders() })
    } finally {
      token.value = ''
      userId.value = null
      username.value = ''
      companies.value = []
      selectedCompanyId.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('username')
      localStorage.removeItem('companies')
      localStorage.removeItem('selectedCompanyId')
    }
  }

  function authHeaders() {
    return { Authorization: `Bearer ${token.value}` }
  }

  return { token, userId, username, companies, selectedCompanyId, selectedCompany, login, selectCompany, logout, authHeaders }
})
