import React, { useState } from 'react';
import { Search, User } from 'lucide-react';
import './KnowledgeBase.css';

const knowledgeData = [
  {
    title: 'New Tax Regulations 2025',
    category: 'Policies',
    source: 'gov.vn',
    date: 'Jan 5, 2024',
    relatedModels: 'AI Model A',
    status: 'Active'
  },
  {
    title: 'Liquidity Ratio Guide',
    category: 'Financial Definitions',
    source: 'docs',
    date: 'May, 2024',
    relatedModels: 'AI Model B',
    status: 'Active'
  },
];

function KnowledgeBase() {
  const [activeTab, setActiveTab] = useState('Macro');

  const tabs = ['Macro', 'Policies', 'Financial Definitions', 'Industry Insights', 'Risk Indicators'];

  return (
    <div className="expert-knowledge">
      <header className="expert-header">
        <div className="expert-header-left">
          <h1 className="expert-page-title">Knowledge Base</h1>
        </div>
        <div className="expert-header-right">
          <div className="expert-search-box">
            <Search size={18} />
            <input type="text" placeholder="Search" />
          </div>
          <button className="expert-user-btn">
            <User size={20} />
            <span>Hello, user</span>
          </button>
        </div>
      </header>

      <div className="expert-knowledge-content">
        <div className="expert-knowledge-section">
          <div className="expert-knowledge-header">
            <div className="expert-knowledge-tabs">
              {tabs.map((tab) => (
                <button
                  key={tab}
                  className={`expert-knowledge-tab ${activeTab === tab ? 'active' : ''}`}
                  onClick={() => setActiveTab(tab)}
                >
                  {tab}
                </button>
              ))}
            </div>
            <button className="expert-add-knowledge-btn">Add Knowledge Item</button>
          </div>

          <div className="expert-knowledge-table">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Category</th>
                  <th>Source</th>
                  <th>Date</th>
                  <th>Related Models</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {knowledgeData.map((item, index) => (
                  <tr key={index}>
                    <td>{item.title}</td>
                    <td>{item.category}</td>
                    <td>{item.source}</td>
                    <td>{item.date}</td>
                    <td>{item.relatedModels}</td>
                    <td>
                      <span className="expert-knowledge-status active">{item.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default KnowledgeBase;
