import { apiClient } from "./client";

// Fetch all prompts
export function getPrompts() {
  return apiClient("/prompts");
}

// Fetch single prompt by ID
export function getPrompt(id) {
  return apiClient(`/prompts/${id}`);
}

// Create new prompt
export function createPrompt(data) {
  return apiClient("/prompts", { method: "POST", body: data });
}

// Update existing prompt
export function updatePrompt(id, data) {
  return apiClient(`/prompts/${id}`, { method: "PUT", body: data });
}

// Delete prompt
export function deletePrompt(id) {
  return apiClient(`/prompts/${id}`, { method: "DELETE" });
}