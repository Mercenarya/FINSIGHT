import React, { useState, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import './UserLayout.css';

function UserLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [user, setUser] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  // Check authentication on mount
  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');

    if (!accessToken) {
      // No token, redirect to login
      navigate('/login', { replace: true });
      return;
    }

    // Parse user data if available
    if (userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (e) {
        console.error('Failed to parse user data:', e);
      }
    }
  }, [navigate]);

  // Handle logout
  const handleLogout = (e) => {
    e.preventDefault();

    // Clear all auth data
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');

    // Redirect to login
    navigate('/login', { replace: true });
  };

  const menuItems = [
    { path: '/user/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/user/analysis', label: 'Analysis', icon: '📈' },
    { path: '/user/comparison', label: 'Comparison', icon: '⚖️' },
    { path: '/user/forecasting', label: 'Forecasting', icon: '🔮' },
    { path: '/user/help', label: 'Help', icon: '❓' },
  ];

  // Don't render if not authenticated
  if (!localStorage.getItem('access_token')) {
    return null;
  }

  return (
    <div className="user-layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2 className="sidebar-logo">FinSight</h2>
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="toggle-btn">
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>
        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn">
            <span className="nav-icon">🚪</span>
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>
      <main className={`main-content ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
        <header className="main-header">
          <h1>Dashboard</h1>
          <div className="user-info">
            <span>Hello, {user?.username || 'user'}</span>
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

