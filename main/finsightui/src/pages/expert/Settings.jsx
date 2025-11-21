import React from 'react';
import { Search, User } from 'lucide-react';
import './Settings.css';

const systemLogs = [
  { time: '10:23 AM', action: 'Update', result: 'Success' },
  { time: '09:45 AM', action: 'Generate Report', result: 'Success' },
];

function Settings() {
  return (
    <div className="expert-settings">
      <header className="expert-header">
        <div className="expert-header-left">
          <h1 className="expert-page-title">Settings</h1>
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

      <div className="expert-settings-content">
        <div className="expert-settings-row">
          <div className="expert-settings-card">
            <h3 className="expert-settings-card-title">Account Settings</h3>
            <div className="expert-settings-group">
              <label className="expert-settings-label">Name</label>
              <input
                type="text"
                className="expert-settings-input"
                defaultValue="John Doe"
              />
            </div>
            <div className="expert-settings-group">
              <label className="expert-settings-label">Email</label>
              <input
                type="email"
                className="expert-settings-input"
                defaultValue="john.doe@example.com"
              />
            </div>
            <button className="expert-settings-change-btn">Change Password</button>
          </div>

          <div className="expert-settings-card">
            <h3 className="expert-settings-card-title">System Settings</h3>
            <div className="expert-settings-toggle-group">
              <span className="expert-settings-toggle-label">Auto-update AI Models</span>
              <label className="expert-toggle-switch">
                <input type="checkbox" defaultChecked />
                <span className="expert-toggle-slider"></span>
              </label>
            </div>
            <div className="expert-settings-toggle-group">
              <span className="expert-settings-toggle-label">Data Refresh Interval</span>
              <select className="expert-settings-select">
                <option>1 hour</option>
                <option>6 hours</option>
                <option>12 hours</option>
                <option>24 hours</option>
              </select>
            </div>
            <div className="expert-settings-toggle-group">
              <span className="expert-settings-toggle-label">Enable Error Reports</span>
              <label className="expert-toggle-switch">
                <input type="checkbox" defaultChecked />
                <span className="expert-toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <div className="expert-settings-logs-section">
          <div className="expert-settings-logs-row">
            <div className="expert-settings-logs-card">
              <h4 className="expert-settings-logs-title">System Logs</h4>
              <div className="expert-settings-logs-search">
                <input type="text" placeholder="Search" />
              </div>
              <table className="expert-settings-logs-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Action</th>
                    <th>User</th>
                    <th>Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>10:23 AM</td>
                    <td>Update</td>
                    <td>John Do</td>
                    <td><span className="expert-log-result success">Success</span></td>
                  </tr>
                  <tr>
                    <td>09:30 AM</td>
                    <td>General</td>
                    <td>John Do</td>
                    <td><span className="expert-log-result success">Success</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="expert-settings-logs-card">
              <h4 className="expert-settings-logs-title">System Logs</h4>
              <div className="expert-settings-logs-search">
                <input type="text" placeholder="Search" />
              </div>
              <table className="expert-settings-logs-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Action</th>
                    <th>User</th>
                    <th>Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>10:23 AM</td>
                    <td>Update</td>
                    <td>John Do</td>
                    <td><span className="expert-log-result success">Success</span></td>
                  </tr>
                  <tr>
                    <td>09:30 AM</td>
                    <td>General</td>
                    <td>John Do</td>
                    <td><span className="expert-log-result success">Success</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
