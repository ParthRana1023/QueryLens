import React from 'react';
import { Upload } from 'lucide-react';

const PDFUploader = ({ onFileUpload }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      onFileUpload(file);
    }
  };

  return (
    <div className="uploader-container">
      <label className="uploader-dropzone">
        <div className="uploader-content">
          <Upload className="uploader-icon" />
          <p className="uploader-text">
            <span className="uploader-text-bold">Click to upload</span> or drag and drop
          </p>
          <p className="uploader-text">PDF files only</p>
        </div>
        <input type="file" style={{ display: 'none' }} accept=".pdf" onChange={handleFileChange} />
      </label>
    </div>
  );
};

export default PDFUploader;