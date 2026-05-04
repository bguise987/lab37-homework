<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const recipes = ref([])
const search = ref('')
const error = ref('')

const filtered = computed(() =>
  recipes.value.filter(r =>
    r.title.toLowerCase().includes(search.value.toLowerCase())
  )
)

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/recipes', {
      params: { company_id: auth.selectedCompanyId },
      headers: auth.authHeaders(),
    })
    recipes.value = data
  } catch {
    error.value = 'Failed to load recipes.'
  }
})

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="page">
    <header>
      <div class="title-group">
        <h1>Recipes</h1>
        <span class="company-name">{{ auth.selectedCompany?.name }}</span>
      </div>
      <div class="header-actions">
        <button v-if="auth.companies.length > 1" class="btn-ghost" @click="router.push('/select-company')">
          Switch company
        </button>
        <button class="btn-secondary" @click="router.push('/recipes/new')">+ New Recipe</button>
        <span class="username">{{ auth.username }}</span>
        <button class="btn-ghost" @click="handleLogout">Sign out</button>
      </div>
    </header>

    <input v-model="search" class="search" placeholder="Search recipes…" />

    <p v-if="error" class="error">{{ error }}</p>

    <ul v-if="filtered.length" class="recipe-list">
      <li v-for="r in filtered" :key="r.id" @click="router.push(`/recipes/${r.id}`)">
        <span class="title">{{ r.title }}</span>
        <span class="yield" v-if="r.yield_grams">{{ r.yield_grams }}g</span>
      </li>
    </ul>
    <p v-else-if="!error" class="empty">No recipes found.</p>
  </div>
</template>

<style scoped>
.page { max-width: 700px; margin: 2rem auto; padding: 0 1rem; }
header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; gap: 1rem; }
.title-group { display: flex; flex-direction: column; }
h1 { margin: 0; line-height: 1.2; }
.company-name { font-size: 0.85rem; color: #6b7280; margin-top: 0.1rem; }
.header-actions { display: flex; gap: 0.5rem; flex-shrink: 0; }
.search { width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; box-sizing: border-box; margin-bottom: 1rem; }
.recipe-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.5rem; }
.recipe-list li { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; background: #fff; border: 1px solid #e5e7eb; border-radius: 6px; cursor: pointer; }
.recipe-list li:hover { background: #f0f9ff; }
.title { font-weight: 500; }
.yield { font-size: 0.85rem; color: #6b7280; }
.empty { color: #6b7280; }
.error { color: #dc2626; }
button { padding: 0.45rem 0.9rem; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
.btn-secondary { background: #3b82f6; color: #fff; border: none; }
.btn-ghost { background: transparent; border: 1px solid #ccc; }
.username { font-size: 0.9rem; color: #6b7280; align-self: center; }
</style>
