<script setup lang="ts">
import { ref } from 'vue'
import { searchProteins } from '../proteinClient'
import type { ProteinSearchResponse } from '../types/api'

const emit = defineEmits<{ 'protein-selected': [proteinId: string] }>()

const query = ref('')
const results = ref<ProteinSearchResponse[]>([])
const isOpen = ref(false)

let debounceTimer: ReturnType<typeof setTimeout>
let latestQuery = ''

function onInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(runSearch, 300)
}

async function runSearch() {
  const q = query.value.trim()
  latestQuery = q
  if (q.length < 2) {
    results.value = []
    isOpen.value = false
    return
  }
  const data = await searchProteins(q)
  if (q !== latestQuery) return
  results.value = data
  isOpen.value = true
}

function selectProtein(p: ProteinSearchResponse) {
  results.value = []
  isOpen.value = false
  query.value = p.protein_name
  emit('protein-selected', p.protein_id)
}

function onBlur() {
  // slight delay so a click on a list item registers before the list disappears
  setTimeout(() => { isOpen.value = false }, 150)
}
</script>

<template>
  <div class="search-row">
    <label for="protein-search" class="search-label">Search Protein</label>
    <div class="search">
      <input
        id="protein-search"
        v-model="query"
        @input="onInput"
        @focus="() => { if (results.length) isOpen = true }"
        @blur="onBlur"
        placeholder="Search by name, gene, or ID..."
        class="search__input"
      />
      <ul v-if="isOpen && results.length" class="search__dropdown">
        <li
          v-for="p in results"
          :key="p.protein_id"
          @mousedown="selectProtein(p)"
          class="search__item"
        >
          <span class="search__name">{{ p.protein_name }}</span>
          <span class="search__meta">{{ p.gene_symbol }} · {{ p.protein_id }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.search-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
}

.search-label {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  color: #333;
}

.search {
  position: relative;
  width: 100%;
  max-width: 420px;
}

.search__input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 14px;
  font-size: 14px;
  border: 1px solid #d5d5d9;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.search__input:focus {
  border-color: #4C78A8;
  box-shadow: 0 0 0 3px rgba(76, 120, 168, 0.15);
}

.search__dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  margin: 0;
  padding: 4px;
  list-style: none;
  background: white;
  border: 1px solid #e2e2e6;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-height: 280px;
  overflow-y: auto;
  z-index: 20;
}

.search__item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
}

.search__item:hover {
  background: #f2f5f9;
}

.search__name {
  font-weight: 500;
  font-size: 14px;
  line-height: 1.2;
}

.search__meta {
  font-size: 12px;
  color: #888;
}
</style>