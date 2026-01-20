export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/ingest/document", {
    method: "POST",
    body: formData,
  });

  return res.json();
}
