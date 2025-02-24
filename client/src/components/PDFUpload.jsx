import React from "react";

function PDFUpload({ onUpload }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    } else {
      alert("Please upload a PDF file.");
    }
  };

  return (
    <div className="pdf-upload">
      <h2>Upload PDF</h2>
      <label htmlFor="file-upload" className="custom-file-upload">
        Choose PDF
      </label>
      <input
        id="file-upload"
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
      />
    </div>
  );
}

export default PDFUpload;
