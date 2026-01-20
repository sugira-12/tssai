import React, { useState } from "react";
import { askQuestion } from "../api/qaAPI";

function ChatUI() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  async function handleAsk() {
    const res = await askQuestion(question, "sample_doc.pdf"); // doc_id from uploaded PDF
    setAnswer(res.answer);
  }

  return (
    <div>
      <h2>Chat with TVET AI</h2>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={handleAsk}>Ask</button>
      <div>{answer && <p>Answer: {answer}</p>}</div>
    </div>
  );
}

export default ChatUI;
