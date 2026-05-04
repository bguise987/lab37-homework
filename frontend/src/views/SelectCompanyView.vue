<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

function select(id) {
  auth.selectCompany(id)
  router.push('/')
}

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="page">
    <div class="card">
      <h1>Select a company</h1>
      <p class="subtitle">Choose which company's recipes you'd like to view.</p>

      <ul class="company-list">
        <li v-for="company in auth.companies" :key="company.id">
          <button class="company-btn" @click="select(company.id)">
            {{ company.name }}
          </button>
        </li>
      </ul>

      <div class="footer">
        <span class="username">{{ auth.username }}</span>
        <button class="btn-ghost" @click="handleLogout">Sign out</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f5f5;
}
.card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}
h1 { margin: 0 0 0.25rem; font-size: 1.4rem; }
.subtitle { margin: 0 0 1.5rem; color: #6b7280; font-size: 0.95rem; }
.company-list { list-style: none; padding: 0; margin: 0 0 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.company-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: left;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  font-weight: 500;
}
.company-btn:hover { background: #f0f9ff; border-color: #3b82f6; }
.footer { display: flex; align-items: center; gap: 0.75rem; }
.username { font-size: 0.9rem; color: #6b7280; }
.btn-ghost { background: transparent; border: 1px solid #ccc; padding: 0.45rem 0.9rem; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
</style>
