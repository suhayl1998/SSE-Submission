<script setup lang="ts">
import { ref, watch } from 'vue'
import type { FeatureMap } from '../types/api'

const props = defineProps<{
  featureMap: FeatureMap
  selectedIsoformId: string | null
}>()
const emit = defineEmits<{ 'isoform-selected': [isoformId: string] }>()

const isOpen = ref(false)
const select = ref('')

// keep the displayed text in sync with whatever isoform is actually selected,
// whether that came from a user click here or a default set by the App.vue
watch(
  () => props.selectedIsoformId,
  (isoformId) => {
    const match = props.featureMap.isoforms.find(i => i.isoform_id === isoformId)
    select.value = match?.isoform_name ?? ''
  },
  { immediate: true } // run once on mount too, not just on future changes
)

function selectIsoform(isoform: { isoform_id: string; isoform_name: string }) {
  isOpen.value = false
  emit('isoform-selected', isoform.isoform_id)
}

function onBlur() {
  setTimeout(() => { isOpen.value = false }, 150)
}
</script>

<template>
  <div class="search-row">
    <label for="isoform-select" class="search-label">Select Isoform</label>
    <div class="search">
      <input
        id="isoform-select"
        v-model="select"
        @focus="() => { if (featureMap.isoforms.length) isOpen = true }"
        @blur="onBlur"
        placeholder="Select Isoform..."
        class="search__input"
      />
      <ul v-if="isOpen && featureMap.isoforms.length" class="search__dropdown">
      <li
        v-for="isoform in featureMap.isoforms"
        :key="isoform.isoform_id"
        @mousedown="selectIsoform(isoform)"
        class="search__item"
      >
          <span class="search__name">{{ isoform.isoform_name }}</span>
          <span class="search__meta">{{ isoform.isoform_id }}</span>
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