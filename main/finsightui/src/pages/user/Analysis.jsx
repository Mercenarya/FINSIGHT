import React, { useState } from 'react';
import './Analysis.css';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import axios from 'axios';

function Analysis() {
  // ==================== STATE MANAGEMENT ====================
  // Company search
  const [companyList, setCompanyList] = useState([]);
  const [searchValue, setSearchValue] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // Analysis parameters
  const [year, setYear] = useState("");
  const [period, setPeriod] = useState('Quarter 1');
  const [periodOpen, setPeriodOpen] = useState(false);

  // Metrics selection
  const [metricsOpen, setMetricsOpen] = useState(false);
  const [selectedMetrics, setSelectedMetrics] = useState([]);
  const [selectionsByCategory, setSelectionsByCategory] = useState({});

  // Modal for metric selection
  const [modalOpen, setModalOpen] = useState(false);
  const [modalCategory, setModalCategory] = useState(null);
  const [modalSelected, setModalSelected] = useState([]);

  // Analysis results
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [metricCards, setMetricCards] = useState([
    { label: 'Revenue', value: '-', change: '-', positive: true },
    { label: 'Profit', value: '-', change: '-', positive: true },
    { label: 'Expenses', value: '-', change: '-', positive: false },
    { label: 'Cash Flow', value: '-', change: '-', positive: true },
  ]);

  // ==================== METRIC OPTIONS ====================
  const metricOptions = [
    { key: 'profitability', label: 'Profitability' },
    { key: 'efficiency', label: 'Efficiency' },
    { key: 'growth', label: 'Growth' },
    { key: 'liquidity', label: 'Liquidity' },
  ];

  const categoryItems = {
    liquidity: [
      { key: 'cash_ratio', label: 'Cash Ratio' },
      { key: 'quick_ratio', label: 'Quick Ratio' },
      { key: 'current_ratio', label: 'Current Ratio' },
    ],
    profitability: [
      { key: 'gross_profit_margin', label: 'Gross Profit Margin' },
      { key: 'opm_margin', label: 'Operating Profit Margin' },
      { key: 'npm_margin', label: 'Net Profit Margin' },
      { key: 'roa_ratio', label: 'Return on Assets' },
      { key: 'roe_profit', label: 'Return on Equity' },
      { key: 'eps_ratios', label: 'Earnings Per Share' },
    ],
    efficiency: [
      { key: 'inventory_turnover_ratio', label: 'Inventory Turnover Ratio' },
      { key: 'dio_stand', label: 'Days Inventory Outstanding' },
      { key: 'art_turnover', label: 'Accounts Receivable Turnover' },
      { key: 'tta_turnover', label: 'Total Asset Turnover' },
      { key: 'apt_turnover', label: 'Accounts Payable Turnover' },
      { key: 'dpo_outstanding', label: 'Days Payable Outstanding' },
    ],
    growth: [
      { key: 'single_growth_rate', label: 'Single Growth Rate' },
      { key: 'cagr_growth_rate', label: 'Compound Annual Growth Rate' },
    ]
  };

  // ==================== COMPANY SEARCH ====================
  async function fetch_api_search(keyword) {
    if (!keyword || keyword.trim().length === 0) {
      setCompanyList([]);
      return;
    }
    try {
      const result = await axios.get(
        `http://127.0.0.1:8001/api/search/suggestions/?query=${keyword}`
      );
      setCompanyList(result.data || []);
    } catch (error) {
      console.error(`Error search: ${error}`);
      setCompanyList([]);
    }
  }

  const handleSearchChange = (e) => {
    const text = e.target.value;
    setSearchValue(text);
    fetch_api_search(text);
    setDropdownOpen(true);
  };

  const handleSelectCompany = (company) => {
    setSearchValue(company);
    setDropdownOpen(false);
  };

  const filteredCompanies = companyList
    .map(c => c.result)
    .filter(name => name.toLowerCase().includes(searchValue.toLowerCase()));

  // ==================== METRICS MODAL ====================
  const openCategoryModal = (categoryKey) => {
    setModalCategory(categoryKey);
    const existing = selectionsByCategory[categoryKey] || [];
    setModalSelected(Array.isArray(existing) ? [...existing] : []);
    setModalOpen(true);
  };

  const toggleModalItem = (key) => {
    const exists = modalSelected.includes(key);
    if (!exists && modalSelected.length >= 4) {
      return;
    }
    setModalSelected(prev => exists ? prev.filter(p => p !== key) : [...prev, key]);
  };

  const confirmModal = () => {
    const updated = { ...selectionsByCategory, [modalCategory]: [...modalSelected] };
    setSelectionsByCategory(updated);
    const categoriesSelected = metricOptions.map(o => o.key).filter(k => updated[k] && updated[k].length > 0);
    setSelectedMetrics(categoriesSelected);
    setModalOpen(false);
  };

  const closeModal = () => {
    setModalOpen(false);
  };

  // ==================== ANALYZE FUNCTION ====================
  const handleAnalyze = async () => {
    // Validation
    if (!searchValue || searchValue.trim().length === 0) {
      setError("Please select a company");
      return;
    }
    if (!year || year.trim().length === 0) {
      setError("Please enter a year");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Gather all selected metric keys
      const allSelectedMetrics = [];
      Object.keys(selectionsByCategory).forEach(category => {
        if (selectionsByCategory[category] && selectionsByCategory[category].length > 0) {
          allSelectedMetrics.push(...selectionsByCategory[category]);
        }
      });

      // Convert period from "Quarter 1" to "1"
      const quarterNumber = period.replace('Quarter ', '');

      // Build API request parameters
      const params = {
        company: searchValue,
        year: year,
        period: quarterNumber,
      };

      // Add metrics if any selected
      if (allSelectedMetrics.length > 0) {
        params.metrics = allSelectedMetrics.join(',');
      }

      console.log('Analyzing with params:', params);

      // Call backend API
      const response = await axios.get('http://127.0.0.1:8001/api/analysis/', {
        params: params
      });

      console.log('Analysis response:', response.data);

      // Process the response
      const data = response.data;
      setAnalysisData(data);

      // Update metric cards with 4 default metrics
      if (data.metrics) {
        const cards = [
          {
            label: 'Revenue',
            value: formatValue(data.metrics.revenue?.value),
            change: formatChange(data.metrics.revenue?.change),
            positive: (data.metrics.revenue?.change || 0) >= 0
          },
          {
            label: 'Profit',
            value: formatValue(data.metrics.profit?.value),
            change: formatChange(data.metrics.profit?.change),
            positive: (data.metrics.profit?.change || 0) >= 0
          },
          {
            label: 'Expenses',
            value: formatValue(data.metrics.expenses?.value),
            change: formatChange(data.metrics.expenses?.change),
            positive: (data.metrics.expenses?.change || 0) < 0 // Lower is better
          },
          {
            label: 'Cash Flow',
            value: formatValue(data.metrics.cashflow?.value),
            change: formatChange(data.metrics.cashflow?.change),
            positive: (data.metrics.cashflow?.change || 0) >= 0
          }
        ];
        setMetricCards(cards);
      }

      // Update chart data - combine default metrics + selected metrics
      if (data.timeSeries) {
        setChartData(data.timeSeries);
      }

    } catch (error) {
      console.error('Analysis error:', error);
      setError(error.response?.data?.error || error.response?.data?.detail || 'Failed to fetch analysis data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // ==================== HELPER FUNCTIONS ====================
  const formatValue = (value) => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'number') {
      return value >= 1000000
        ? `$${(value / 1000000).toFixed(2)}M`
        : value >= 1000
          ? `$${(value / 1000).toFixed(2)}K`
          : `$${value.toFixed(2)}`;
    }
    return value;
  };

  const formatChange = (change) => {
    if (change === null || change === undefined) return '-';
    const num = typeof change === 'number' ? change : parseFloat(change);
    return `${num >= 0 ? '+' : ''}${num.toFixed(1)}%`;
  };

  // Get all metric keys for chart lines
  const getChartMetrics = () => {
    const metrics = ['revenue', 'profit', 'expenses', 'cashflow'];

    // Add selected custom metrics
    Object.keys(selectionsByCategory).forEach(category => {
      if (selectionsByCategory[category]) {
        metrics.push(...selectionsByCategory[category]);
      }
    });

    return metrics;
  };

  // Color palette for chart lines
  const metricColors = {
    revenue: '#00d9ff',
    profit: '#4aa3ff',
    expenses: '#ef4444',
    cashflow: '#10b981',
    // Additional metrics
    cash_ratio: '#f59e0b',
    quick_ratio: '#8b5cf6',
    current_ratio: '#ec4899',
    gross_profit_margin: '#14b8a6',
    opm_margin: '#f97316',
    npm_margin: '#06b6d4',
    roa_ratio: '#84cc16',
    roe_profit: '#eab308',
    single_growth_rate: '#6366f1',
    cagr_growth_rate: '#a855f7',
  };

  // Get human-readable label for metric key
  const getMetricLabel = (key) => {
    const allItems = Object.values(categoryItems).flat();
    const item = allItems.find(i => i.key === key);
    return item?.label || key;
  };

  // ==================== RENDER ====================
  return (
    <div className="analysis-page">
      {/* Header */}
      <div className="analysis-header">
        <h2 className="page-title">Analysis</h2>
      </div>

      {/* Controls Section */}
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
              <path d="M11 19a8 8 0 1 1 0-16 8 8 0 0 1 0 16z" stroke="#0f1724" strokeWidth="1.5" fill="#00d9ff" />
              <path d="M21 21l-4.35-4.35" stroke="#0f1724" strokeWidth="1.6" strokeLinecap="round" />
            </svg>
          </button>
          {dropdownOpen && filteredCompanies.length > 0 && (
            <div className="search-dropdown">
              {filteredCompanies.map((company, idx) => (
                <div
                  key={company}
                  className={`search-dropdown-item`}
                  onMouseDown={() => handleSelectCompany(company)}
                >
                  {company}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Year and Period controls */}
        <div className="search-extras">
          <input
            className="small-input"
            type="text"
            placeholder="Year"
            value={year}
            onChange={(e) => setYear(e.target.value)}
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
                {['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4'].map((p) => (
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

        {/* Action Buttons */}
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
                  const active = Array.isArray(selectedMetrics) && selectedMetrics.includes(opt.key);
                  return (
                    <div
                      key={opt.key}
                      className={`metrics-item${active ? ' active' : ''}`}
                      onMouseDown={() => {
                        setSelectedMetrics(prev => (Array.isArray(prev) && prev.includes(opt.key)) ? prev : [...(Array.isArray(prev) ? prev : []), opt.key]);
                        openCategoryModal(opt.key);
                      }}
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
          <button
            className="btn-analyze"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div style={{ padding: '10px', margin: '10px 0', backgroundColor: '#fee', color: '#c00', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {/* Metric Cards */}
      <div className="metrics-grid">
        {metricCards.map((m) => (
          <div className="metric-card" key={m.label}>
            <div className="metric-header">
              <span className="metric-label">{m.label}</span>
            </div>
            <div className="metric-value">{m.value}</div>
            <div className={`metric-change ${m.positive ? 'positive' : 'negative'}`}>{m.change}</div>
          </div>
        ))}
      </div>

      {/* Chart Section */}
      <div className="chart-section">
        <h3 className="section-title">Financial Metrics Trend</h3>
        <div className="chart-container">
          <div className="chart-placeholder">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData.length > 0 ? chartData : [
                { period: 'Q1', revenue: 0, profit: 0, expenses: 0, cashflow: 0 },
                { period: 'Q2', revenue: 0, profit: 0, expenses: 0, cashflow: 0 },
                { period: 'Q3', revenue: 0, profit: 0, expenses: 0, cashflow: 0 },
                { period: 'Q4', revenue: 0, profit: 0, expenses: 0, cashflow: 0 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a3441" />
                <XAxis dataKey="period" stroke="#9aa4b2" />
                <YAxis stroke="#9aa4b2" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a2332', border: '1px solid #2a3441' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend verticalAlign="top" align="right" />

                {/* Default metric lines */}
                {chartData.length > 0 && (
                  <>
                    <Line type="monotone" dataKey="revenue" name="Revenue" stroke={metricColors.revenue} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="profit" name="Profit" stroke={metricColors.profit} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="expenses" name="Expenses" stroke={metricColors.expenses} strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="cashflow" name="Cash Flow" stroke={metricColors.cashflow} strokeWidth={2} dot={false} />

                    {/* Dynamically add selected metric lines */}
                    {Object.keys(selectionsByCategory).map(category =>
                      selectionsByCategory[category]?.map(metricKey => (
                        <Line
                          key={metricKey}
                          type="monotone"
                          dataKey={metricKey}
                          name={getMetricLabel(metricKey)}
                          stroke={metricColors[metricKey] || '#999'}
                          strokeWidth={2}
                          dot={false}
                        />
                      ))
                    )}
                  </>
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="ratios-container">
        <div className="ratios-section">
          <h3 className="section-title">Financial Data by Period</h3>
          <table className="ratios-table">
            <thead>
              <tr>
                <th>Period</th>
                <th>Revenue</th>
                <th>Profit</th>
                <th>Expenses</th>
                <th>Cash Flow</th>
                {/* Dynamic columns for selected metrics */}
                {Object.keys(selectionsByCategory).map(category =>
                  selectionsByCategory[category]?.map(metricKey => (
                    <th key={metricKey}>{getMetricLabel(metricKey)}</th>
                  ))
                )}
              </tr>
            </thead>
            <tbody>
              {chartData.length > 0 ? chartData.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.period}</td>
                  <td>{formatValue(row.revenue)}</td>
                  <td>{formatValue(row.profit)}</td>
                  <td>{formatValue(row.expenses)}</td>
                  <td>{formatValue(row.cashflow)}</td>
                  {/* Dynamic cells for selected metrics */}
                  {Object.keys(selectionsByCategory).map(category =>
                    selectionsByCategory[category]?.map(metricKey => (
                      <td key={metricKey}>{row[metricKey] !== undefined ? formatValue(row[metricKey]) : '-'}</td>
                    ))
                  )}
                </tr>
              )) : (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#9aa4b2' }}>
                    No data available. Click "Analyze" to fetch data.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* AI Insight Section */}
        <div className="insight-section">
          <h3 className="section-title">AI Insight</h3>
          <div className="insight-box">
            <div className="insight-icon">💡</div>
            <p className="insight-text">
              {analysisData?.insight || 'Run analysis to see AI-generated insights about the company\'s financial health.'}
            </p>
          </div>
        </div>
      </div>

      {/* Metric Selection Modal */}
      {modalOpen && (
        <div className="metric-modal-overlay" onMouseDown={closeModal}>
          <div className="metric-modal" onMouseDown={e => e.stopPropagation()} role="dialog" aria-modal="true">
            <div className="metric-modal-header">
              <div className="metric-modal-title">Choose Calculation</div>
              <div className="metric-modal-close" onClick={closeModal} aria-label="Close">✕</div>
            </div>

            <div className="metric-modal-list">
              {(modalCategory && categoryItems[modalCategory]) ? categoryItems[modalCategory].map(item => {
                const checked = modalSelected.includes(item.key);
                return (
                  <div
                    key={item.key}
                    className="metric-modal-item"
                    onMouseDown={() => toggleModalItem(item.key)}
                  >
                    <div className="metric-modal-left">
                      <span className="metric-modal-label">{item.label}</span>
                    </div>
                    <div className={`custom-checkbox${checked ? ' checked' : ''}`} aria-hidden />
                  </div>
                );
              }) : <div className="metric-modal-item"><span className="metric-modal-label">No items</span></div>}
            </div>

            <div className="metric-modal-footer">
              <button className="metric-modal-confirm" onMouseDown={confirmModal}>Confirm</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Analysis;