import React from "react";

function Sidebar({ uploadedPDFs }) {
  return (
    <aside className="sidebar">
      <h2>Uploaded PDFs</h2>
      <ul>
        {uploadedPDFs.map((pdf, index) => (
          <li key={index}>{pdf}</li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;
