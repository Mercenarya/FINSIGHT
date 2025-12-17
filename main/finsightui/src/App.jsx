import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthLayout from './components/layout/AuthLayout';
import UserLayout from './components/layout/UserLayout';
import AdminLayout from './components/layout/AdminLayout';
import ExpertLayout from './components/layout/ExpertLayout';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ResetPassword from './pages/auth/ResetPassword';
import VerifyEmail from './pages/auth/VerifyEmail';
import UserDashboard from './pages/user/Dashboard';
import Analysis from './pages/user/Analysis';
import Comparison from './pages/user/Comparison';
import Forecasting from './pages/user/Forecasting';
import Help from './pages/user/Help';
import AdminDashboard from './pages/admin/Dashboard';
import UserManagement from './pages/admin/UserManagement';
import DataManagement from './pages/admin/DataManagement';
import AIModelAdmin from './pages/admin/AIModel';
import Logs from './pages/admin/Logs';
import SystemHealth from './pages/admin/SystemHealth';
import ExpertDashboard from './pages/expert/Dashboard';
import AIModelExpert from './pages/expert/AIModel';
import Validation from './pages/expert/Validation';
import Report from './pages/expert/Report';
import KnowledgeBase from './pages/expert/KnowledgeBase';
import Settings from './pages/expert/Settings';
import './App.css';
import LandingPage from './pages/auth/LandingPage';

function App() {
  console.log('[v0] App component loaded');

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/landing" replace />} />
        <Route path="/landing" element={<LandingPage />} />

        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
        </Route>

        <Route path="/user" element={<UserLayout />}>
          <Route path="dashboard" element={<UserDashboard />} />
          <Route path="analysis" element={<Analysis />} />
          <Route path="comparison" element={<Comparison />} />
          <Route path="forecasting" element={<Forecasting />} />
          <Route path="help" element={<Help />} />
        </Route>

        <Route path="/admin" element={<AdminLayout />}>
          <Route path="dashboard" element={<AdminDashboard />} />
          <Route path="users" element={<UserManagement />} />
          <Route path="data" element={<DataManagement />} />
          <Route path="ai-model" element={<AIModelAdmin />} />
          <Route path="logs" element={<Logs />} />
          <Route path="system-health" element={<SystemHealth />} />
        </Route>

        <Route path="/expert" element={<ExpertLayout />}>
          <Route path="dashboard" element={<ExpertDashboard />} />
          <Route path="ai-model" element={<AIModelExpert />} />
          <Route path="validation" element={<Validation />} />
          <Route path="report" element={<Report />} />
          <Route path="knowledge-base" element={<KnowledgeBase />} />
          <Route path="settings" element={<Settings />} />
        </Route>

        <Route path="*" element={<div className="not-found">404 - Page Not Found</div>} />
      </Routes>
    </Router>
  );
}

export default App;
