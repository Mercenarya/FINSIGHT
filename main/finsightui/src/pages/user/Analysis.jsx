import React, { useState } from 'react';
import './Analysis.css';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend } from 'recharts';

const companyList = [
  
];



function Analysis() {
  const [activeTab, setActiveTab] = useState('balance-sheet');
  const [searchValue, setSearchValue] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [dropdownIndex, setDropdownIndex] = useState(-1);
  
  const [suggestions,setSuggestions] = useState([])
  
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

        <div className="controls-group">
          <button className="control-btn">Change Metrics</button>
          <button className="control-btn">Exchange Rate</button>
          <button className="btn-analyze">Analyze</button>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Revenue</span>
          </div>
          <div className="metric-value">$1,250,000</div>
          <div className="metric-change positive">+5%</div>
        </div>
        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Profit</span>
          </div>
          <div className="metric-value">$320,000</div>
          <div className="metric-change positive">+8%</div>
        </div>
        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Expenses</span>
          </div>
          <div className="metric-value">$185,000</div>
          <div className="metric-change negative">-3%</div>
        </div>
        <div className="metric-card">
          <div className="metric-header">
            <span className="metric-label">Cash Flow</span>
          </div>
          <div className="metric-value">$150,000</div>
          <div className="metric-change positive">+2%</div>
        </div>
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
