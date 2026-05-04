<script setup>
import { ref } from 'vue'

const MAX_INGREDIENTS = 20

const list = defineModel({ default: [] })

const dragIndex = ref(null)
const dragOverIndex = ref(null)

function add() {
  if (list.value.length >= MAX_INGREDIENTS) return
  list.value = [...list.value, '']
}

function remove(index) {
  list.value = list.value.filter((_, i) => i !== index)
}

function update(index, value) {
  const next = [...list.value]
  next[index] = value
  list.value = next
}

function onDragStart(e, index) {
  dragIndex.value = index
  if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move'
}

function onDragOver(e, index) {
  e.preventDefault()
  if (e.dataTransfer) e.dataTransfer.dropEffect = 'move'
  dragOverIndex.value = index
}

function onDrop(e, index) {
  e.preventDefault()
  if (dragIndex.value === null || dragIndex.value === index) return
  const next = [...list.value]
  const [moved] = next.splice(dragIndex.value, 1)
  next.splice(index, 0, moved)
  list.value = next
  dragIndex.value = null
  dragOverIndex.value = null
}

function onDragEnd() {
  dragIndex.value = null
  dragOverIndex.value = null
}
</script>

<template>
  <div class="ingredient-list">
    <div
      v-for="(ingredient, index) in list"
      :key="index"
      class="ingredient-row"
      :class="{
        dragging: dragIndex === index,
        'drag-over': dragOverIndex === index && dragIndex !== index,
      }"
      draggable="true"
      @dragstart="onDragStart($event, index)"
      @dragover="onDragOver($event, index)"
      @drop="onDrop($event, index)"
      @dragend="onDragEnd"
    >
      <span class="drag-handle" title="Drag to reorder">⠿</span>
      <span class="bin-label">Bin {{ index + 1 }}</span>
      <input
        :value="ingredient"
        type="text"
        placeholder="e.g. 500g bread flour"
        @input="update(index, $event.target.value)"
      />
      <button type="button" class="btn-remove" aria-label="Remove ingredient" @click="remove(index)">
        ×
      </button>
    </div>

    <div class="add-row">
      <button type="button" class="btn-add" :disabled="list.length >= MAX_INGREDIENTS" @click="add">
        + Add Ingredient
      </button>
      <span v-if="list.length >= MAX_INGREDIENTS" class="limit-note">
        Maximum {{ MAX_INGREDIENTS }} ingredients reached
      </span>
    </div>
  </div>
</template>

<style scoped>
.ingredient-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.ingredient-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.4rem;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background: #fff;
  transition: opacity 0.15s, border-color 0.15s;
  cursor: default;
}

.ingredient-row.dragging {
  opacity: 0.4;
}

.ingredient-row.drag-over {
  border-color: #3b82f6;
  background: #eff6ff;
}

.drag-handle {
  color: #9ca3af;
  cursor: grab;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0 0.1rem;
  user-select: none;
}

.drag-handle:active {
  cursor: grabbing;
}

.bin-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #6b7280;
  white-space: nowrap;
  min-width: 3.2rem;
}

.ingredient-row input {
  flex: 1;
  padding: 0.35rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.95rem;
  font-family: inherit;
}

.ingredient-row input:focus {
  outline: none;
  border-color: #3b82f6;
}

.btn-remove {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0.1rem 0.3rem;
  cursor: pointer;
  border-radius: 3px;
}

.btn-remove:hover {
  color: #dc2626;
  background: #fee2e2;
}

.add-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.btn-add {
  padding: 0.4rem 0.9rem;
  border: 1px dashed #9ca3af;
  border-radius: 4px;
  background: transparent;
  color: #374151;
  font-size: 0.9rem;
  cursor: pointer;
}

.btn-add:hover:not(:disabled) {
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-add:disabled {
  opacity: 0.5;
  cursor: default;
}

.limit-note {
  font-size: 0.8rem;
  color: #6b7280;
}
</style>
