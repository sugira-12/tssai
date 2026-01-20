import React from "react";
import ChatUI from "./components/ChatUI";
import QuizUI from "./components/QuizUI";
import AdminDashboard from "./components/AdminDashboard";

function App() {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>TSS.AI TVET Assistant</h1>
      <ChatUI />
      <hr />
      <QuizUI />
      <hr />
      <AdminDashboard />
    </div>
  );
}

export default App;
