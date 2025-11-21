import React from 'react';
import './Dashboard.css';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  LineChart,
  Line,
} from 'recharts';

const ComparisonBlock = () => {
  const revenueData = [
    { name: 'Tesla', revenue: 850, netProfit: 104 },
    { name: 'Apple', revenue: 710, netProfit: 131 },
    { name: 'Microsoft', revenue: 794, netProfit: 152 },
  ];

  const growthData = [
    { name: 'Tesla', growth: 10, roi: 15 },
    { name: 'Apple', growth: -5, roi: 12 },
    { name: 'Microsoft', growth: 8, roi: 14 },
  ];

  return (
    <div className="comparison-section">
      <div className="comparison-header">
        <div>
          <h3 className="section-title">Company & Industry Comparison</h3>
          <div className="comparison-subtitle">Compare financial performance metrics across selected companies or industries.</div>
        </div>
        <div className="comparison-controls">
          <select className="control-select">
            <option>Companies</option>
          </select>
          <select className="control-select">
            <option>Time range</option>
          </select>
          <button className="btn-compare-now">Compare Now</button>
        </div>
      </div>

      <div className="comparison-metrics">
        <div className="summary-card">Revenue Growth %<div className="summary-value">15%</div></div>
        <div className="summary-card">Net Profit Margin<div className="summary-value">20%</div></div>
        <div className="summary-card">ROI<div className="summary-value">12%</div></div>
        <div className="summary-card">Debt-to-Equity Ratio<div className="summary-value">0.45</div></div>
        <div className="summary-card">Market Growth %<div className="summary-value">10%</div></div>
      </div>

      <div className="comparison-body">
        <div className="comparison-charts">
          <div className="chart-card">
            <div className="chart-card-title">Revenue & Net Profit Comparison</div>
            <div className="chart-placeholder">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={revenueData}>
                  <XAxis dataKey="name" stroke="#9aa4b2" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="revenue" name="Revenue" fill="#f6b84b" />
                  <Bar dataKey="netProfit" name="Net Profit" fill="#4aa3ff" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-card-title">Growth Trends Across Industries</div>
            <div className="chart-placeholder">
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={growthData}>
                  <XAxis dataKey="name" stroke="#9aa4b2" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="growth" name="Growth %" stroke="#f6b84b" />
                  <Line type="monotone" dataKey="roi" name="ROI %" stroke="#4aa3ff" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="comparison-table-card">
          <div className="table-wrapper">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Company</th>
                  <th>Industry</th>
                  <th>Revenue</th>
                  <th>Net Profit</th>
                  <th>ROI</th>
                  <th>Debt Ratio</th>
                  <th>Growth %</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Tesla</td>
                  <td>Automotive</td>
                  <td>850M</td>
                  <td>104M</td>
                  <td>15%</td>
                  <td>0.35</td>
                  <td className="positive">+10%</td>
                </tr>
                <tr>
                  <td>Apple</td>
                  <td>Technology</td>
                  <td>710M</td>
                  <td>131M</td>
                  <td>12%</td>
                  <td>0.45</td>
                  <td className="negative">-5%</td>
                </tr>
                <tr>
                  <td>Microsoft</td>
                  <td>Technology</td>
                  <td>794M</td>
                  <td>152M</td>
                  <td>14%</td>
                  <td>0.40</td>
                  <td className="positive">+8%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="comparison-actions">
            <div className="ai-insight">AI Insight: The Technology sector outperformed Energy by 12% ROI in 2025 due to higher efficiency and market expansion.</div>
            <div className="action-buttons">
              <button className="btn-export">Export Comparison Report</button>
              <button className="btn-generate">Generate AI Summary</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

function Dashboard() {
  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h3 className="section-title">Key Metrics Overview</h3>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Revenue</div>
          <div className="metric-value">$1,250,000</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Profit</div>
          <div className="metric-value">$320,000</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Expenses</div>
          <div className="metric-value">$185,000</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Cash Flow</div>
          <div className="metric-value">$150,000</div>
        </div>
      </div>

      {/* AI Forecast Section */}
      <div className="forecast-section">
        <h3 className="section-title">AI Forecast: Next Quarter Projection</h3>
        <div className="forecast-chart-placeholder">
          <div className="chart-area">
            {/* Placeholder for chart - will be filled with actual chart library */}
            <p className="chart-placeholder-text">Chart will be rendered here with Recharts</p>
          </div>
        </div>
        
        <div className="forecast-metrics">
          <div className="forecast-metric">
            <div className="forecast-label">Predicted Revenue</div>
            <div className="forecast-value">$155,000</div>
            <div className="forecast-change positive">+3.2%</div>
          </div>
          <div className="forecast-metric">
            <div className="forecast-label">Profit Margin</div>
            <div className="forecast-value">17%</div>
            <div className="forecast-change positive">+2.6%</div>
          </div>
          <div className="forecast-metric">
            <div className="forecast-label">Model Accuracy</div>
            <div className="forecast-value">87.6%</div>
          </div>
        </div>

        <button className="btn-primary">View Detailed Forecast →</button>
      </div>

      {/* Company & Industry Comparison Section (moved below forecast) */}
      <ComparisonBlock />
    </div>
  );
}

export default Dashboard;
