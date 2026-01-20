export const BASE_URL = "http://127.0.0.1:8000";


export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BACKEND_URL}/ingest/document`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}
