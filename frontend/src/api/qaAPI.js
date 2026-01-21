const BASE_URL = "http://127.0.0.1:8000";

export async function askQuestion(question, doc_id) {
  const res = await fetch(`${BASE_URL}/qa/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, doc_id }),
  });
  return res.json();
}
