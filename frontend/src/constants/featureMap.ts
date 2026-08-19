// This file contains constants and utility functions for the feature map visualization.
import { DEFAULT_COLOR, PALETTE } from "./colours";
import { ref } from 'vue'

// Define the rows for different feature types in the visualization.
export const ROWS = {
  isoform: { y: 20, height: 25 },
  domain: { y: 60, height: 25 },
  peptide: { y: 100, height: 25 },
  variant: { y1: 10, y2: 140 },
} as const;

// Define the colors for different feature types.

export const assignedColours = ref(new Map<string, string>())

export function colourForType(type: string | null): string {
  if (!type) return DEFAULT_COLOR

  if (!assignedColours.value.has(type)) {
    const nextIndex = assignedColours.value.size % PALETTE.length
    assignedColours.value.set(type, PALETTE[nextIndex])
  }

  return assignedColours.value.get(type)!
}