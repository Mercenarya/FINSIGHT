import React, { useState, useEffect } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import './UserLayout.css';

function UserLayout() {
  const location = useLocation();
  const [username, setUsername] = useState('user');

  useEffect(() => {
    // Get user info from localStorage
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        setUsername(user.username || 'user');
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
  }, []);

  const menuItems = [
    { path: '/user/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/user/analysis', label: 'Analysis', icon: '📈' },
    { path: '/user/comparison', label: 'Comparison', icon: '⚖️' },
    { path: '/user/forecasting', label: 'Forecasting', icon: '🔮' },
    { path: '/user/help', label: 'Help', icon: '❓' },
  ];

  return (
    <div className="user-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-logo">FinSight</h2>
        </div>
        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
          <Link to="/login" className="logout-btn">
            <span className="nav-icon">🚪</span>
            <span>Logout</span>
          </Link>
        </div>
      </aside>
      <main className="main-content">
        <header className="main-header">
          <h1>Dashboard</h1>
          <div className="user-info">
            <span>Hello, {username}</span>
          </div>
        </header>
        <div className="content-wrapper">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

export default UserLayout;
