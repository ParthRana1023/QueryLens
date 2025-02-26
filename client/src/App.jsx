import React, { useState, useEffect } from "react";
import PDFUploader from "./components/PDFUploader";
import PDFLibrary from "./components/PDFLibrary";
import ChatInterface from "./components/ChatInterface";
import PDFViewer from "./components/PDFViewer";
import { BookOpen } from "lucide-react";

function App() {
  const [pdfs, setPdfs] = useState([]);
  const [selectedPDF, setSelectedPDF] = useState(null);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  // Fetch existing PDFs from the server when the component mounts
  useEffect(() => {
    const fetchPDFs = async () => {
      try {
        const response = await fetch("http://localhost:8000/pdf/list");
        if (response.ok) {
          const data = await response.json();
          // Data now comes with creation time, already sorted from the backend
          setPdfs(
            data.map((item) => ({
              name: item.name,
              created: new Date(item.created * 1000), // Convert Unix timestamp to Date
            }))
          );
        } else {
          console.error("Failed to fetch PDFs");
        }
      } catch (error) {
        console.error("Error fetching PDFs:", error);
      }
    };

    fetchPDFs();
  }, []);

  const handlePDFUpload = async (file) => {
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/pdf/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        // Fetch the updated list after upload to get the correct creation time
        const listResponse = await fetch("http://localhost:8000/pdf/list");
        if (listResponse.ok) {
          const pdfsData = await listResponse.json();
          setPdfs(
            pdfsData.map((item) => ({
              name: item.name,
              created: new Date(item.created * 1000),
            }))
          );
        }
        return;
      }

      // Handle specific error cases
      if (response.status === 413) {
        throw new Error("File size too large");
      } else if (response.status === 415) {
        throw new Error("Invalid file type. Please upload a PDF file");
      } else if (response.status === 500) {
        throw new Error(
          "Server error: " + (data.error || "Unknown error occurred")
        );
      } else {
        throw new Error(data.error || "Failed to upload file");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert(error.message || "An error occurred while uploading the file.");
    } finally {
      setUploading(false);
    }
  };

  const handlePDFDelete = async (pdfToDelete) => {
    try {
      const response = await fetch(
        `http://localhost:8000/pdf/delete/${pdfToDelete.name}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        setPdfs(pdfs.filter((pdf) => pdf.name !== pdfToDelete.name)); // Remove from state
      } else {
        alert("Failed to delete PDF.");
      }
    } catch (error) {
      console.error("Error deleting file:", error);
      alert("An error occurred while deleting the file.");
    }
  };

  // Function for asking questions
  const handleQuestionSubmit = async (question) => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/chat/ask", {
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

  // Function to view a PDF by setting the selectedPDF to the URL
  const handlePDFSelect = (pdf) => {
    setSelectedPDF({
      name: pdf.name,
      url: `http://localhost:8000/pdf/view/${pdf.name}`,
    });
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-content">
          <div className="header-title">
            <BookOpen className="header-icon" size={32} />
            <h1>QueryLens</h1>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="grid-layout">
          <div className="sidebar">
            <PDFUploader onFileUpload={handlePDFUpload} />
            <PDFLibrary
              pdfs={pdfs}
              onPDFSelect={handlePDFSelect}
              onPDFDelete={handlePDFDelete}
            />
          </div>

          <ChatInterface onSubmit={handleQuestionSubmit} />
        </div>

        {loading && <p className="loading">Thinking</p>}
        {answer && (
          <div className="answer">
            <h2>Answer:</h2>
            <p>{answer}</p>
          </div>
        )}
      </main>

      {selectedPDF && (
        <PDFViewer pdf={selectedPDF} onClose={() => setSelectedPDF(null)} />
      )}
    </div>
  );
}

export default App;
