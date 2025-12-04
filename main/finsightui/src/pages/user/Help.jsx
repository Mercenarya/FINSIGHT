import React, { useState } from 'react';
import './Help.css';

function Help() {
  const [openFaq, setOpenFaq] = useState(null);
  const [chatInput, setChatInput] = useState('');

  const toggleFaq = (index) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  return (
    <div className="help-page">
      {/* Header */}
      <div className="help-header">
        <h2 className="page-title">Help</h2>
        <p className="page-subtitle">Find support resources and get help</p>
      </div>

      <div className="quick-guide-section">
        <h3 className="section-title">Quick User Guide</h3>
        <div className="guide-cards">
          <div className="guide-card">
            <div className="guide-icon">🚀</div>
            <div className="guide-title">Getting Started</div>
          </div>
          <div className="guide-card">
            <div className="guide-icon">📊</div>
            <div className="guide-title">How to Compare</div>
          </div>
          <div className="guide-card">
            <div className="guide-icon">🔮</div>
            <div className="guide-title">How to Forecast</div>
          </div>
        </div>
      </div>

      <div className="help-content-grid">
        <div className="faq-section">
          <h3 className="section-title">FAQ Section</h3>
          
          <div className="faq-category">
            <div className="faq-category-header" onClick={() => toggleFaq(1)}>
              <span>Account Issues</span>
              <span className="faq-toggle">{openFaq === 1 ? '▼' : '▶'}</span>
            </div>
            {openFaq === 1 && (
              <div className="faq-content">
                <p className="faq-item">How do I reset my password?</p>
                <p className="faq-item">How do I change my email address?</p>
              </div>
            )}
          </div>

          <div className="faq-category">
            <div className="faq-category-header" onClick={() => toggleFaq(2)}>
              <span>Data Upload</span>
              <span className="faq-toggle">{openFaq === 2 ? '▼' : '▶'}</span>
            </div>
            {openFaq === 2 && (
              <div className="faq-content">
                <p className="faq-item">What file formats are supported?</p>
                <p className="faq-item">How large can my data file be?</p>
              </div>
            )}
          </div>

          <div className="faq-category">
            <div className="faq-category-header" onClick={() => toggleFaq(3)}>
              <span>Report Export</span>
              <span className="faq-toggle">{openFaq === 3 ? '▼' : '▶'}</span>
            </div>
          </div>

          <div className="faq-category">
            <div className="faq-category-header" onClick={() => toggleFaq(4)}>
              <span>Forecasting</span>
              <span className="faq-toggle">{openFaq === 4 ? '▼' : '▶'}</span>
            </div>
          </div>
        </div>

        <div className="ai-chat-section">
          <h3 className="section-title">AI Chat Support</h3>
          <div className="chat-box">
            <div className="chat-prompt">
              <p>Ask me AI assistant anything!</p>
              <input 
                type="text" 
                className="chat-input" 
                placeholder="Type your question..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
              />
              <button className="chat-send-btn">→</button>
            </div>
            <div className="suggested-topics">
              <p className="suggested-label">Suggested topics</p>
              <button className="topic-btn">How to export report to Excel?</button>
              <button className="topic-btn">How to upload data file?</button>
            </div>
          </div>
        </div>
      </div>

      <div className="help-bottom-grid">
        <div className="contact-section">
          <h3 className="section-title">Contact & Feedback</h3>
          <div className="contact-info">
            <p><strong>Email:</strong> support@finsight.com</p>
            <p><strong>Hotline:</strong> 1-800-555-0199</p>
          </div>
          <button className="btn-primary-help">Send Feedback</button>
        </div>

        <div className="documentation-section">
          <h3 className="section-title">Documentation</h3>
          <a href="#" className="doc-link">View API Docs →</a>
          <button className="btn-secondary-help">Report a Problem</button>
        </div>
      </div>
    </div>
  );
}

export default Help;
