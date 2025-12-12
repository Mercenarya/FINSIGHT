import React from 'react';
import { Download } from 'lucide-react';
import './DataManagement.css';

function DataManagement() {
  const dataFiles = [
    { name: 'Q1_Data.csv', size: '2 MB', date: '2023-01-15' },
    { name: 'Q2_Data.csv', size: '3 MB', date: '2023-04-19' },
    { name: 'Q3_Data.csv', size: '3 MB', date: '2023-07-15' },
    { name: 'Q4_Data.csv', size: '1 MB', date: '2023-10-12' },
  ];

  return (
    <div className="data-management">
      <div className="data-panel">
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Size</th>
                <th>Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {dataFiles.map((file, index) => (
                <tr key={index}>
                  <td>{file.name}</td>
                  <td>{file.size}</td>
                  <td>{file.date}</td>
                  <td>
                    <button className="download-btn">
                      <Download size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default DataManagement;
