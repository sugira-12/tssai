const BACKEND_URL = "http://localhost:8000";

export async function generateQuiz(module_id) {
  const res = await fetch(`${BACKEND_URL}/quiz/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ module_id }),
  });
  return res.json();
}
