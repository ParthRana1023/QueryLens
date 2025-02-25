import React from 'react';
import { FileText, Trash2 } from 'lucide-react';

const PDFLibrary = ({ pdfs = [], onPDFSelect, onPDFDelete }) => {
  const truncateName = (name) => {
    if (!name) return "Unnamed PDF";
    return name.length > 15 ? name.substring(0, 15) + '...' : name;
  };

  return (
    <div className="library-container">
      <h2 className="library-title">Your PDFs</h2>
      <div className="library-list">
        {pdfs.length > 0 ? (
          pdfs.map((pdf, index) => (
            pdf && pdf.name ? (
              <div key={index} className="library-item">
                <div className="library-item-content" onClick={() => onPDFSelect(pdf)}>
                  <FileText className="library-item-icon" />
                  <span className="library-item-name">{truncateName(pdf.name)}</span>
                </div>
                <button
                  className="library-delete-btn"
                  onClick={() => onPDFDelete(pdf)}
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ) : null
          ))
        ) : (
          <div className="library-empty">
            No PDFs uploaded yet
          </div>
        )}
      </div>
    </div>
  );
};

export default PDFLibrary;
