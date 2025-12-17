import React, { useState, useEffect } from 'react';
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

const API_BASE_URL = 'http://localhost:8001';

const ComparisonBlock = ({ dashboardData, loading }) => {
  // Prepare chart data from API response
  const revenueData = dashboardData.slice(0, 5).map(item => ({
    name: item.company,
    revenue: parseFloat(item.revenue.replace(/[BMK]/g, '')) || 0,
    netProfit: parseFloat(item.netProfit.replace(/[BMK]/g, '')) || 0,
  }));

  const growthData = dashboardData.slice(0, 5).map(item => ({
    name: item.company,
    growth: item.growth || 0,
    roi: parseFloat(item.roi.replace('%', '')) || 0,
  }));

  // Calculate summary metrics
  const avgRevGrowth = dashboardData.length > 0
    ? (dashboardData.reduce((sum, item) => sum + (item.growth || 0), 0) / dashboardData.length).toFixed(1)
    : 0;
  const avgROI = dashboardData.length > 0
    ? (dashboardData.reduce((sum, item) => sum + parseFloat(item.roi || 0), 0) / dashboardData.length).toFixed(1)
    : 0;
  const avgDebtRatio = dashboardData.length > 0
    ? (dashboardData.reduce((sum, item) => sum + (item.debtRatio || 0), 0) / dashboardData.length).toFixed(2)
    : 0;

  return (
    <div className="comparison-section">
      <div className="comparison-header">
        <div>
          <h3 className="section-title">Company & Industry Comparison</h3>
          <div className="comparison-subtitle">Compare financial performance metrics across selected companies or industries.</div>
        </div>
        <div className="comparison-controls">
          <select className="control-select">
            <option>All Companies</option>
          </select>
          <select className="control-select">
            <option>Q3 2024</option>
            <option>Q2 2024</option>
            <option>Q1 2024</option>
          </select>
        </div>
      </div>

      <div className="comparison-metrics">
        <div className="summary-card">Revenue Growth %<div className="summary-value">{avgRevGrowth}%</div></div>
        <div className="summary-card">Net Profit Margin<div className="summary-value">{avgRevGrowth}%</div></div>
        <div className="summary-card">ROI<div className="summary-value">{avgROI}%</div></div>
        <div className="summary-card">Debt-to-Equity Ratio<div className="summary-value">{avgDebtRatio}</div></div>
        <div className="summary-card">Companies<div className="summary-value">{dashboardData.length}</div></div>
      </div>

      <div className="comparison-body">
        <div className="comparison-charts">
          <div className="chart-card">
            <div className="chart-card-title">Revenue & Net Profit Comparison</div>
            <div className="chart-placeholder">
              {loading ? (
                <div style={{ textAlign: 'center', padding: '60px', color: 'rgba(255,255,255,0.6)' }}>Loading...</div>
              ) : (
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={revenueData}>
                    <XAxis dataKey="name" stroke="#9aa4b2" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="revenue" name="Revenue" fill="#f6b84b" />
                    <Bar dataKey="netProfit" name="Net Profit" fill="#4aa3ff" />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-card-title">Growth Trends Across Industries</div>
            <div className="chart-placeholder">
              {loading ? (
                <div style={{ textAlign: 'center', padding: '60px', color: 'rgba(255,255,255,0.6)' }}>Loading...</div>
              ) : (
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={growthData}>
                    <XAxis dataKey="name" stroke="#9aa4b2" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="growth" name="Growth %" stroke="#f6b84b" />
                    <Line type="monotone" dataKey="roi" name="ROI %" stroke="#4aa3ff" />
                  </LineChart>
                </ResponsiveContainer>
              )}
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
                {loading ? (
                  <tr>
                    <td colSpan="7" style={{ textAlign: 'center', padding: '20px' }}>Loading data...</td>
                  </tr>
                ) : dashboardData.length === 0 ? (
                  <tr>
                    <td colSpan="7" style={{ textAlign: 'center', padding: '20px' }}>No data available</td>
                  </tr>
                ) : (
                  dashboardData.map((item, index) => (
                    <tr key={index}>
                      <td>{item.company}</td>
                      <td>{item.industry}</td>
                      <td>{item.revenue}</td>
                      <td>{item.netProfit}</td>
                      <td>{item.roi}</td>
                      <td>{item.debtRatio}</td>
                      <td className={item.growth >= 0 ? 'positive' : 'negative'}>
                        {item.growth >= 0 ? '+' : ''}{item.growth}%
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          <div className="comparison-actions">
            <div className="ai-insight">AI Insight: Data fetched in real-time from MongoDB database.</div>
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
  const [dashboardData, setDashboardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch dashboard data on mount
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/api/v1/dashboard/`);
        const result = await response.json();

        if (result.data) {
          setDashboardData(result.data);
        } else if (result.error) {
          setError(result.error);
        }
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to connect to server');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();

    // Refresh data every 30 seconds for real-time updates
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  // Calculate key metrics from dashboard data
  const totalRevenue = dashboardData.reduce((sum, item) => {
    const val = item.revenue.replace(/[BMK]/g, '');
    const multiplier = item.revenue.includes('B') ? 1000000000 : item.revenue.includes('M') ? 1000000 : 1000;
    return sum + (parseFloat(val) || 0) * multiplier;
  }, 0);

  const totalProfit = dashboardData.reduce((sum, item) => {
    const val = item.netProfit.replace(/[BMK]/g, '');
    const multiplier = item.netProfit.includes('B') ? 1000000000 : item.netProfit.includes('M') ? 1000000 : 1000;
    return sum + (parseFloat(val) || 0) * multiplier;
  }, 0);

  const formatCurrency = (num) => {
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(1)}B`;
    if (num >= 1000000) return `$${(num / 1000000).toFixed(0)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(0)}K`;
    return `$${num.toFixed(0)}`;
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h3 className="section-title">Key Metrics Overview</h3>
          {error && <div style={{ color: '#f87171', fontSize: '13px' }}>{error}</div>}
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Total Revenue</div>
          <div className="metric-value">{loading ? '...' : formatCurrency(totalRevenue)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Total Profit</div>
          <div className="metric-value">{loading ? '...' : formatCurrency(totalProfit)}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Companies</div>
          <div className="metric-value">{loading ? '...' : dashboardData.length}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Last Updated</div>
          <div className="metric-value" style={{ fontSize: '16px' }}>{new Date().toLocaleTimeString()}</div>
        </div>
      </div>

      {/* AI Forecast Section */}
      <div className="forecast-section">
        <h3 className="section-title">AI Forecast: Next Quarter Projection</h3>
        <div className="forecast-chart-placeholder">
          <div className="chart-area">
            <p className="chart-placeholder-text">Real-time data from MongoDB - refreshes every 30 seconds</p>
          </div>
        </div>

        <div className="forecast-metrics">
          <div className="forecast-metric">
            <div className="forecast-label">Avg Growth Rate</div>
            <div className="forecast-value">
              {loading ? '...' : `${(dashboardData.reduce((s, i) => s + (i.growth || 0), 0) / (dashboardData.length || 1)).toFixed(1)}%`}
            </div>
            <div className="forecast-change positive">Real-time</div>
          </div>
          <div className="forecast-metric">
            <div className="forecast-label">Avg ROI</div>
            <div className="forecast-value">
              {loading ? '...' : `${(dashboardData.reduce((s, i) => s + parseFloat(i.roi || 0), 0) / (dashboardData.length || 1)).toFixed(1)}%`}
            </div>
            <div className="forecast-change positive">From API</div>
          </div>
          <div className="forecast-metric">
            <div className="forecast-label">Data Source</div>
            <div className="forecast-value">MongoDB</div>
          </div>
        </div>

        <button className="btn-primary">View Detailed Forecast →</button>
      </div>

      {/* Company & Industry Comparison Section */}
      <ComparisonBlock dashboardData={dashboardData} loading={loading} />
    </div>
  );
}

export default Dashboard;
