import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Database, Bot, FileText, Activity, Settings, Search, User } from 'lucide-react';
import './AdminLayout.css';

function AdminLayout() {
  const location = useLocation();

  const menuItems = [
    { path: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/admin/users', label: 'User', icon: Users },
    { path: '/admin/data', label: 'Data', icon: Database },
    { path: '/admin/ai-model', label: 'AI Models', icon: Bot },
    { path: '/admin/logs', label: 'Logs', icon: FileText },
    { path: '/admin/reports', label: 'Reports', icon: FileText },
    { path: '/admin/system-health', label: 'System Health', icon: Activity },
    { path: '/admin/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-sidebar-header">
          <div className="admin-logo">
            <div className="logo-icon"></div>
            <span className="logo-text">FinSight</span>
          </div>
        </div>
        <nav className="admin-sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`admin-nav-item ${location.pathname === item.path ? 'active' : ''}`}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>
      <main className="admin-main">
        <header className="admin-header">
          <h1 className="admin-page-title">
            {menuItems.find(item => item.path === location.pathname)?.label || 'Dashboard'}
          </h1>
          <div className="admin-header-actions">
            <div className="admin-search-box">
              <Search size={16} />
              <input type="text" placeholder="Search" />
            </div>
            <div className="admin-user-avatar">
              <User size={20} />
            </div>
          </div>
        </header>
        <div className="admin-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

export default AdminLayout;
