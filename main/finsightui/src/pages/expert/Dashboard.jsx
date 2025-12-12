import React from 'react';
import { Search, User, TrendingUp, TrendingDown } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './Dashboard.css';

const modelPerformanceData = [
  { month: 'Jan', value: 78 },
  { month: 'Feb', value: 82 },
  { month: 'Mar', value: 75 },
  { month: 'Apr', value: 88 },
  { month: 'May', value: 85 },
  { month: 'Jun', value: 92 },
];

const healthRatioData = [
  { day: 'Mon', ratio: 85 },
  { day: 'Tue', ratio: 92 },
  { day: 'Wed', ratio: 78 },
  { day: 'Thu', ratio: 88 },
  { day: 'Fri', ratio: 95 },
  { day: 'Sat', ratio: 82 },
  { day: 'Sun', ratio: 90 },
];

const recentUpdates = [
  { id: 'Model A', date: '21-09-2025', status: 'Validated' },
  { id: 'Model B', date: '20-09-2025', status: 'Validated' },
  { id: 'Model C', date: '19-09-2025', status: 'Pending' },
  { id: 'Model D', date: '18-09-2025', status: 'Pending' },
];

function Dashboard() {
  return (
    <div className="expert-dashboard">
      <header className="expert-header">
        <div className="expert-header-left">
          <h1 className="expert-page-title">Dashboard</h1>
        </div>
        <div className="expert-header-right">
          <div className="expert-search-box">
            <Search size={18} />
            <input type="text" placeholder="Search" />
          </div>
          <button className="expert-user-btn">
            <User size={20} />
            <span>Howard Stark</span>
          </button>
        </div>
      </header>

      <div className="expert-dashboard-content">
        <div className="expert-metrics-row">
          <div className="expert-metric-card">
            <div className="expert-metric-header">
              <span className="expert-metric-label">Model Accuracy</span>
              <TrendingUp size={16} className="expert-trend-icon up" />
            </div>
            <div className="expert-metric-value">92%</div>
            <div className="expert-metric-change positive">+5% from last week</div>
          </div>

          <div className="expert-metric-card">
            <div className="expert-metric-header">
              <span className="expert-metric-label">Pending Validations</span>
              <TrendingDown size={16} className="expert-trend-icon down" />
            </div>
            <div className="expert-metric-value">5</div>
            <div className="expert-metric-change negative">-2 from yesterday</div>
          </div>

          <div className="expert-metric-card">
            <div className="expert-metric-header">
              <span className="expert-metric-label">Reports Generated</span>
              <TrendingUp size={16} className="expert-trend-icon up" />
            </div>
            <div className="expert-metric-value">12</div>
            <div className="expert-metric-change positive">+3 this week</div>
          </div>

          <div className="expert-metric-card">
            <div className="expert-metric-header">
              <span className="expert-metric-label">Active Models</span>
            </div>
            <div className="expert-metric-value">8</div>
            <div className="expert-metric-change neutral">No change</div>
          </div>
        </div>

        <div className="expert-charts-row">
          <div className="expert-chart-card">
            <h3 className="expert-chart-title">Model Performance</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={modelPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="month" stroke="rgba(255,255,255,0.5)" />
                <YAxis stroke="rgba(255,255,255,0.5)" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e3a5f', border: 'none', borderRadius: '8px' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Line type="monotone" dataKey="value" stroke="#00d9ff" strokeWidth={2} dot={{ fill: '#00d9ff' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="expert-chart-card">
            <h3 className="expert-chart-title">Health of AI Ratio</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={healthRatioData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,0.5)" />
                <YAxis stroke="rgba(255,255,255,0.5)" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e3a5f', border: 'none', borderRadius: '8px' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Bar dataKey="ratio" fill="#0d6efd" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="expert-updates-section">
          <div className="expert-updates-header">
            <h3 className="expert-section-title">Recent Model Updates</h3>
          </div>
          <div className="expert-updates-table">
            <table>
              <thead>
                <tr>
                  <th>Model</th>
                  <th>Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentUpdates.map((update, index) => (
                  <tr key={index}>
                    <td>{update.id}</td>
                    <td>{update.date}</td>
                    <td>
                      <span className={`expert-status-badge ${update.status.toLowerCase()}`}>
                        {update.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
