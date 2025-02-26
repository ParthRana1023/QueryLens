import React from "react";
import { X, Download } from "lucide-react";

const PDFViewer = ({ pdf, onClose }) => {
  if (!pdf) return null;

  const pdfUrl = `${pdf.url}#toolbar=0&view=FitH`;

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = pdf.url;
    link.download = pdf.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="pdf-viewer-overlay">
      <div className="pdf-viewer-container">
        <div className="pdf-viewer-header">
          <h3 className="pdf-viewer-title">{pdf.name}</h3>
          <div className="pdf-viewer-actions">
            <button
              className="pdf-viewer-button"
              onClick={handleDownload}
              title="Download PDF"
            >
              <Download size={24} />
            </button>
            <button
              className="pdf-viewer-close"
              onClick={onClose}
              title="Close"
            >
              <X size={24} />
            </button>
          </div>
        </div>
        <div className="pdf-viewer-content">
          <embed
            src={pdfUrl}
            type="application/pdf"
            className="pdf-viewer-iframe"
            width="100%"
            height="100%"
          />
        </div>
      </div>
    </div>
  );
};

export default PDFViewer;
