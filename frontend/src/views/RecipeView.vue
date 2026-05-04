<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const recipe = ref(null)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await axios.get(`/api/recipes/${route.params.id}`, { headers: auth.authHeaders() })
    recipe.value = data
  } catch {
    error.value = 'Recipe not found or access denied.'
  }
})
</script>

<template>
  <div class="page">
    <nav>
      <button class="btn-ghost" @click="router.push('/')">← Back</button>
    </nav>

    <p v-if="error" class="error">{{ error }}</p>

    <template v-if="recipe">
      <div class="title-row">
        <h1>{{ recipe.title }}</h1>
        <button class="btn-secondary" @click="router.push(`/recipes/${recipe.id}/edit`)">Edit</button>
      </div>

      <p v-if="recipe.yield_grams" class="yield">Yield: {{ recipe.yield_grams }}g</p>

      <section>
        <h2>Ingredients</h2>
        <ul class="ingredient-list">
          <li v-for="(ingredient, index) in recipe.ingredients.split('\n').filter(Boolean)" :key="index">
            <span class="bin-label">Bin {{ index + 1 }}</span>
            {{ ingredient }}
          </li>
        </ul>
      </section>

      <section>
        <h2>Instructions</h2>
        <pre>{{ recipe.instructions }}</pre>
      </section>
    </template>
  </div>
</template>

<style scoped>
.page { max-width: 700px; margin: 2rem auto; padding: 0 1rem; }
nav { margin-bottom: 1.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
h1 { margin: 0 0 0.25rem; }
.yield { color: #6b7280; margin: 0 0 1.5rem; }
section { margin-bottom: 1.5rem; }
h2 { font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; color: #6b7280; margin-bottom: 0.5rem; }
pre { white-space: pre-wrap; margin: 0; font-family: inherit; background: #f9fafb; padding: 0.75rem; border-radius: 6px; border: 1px solid #e5e7eb; }
.ingredient-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.35rem; }
.ingredient-list li { display: flex; align-items: baseline; gap: 0.6rem; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 6px; padding: 0.5rem 0.75rem; }
.bin-label { font-size: 0.75rem; font-weight: 700; color: #6b7280; white-space: nowrap; min-width: 3rem; }
.error { color: #dc2626; }
button { padding: 0.45rem 0.9rem; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
.btn-secondary { background: #3b82f6; color: #fff; border: none; }
.btn-ghost { background: transparent; border: 1px solid #ccc; }
</style>
