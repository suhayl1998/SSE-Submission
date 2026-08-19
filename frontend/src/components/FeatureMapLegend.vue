<script setup lang="ts">
import { computed } from 'vue'
import { assignedColours } from '../constants/featureMap'

const legend = computed(() =>
  Array.from(assignedColours.value, ([type, colour]) => ({
    type,
    colour,
  }))
)
</script>

<template>
  <div class="legend">
    <div
      v-for="item in legend"
      :key="item.type"
      class="legend-item"
    >
      <span
        class="legend-colour"
        :style="{ backgroundColor: item.colour }"
      />

      <span>{{ item.type }}</span>
    </div>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 20px;
  margin-top: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-colour {
  width: 14px;
  height: 14px;
  border: 1px solid #666;
  border-radius: 2px;
}
</style>