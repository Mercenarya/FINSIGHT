import React, { useState, useEffect } from 'react';
import './Comparison.css';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

const API_BASE_URL = 'http://localhost:8001';

function Comparison() {
  // State for company selection
  const [company1, setCompany1] = useState('');
  const [company2, setCompany2] = useState('');
  const [company1Open, setCompany1Open] = useState(false);
  const [company2Open, setCompany2Open] = useState(false);
  const [quarter, setQuarter] = useState('Third_quarter');
  const [quarterOpen, setQuarterOpen] = useState(false);
  const [year, setYear] = useState('2024');
  const [yearOpen, setYearOpen] = useState(false);

  // State for data
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableCompanies, setAvailableCompanies] = useState(['ICT', 'PLP', 'SPM', 'VNM', 'VPL', 'VSI']);
  const [filteredCompanies1, setFilteredCompanies1] = useState([]);
  const [filteredCompanies2, setFilteredCompanies2] = useState([]);

  const yearOptions = ['2020', '2021', '2022', '2023', '2024', '2025'];

  const quarterOptions = [
    { value: 'First_quarter', label: 'Quarter 1' },
    { value: 'Second_quarter', label: 'Quarter 2' },
    { value: 'Third_quarter', label: 'Quarter 3' },
    { value: 'Fourth_quarter', label: 'Quarter 4' },
  ];

  // Filter companies based on search
  useEffect(() => {
    if (company1.length > 0) {
      const filtered = availableCompanies.filter(c =>
        c.toLowerCase().includes(company1.toLowerCase())
      );
      setFilteredCompanies1(filtered);
    } else {
      setFilteredCompanies1(availableCompanies);
    }
  }, [company1, availableCompanies]);

  useEffect(() => {
    if (company2.length > 0) {
      const filtered = availableCompanies.filter(c =>
        c.toLowerCase().includes(company2.toLowerCase())
      );
      setFilteredCompanies2(filtered);
    } else {
      setFilteredCompanies2(availableCompanies);
    }
  }, [company2, availableCompanies]);

  // Fetch comparison data
  const fetchComparison = async () => {
    if (!company1 || !company2) {
      setError('Please select 2 companies to compare');
      return;
    }

    if (company1 === company2) {
      setError('Please select 2 different companies');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/compare/?ticker1=${company1}&ticker2=${company2}&quarter=${quarter}&year=${year}`
      );
      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setComparisonData(null);
      } else {
        setComparisonData(data);
      }
    } catch (err) {
      setError('Cannot connect to server. Please try again.');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Chart colors
  const COLORS = { company1: '#00d9ff', company2: '#F6B84B' };

  // Render comparison chart
  const renderComparisonChart = (data, title, company1Key, company2Key) => {
    console.log('Rendering chart:', title, 'Data:', data, 'Keys:', company1Key, company2Key);

    if (!data || data.length === 0) {
      console.log('No data for chart:', title);
      return null;
    }

    return (
      <div className="chart-section">
        <h3 className="section-title">{title}</h3>
        <div className="chart-placeholder-large">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={data}
              margin={{ top: 20, right: 40, left: 40, bottom: 40 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis
                dataKey="metric"
                stroke="rgba(255,255,255,0.7)"
                tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 11 }}
                interval={0}
              />
              <YAxis stroke="rgba(255,255,255,0.7)" tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e3a5f', border: 'none', borderRadius: 8 }}
                labelStyle={{ color: '#fff' }}
              />
              <Legend wrapperStyle={{ paddingTop: 10 }} />
              <Bar dataKey={company1Key} name={company1Key} fill={COLORS.company1} barSize={40} />
              <Bar dataKey={company2Key} name={company2Key} fill={COLORS.company2} barSize={40} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  return (
    <div className="comparison-page">
      <div className="comparison-header">
        <h2 className="page-title">Comparison</h2>
      </div>

      {/* Filter Section */}
      <div className="comparison-filters">
        {/* Company 1 */}
        <div className="filter-group">
          <label>Company 1</label>
          <div className="search-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setCompany1Open(false), 150)}>
            <input
              type="text"
              className="filter-input company-search"
              placeholder="Enter ticker (e.g., VNM)"
              value={company1}
              onChange={(e) => setCompany1(e.target.value.toUpperCase())}
              onFocus={() => setCompany1Open(true)}
            />
            {company1Open && filteredCompanies1.length > 0 && (
              <div className="search-dropdown">
                {filteredCompanies1.map(c => (
                  <div
                    key={c}
                    className={`search-dropdown-item${c === company1 ? ' active' : ''}`}
                    onMouseDown={() => { setCompany1(c); setCompany1Open(false); }}
                  >
                    {c}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Company 2 */}
        <div className="filter-group">
          <label>Company 2</label>
          <div className="search-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setCompany2Open(false), 150)}>
            <input
              type="text"
              className="filter-input company-search"
              placeholder="Enter ticker (e.g., ICT)"
              value={company2}
              onChange={(e) => setCompany2(e.target.value.toUpperCase())}
              onFocus={() => setCompany2Open(true)}
            />
            {company2Open && filteredCompanies2.length > 0 && (
              <div className="search-dropdown">
                {filteredCompanies2.map(c => (
                  <div
                    key={c}
                    className={`search-dropdown-item${c === company2 ? ' active' : ''}`}
                    onMouseDown={() => { setCompany2(c); setCompany2Open(false); }}
                  >
                    {c}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Year */}
        <div className="filter-group">
          <label>Year</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setYearOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setYearOpen(open => !open)}>
              <span className="period-value">{year}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                <path d="M7 10l5 5 5-5z" fill="#b0b8c1" />
              </svg>
            </div>
            {yearOpen && (
              <div className="search-dropdown">
                {yearOptions.map(y => (
                  <div
                    key={y}
                    className={`search-dropdown-item${y === year ? ' active' : ''}`}
                    onMouseDown={() => { setYear(y); setYearOpen(false); }}
                  >
                    {y}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Time Range (Quarter) */}
        <div className="filter-group">
          <label>Time Range</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setQuarterOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setQuarterOpen(open => !open)}>
              <span className="period-value">{quarterOptions.find(q => q.value === quarter)?.label}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                <path d="M7 10l5 5 5-5z" fill="#b0b8c1" />
              </svg>
            </div>
            {quarterOpen && (
              <div className="search-dropdown">
                {quarterOptions.map(q => (
                  <div
                    key={q.value}
                    className={`search-dropdown-item${q.value === quarter ? ' active' : ''}`}
                    onMouseDown={() => { setQuarter(q.value); setQuarterOpen(false); }}
                  >
                    {q.label}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Compare Button */}
        <button
          className="btn-compare"
          onClick={fetchComparison}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Compare Now'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-message" style={{
          background: 'rgba(239, 68, 68, 0.2)',
          padding: '16px',
          borderRadius: '8px',
          marginBottom: '24px',
          color: '#f87171'
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* Info Banner - Show when no data */}
      {!comparisonData && !loading && !error && (
        <div className="info-banner">
          <span className="info-icon">ℹ️</span>
          <span>Select 2 companies and click "Compare Now" to view comparison data.</span>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading-state" style={{
          textAlign: 'center',
          padding: '48px',
          color: 'rgba(255,255,255,0.7)'
        }}>
          <div className="loading-spinner" style={{ fontSize: '24px', marginBottom: '16px' }}>⏳</div>
          Loading data and analyzing with AI...
        </div>
      )}

      {/* Results Section */}
      {comparisonData && !loading && (
        <>
          {/* Summary Metrics */}
          <div className="metrics-summary">
            <div className="summary-metric">
              <div className="summary-label">Better Profitability</div>
              <div className="summary-value">{comparisonData.analysis?.profitability_winner || 'N/A'}</div>
            </div>
            <div className="summary-metric">
              <div className="summary-label">Better Growth</div>
              <div className="summary-value">{comparisonData.analysis?.growth_winner || 'N/A'}</div>
            </div>
          </div>

          {/* Profitability Chart */}
          {comparisonData.chart_data?.profitability && renderComparisonChart(
            comparisonData.chart_data.profitability,
            'Profitability Comparison',
            comparisonData.meta?.company1,
            comparisonData.meta?.company2
          )}



          {/* Growth Chart */}
          {comparisonData.chart_data?.growth && renderComparisonChart(
            comparisonData.chart_data.growth,
            'Growth Comparison',
            comparisonData.meta?.company1,
            comparisonData.meta?.company2
          )}

          {/* AI Recommendation Box */}
          <div className="ai-insight-box">
            <div className="insight-icon-large">🤖</div>
            <div className="insight-content">
              <h4 style={{ color: '#00d9ff', marginBottom: '12px', marginTop: 0 }}>
                AI Investment Recommendation (Google Gemini)
              </h4>
              <p className="insight-text-large" style={{ whiteSpace: 'pre-line' }}>
                {comparisonData.ai_recommendation || 'Click Compare Now to get AI recommendation.'}
              </p>
            </div>
          </div>

          {/* Disclaimer */}
          {comparisonData.prediction?.disclaimer && (
            <div style={{
              marginTop: '24px',
              padding: '16px',
              background: 'rgba(255,255,255,0.05)',
              borderRadius: '8px',
              fontSize: '13px',
              color: 'rgba(255,255,255,0.6)'
            }}>
              ⚠️ {comparisonData.prediction.disclaimer}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Comparison;