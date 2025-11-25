import React, { useState } from 'react';
import './Analysis.css';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';

const companyList = [
  "Apple Inc.",
  "Microsoft Corp.",
  "FPT Corp.",
  "Vin C.",
];

function Analysis() {
  const [activeTab, setActiveTab] = useState('balance-sheet');
  const [searchValue, setSearchValue] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [dropdownIndex, setDropdownIndex] = useState(-1);
  const [metricsOpen, setMetricsOpen] = useState(false);
  const [selectedMetrics, setSelectedMetrics] = useState([]);
  const [period, setPeriod] = useState('1 Month');
  const [periodOpen, setPeriodOpen] = useState(false);

  const filteredCompanies = companyList.filter(c =>
    c.toLowerCase().includes(searchValue.toLowerCase())
  );

  const handleSearchChange = e => {
    setSearchValue(e.target.value);
    setDropdownIndex(-1);
    setDropdownOpen(true);
  };

  const handleSelectCompany = company => {
    setSearchValue(company);
    setDropdownOpen(false);
  };

  const metricOptions = [
    { key: 'profitability', label: 'Profitability' },
    { key: 'efficiency', label: 'Efficiency' },
    { key: 'growth', label: 'Growth' },
    { key: 'liquidity', label: 'Liquidity' },
  ];

  const toggleMetric = (key) => {
    const exists = selectedMetrics.includes(key);
    if (!exists && selectedMetrics.length >= 4) {
      // limit reached
      alert('Maximum 4 metrics can be selected');
      return;
    }
    setSelectedMetrics(prev => exists ? prev.filter(p => p !== key) : [...prev, key]);
  };

  const metricDataMap = {
    profitability: { label: 'Profitability', value: '18%', change: '+8%', positive: true },
    efficiency: { label: 'Efficiency', value: '1.8', change: '-3%', positive: false },
    growth: { label: 'Growth', value: '+12%', change: '+12%', positive: true },
    liquidity: { label: 'Liquidity', value: '2.5', change: '+1%', positive: true },
    revenue: { label: 'Revenue', value: '$1,250,000', change: '+5%', positive: true },
    profit: { label: 'Profit', value: '$320,000', change: '+8%', positive: true },
    expenses: { label: 'Expenses', value: '$185,000', change: '-3%', positive: false },
    cash: { label: 'Cash Flow', value: '$150,000', change: '+2%', positive: true },
  };

  const getMetricCards = () => {
    if (selectedMetrics.length > 0) {
      return selectedMetrics.map(k => metricDataMap[k] || { label: k, value: '-', change: '' });
    }
    // default cards
    return [metricDataMap.revenue, metricDataMap.profit, metricDataMap.expenses, metricDataMap.cash];
  };

  return (
    <div className="analysis-page">
      {/* Header */}
      <div className="analysis-header">
        <h2 className="page-title">Analysis</h2>
      </div>

      <div className="analysis-controls">
        <div className="search-box">
          <input
            className="search-input"
            type="text"
            placeholder="Search company..."
            value={searchValue}
            onChange={handleSearchChange}
            onFocus={() => setDropdownOpen(true)}
            onBlur={() => setTimeout(() => setDropdownOpen(false), 150)}
          />
          <button className="search-btn" aria-label="Search">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M11 19a8 8 0 1 1 0-16 8 8 0 0 1 0 16z" stroke="#0f1724" strokeWidth="1.5" fill="#00d9ff"/>
              <path d="M21 21l-4.35-4.35" stroke="#0f1724" strokeWidth="1.6" strokeLinecap="round"/>
            </svg>
          </button>
          {dropdownOpen && filteredCompanies.length > 0 && (
            <div className="search-dropdown">
              {filteredCompanies.map((company, idx) => (
                <div
                  key={company}
                  className={`search-dropdown-item${idx === dropdownIndex ? ' active' : ''}`}
                  onMouseDown={() => handleSelectCompany(company)}
                >
                  {company}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* New small controls: Year input and Period select */}
        <div className="search-extras">
          <input
            className="small-input"
            type="text"
            placeholder="Year"
          />
          <div
            className="period-wrapper"
            tabIndex={0}
            onBlur={() => setTimeout(() => setPeriodOpen(false), 150)}
          >
            <div
              className="filter-select period-trigger"
              onClick={() => setPeriodOpen(!periodOpen)}
            >
              <span className="period-value">{period}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 10l5 5 5-5z" fill="#b0b8c1" />
              </svg>
            </div>

            {periodOpen && (
              <div className="search-dropdown" style={{ width: 150 }}>
                {['1 Month','6 Month','First Quarter','Second Quarter','Third Quarter','Fourth Quarter'].map((p) => (
                  <div
                    key={p}
                    className={`search-dropdown-item${p === period ? ' active' : ''}`}
                    onMouseDown={() => { setPeriod(p); setPeriodOpen(false); }}
                  >
                    {p}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="controls-group">
          <div
            className="metrics-wrapper"
            tabIndex={0}
          >
            <button
              className="control-btn"
              onClick={() => setMetricsOpen(open => !open)}
              aria-haspopup="true"
              aria-expanded={metricsOpen}
            >
              Change Metrics
            </button>

            {metricsOpen && (
              <div className="metrics-dropdown">
                {metricOptions.map(opt => {
                  const active = selectedMetrics.includes(opt.key);
                  return (
                    <div
                      key={opt.key}
                      className={`metrics-item${active ? ' active' : ''}`}
                      onMouseDown={() => toggleMetric(opt.key)}
                    >
                      <span className="metrics-label">{opt.label}</span>
                      {active ? <span className="metrics-check">✓</span> : <span className="metrics-box" />}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <button className="control-btn">Exchange Rate</button>
          <button className="btn-analyze">Analyze</button>
        </div>
      </div>

      <div className="metrics-grid">
        {getMetricCards().map((m) => (
          <div className="metric-card" key={m.label}>
            <div className="metric-header">
              <span className="metric-label">{m.label}</span>
            </div>
            <div className="metric-value">{m.value}</div>
            <div className={`metric-change ${m.positive ? 'positive' : 'negative'}`}>{m.change}</div>
          </div>
        ))}
      </div>

      <div className="chart-section">
        <h3 className="section-title">Revenue Trend</h3>
        <div className="chart-container">
          {/* Line chart showing 4 series: Revenue, Profit, Expenses, Cash Flow */}
          <div className="chart-placeholder">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={[
                  { name: 'Jan', revenue: 1000, profit: 200, expenses: 150, cash: 120 },
                  { name: 'Feb', revenue: 1200, profit: 240, expenses: 160, cash: 140 },
                  { name: 'Mar', revenue: 1400, profit: 260, expenses: 180, cash: 150 },
                  { name: 'Apr', revenue: 1300, profit: 250, expenses: 170, cash: 160 },
                  { name: 'May', revenue: 1500, profit: 300, expenses: 190, cash: 170 },
                  { name: 'Jun', revenue: 1700, profit: 340, expenses: 200, cash: 180 },
                ]}
              >
                <XAxis dataKey="name" stroke="#9aa4b2" />
                <YAxis stroke="#9aa4b2" />
                <Tooltip />
                <Legend verticalAlign="top" align="right" />
                  <Line type="linear" dataKey="revenue" name="Revenue" stroke="#00d9ff" strokeWidth={2} dot={false} />
                  <Line type="linear" dataKey="profit" name="Profit" stroke="#4aa3ff" strokeWidth={2} dot={false} />
                  <Line type="linear" dataKey="expenses" name="Expenses" stroke="#ef4444" strokeWidth={2} dot={false} />
                  <Line type="linear" dataKey="cash" name="Cash Flow" stroke="#10b981" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="ratios-container">
        <div className="ratios-section">
          <h3 className="section-title">Financial Ratios</h3>
          <table className="ratios-table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Ratio</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Liquidity Ratio</td>
                <td>Current Ratio</td>
                <td>2.5</td>
              </tr>
              <tr>
                <td>Profitability</td>
                <td>Net Profit Margin</td>
                <td>18%</td>
              </tr>
              <tr>
                <td>Efficiency</td>
                <td>Leverage Ratio</td>
                <td>1.8</td>
              </tr>
              <tr>
                <td>Solvency</td>
                <td>Debt-to-Equity</td>
                <td>0.45</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="insight-section">
          <h3 className="section-title">AI Insight</h3>
          <div className="insight-box">
            <div className="insight-icon">💡</div>
            <p className="insight-text">
              The company has strong short-term liquidity, 
              but profit margins are decreasing.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Analysis;
