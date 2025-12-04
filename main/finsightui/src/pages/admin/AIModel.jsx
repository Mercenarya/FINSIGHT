import React from 'react';
import './AIModel.css';

function AIModel() {
  const models = [
    { name: 'Sales Forecasting', version: '1.0' },
    { name: 'Customer Segmentation', version: '2.0' },
    { name: 'Risk Assessment', version: '1.0' },
    { name: 'Demand Forecasting', version: '1.0' },
  ];

  return (
    <div className="ai-model-page">
      <div className="ai-model-panel">
        <div className="model-table">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Version</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {models.map((model, index) => (
                <tr key={index}>
                  <td>{model.name}</td>
                  <td>{model.version}</td>
                  <td>
                    <button className="deploy-btn">Deploy</button>
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

export default AIModel;
