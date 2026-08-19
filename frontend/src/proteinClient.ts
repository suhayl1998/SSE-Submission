import axios from "axios";
import type { ProteinSearchResponse, FeatureMap, ProteinExpressionSample, ProteinInteractionDetails, ProteinDetails } from "./types/api";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // Adjust the base URL as needed
});

export async function searchProteins(query: string, limit: number = 10): Promise<ProteinSearchResponse[]> {
  const response = await client.get<ProteinSearchResponse[]>("/proteins", {
    params: { query, limit },
  });
  return response.data;
}

export async function getFeatureMap(proteinId: string): Promise<FeatureMap> {
  const response = await client.get<FeatureMap>(`/proteins/${proteinId}/feature-map`);
  return response.data;
}

export async function getProteinExpressions(proteinId: string): Promise<ProteinExpressionSample[]>{
  const response = await client.get<ProteinExpressionSample[]>(`/proteins/${proteinId}/protein-expressions`)
  return response.data
}

export async function getProteinInteractions(proteinId: string): Promise<ProteinInteractionDetails[]>{
  const response = await client.get<ProteinInteractionDetails[]>(`/proteins/${proteinId}/interactions`)
  return response.data
}

export async function getProteinDetails(proteinId: string): Promise<ProteinDetails>{
  const reponse = await client.get<ProteinDetails>(`/proteins/${proteinId}/details`)
  return reponse.data
}