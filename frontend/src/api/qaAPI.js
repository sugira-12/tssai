export const BASE_URL = "http://127.0.0.1:8000";


// qaAPI.js
export async function askQuestion(doc_id, question) {
  const res = await fetch(`${BASE_URL}/qa/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ doc_id, question }),
  });
  return res.json();
}
