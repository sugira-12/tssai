const BASE_URL = "http://127.0.0.1:8000/qa";

export async function askQuestion(question, doc_id) {
  const response = await fetch(`${BASE_URL}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, doc_id }),
  });
  return await response.json();
}
