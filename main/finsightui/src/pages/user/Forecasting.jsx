import React, { useState } from 'react';
import './Forecasting.css';

function Forecasting() {
  const [selectedCompany, setSelectedCompany] = useState('');
  const [timePeriod, setTimePeriod] = useState('');
  const [metric, setMetric] = useState('');

  return (
    <div className="forecasting-page">
      {/* Header */}
      <div className="forecasting-header">
        <h2 className="page-title">Forecasting</h2>
      </div>

      <div className="forecasting-filters">
        <div className="filter-group">
          <label>Company</label>
          <select className="filter-select" value={selectedCompany} onChange={(e) => setSelectedCompany(e.target.value)}>
            <option value="">Select Company</option>
            <option value="tesla">Tesla</option>
            <option value="apple">Apple</option>
            <option value="microsoft">Microsoft</option>
          </select>
        </div>
        <div className="filter-group">
          <label>Time Period</label>
          <select className="filter-select" value={timePeriod} onChange={(e) => setTimePeriod(e.target.value)}>
            <option value="">Select Period</option>
            <option value="q1">Q1 2025</option>
            <option value="q2">Q2 2025</option>
            <option value="yearly">2025</option>
          </select>
        </div>
        <div className="filter-group">
          <label>Metric</label>
          <select className="filter-select" value={metric} onChange={(e) => setMetric(e.target.value)}>
            <option value="">Select Metric</option>
            <option value="revenue">Revenue</option>
            <option value="profit">Profit</option>
            <option value="cashflow">Cash Flow</option>
          </select>
        </div>
        <button className="btn-run">Run</button>
      </div>

      <div className="forecast-visualization">
        <h3 className="section-title">Forecast Visualization</h3>
        <div className="forecast-chart-large">
          <svg width="100%" height="300" viewBox="0 0 800 300">
            {/* Actual line */}
            <path d="M 50 250 L 150 230 L 250 220 L 350 210 L 450 200" 
                  stroke="#00d9ff" strokeWidth="3" fill="none"/>
            {/* Predicted line (solid) */}
            <path d="M 450 200 L 550 180 L 650 160 L 750 140" 
                  stroke="#00d9ff" strokeWidth="3" fill="none"/>
            {/* Predicted line (dashed) */}
            <path d="M 450 200 L 550 190 L 650 175 L 750 155" 
                  stroke="#00d9ff" strokeWidth="2" strokeDasharray="5,5" fill="none" opacity="0.6"/>
          </svg>
        </div>
      </div>

      <div className="forecast-metrics-row">
        <div className="forecast-metric-small">
          <div className="metric-icon">📈</div>
          <div className="metric-label-small">Revenue</div>
        </div>
        <div className="forecast-metric-small">
          <div className="metric-icon">📈</div>
          <div className="metric-label-small">Revenue</div>
        </div>
        <div className="forecast-metric-small">
          <div className="metric-icon">📊</div>
          <div className="metric-label-small">Ranking</div>
        </div>
      </div>

      <div className="ai-insight-forecast">
        <div className="insight-icon-large">🤖</div>
        <p className="insight-text-forecast">
          <strong>AI Insight:</strong> Forecasted 3% increase in revenue for the next quarter. 
          Suggested investing in market expansion strategies.
        </p>
      </div>
    </div>
  );
}

export default Forecasting;
