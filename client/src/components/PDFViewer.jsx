import React from "react";
import { X } from "lucide-react";

const PDFViewer = ({ pdf, onClose }) => {
  if (!pdf) return null;

  return (
    <div className="pdf-viewer-overlay">
      <div className="pdf-viewer-container">
        <div className="pdf-viewer-header">
          <h3 className="pdf-viewer-title">{pdf}</h3>
          <button className="pdf-viewer-close" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div className="pdf-viewer-content">
          {/* Ensure this is the correct URL to the PDF viewer */}
          <iframe
            src={`http://localhost:8000/pdf/view/${pdf}`} // Full URL to the PDF
            className="pdf-viewer-iframe"
            title="PDF Viewer"
            width="100%" // You can adjust the width as needed
            height="600px" // You can adjust the height as needed
          />
        </div>
      </div>
    </div>
  );
};

export default PDFViewer;
