const BASE_URL = "/api"; // Vite proxy

export async function fetchPrompts() {
  try {
    const response = await fetch(`${BASE_URL}/prompts`);
    if (!response.ok) throw new Error("Failed to fetch prompts");

    const data = await response.json();
    console.log("Fetched prompts:", data);
    return data.prompts;
  } catch (error) {
    console.error(error);
    return [];
  }
}