<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch {
    error.value = 'Invalid username or password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Recipe Manager</h1>
      <form @submit.prevent="submit">
        <label>
          Username
          <input v-model="username" type="text" autocomplete="username" required />
        </label>
        <label>
          Password
          <input v-model="password" type="password" autocomplete="current-password" required />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f5f5;
}
.login-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 360px;
}
h1 { margin-top: 0; font-size: 1.5rem; }
form { display: flex; flex-direction: column; gap: 1rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.9rem; font-weight: 600; }
input { padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
button { padding: 0.6rem; background: #3b82f6; color: #fff; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: default; }
.error { color: #dc2626; margin: 0; font-size: 0.9rem; }
</style>
