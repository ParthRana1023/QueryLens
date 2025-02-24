import React, { useState } from "react";

function UserInput({ onSubmit }) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      onSubmit(question);
      setQuestion("");
    }
  };

  return (
    <form className="user-input" onSubmit={handleSubmit}>
      <h2>Ask a Question</h2>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your question here..."
        rows="4"
      ></textarea>
      <button type="submit">Submit Question</button>
    </form>
  );
}

export default UserInput;
