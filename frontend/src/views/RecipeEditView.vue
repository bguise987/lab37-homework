<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import IngredientList from '../components/IngredientList.vue'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const isNew = computed(() => route.params.id === undefined)
const title = ref('')
const ingredientList = ref([])
const instructions = ref('')
const yieldGrams = ref('')
const companyId = ref(null)
const error = ref('')
const saving = ref(false)
const deleting = ref(false)

function parseIngredients(raw) {
  return raw.split('\n').map(s => s.trim()).filter(Boolean)
}

function serializeIngredients(list) {
  return list.filter(s => s.trim()).join('\n')
}

onMounted(async () => {
  if (isNew.value) return
  try {
    const { data } = await axios.get(`/api/recipes/${route.params.id}`, { headers: auth.authHeaders() })
    title.value = data.title
    ingredientList.value = parseIngredients(data.ingredients)
    instructions.value = data.instructions
    yieldGrams.value = data.yield_grams ?? ''
    companyId.value = data.company_id
  } catch {
    error.value = 'Recipe not found or access denied.'
  }
})

async function save() {
  error.value = ''
  saving.value = true
  const payload = {
    title: title.value,
    ingredients: serializeIngredients(ingredientList.value),
    instructions: instructions.value,
    yield_grams: yieldGrams.value !== '' ? Number(yieldGrams.value) : null,
    company_id: isNew.value ? auth.selectedCompanyId : companyId.value,
  }
  try {
    if (isNew.value) {
      const { data } = await axios.post('/api/recipes', payload, { headers: auth.authHeaders() })
      router.push(`/recipes/${data.id}`)
    } else {
      await axios.put(`/api/recipes/${route.params.id}`, payload, { headers: auth.authHeaders() })
      router.push(`/recipes/${route.params.id}`)
    }
  } catch (e) {
    error.value = e.response?.data?.detail ?? 'Failed to save recipe.'
  } finally {
    saving.value = false
  }
}

async function remove() {
  if (!confirm('Delete this recipe? This cannot be undone.')) return
  deleting.value = true
  try {
    await axios.delete(`/api/recipes/${route.params.id}`, { headers: auth.authHeaders() })
    router.push('/')
  } catch {
    error.value = 'Failed to delete recipe.'
    deleting.value = false
  }
}
</script>

<template>
  <div class="page">
    <nav>
      <button class="btn-ghost" @click="router.back()">← Back</button>
    </nav>

    <h1>{{ isNew ? 'New Recipe' : 'Edit Recipe' }}</h1>
    <p v-if="error" class="error">{{ error }}</p>

    <form @submit.prevent="save">
      <label>
        Title
        <input v-model="title" type="text" required />
      </label>

      <label>
        Yield (grams)
        <input v-model="yieldGrams" type="number" min="0" step="any" placeholder="optional" />
      </label>

      <div class="field">
        <span class="field-label">Ingredients</span>
        <IngredientList v-model="ingredientList" />
      </div>

      <label>
        Instructions
        <textarea v-model="instructions" rows="10" required placeholder="One step per line" />
      </label>

      <div class="actions">
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? 'Saving…' : 'Save' }}
        </button>
        <button
          v-if="!isNew"
          type="button"
          class="btn-danger"
          :disabled="deleting"
          @click="remove"
        >
          {{ deleting ? 'Deleting…' : 'Delete' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.page { max-width: 700px; margin: 2rem auto; padding: 0 1rem; }
nav { margin-bottom: 1.5rem; }
h1 { margin: 0 0 1rem; }
form { display: flex; flex-direction: column; gap: 1rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.9rem; font-weight: 600; }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.field-label { font-size: 0.9rem; font-weight: 600; }
input, textarea { padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; font-family: inherit; resize: vertical; }
.actions { display: flex; gap: 0.75rem; margin-top: 0.5rem; }
button { padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-size: 0.95rem; }
.btn-primary { background: #3b82f6; color: #fff; border: none; }
.btn-danger { background: #dc2626; color: #fff; border: none; }
.btn-ghost { background: transparent; border: 1px solid #ccc; }
button:disabled { opacity: 0.6; cursor: default; }
.error { color: #dc2626; }
</style>
