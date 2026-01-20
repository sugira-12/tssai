from backend.services.vectorstore import store_chunks

chunks = ["Example chunk 1", "Example chunk 2"]
embeddings = [[0.1]*384, [0.2]*384]

store_chunks(chunks, embeddings, "sample.pdf")
print("Embeddings stored.")
