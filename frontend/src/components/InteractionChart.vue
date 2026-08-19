<script setup lang="ts">
import { computed } from 'vue'
import type { ProteinInteractionDetails, ProteinDetails } from '../types/api'

const props = defineProps<{
  interactions: ProteinInteractionDetails[]
  proteinDetails: ProteinDetails
}>();

const RADIUS = 150;
const CENTRE_X = 200;
const CENTRE_Y = 200;

const nodePositions = computed(() => {
  const others = props.interactions
  return others.map((interaction, i) => {
    const angle = (2 * Math.PI * i) / others.length
    return {
      interaction,
      protein: interaction.interactor_protein,
      x: CENTRE_X + RADIUS * Math.cos(angle),
      y: CENTRE_Y + RADIUS * Math.sin(angle),
    }
  })
})
</script>

<template>
  <div>
    <svg viewBox="0 0 400 400" class="interaction-svg" v-if="interactions.length">
      <!-- connecting lines, weighted by confidence -->
      <line
        v-for="node in nodePositions"
        :key="node.interaction.interaction_id"
        :x1="CENTRE_X" :y1="CENTRE_Y"
        :x2="node.x" :y2="node.y"
        stroke="#888"
        :stroke-width="(node.interaction.confidence_score ?? 0.5) * 6"
        :stroke-opacity="node.interaction.confidence_score ?? 0.5"
      >
        <title>{{ node.interaction.interaction_label ?? 'Interaction' }} — confidence {{ node.interaction.confidence_score }}</title>
      </line>

      <!-- selected protein, center -->
      <circle :cx="CENTRE_X" :cy="CENTRE_Y" r="24" fill="#4C78A8">
        <title>{{ proteinDetails.protein_name }}</title>
      </circle>
      <text :x="CENTRE_X" :y="CENTRE_Y + 40" text-anchor="middle" font-size="11">
        {{ proteinDetails.gene_symbol }}
      </text>

      <!-- interactor nodes -->
      <g v-for="node in nodePositions" :key="node.interaction.interaction_id">
        <circle :cx="node.x" :cy="node.y" r="18" fill="#F58518">
          <title>{{ node.protein.protein_name }} ({{ node.protein.gene_symbol }})</title>
        </circle>
        <text :x="node.x" :y="node.y + 32" text-anchor="middle" font-size="10">
          {{ node.protein.gene_symbol }}
        </text>
      </g>
    </svg>

    <p v-else>No known interactions for this protein.</p>
  </div>
</template>

<style scoped>
.interaction-svg {
  width: 100%;
  height: auto;
  min-width: 0;
  display: block; /* SVG is inline by default, which can add unwanted bottom spacing */
}
</style>