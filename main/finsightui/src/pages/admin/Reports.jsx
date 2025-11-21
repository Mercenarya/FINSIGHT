import React from 'react';
import { Eye, Download, Share2 } from 'lucide-react';
import './Reports.css';

function Reports() {
  const reports = [
    { id: 1, title: 'Quarterly Report', author: 'Nguyen Hong Manh', date: 'Sept 24, 2025', status: 'Approved' },
    { id: 2, title: 'Annual Report', author: 'Tran Quoc Minh', date: 'Sept 22, 2025', status: 'Pending' },
    { id: 3, title: 'Financial Analysis', author: 'Pham Tan Van', date: 'Sept 19, 2025', status: 'Approved' },
    { id: 4, title: 'Year End Summary', author: 'Pham Chi Thanh', date: 'Sept 17, 2025', status: 'Approved' },
  ];

  return (
    <div className="reports-page">
      <div className="reports-search">
        <input type="text" placeholder="Search" className="search-input" />
      </div>
      
      <div className="reports-panel">
        <div className="reports-table">
          <table>
            <thead>
              <tr>
                <th>Report ID</th>
                <th>Title</th>
                <th>Author</th>
                <th>Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((report) => (
                <tr key={report.id}>
                  <td>{report.id}</td>
                  <td>{report.title}</td>
                  <td>{report.author}</td>
                  <td>{report.date}</td>
                  <td>
                    <span className={`report-status ${report.status.toLowerCase()}`}>
                      {report.status}
                    </span>
                  </td>
                  <td>
                    <div className="report-actions">
                      <button className="action-btn view">View</button>
                      <button className="action-btn edit">Edit</button>
                      <button className="action-btn download">Download</button>
                    </div>
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

export default Reports;
