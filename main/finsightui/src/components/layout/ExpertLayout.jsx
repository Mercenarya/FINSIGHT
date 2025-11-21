import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Brain, CheckCircle, FileText, BookOpen, Settings } from 'lucide-react';
import './ExpertLayout.css';
import finsightLogo from '../../assets/finsight_logo.svg';

function ExpertLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const menuItems = [
    { path: '/expert/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/expert/ai-model', label: 'AI Models', icon: Brain },
    { path: '/expert/validation', label: 'Validation', icon: CheckCircle },
    { path: '/expert/report', label: 'Report Adjustment', icon: FileText },
    { path: '/expert/knowledge-base', label: 'Knowledge Base', icon: BookOpen },
    { path: '/expert/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="expert-layout">
      <aside className={`expert-sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="expert-sidebar-header">
          <div className="expert-logo">
            <div className="expert-logo-icon"><img src={finsightLogo} alt="FinSight logo" /></div>
            {sidebarOpen && <span className="expert-logo-text">FinSight</span>}
          </div>
        </div>
        <nav className="expert-sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`expert-nav-item ${location.pathname === item.path ? 'active' : ''}`}
              >
                <Icon size={20} className="expert-nav-icon" />
                {sidebarOpen && <span className="expert-nav-label">{item.label}</span>}
              </Link>
            );
          })}
        </nav>
      </aside>
      <main className={`expert-main-content ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
        <Outlet />
      </main>
    </div>
  );
}

export default ExpertLayout;
