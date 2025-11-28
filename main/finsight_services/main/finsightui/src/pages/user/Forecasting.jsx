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

function Forecasting() {
  const [selectedCompany, setSelectedCompany] = useState('Tesla');
  const [companyOpen, setCompanyOpen] = useState(false);
  const [timePeriod, setTimePeriod] = useState('1 Month');
  const [timePeriodOpen, setTimePeriodOpen] = useState(false);
  const [metric, setMetric] = useState('Revenue');
  const [metricOpen, setMetricOpen] = useState(false);
  const [year, setYear] = useState('Year');

  // sample time-series data (replace with real data from API)
  const sampleData = [
    { time: 'Jan', revenue: 120, profit: 18, roi: 5 },
    { time: 'Feb', revenue: 130, profit: 20, roi: 5.5 },
    { time: 'Mar', revenue: 140, profit: 22, roi: 6 },
    { time: 'Apr', revenue: 150, profit: 24, roi: 6.5 },
    { time: 'May', revenue: 160, profit: 26, roi: 7 },
    { time: 'Jun', revenue: 170, profit: 28, roi: 7.5 },
    { time: 'Jul', revenue: 180, profit: 30, roi: 8 },
  ];

  return (
    <div className="forecasting-page">
      {/* Header */}
      <div className="forecasting-header">
        <h2 className="page-title">Forecasting</h2>
      </div>

      <div className="forecasting-filters">
        <div className="filter-group">
          <label>Company</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setCompanyOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setCompanyOpen(s => !s)}>
              <span className="period-value">{selectedCompany}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z" fill="#b0b8c1" /></svg>
            </div>
            {companyOpen && (
              <div className="search-dropdown">
                {['Tesla','Apple','Microsoft'].map(c => (
                  <div key={c} className={`search-dropdown-item${c === selectedCompany ? ' active' : ''}`} onMouseDown={() => { setSelectedCompany(c); setCompanyOpen(false); }}>
                    {c}
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
          <label>Time Period</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setTimePeriodOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setTimePeriodOpen(s => !s)}>
              <span className="period-value">{timePeriod}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z" fill="#b0b8c1" /></svg>
            </div>
            {timePeriodOpen && (
              <div className="search-dropdown">
                {['1 Month','3 Month','6 Month','First Quarter','Second Quarter','Third Quarter', 'Fourth Quarter'].map(p => (
                  <div key={p} className={`search-dropdown-item${p === timePeriod ? ' active' : ''}`} onMouseDown={() => { setTimePeriod(p); setTimePeriodOpen(false); }}>
                    {p}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="filter-group">
          <label>Metric</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setMetricOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setMetricOpen(s => !s)}>
              <span className="period-value">{metric}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z" fill="#b0b8c1" /></svg>
            </div>
            {metricOpen && (
              <div className="search-dropdown">
                {['Revenue','Profit','Cash Flow'].map(m => (
                  <div key={m} className={`search-dropdown-item${m === metric ? ' active' : ''}`} onMouseDown={() => { setMetric(m); setMetricOpen(false); }}>
                    {m}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <button className="btn-run">Run</button>
      </div>

      <div className="forecasting-panel">
        <h3 className="section-title">Forecast Visualization</h3>

        <div className="forecast-chart-large">
          {/* Time-series sample data: replace with real data as needed */}
          <ResponsiveContainer width="100%" height={480}>
            <LineChart data={sampleData} margin={{ top: 24, right: 48, left: 12, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="time" stroke="rgba(255,255,255,0.7)" />
              <YAxis yAxisId="left" stroke="rgba(255,255,255,0.7)" />
              <YAxis yAxisId="right" orientation="right" stroke="rgba(255,255,255,0.7)" />
              <Tooltip formatter={(value, name) => {
                if (name === 'ROI') return `${value}%`;
                return `${value}M`;
              }} />
              <Legend verticalAlign="top" wrapperStyle={{ color: 'rgba(255,255,255,0.9)', paddingBottom: 8 }} />

              <Line yAxisId="left" type="monotone" dataKey="revenue" name="Revenue" stroke="#00d9ff" strokeWidth={3} dot={false} />
              <Line yAxisId="left" type="monotone" dataKey="profit" name="Profit" stroke="#4A90E2" strokeWidth={3} dot={false} />
              <Line yAxisId="right" type="monotone" dataKey="roi" name="ROI" stroke="#F6B84B" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Metrics row removed — chart expanded to fill this space */}

        <div className="ai-insight-forecast">
          <div className="insight-icon-large">🤖</div>
          <p className="insight-text-forecast">
            <strong>AI Insight:</strong> Forecasted 3% increase in revenue for the next quarter. 
            Suggested investing in market expansion strategies.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Forecasting;
