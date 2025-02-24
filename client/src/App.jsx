import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import PDFUpload from "./components/PDFUpload";
import UserInput from "./components/UserInput";
import "./App.css";

function App() {
  const [uploadedPDFs, setUploadedPDFs] = useState([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handlePDFUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setUploadedPDFs([...uploadedPDFs, file.name]);
      } else {
        const data = await response.json();
        alert(`Upload failed: ${data.error}`);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
    }
  };

  const handleQuestionSubmit = async (question) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer);
      } else {
        const data = await response.json();
        alert(`Failed to get answer: ${data.error}`);
      }
    } catch (error) {
      console.error("Error asking question:", error);
      alert("An error occurred while asking the question.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <Sidebar uploadedPDFs={uploadedPDFs} />
      <main className="main-content">
        <h1>RAG Model Q&A</h1>
        <PDFUpload onUpload={handlePDFUpload} />
        <UserInput onSubmit={handleQuestionSubmit} />
        {loading && <p className="loading">Thinking...</p>}
        {answer && (
          <div className="answer">
            <h2>Answer:</h2>
            <p>{answer}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
