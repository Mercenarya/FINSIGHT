import React, { useState } from 'react';
import './Forecasting.css';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from 'recharts';
import axios from 'axios';

function Forecasting() {
  const [searchValue, setSearchValue] = useState("");
  const [companyList, setCompanyList] = useState([]);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [year, setYear] = useState("2023");
  const [period, setPeriod] = useState('Quarter 4');
  const [modalOpen, setModalOpen] = useState(false);
  const [modalCategory, setModalCategory] = useState(null);
  const [modalSelected, setModalSelected] = useState([]);
  const [selectionsByCategory, setSelectionsByCategory] = useState({});
  const [metricsOpen, setMetricsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState([]);
  const [insight, setInsight] = useState("Please select a company and metrics to view forecast.");

  const metricOptions = [
    { key: 'liquidity', label: 'Liquidity Forecasting' },
  ];

  const categoryItems = {
    liquidity: [
      { key: 'cash_ratio', label: 'Cash Ratio' },
      { key: 'quick_ratio', label: 'Quick Ratio' },
      { key: 'current_ratio', label: 'Current Ratio' },
    ]
  };

  const metricColors = {
    cash_ratio: '#f59e0b',
    quick_ratio: '#8b5cf6',
    current_ratio: '#ec4899',
  };

  // Format metric key thành readable label
  const formatLabel = (key) => {
    return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  const fetch_api_search = async (keyword) => {
    if (!keyword) return;
    try {
      const result = await axios.get(`http://127.0.0.1:8001/api/search/suggestions/?query=${keyword}`);
      setCompanyList(result.data || []);
    } catch (err) { console.error(err); }
  };

  const openCategoryModal = (categoryKey) => {
    setModalCategory(categoryKey);
    setModalSelected(selectionsByCategory[categoryKey] || []);
    setModalOpen(true);
  };

  const confirmModal = () => {
    setSelectionsByCategory({ ...selectionsByCategory, [modalCategory]: [...modalSelected] });
    setModalOpen(false);
    setMetricsOpen(false);
  };

  const handleRun = async () => {
    if (!searchValue) return alert("Please select a company");
    setLoading(true);
    try {
      const allSelected = Object.values(selectionsByCategory).flat();
      const quarterNum = period.replace('Quarter ', '');

      // Corrected URL with /api/ prefix
      const response = await axios.get(`http://127.0.0.1:8001/api/v1/forecast/`, {
        params: {
          company: searchValue,
          year: year,
          period: quarterNum,
          metrics: allSelected.join(',')
        }
      });

      if (response.data && response.data.chart_data) {
        setChartData(response.data.chart_data);
        setInsight(response.data.ai_insight || "Forecast analysis completed.");
      }
    } catch (error) {
      console.error(error);
      alert("Server connection error. Please check CORS or API path.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="forecasting-page">
      <div className="forecasting-header">
        <h2 className="page-title">Forecasting Analysis</h2>
      </div>

      <div className="forecasting-filters">
        <div className="filter-group">
          <label>Company</label>
          <div className="search-box">
            <input
              className="small-input"
              type="text"
              placeholder="Search company..."
              value={searchValue}
              onChange={(e) => { setSearchValue(e.target.value); fetch_api_search(e.target.value); }}
              onFocus={() => setDropdownOpen(true)}
              onBlur={() => setTimeout(() => setDropdownOpen(false), 200)}
            />

            {dropdownOpen && companyList.length > 0 && (
              <div className="search-dropdown">
                {companyList.map(c => (
                  <div key={c.result} className="search-dropdown-item" onMouseDown={() => setSearchValue(c.result)}>
                    {c.result}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="filter-group">
          <label>Year</label>
          <input className="small-input" value={year} onChange={e => setYear(e.target.value)} />
        </div>

        <div className="filter-group">
          <label>Metrics</label>
          <div className="metrics-wrapper">
            <button className="control-btn" onClick={() => setMetricsOpen(!metricsOpen)}>
              Select Forecast Metrics
            </button>
            {metricsOpen && (
              <div className="metrics-dropdown">
                {metricOptions.map(opt => (
                  <div key={opt.key} className="metrics-item" onClick={() => openCategoryModal(opt.key)}>
                    {opt.label}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <button className="btn-run" onClick={handleRun} disabled={loading}>
          {loading ? 'Calculating...' : 'Run Forecast'}
        </button>
      </div>

      <div className="forecasting-panel">
        <h3 className="section-title">Prediction Visualization</h3>
        <div className="forecast-chart-large">
          <ResponsiveContainer width="100%" height={480}>
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a3441" vertical={false} />
              <XAxis dataKey="quarter" stroke="#9aa4b2" tick={{ fill: '#ffffff' }} />
              <YAxis stroke="#9aa4b2" tick={{ fill: '#ffffff' }} domain={['auto', 'auto']} tickFormatter={(value) => typeof value === 'number' ? value.toFixed(2) : value} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1a2332', border: 'none', borderRadius: '8px' }}
                labelStyle={{ color: '#ffffff' }}
                formatter={(value, name) => [typeof value === 'number' ? value.toFixed(2) : value, formatLabel(name)]}
              />
              <Legend formatter={(value) => formatLabel(value)} />
              {Object.values(selectionsByCategory).flat().map(key => (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={key}
                  name={key}
                  stroke={metricColors[key]}
                  strokeWidth={3}
                  connectNulls={true}
                  dot={(props) => {
                    const { cx, cy, payload } = props;
                    if (payload.isForecast) {
                      return <circle cx={cx} cy={cy} r={6} fill="#fff" stroke={metricColors[key]} strokeWidth={2} />;
                    }
                    return <circle cx={cx} cy={cy} r={4} fill={metricColors[key]} />;
                  }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="ai-insight-forecast">
          <div className="insight-icon-large">🤖</div>
          <p className="insight-text-forecast">
            <strong>AI Prediction Insight:</strong> {insight}
          </p>
        </div>
      </div>

      {modalOpen && (
        <div className="metric-modal-overlay" onMouseDown={() => setModalOpen(false)}>
          <div className="metric-modal" onMouseDown={e => e.stopPropagation()} role="dialog" aria-modal="true">
            <div className="metric-modal-header">
              <div className="metric-modal-title">Choose Calculation</div>
              <div className="metric-modal-close" onClick={() => setModalOpen(false)} aria-label="Close">✕</div>
            </div>
            <div className="metric-modal-list">
              {categoryItems[modalCategory].map(item => {
                const checked = modalSelected.includes(item.key);
                return (
                  <div
                    key={item.key}
                    className="metric-modal-item"
                    onMouseDown={() => {
                      setModalSelected(prev => prev.includes(item.key) ? prev.filter(k => k !== item.key) : [...prev, item.key])
                    }}
                  >
                    <div className="metric-modal-left">
                      <span className="metric-modal-label">{item.label}</span>
                    </div>
                    <div className={`custom-checkbox${checked ? ' checked' : ''}`} aria-hidden />
                  </div>
                );
              })}
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

export default Forecasting;