import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import './SystemHealth.css';

const chartData = [
  { value: 88 }, { value: 90 }, { value: 87 }, { value: 92 },
  { value: 94 }, { value: 91 }, { value: 95 }, { value: 93 },
  { value: 96 }, { value: 94 }, { value: 97 }, { value: 95 }
];

function SystemHealth() {
  const events = [
    { time: '10:03 AM', component: 'API Gateway', event: 'Increased response time', severity: 'Warning' },
    { time: '09:47 AM', component: 'Database', event: 'Backup completed', severity: 'Normal' },
    { time: '09:19 AM', component: 'Auth Service', event: 'Unauthorized access attempt', severity: 'Critical' },
  ];

  return (
    <div className="system-health-page">
      <div className="health-metrics-grid">
        <div className="health-metric-card">
          <div className="metric-header">
            <div className="metric-label">API Uptime</div>
            <div className="metric-time">Last 24 hours</div>
          </div>
          <div className="metric-value large">99.98%</div>
        </div>
        
        <div className="health-metric-card">
          <div className="metric-header">
            <div className="metric-label">Requests / Day</div>
            <div className="metric-time">Average daily load</div>
          </div>
          <div className="metric-value large">12,340</div>
        </div>
        
        <div className="health-metric-card">
          <div className="metric-header">
            <div className="metric-label">Avg. Response</div>
            <div className="metric-time">Current average</div>
          </div>
          <div className="metric-value large">350 ms</div>
        </div>
        
        <div className="health-metric-card">
          <div className="metric-header">
            <div className="metric-label">Active Alerts</div>
            <div className="metric-time">Requires attention</div>
          </div>
          <div className="metric-value large alert">3</div>
        </div>
      </div>

      <div className="health-chart-panel">
        <h3>API Uptime Over Time</h3>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={chartData}>
            <Line type="monotone" dataKey="value" stroke="#00d9ff" strokeWidth={3} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="events-panel">
        <h3>Recent System Events</h3>
        <div className="events-table">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Component</th>
                <th>Event</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event, index) => (
                <tr key={index}>
                  <td>{event.time}</td>
                  <td>{event.component}</td>
                  <td>{event.event}</td>
                  <td>
                    <span className={`severity-badge ${event.severity.toLowerCase()}`}>
                      {event.severity}
                    </span>
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

export default SystemHealth;
