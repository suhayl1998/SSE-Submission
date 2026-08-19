<script setup lang="ts">
import { computed } from 'vue'
import type { IsoformMap } from '../types/api'
import FeatureMapLegend from './FeatureMapLegend.vue'
import { ROWS, colourForType } from '../constants/featureMap'

const props = defineProps<{ isoform: IsoformMap }>();
const VIEWBOX_WIDTH = 800;
const VIEWBOX_HEIGHT = 150;
const labelFontSize = computed(() => Math.max(8, props.isoform.end_pos * 0.015))



</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${isoform.end_pos} ${VIEWBOX_HEIGHT}`" :width="VIEWBOX_WIDTH" :height="VIEWBOX_HEIGHT">
      <rect x="0" :y="ROWS.isoform.y" :width="isoform.end_pos - isoform.start_pos" :height="ROWS.isoform.height" :fill="colourForType('isoform')">
        <title>Isoform: {{ isoform.isoform_id }} {{ isoform.isoform_name }}</title>
      </rect>
      <rect v-for="domain in isoform.domains" :key="domain.domain_id"
      :x="domain.start_pos" :y="ROWS.domain.y" :width="domain.end_pos - domain.start_pos" :height="ROWS.domain.height" :fill="colourForType(domain.feature_type)">
        <title>Domain: {{ domain.feature_name }} ({{ domain.start_pos }}-{{ domain.end_pos }})</title>
      </rect>
      
      <rect v-for="peptide in isoform.peptides" :key="peptide.peptide_id"
      :x="peptide.start_pos" :y="ROWS.peptide.y" :width="Math.max(1, peptide.end_pos - peptide.start_pos)" :height="ROWS.peptide.height" :fill="colourForType('peptide')">
        <title>Peptide: {{ peptide.peptide_label }} ({{ peptide.start_pos }}-{{ peptide.end_pos }})</title>
      </rect>
      <line v-for="variant in isoform.variants" :key="variant.variant_id"
      :x1="variant.position" :y1="ROWS.variant.y1" :x2="variant.position" :y2="ROWS.variant.y2" stroke="black" stroke-width="2">
        <title>{{ variant.variant_type }}{{ variant.variant_label ? ` — ${variant.variant_label}` : '' }} ({{ variant.position }})</title>
      </line>

      <line
        :x1="isoform.start_pos" :y1="ROWS.isoform.y - 5"
        :x2="isoform.start_pos" :y2="ROWS.isoform.y + ROWS.isoform.height + 5"
        stroke="black" stroke-width="2"
      />
      <text
        :x="isoform.start_pos"
        :y="ROWS.isoform.y - 8"
        text-anchor="start"
        :font-size="labelFontSize"
      >{{ isoform.start_pos }}</text>

      <line
        :x1="isoform.end_pos" :y1="ROWS.isoform.y - 5"
        :x2="isoform.end_pos" :y2="ROWS.isoform.y + ROWS.isoform.height + 5"
        stroke="black" stroke-width="2"
      />
      <text
        :x="isoform.end_pos"
        :y="ROWS.isoform.y - 8"
        text-anchor="end"
        :font-size="labelFontSize"
      >{{ isoform.end_pos }}</text>
    </svg>
    <FeatureMapLegend />
  </div>
</template>
