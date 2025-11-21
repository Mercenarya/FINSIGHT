import React from 'react';
import { Edit2, Trash2 } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import './UserManagement.css';

const chartData = [
  { value: 75 }, { value: 78 }, { value: 76 }, { value: 80 }, 
  { value: 82 }, { value: 79 }, { value: 85 }
];

function UserManagement() {
  const users = [
    { name: 'David Smith', email: 'david.smith@example.com', role: 'Admin', status: 'Active' },
    { name: 'Emma Johnson', email: 'emma.johnson@exaroot.com', role: 'Analyst', status: 'Pending' },
    { name: 'Michael Brown', email: 'michael.brown@example.com', role: 'Investor', status: 'Active' },
    { name: 'Sarah Davis', email: 'sarah.davis@example.com', role: 'Student', status: 'Inactive' },
  ];

  return (
    <div className="user-management">
      <div className="user-panel">
        <div className="panel-header">
          <h2>User</h2>
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

      <div className="system-health-panel">
        <h3>System Health Overview</h3>
        <div className="health-chart">
          <ResponsiveContainer width="100%" height={120}>
            <LineChart data={chartData}>
              <Line type="monotone" dataKey="value" stroke="#00d9ff" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="health-metrics">
          <div className="health-metric">
            <span className="metric-label">API Uptime</span>
            <span className="metric-value">99.9%</span>
          </div>
          <div className="health-metric">
            <span className="metric-label">Requests/Day</span>
            <span className="metric-value">12,340</span>
          </div>
          <div className="health-metric">
            <span className="metric-label">Avg. Response Time</span>
            <span className="metric-value">350ms</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserManagement;
