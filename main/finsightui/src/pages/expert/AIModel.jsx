import React from 'react';
import { Search, User } from 'lucide-react';
import './AIModel.css';

const modelsData = [
  { name: 'Model A', version: 'v1.3', accuracy: '92%', lastUpdated: '01/2025', status: 'Validated' },
  { name: 'Model B', version: 'v1.0', accuracy: '86%', lastUpdated: '01/2025', status: 'Pending' },
  { name: 'Model B', version: 'v1.0', accuracy: '86%', lastUpdated: '01/2025', status: 'Pending' },
];

function AIModel() {
  return (
    <div className="expert-ai-model">
      <header className="expert-header">
        <div className="expert-header-left">
          <h1 className="expert-page-title">AI Models</h1>
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

      <div className="expert-ai-model-content">
        <div className="expert-ai-metrics">
          <div className="expert-ai-metric-card">
            <span className="expert-ai-metric-label">Total Models</span>
            <span className="expert-ai-metric-value">8</span>
          </div>
          <div className="expert-ai-metric-card">
            <span className="expert-ai-metric-label">Active Models</span>
            <span className="expert-ai-metric-value">5</span>
          </div>
          <div className="expert-ai-metric-card">
            <span className="expert-ai-metric-label">Pending Training</span>
            <span className="expert-ai-metric-value">2</span>
          </div>
          <div className="expert-ai-metric-card">
            <span className="expert-ai-metric-label">Accuracy</span>
            <span className="expert-ai-metric-value">89%</span>
          </div>
        </div>

        <div className="expert-ai-table-section">
          <div className="expert-ai-table-header">
            <button className="expert-upload-btn">Upload New Model</button>
          </div>
          <div className="expert-ai-table">
            <table>
              <thead>
                <tr>
                  <th>Model Name</th>
                  <th>Version</th>
                  <th>Accuracy</th>
                  <th>Last Updated</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {modelsData.map((model, index) => (
                  <tr key={index}>
                    <td>{model.name}</td>
                    <td>{model.version}</td>
                    <td>{model.accuracy}</td>
                    <td>{model.lastUpdated}</td>
                    <td>
                      <span className={`expert-ai-status-badge ${model.status.toLowerCase()}`}>
                        {model.status}
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

export default AIModel;
