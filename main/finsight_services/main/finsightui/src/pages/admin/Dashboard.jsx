import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import { Edit2, Trash2 } from 'lucide-react';
import './Dashboard.css';

const chartData = [
  { value: 80 }, { value: 82 }, { value: 85 }, { value: 83 }, 
  { value: 87 }, { value: 90 }, { value: 88 }
];

function Dashboard() {
  const users = [
    { name: 'David Smith', email: 'david.smith@ex...', role: 'Admin', status: 'Active' },
    { name: 'Emma Johnson', email: 'emma.johnson@...', role: 'Analyst', status: 'Pending' },
    { name: 'Michael Brown', email: 'michael.brown@...', role: 'Investor', status: 'Active' },
    { name: 'Sarah Davis', email: 'sarah.davis@ex...', role: 'Student', status: 'Inactive' },
  ];

  const dataSources = [
    { name: 'Excel Data', status: 'Synced' },
    { name: 'CSV Files', status: 'Synced' },
  ];

  return (
    <div className="admin-dashboard">
      <div className="admin-metrics-grid">
        <div className="admin-metric-card">
          <div className="metric-label">Active Users</div>
          <div className="metric-value">5,620</div>
        </div>
        <div className="admin-metric-card">
          <div className="metric-label">Data Sources</div>
          <div className="metric-value">24</div>
        </div>
        <div className="admin-metric-card">
          <div className="metric-label">Models Running</div>
          <div className="metric-value">8</div>
        </div>
        <div className="admin-metric-card">
          <div className="metric-label">Alerts</div>
          <div className="metric-value">3</div>
        </div>
      </div>

      <div className="admin-dashboard-grid">
        <div className="admin-panel">
          <div className="panel-header">
            <h3>User Management</h3>
            <button className="btn-primary">Add User</button>
          </div>
          <div className="user-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user, index) => (
                  <tr key={index}>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td>
                      <span className={`status-badge ${user.status.toLowerCase()}`}>
                        {user.status}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button className="icon-btn"><Edit2 size={14} /></button>
                        <button className="icon-btn"><Trash2 size={14} /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="admin-panel">
          <h3>AI Model Performance</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={chartData}>
                <Line type="monotone" dataKey="value" stroke="#00d9ff" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="model-metrics">
            <div className="model-metric">
              <div className="metric-label">Accuracy</div>
              <div className="metric-value">97.6%</div>
            </div>
            <div className="model-metric">
              <div className="metric-label">Precision</div>
              <div className="metric-value">91.4%</div>
            </div>
            <div className="model-metric">
              <div className="metric-label">Recall</div>
              <div className="metric-value">85.3%</div>
            </div>
          </div>
          <button className="btn-primary full-width">Train Model</button>
        </div>
      </div>

      <div className="admin-panel">
        <h3>System Health Overview</h3>
        <div className="system-metrics">
          <div className="sys-metric">
            <div className="metric-label">Uptime</div>
            <div className="metric-value">95%</div>
          </div>
          <div className="sys-metric">
            <div className="metric-label">Requests per Day</div>
            <div className="metric-value">1500</div>
          </div>
          <div className="sys-metric">
            <div className="metric-label">Avg. Response Time</div>
            <div className="metric-value">250 ms</div>
          </div>
        </div>
        <div className="data-sources">
          <div className="source-label">Data Sources</div>
          {dataSources.map((source, index) => (
            <div key={index} className="source-item">
              <span>{source.name}</span>
              <span className="source-status">{source.status}</span>
            </div>
          ))}
        </div>
        <div className="system-health-info">
          <div className="info-item">
            <span>API HEALTH SCORE</span>
            <span>99.9%</span>
          </div>
          <div className="info-item">
            <span>API Uptime</span>
            <span>99.9%</span>
          </div>
          <div className="info-item">
            <span>Requests /Day</span>
            <span>12,340</span>
          </div>
          <div className="info-item">
            <span>Avg. Response Time</span>
            <span>350ms</span>
          </div>
        </div>
        <button className="btn-primary">Report & Export Center</button>
      </div>
    </div>
  );
}

export default Dashboard;
