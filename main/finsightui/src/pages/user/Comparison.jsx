import React, { useState, useEffect } from 'react';
import './Comparison.css';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Cell } from 'recharts';

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

  const yearOptions = ['2020', '2021', '2022', '2023', '2024', '2025'];

  const quarterOptions = [
    { value: 'First_quarter', label: 'Q1' },
    { value: 'Second_quarter', label: 'Q2' },
    { value: 'Third_quarter', label: 'Q3' },
    { value: 'Fourth_quarter', label: 'Q4' },
  ];

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
  const COLORS = ['#00d9ff', '#F6B84B'];

  // Render comparison chart
  const renderComparisonChart = (data, title, company1Key, company2Key) => {
    if (!data || data.length === 0) {
      console.log('No chart data for:', title);
      return null;
    }

    console.log('Rendering chart:', title, 'Data:', data, 'Keys:', company1Key, company2Key);

    return (
      <div className="chart-section">
        <h3 className="section-title">{title}</h3>
        <div className="chart-placeholder-large" style={{ width: '100%', minHeight: 450 }}>
          <BarChart
            width={1100}
            height={400}
            data={data}
            margin={{ top: 20, right: 40, left: 40, bottom: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis
              dataKey="metric"
              stroke="rgba(255,255,255,0.7)"
              tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }}
              height={40}
            />
            <YAxis stroke="rgba(255,255,255,0.7)" tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 12 }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e3a5f', border: 'none', borderRadius: 8 }}
              labelStyle={{ color: '#fff' }}
            />
            <Legend wrapperStyle={{ paddingTop: 10 }} />
            <Bar dataKey={company1Key} name={company1Key} fill="#00d9ff" barSize={40} />
            <Bar dataKey={company2Key} name={company2Key} fill="#F6B84B" barSize={40} />
          </BarChart>
        </div>
      </div>
    );
  };

  return (
    <div className="comparison-page">
      <div className="comparison-header">
        <h2 className="page-title">Company Comparison</h2>
      </div>

      {/* Filter Section */}
      <div className="comparison-filters">
        <div className="filter-group">
          <label>Company 1</label>
          <input
            type="text"
            className="filter-input"
            placeholder="Enter ticker (e.g., VNM)"
            value={company1}
            onChange={(e) => setCompany1(e.target.value.toUpperCase())}
            style={{
              background: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
              padding: '12px 16px',
              color: '#fff',
              fontSize: '14px',
              width: '100%',
              outline: 'none'
            }}
          />
        </div>

        <div className="filter-group">
          <label>Company 2</label>
          <input
            type="text"
            className="filter-input"
            placeholder="Enter ticker (e.g., ICT)"
            value={company2}
            onChange={(e) => setCompany2(e.target.value.toUpperCase())}
            style={{
              background: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
              padding: '12px 16px',
              color: '#fff',
              fontSize: '14px',
              width: '100%',
              outline: 'none'
            }}
          />
        </div>

        <div className="filter-group">
          <label>Quarter</label>
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

        <button
          className="btn-compare btn-analyze"
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
              <div className="summary-value">{comparisonData.analysis?.profitability_winner}</div>
            </div>
            <div className="summary-metric">
              <div className="summary-label">Better Liquidity</div>
              <div className="summary-value">{comparisonData.analysis?.liquidity_winner || 'N/A'}</div>
            </div>
            <div className="summary-metric">
              <div className="summary-label">Better Efficiency</div>
              <div className="summary-value">{comparisonData.analysis?.efficiency_winner || 'N/A'}</div>
            </div>
            <div className="summary-metric">
              <div className="summary-label">Better Growth</div>
              <div className="summary-value">{comparisonData.analysis?.growth_winner}</div>
            </div>
          </div>

          {/* Profitability Chart */}
          {comparisonData.chart_data && renderComparisonChart(
            comparisonData.chart_data.profitability,
            '📊 Profitability Comparison',
            comparisonData.meta?.company1,
            comparisonData.meta?.company2
          )}

          {/* Liquidity Chart */}
          {comparisonData.chart_data && renderComparisonChart(
            comparisonData.chart_data.liquidity,
            '💧 Liquidity Comparison',
            comparisonData.meta?.company1,
            comparisonData.meta?.company2
          )}

          {/* Efficiency Chart */}
          {comparisonData.chart_data && renderComparisonChart(
            comparisonData.chart_data.efficiency,
            '⚡ Efficiency Comparison',
            comparisonData.meta?.company1,
            comparisonData.meta?.company2
          )}

          {/* Growth Chart */}
          {comparisonData.chart_data && renderComparisonChart(
            comparisonData.chart_data.growth,
            '📈 Growth Comparison',
            comparisonData.meta?.company1,
            comparisonData.meta?.company2
          )}

          {/* AI Recommendation Box */}
          <div className="ai-insight-box">
            <div className="insight-icon-large">🤖</div>
            <div className="insight-content">
              <h4 style={{ color: '#00d9ff', marginBottom: '12px', marginTop: 0 }}>
                AI Investment Recommendation (Gemini)
              </h4>
              <p className="insight-text-large" style={{ whiteSpace: 'pre-line' }}>
                {comparisonData.ai_recommendation || 'No AI recommendation available.'}
              </p>
            </div>
          </div>

          {/* Disclaimer */}
          <div style={{
            marginTop: '24px',
            padding: '16px',
            background: 'rgba(255,255,255,0.05)',
            borderRadius: '8px',
            fontSize: '13px',
            color: 'rgba(255,255,255,0.6)'
          }}>
            ⚠️ {comparisonData.prediction?.disclaimer}
          </div>
        </>
      )}
    </div>
  );
}

export default Comparison;
