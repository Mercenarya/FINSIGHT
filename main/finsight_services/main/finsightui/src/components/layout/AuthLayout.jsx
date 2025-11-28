import React from 'react';
import { Outlet } from 'react-router-dom';
import './AuthLayout.css';

function AuthLayout() {
  return (
    <div className="auth-layout">
      <div className="auth-container">
        <div className="auth-left">
          <div className="auth-branding">
            <div className="brand-logo">
              <div className="brand-icon">📊</div>
            </div>
            <h1 className="brand-title">FinSight</h1>
            <p className="brand-subtitle">Smart Financial Analysis</p>
            
            <div className="brand-illustration">
              <div className="chart-bars">
                <div className="bar"></div>
                <div className="bar"></div>
                <div className="bar"></div>
                <div className="bar"></div>

              </div>
            </div>
          </div>
        </div>
        <div className="auth-right">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default AuthLayout;
