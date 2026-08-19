<script setup lang="ts">
import { ref, computed } from 'vue';
import FeatureMapView from './components/FeatureMapView.vue';
import ProteinSearch from './components/ProteinSearch.vue';
import IsoformSelect from './components/IsoformSelect.vue';
import ExpressionChart from './components/ExpressionChart.vue';
import InteractionChart from './components/InteractionChart.vue';
import { getFeatureMap, getProteinExpressions, getProteinInteractions, getProteinDetails } from './proteinClient';
import type { FeatureMap, ProteinExpressionSample, ProteinInteractionDetails, ProteinDetails } from './types/api';

const selectedProteinId = ref<string | null>(null);
const featureMap = ref<FeatureMap | null>(null);
const proteinExpressions = ref<ProteinExpressionSample[] | null>(null);
const proteinInteractions = ref<ProteinInteractionDetails[] | null>(null);
const proteinDetails = ref<ProteinDetails | null>(null);
const selectedIsoformId = ref<string | null>(null);

async function onProteinSelected(proteinId: string) {
  selectedProteinId.value = proteinId;
  try {
    const [featureMapData, expressionsData, interactionsData, detailsData] = await Promise.all([
      getFeatureMap(proteinId),
      getProteinExpressions(proteinId),
      getProteinInteractions(proteinId),
      getProteinDetails(proteinId),
    ]);
    featureMap.value = featureMapData;
    proteinExpressions.value = expressionsData;
    proteinInteractions.value = interactionsData;
    proteinDetails.value = detailsData;
    selectedIsoformId.value = featureMap.value?.isoforms[0]?.isoform_id ?? null;

  } catch (err) {
    console.error('Failed to load protein data', err);
  }
}

function onIsoformSelected(isoformId: string) {
  selectedIsoformId.value = isoformId;
}

const selectedIsoform = computed(() => {
  if (!featureMap.value || !selectedIsoformId.value) return null;
  return featureMap.value.isoforms.find(i => i.isoform_id === selectedIsoformId.value) ?? null;
});
</script>

<template>
  <div class="app">
    <h1 class="app__title">Protein Explorer</h1>

    <ProteinSearch @protein-selected="onProteinSelected" />

    <IsoformSelect
      v-if="featureMap"
      :key="selectedProteinId ?? undefined"
      :featureMap="featureMap"
      :selectedIsoformId="selectedIsoformId"
      @isoform-selected="onIsoformSelected"
    />

    <!-- Feature map panel -->
    <div v-if="selectedIsoform" class="chart-panel">
      <h2 class="chart-panel__title">Feature Map - {{ selectedIsoform?.isoform_name }} ({{ selectedIsoform?.isoform_id }})</h2>
      <FeatureMapView :isoform="selectedIsoform" />
    </div>

    <!-- Expression + interaction panels -->
    <div class="charts">
      <div v-if="proteinExpressions" class="chart-panel">
        <h2 class="chart-panel__title">Protein Expression - {{ proteinDetails?.protein_name }} ({{ proteinDetails?.gene_symbol }})</h2>
        <ExpressionChart
          :proteinExpressions="proteinExpressions"
        />
      </div>

      <div
        v-if="proteinInteractions && proteinDetails"
        class="chart-panel"
      >
        <h2 class="chart-panel__title">Protein Interactions - {{ proteinDetails?.protein_name }} ({{ proteinDetails?.gene_symbol }})</h2>
        <InteractionChart
          :interactions="proteinInteractions"
          :proteinDetails="proteinDetails"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>

.app {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 36px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
  box-sizing: border-box;
}

.app__title {
  margin: 0;
  font-size: 56px;
}

.chart-panel {
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.chart-panel__title {
  margin: 0 0 16px;
  text-align: center;
  font-size: 20px;
  font-weight: 600;
}

.charts {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 24px;
  width: 100%;
}

@media (max-width: 700px) {
  .charts {
    grid-template-columns: 1fr;
  }
}
</style>