import React from 'react';
import { Search, User } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './Report.css';

const reportTimeData = [
  { month: 'Jan', reports: 30 },
  { month: 'Feb', reports: 45 },
  { month: 'Mar', reports: 35 },
  { month: 'Apr', reports: 50 },
  { month: 'May', reports: 40 },
  { month: 'Jun', reports: 55 },
];

const reportsList = [
  { id: 'Report 01', status: 'Pending' },
  { id: 'Report 02', status: 'Validated' },
  { id: 'Report 03', status: 'Pending' },
];

function Report() {
  return (
    <div className="expert-report">
      <header className="expert-header">
        <div className="expert-header-left">
          <h1 className="expert-page-title">Report Adjustment</h1>
        </div>
        <div className="expert-header-right">
          <div className="expert-search-box">
            <Search size={18} />
            <input type="text" placeholder="Search" />
          </div>
          <button className="expert-user-btn">
            <User size={20} />
            <span>Hello, user</span>
          </button>
        </div>
      </header>

      <div className="expert-report-content">
        <div className="expert-report-chart-section">
          <h3 className="expert-report-chart-title">Reports Over Time</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={reportTimeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="month" stroke="rgba(255,255,255,0.5)" />
              <YAxis stroke="rgba(255,255,255,0.5)" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e3a5f', border: 'none', borderRadius: '8px' }}
                labelStyle={{ color: '#fff' }}
              />
              <Line type="monotone" dataKey="reports" stroke="#00d9ff" strokeWidth={2} dot={{ fill: '#00d9ff' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="expert-report-bottom-row">
          <div className="expert-report-total-card">
            <span className="expert-report-total-label">Total Reports</span>
            <span className="expert-report-total-value">372</span>
          </div>

          <div className="expert-report-list-card">
            <h4 className="expert-report-list-title">Report List</h4>
            <div className="expert-report-list">
              {reportsList.map((report, index) => (
                <div key={index} className="expert-report-list-item">
                  <span className="expert-report-id">{report.id}</span>
                  <span className={`expert-report-status ${report.status.toLowerCase()}`}>
                    {report.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="expert-report-footer">
          <button className="expert-generate-btn">Generate Report</button>
        </div>
      </div>
    </div>
  );
}

export default Report;
