import React from 'react';
import { Search, User } from 'lucide-react';
import './Validation.css';

const validationData = [
  { model: 'Model A', version: 'v1.2', status: 'Validated' },
  { model: 'Model B', version: 'v1.0', status: 'Pending' },
  { model: 'Model C', version: 'v2.1', status: 'Validated' },
  { model: 'Model D', version: 'v1.8', status: 'Pending' },
];

function Validation() {
  return (
    <div className="expert-validation">
      <header className="expert-header">
        <div className="expert-header-left">
          <h1 className="expert-page-title">Validation</h1>
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

      <div className="expert-validation-content">
        <div className="expert-validation-table-section">
          <div className="expert-validation-table">
            <table>
              <thead>
                <tr>
                  <th>Model Name</th>
                  <th>Version</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {validationData.map((item, index) => (
                  <tr key={index}>
                    <td>{item.model}</td>
                    <td>{item.version}</td>
                    <td>
                      <span className={`expert-validation-status-badge ${item.status.toLowerCase()}`}>
                        {item.status}
                      </span>
                    </td>
                    <td>
                      <button className="expert-view-btn">View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="expert-validation-footer">
            <button className="expert-validate-btn">Validate</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Validation;
