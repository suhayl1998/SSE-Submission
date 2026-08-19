<script setup lang="ts">
import type { ProteinExpressionSample} from '../types/api'
import { SAMPLE_CLASS_COLORS } from "../constants/colours";
import { ref, onMounted, watch, nextTick } from 'vue'
import Plotly from 'plotly.js-dist-min'

const props = defineProps<{proteinExpressions: ProteinExpressionSample[]}>();
const chartDiv = ref<HTMLDivElement | null>(null)

async function render() {
  if (!chartDiv.value) return

  const classes = ['Cancer', 'Normal', 'Cell line'] as const

  const traces = classes.map(cls => {
    const samples = props.proteinExpressions.filter(d => d.sample_detail.sample_class === cls)

    return {
      type: 'bar' as const,
      name: cls,
      x: samples.map(d => d.sample_detail.sample_name),
      y: samples.map(d => d.abundance_score),
      marker: {
        color: SAMPLE_CLASS_COLORS[cls],
        opacity: samples.map(d => (d.observed ? 1 : 0.4)),
      },
      customdata: samples.map(d => [d.sample_detail.sample_class, d.observed ? 'Yes' : 'No']),
      hovertemplate:
        '<b>%{x}</b><br>' +
        'Abundance: %{y}<br>' +
        'Class: %{customdata[0]}<br>' +
        'Observed: %{customdata[1]}' +
        '<extra></extra>', // removes Plotly's default trace-name box in the tooltip
    }
  })

  await Plotly.newPlot(chartDiv.value, traces, {
    barmode: 'group',
    xaxis: { title: { text: 'Sample' }, tickangle: -45 },
    yaxis: { title: { text: 'Abundance Score' } },
    legend: { title: { text: 'Sample Class' } },
    margin: { b: 120 }, // rotated x-axis labels
  }, { responsive: true })

  await nextTick()
  Plotly.Plots.resize(chartDiv.value)
}

onMounted(render)
watch(() => props.proteinExpressions, render)
</script>

<template>
  <div ref="chartDiv" class="expression-chart"></div>
</template>

<style scoped>
.expression-chart {
  width: 100%;
  min-width: 0;
}
</style>
