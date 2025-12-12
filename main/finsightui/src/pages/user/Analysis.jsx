import React, { useState } from 'react';
import './Analysis.css';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell } from 'recharts';
import axios from 'axios';

function Analysis() {
  // ==================== QUẢN LÝ STATE ====================
  // Tìm kiếm công ty
  const [companyList, setCompanyList] = useState([]);
  const [searchValue, setSearchValue] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // Tham số phân tích
  const [year, setYear] = useState("");
  const [period, setPeriod] = useState('Quarter 1');
  const [periodOpen, setPeriodOpen] = useState(false);

  // Chọn chỉ số
  const [metricsOpen, setMetricsOpen] = useState(false);
  const [selectedMetrics, setSelectedMetrics] = useState([]);
  const [selectionsByCategory, setSelectionsByCategory] = useState({});

  // Modal chọn chỉ số
  const [modalOpen, setModalOpen] = useState(false);
  const [modalCategory, setModalCategory] = useState(null);
  const [modalSelected, setModalSelected] = useState([]);

  // Kết quả phân tích
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [metricCards, setMetricCards] = useState([]);

  // ==================== TÙY CHỌN CHỈ SỐ ====================
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

  // ==================== TÌM KIẾM CÔNG TY ====================
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

  // ==================== MODAL CHỈ SỐ ====================
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

  // ==================== HÀM PHÂN TÍCH ====================
  // ==================== HÀM PHÂN TÍCH (ĐÃ SỬA LỖI HIỂN THỊ) ====================
  const handleAnalyze = async () => {
    // 1. Validate Input
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
      // 2. Thu thập Metrics đã chọn
      const allSelectedMetrics = [];
      Object.keys(selectionsByCategory).forEach(category => {
        if (selectionsByCategory[category] && selectionsByCategory[category].length > 0) {
          allSelectedMetrics.push(...selectionsByCategory[category]);
        }
      });

      const quarterNumber = period.replace('Quarter ', '');

      const params = {
        company: searchValue,
        year: year,
        period: quarterNumber,
      };

      if (allSelectedMetrics.length > 0) {
        params.metrics = allSelectedMetrics.join(',');
      }

      // 3. Gọi API
      const response = await axios.get('http://127.0.0.1:8001/api/analysis/', {
        params: params
      });

      const rawData = response.data;

      // ================= QUAN TRỌNG: CHUẨN HÓA DỮ LIỆU =================
      // Tạo từ điển ánh xạ: "Tên Key từ API" : "Tên Key trong React Code"
      const keyMap = {
        // --- Nhóm Liquidity ---
        "cash ratio": "cash_ratio",
        "quick ratio": "quick_ratio",
        "current ratio": "current_ratio",

        // --- Nhóm Profitability ---
        "Gross marrgin": "gross_profit_margin",         // API sai chính tả 'marrgin', phải map đúng theo API
        "Operating profit margin": "opm_margin",
        "ROA Ratio value": "roa_ratio",
        "ROE Profit": "roe_profit",
        
        // --- Net Profit Margin (Lưu ý quan trọng) ---
        // Trong JSON bạn gửi không có key này. Nếu API cập nhật, hãy bỏ comment dòng dưới:
        // "Net Profit Margin": "npm_margin", 
        // "Net Income Margin": "npm_margin",
      };

      // Xử lý mảng chart_data: Đổi tên key cũ sang key mới
      const normalizedChartData = (rawData.chart_data || []).map(item => {
        // Chuẩn hóa tên Quý
        const newItem = { quarter: item.quarter || item.Quarter }; 

        // Duyệt qua tất cả các key trong object trả về từ API
        Object.keys(item).forEach(originalKey => {
          // Nếu key nằm trong bản đồ map thì dùng tên mới, nếu không thì giữ nguyên tên cũ
          const newKey = keyMap[originalKey] || originalKey;
          newItem[newKey] = item[originalKey];
        });

        return newItem;
      });

      console.log('Normalized Data (Dữ liệu đã chuẩn hóa):', normalizedChartData);

      // ================= CẬP NHẬT STATE =================
      setAnalysisData(rawData);
      setChartData(normalizedChartData);

      // Xử lý Metric Cards (Thẻ chỉ số ở trên cùng)
      if (normalizedChartData.length > 0 && allSelectedMetrics.length > 0) {
        // Lấy dữ liệu quý mới nhất (phần tử cuối cùng của mảng)
        const latestData = normalizedChartData[normalizedChartData.length - 1];
        const previousData = normalizedChartData.length > 1 ? normalizedChartData[normalizedChartData.length - 2] : null;

        const cards = allSelectedMetrics.map(metricKey => {
          const value = latestData[metricKey];
          const prevValue = previousData ? previousData[metricKey] : 0;
          
          // Tính % tăng trưởng
          let change = 0;
          if (typeof value === 'number' && typeof prevValue === 'number' && prevValue !== 0) {
             change = ((value - prevValue) / prevValue) * 100;
          }

          return {
            key: metricKey,
            label: getMetricLabel(metricKey),
            // Format giá trị hiển thị
            value: value !== undefined ? formatMetricValue(value, metricKey) : '-',
            change: formatChange(change),
            positive: change >= 0,
            color: metricColors[metricKey] || '#999'
          };
        });
        setMetricCards(cards);
      } else {
        setMetricCards([]);
      }

    } catch (error) {
      console.error('Analysis error:', error);
      setError('Failed to fetch data. Please check API connection.');
    } finally {
      setLoading(false);
    }
  };
  // ==================== HÀM HỖ TRỢ ====================
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

  // Format giá trị metric dựa vào loại metric (ratio, percentage, etc.)
  const formatMetricValue = (value, metricKey) => {
    if (value === null || value === undefined) return '-';
    if (typeof value !== 'number') return value;

    // Các metric là tỷ lệ (ratio) - hiển thị dạng số thập phân
    const ratioMetrics = ['cash_ratio', 'quick_ratio', 'current_ratio', 'inventory_turnover_ratio', 'art_turnover', 'tta_turnover', 'apt_turnover'];
    if (ratioMetrics.includes(metricKey)) {
      return value.toFixed(2);
    }

    // Các metric là phần trăm (margin, ROA, ROE, growth rate)
    const percentMetrics = ['gross_profit_margin', 'opm_margin', 'npm_margin', 'roa_ratio', 'roe_profit', 'single_growth_rate', 'cagr_growth_rate'];
    if (percentMetrics.includes(metricKey)) {
      return `${value.toFixed(2)}%`;
    }

    // Các metric là số ngày
    const dayMetrics = ['dio_stand', 'dpo_outstanding'];
    if (dayMetrics.includes(metricKey)) {
      return `${value.toFixed(0)} days`;
    }

    // EPS - hiển thị đơn vị tiền tệ
    if (metricKey === 'eps_ratios') {
      return `$${value.toFixed(2)}`;
    }

    // Mặc định
    return value.toFixed(2);
  };

  const formatChange = (change) => {
    if (change === null || change === undefined) return '-';
    const num = typeof change === 'number' ? change : parseFloat(change);
    return `${num >= 0 ? '+' : ''}${num.toFixed(1)}%`;
  };

  // Lấy tất cả key chỉ số cho đường biểu đồ
  const getChartMetrics = () => {
    const metrics = ['revenue', 'profit', 'expenses', 'cashflow'];

    // Thêm các chỉ số tùy chỉnh đã chọn
    Object.keys(selectionsByCategory).forEach(category => {
      if (selectionsByCategory[category]) {
        metrics.push(...selectionsByCategory[category]);
      }
    });

    return metrics;
  };

  // Bảng màu cho đường biểu đồ
  const metricColors = {
    revenue: '#00d9ff',
    profit: '#4aa3ff',
    expenses: '#ef4444',
    cashflow: '#10b981',
    // Chỉ số bổ sung
    cash_ratio: '#f59e0b',
    quick_ratio: '#8b5cf6',
    current_ratio: '#ec4899',
    gross_profit_margin: '#14b8a6',
    opm_margin: '#f97316',
    npm_margin: '#06b6d4',
    roa_ratio: '#84cc16',
    roe_profit: '#eab308',
    eps_ratios: '#22c55e',
    inventory_turnover_ratio: '#3b82f6',
    dio_stand: '#f472b6',
    art_turnover: '#fb923c',
    tta_turnover: '#a3e635',
    apt_turnover: '#2dd4bf',
    dpo_outstanding: '#c084fc',
    single_growth_rate: '#6366f1',
    cagr_growth_rate: '#a855f7',
  };

  // Lấy nhãn dễ đọc cho key chỉ số
  const getMetricLabel = (key) => {
    const allItems = Object.values(categoryItems).flat();
    const item = allItems.find(i => i.key === key);
    return item?.label || key;
  };

  // ==================== HIỂN THỊ ====================
  return (
    <div className="analysis-page">
      {/* Tiêu đề */}
      <div className="analysis-header">
        <h2 className="page-title">Analysis</h2>
      </div>

      {/* Phần điều khiển */}
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

        {/* Điều khiển Năm và Kỳ */}
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

        {/* Các nút hành động */}
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

      {/* Thông báo lỗi */}
      {error && (
        <div style={{ padding: '10px', margin: '10px 0', backgroundColor: '#fee', color: '#c00', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      {/* Thẻ chỉ số - chỉ hiển thị các metric đã chọn */}
      <div className="metrics-grid">
        {metricCards.length > 0 ? (
          metricCards.map((m) => (
            <div className="metric-card" key={m.key || m.label} style={{ borderTop: `3px solid ${m.color || '#00d9ff'}` }}>
              <div className="metric-header">
                <span className="metric-label">{m.label}</span>
                <span className="metric-color-dot" style={{ backgroundColor: m.color || '#00d9ff' }}></span>
              </div>
              <div className="metric-value">{m.value}</div>
              <div className={`metric-change ${m.positive ? 'positive' : 'negative'}`}>{m.change}</div>
            </div>
          ))
        ) : (
          <div className="metrics-empty-message">
            <p>📊 Select metrics from "Change Metrics" and click "Analyze" to view data.</p>
          </div>
        )}
      </div>

      {/* Phần biểu đồ */}
      <div className="chart-section">
        <h3 className="section-title">Financial Metrics Trend</h3>
        <div className="chart-container">
          <div className="chart-placeholder">
            {/* Lấy danh sách các metric đã chọn để hiển thị */}
            {(() => {
              // Thu thập tất cả metric đã chọn từ các category
              const selectedMetricKeys = [];
              Object.keys(selectionsByCategory).forEach(category => {
                if (selectionsByCategory[category] && selectionsByCategory[category].length > 0) {
                  selectedMetricKeys.push(...selectionsByCategory[category]);
                }
              });

              // Tạo dữ liệu cho BarChart với 4 quarters
              const barChartData = ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4'].map((quarter, idx) => {
                const dataPoint = { quarter };
                selectedMetricKeys.forEach(metricKey => {
                  // Lấy giá trị từ chartData nếu có, nếu không thì dùng giá trị mặc định
                  if (chartData.length > idx && chartData[idx][metricKey] !== undefined) {
                    dataPoint[metricKey] = chartData[idx][metricKey];
                  } else {
                    dataPoint[metricKey] = 0;
                  }
                });
                return dataPoint;
              });

              return (
                <div className="bar-chart-wrapper">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart
                      data={barChartData}
                      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#2a3441" />
                      <XAxis
                        dataKey="quarter"
                        stroke="#9aa4b2"
                        tick={{ fill: '#9aa4b2', fontSize: 12 }}
                        axisLine={{ stroke: '#2a3441' }}
                      />
                      <YAxis
                        stroke="#9aa4b2"
                        tick={{ fill: '#9aa4b2', fontSize: 12 }}
                        axisLine={{ stroke: '#2a3441' }}
                        tickFormatter={(value) => {
                          if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`;
                          if (value >= 1000) return `${(value / 1000).toFixed(1)}K`;
                          return value;
                        }}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1a2332',
                          border: '1px solid #2a3441',
                          borderRadius: '8px',
                          color: '#fff'
                        }}
                        labelStyle={{ color: '#00d9ff', fontWeight: 'bold' }}
                        formatter={(value, name) => [
                          typeof value === 'number' ? value.toLocaleString() : value,
                          getMetricLabel(name)
                        ]}
                      />

                      {/* Render Bar cho mỗi metric đã chọn */}
                      {selectedMetricKeys.map((metricKey) => (
                        <Bar
                          key={metricKey}
                          dataKey={metricKey}
                          name={metricKey}
                          fill={metricColors[metricKey] || '#999'}
                          radius={[4, 4, 0, 0]}
                        />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>

                  {/* Legend tùy chỉnh - nằm bên trong chart section nhưng tách biệt */}
                  {selectedMetricKeys.length > 0 && (
                    <div className="custom-chart-legend">
                      <div className="legend-title">Selected Metrics</div>
                      <div className="legend-items">
                        {selectedMetricKeys.map((metricKey) => (
                          <div key={metricKey} className="legend-item">
                            <span
                              className="legend-color"
                              style={{ backgroundColor: metricColors[metricKey] || '#999' }}
                            ></span>
                            <span className="legend-label">{getMetricLabel(metricKey)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Thông báo khi chưa chọn metric nào */}
                  {selectedMetricKeys.length === 0 && (
                    <div className="chart-empty-message">
                      <p>📊 No metrics selected. Please select metrics from "Change Metrics" and click "Analyze" to view the chart.</p>
                    </div>
                  )}
                </div>
              );
            })()}
          </div>
        </div>
      </div>

      {/* Bảng dữ liệu - Key Financial Metric */}
      <div className="ratios-container">
        <div className="ratios-section">
          <h3 className="section-title">Key Financial Metric</h3>
          {(() => {
            // Thu thập tất cả metric đã chọn
            const selectedMetricKeys = [];
            Object.keys(selectionsByCategory).forEach(category => {
              if (selectionsByCategory[category] && selectionsByCategory[category].length > 0) {
                selectedMetricKeys.push(...selectionsByCategory[category]);
              }
            });

            // Tạo dữ liệu bảng với 4 quarters
            const tableData = ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4'].map((quarter, idx) => {
              const rowData = { period: quarter };
              selectedMetricKeys.forEach(metricKey => {
                if (chartData.length > idx && chartData[idx][metricKey] !== undefined) {
                  rowData[metricKey] = chartData[idx][metricKey];
                } else {
                  rowData[metricKey] = null;
                }
              });
              return rowData;
            });

            if (selectedMetricKeys.length === 0) {
              return (
                <div className="table-empty-message">
                  <p>📊 No metrics selected. Please select metrics from "Change Metrics" and click "Analyze" to view data.</p>
                </div>
              );
            }

            return (
              <table className="ratios-table">
                <thead>
                  <tr>
                    <th>Period</th>
                    {selectedMetricKeys.map(metricKey => (
                      <th key={metricKey}>
                        <div className="table-header-cell">
                          <span className="table-header-color" style={{ backgroundColor: metricColors[metricKey] || '#999' }}></span>
                          {getMetricLabel(metricKey)}
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {tableData.map((row, idx) => (
                    <tr key={idx}>
                      <td className="period-cell">{row.period}</td>
                      {selectedMetricKeys.map(metricKey => (
                        <td key={metricKey}>
                          {row[metricKey] !== null ? formatMetricValue(row[metricKey], metricKey) : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            );
          })()}
        </div>

        {/* Phần phân tích AI */}
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

      {/* Modal chọn chỉ số */}
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