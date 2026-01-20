import React, { useState } from "react";
import { askQuestion } from "../api/qaAPI";

function ChatUI() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    if (!question) return;
    const res = await askQuestion(question, "sample_doc.pdf"); // stub doc_id
    setAnswer(res.answer);
  };

  return (
    <div>
      <h2>Ask a Question</h2>
      <input
        type="text"
        value={question}
        placeholder="Enter your question..."
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "70%" }}
      />
      <button onClick={handleAsk}>Ask</button>
      <div style={{ marginTop: "10px" }}>
        <strong>Answer:</strong>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default ChatUI;
