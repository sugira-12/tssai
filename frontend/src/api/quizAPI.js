const BASE_URL = "http://127.0.0.1:8000/quiz";

export async function generateQuiz(module_id) {
  const response = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ module_id }),
  });
  return await response.json();
}
