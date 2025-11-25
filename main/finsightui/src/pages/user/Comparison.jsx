import React, { useState } from 'react';
import './Comparison.css';
import { ResponsiveContainer, BarChart, Bar, Line, XAxis, YAxis, Tooltip, Legend, LabelList, CartesianGrid } from 'recharts';

function Comparison() {
  const [selectedCompanies, setSelectedCompanies] = useState(['Tesla', 'Apple', 'Microsoft']);
  const [timeRange, setTimeRange] = useState('Year');
  const [period, setPeriod] = useState('1 Month');
  const [periodOpen, setPeriodOpen] = useState(false);
  const [year, setYear] = useState('Year');
  const [company, setCompany] = useState('Tesla');
  const [companyOpen, setCompanyOpen] = useState(false);
  const [metric, setMetric] = useState('Revenue');
  const [metricOpen, setMetricOpen] = useState(false);

  const comparisonData = [
    {
      company: 'Tesla',
      industry: 'Automotive',
      revenue: 850,
      netProfit: 104,
      roi: 15,
      debtRatio: 0.35,
      growth: +10
    },
    {
      company: 'Apple',
      industry: 'Technology',
      revenue: 710,
      netProfit: 131,
      roi: 12,
      debtRatio: 0.45,
      growth: -5
    },
    {
      company: 'Microsoft',
      industry: 'Technology',
      revenue: 794,
      netProfit: 152,
      roi: 14,
      debtRatio: 0.40,
      growth: +8
    }
  ];

  // Prepare numeric data for charts (strip non-digits and parse as numbers)
  const barData = comparisonData.map(item => ({
    company: item.company,
    revenue: parseInt(String(item.revenue).replace(/[^0-9]/g, '')) || 0,
    netProfit: parseInt(String(item.netProfit).replace(/[^0-9]/g, '')) || 0,
    roi: parseInt(String(item.roi).replace(/[^0-9]/g, '')) || 0,
  }));

  return (
    <div className="comparison-page">
      <div className="comparison-header">
        <h2 className="page-title">Comparison</h2>
      </div>

      <div className="comparison-filters">
        <div className="filter-group">
          <label>Company</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setCompanyOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setCompanyOpen(open => !open)}>
              <span className="period-value">{company}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 10l5 5 5-5z" fill="#b0b8c1" />
              </svg>
            </div>
            {companyOpen && (
              <div className="search-dropdown">
                {['Tesla','Apple','Microsoft','Amazon'].map(c => (
                  <div
                    key={c}
                    className={`search-dropdown-item${c === company ? ' active' : ''}`}
                    onMouseDown={() => { setCompany(c); setCompanyOpen(false); }}
                  >
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
          <label>Time Range</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setPeriodOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setPeriodOpen(open => !open)}>
              <span className="period-value">{period}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 10l5 5 5-5z" fill="#b0b8c1" />
              </svg>
            </div>
            {periodOpen && (
              <div className="search-dropdown">
                {['1 Month','6 Month','First Quarter','Second Quarter','Third Quarter','Fourth Quarter'].map(p => (
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
        <div className="filter-group">
          <label>Metric</label>
          <div className="period-wrapper" tabIndex={0} onBlur={() => setTimeout(() => setMetricOpen(false), 150)}>
            <div className="filter-select period-trigger" onClick={() => setMetricOpen(open => !open)}>
              <span className="period-value">{metric}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 10l5 5 5-5z" fill="#b0b8c1" />
              </svg>
            </div>
            {metricOpen && (
              <div className="search-dropdown">
                {['Revenue','Profit','ROI'].map(m => (
                  <div
                    key={m}
                    className={`search-dropdown-item${m === metric ? ' active' : ''}`}
                    onMouseDown={() => { setMetric(m); setMetricOpen(false); }}
                  >
                    {m}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <button className="btn-compare btn-analyze">Compare Now</button>
      </div>

      <div className="metrics-summary">
        <div className="summary-metric">
          <div className="summary-label">Average Revenue Growth</div>
          <div className="summary-value">19%</div>
        </div>
        <div className="summary-metric">
          <div className="summary-label">Profit Margin</div>
          <div className="summary-value">17.5%</div>
        </div>
        <div className="summary-metric">
          <div className="summary-label">ROE</div>
          <div className="summary-value">34%</div>
        </div>
      </div>

      <div className="chart-section">
        <h3 className="section-title">Revenue, Net Profit & ROI</h3>
        <div className="chart-placeholder-large">
          <div className="bar-chart-area chart-card" style={{height: 420}}>
            <ResponsiveContainer width="100%" height="100%">
              {/* Grouped bar chart: revenue + netProfit on left axis, ROI on right axis */}
              <BarChart data={barData} margin={{ top: 48, right: 40, left: 12, bottom: 20 }} barCategoryGap={'25%'} barGap={6}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="company" stroke="rgba(255,255,255,0.7)" interval={0} tick={{ fill: 'rgba(255,255,255,0.8)' }} />
                <YAxis yAxisId="left" stroke="rgba(255,255,255,0.7)" tick={{ fill: 'rgba(255,255,255,0.8)' }} label={{ value: 'Value (M)', angle: -90, position: 'insideLeft', fill: 'rgba(255,255,255,0.8)' }} />
                <YAxis yAxisId="right" orientation="right" stroke="rgba(255,255,255,0.7)" tick={{ fill: 'rgba(255,255,255,0.8)' }} label={{ value: 'ROI (%)', angle: 90, position: 'insideRight', fill: 'rgba(255,255,255,0.8)' }} />
                <Tooltip formatter={(value, name) => {
                  if (name === 'ROI') return `${value}%`;
                  return `${value}M`;
                }} />
                <Legend verticalAlign="top" align="center" wrapperStyle={{ paddingBottom: 8, color: 'rgba(255,255,255,0.9)' }} />

                <Bar yAxisId="left" dataKey="revenue" name="Revenue" fill="#F6B84B" barSize={36}>
                  <LabelList dataKey="revenue" position="top" formatter={val => `${val}M`} style={{fill: 'rgba(255,255,255,0.9)', fontSize: 12}} />
                </Bar>
                <Bar yAxisId="left" dataKey="netProfit" name="Net Profit" fill="#4AA3FF" barSize={28}>
                  <LabelList dataKey="netProfit" position="top" formatter={val => `${val}M`} style={{fill: 'rgba(255,255,255,0.9)', fontSize: 12}} />
                </Bar>
                <Bar yAxisId="right" dataKey="roi" name="ROI" fill="#10B981" barSize={20}>
                  <LabelList dataKey="roi" position="top" formatter={val => `${val}%`} style={{fill: 'rgba(255,255,255,0.9)', fontSize: 12}} />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="chart-section">
        <h3 className="section-title">Growth Trend</h3>
        <div className="chart-placeholder-large">
          <div className="line-chart-area">
            <svg width="100%" height="200" viewBox="0 0 600 200">
              <path d="M 50 150 L 200 120 L 350 100 L 500 80" 
                    stroke="#4A90E2" strokeWidth="3" fill="none"/>
              <path d="M 50 140 L 200 130 L 350 115 L 500 95" 
                    stroke="#FFA500" strokeWidth="3" fill="none"/>
            </svg>
          </div>
        </div>
      </div>

      <div className="comparison-table-section">
        <h3 className="section-title">Detailed Comparison</h3>
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Industry</th>
              <th>Revenue</th>
              <th>Net Profit</th>
              <th>ROE</th>
              <th>Debt Ratio</th>
              <th>Revenue Growth</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>PPF</td>
              <td>CPG (Fast Moving...)</td>
              <td className="value-green">524.1</td>
              <td className="value-green">6.00</td>
              <td>26.2</td>
              <td>0.5</td>
              <td className="value-green">19%</td>
            </tr>
            <tr>
              <td>VNM</td>
              <td>Food (Dairy...)</td>
              <td className="value-green">67.00</td>
              <td className="value-green">6.00</td>
              <td>31.0</td>
              <td>0.5</td>
              <td className="value-green">4%</td>
            </tr>
            <tr>
              <td>HPG</td>
              <td>Basic (Iron, Steel...)</td>
              <td className="value-green">158.00</td>
              <td className="value-green">10.00</td>
              <td>25.4</td>
              <td>0.5</td>
              <td className="value-green">6%</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="ai-insight-box">
        <div className="insight-icon-large">🤖</div>
        <p className="insight-text-large">
          Nhật đầu tư vào PPF khi tỷ lệ vốn của nợ là 0.5, tăng 5% trong năm ngoái. 
          HPG nhảy từ chậm lớn trước phí sinh lời từ thép trong ngành.
        </p>
      </div>
    </div>
  );
}

export default Comparison;
