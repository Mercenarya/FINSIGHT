import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Auth.css';

function ResetPassword() {
  const navigate = useNavigate();
  const [emailOrPhone, setEmailOrPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Add reset password logic
    console.log('Reset password for:', emailOrPhone);
    navigate('/verify-email');
  };

  return (
    <div className="auth-form-container">
      <h2 className="auth-title">Reset Password</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="form-group">
          <label htmlFor="emailOrPhone">Enter your email or phone number</label>
          <div className="input-wrapper">
            <input
              type="text"
              id="emailOrPhone"
              name="emailOrPhone"
              placeholder=""
              value={emailOrPhone}
              onChange={(e) => setEmailOrPhone(e.target.value)}
              required
            />
          </div>
        </div>

        <button type="submit" className="auth-button">Send Reset Code</button>

        <p className="auth-footer">
          Already have an account? <Link to="/login" className="auth-link">Sign In</Link>
        </p>
      </form>
    </div>
  );
}

export default ResetPassword;
