import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

function VerifyEmail() {
  const navigate = useNavigate();
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const inputRefs = useRef([]);

  const handleChange = (index, value) => {
    if (value.length <= 1 && /^\d*$/.test(value)) {
      const newCode = [...code];
      newCode[index] = value;
      setCode(newCode);

      // Auto-focus next input
      if (value && index < 5) {
        inputRefs.current[index + 1]?.focus();
      }
    }
  };

  const handleKeyDown = (index, e) => {
    // Handle backspace
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const verificationCode = code.join('');
    if (verificationCode.length === 6) {
      // TODO: Add verification logic
      console.log('Verification code:', verificationCode);
      navigate('/login');
    } else {
      alert('Please enter the complete 6-digit code');
    }
  };

  return (
    <div className="auth-form-container">
      <h2 className="auth-title">Reset Password</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="form-group">
          <label className="verify-label">Type your verification code</label>
          <div className="code-input-group">
            {code.map((digit, index) => (
              <input
                key={index}
                ref={(el) => (inputRefs.current[index] = el)}
                type="text"
                maxLength="1"
                className="code-input"
                value={digit}
                onChange={(e) => handleChange(index, e.target.value)}
                onKeyDown={(e) => handleKeyDown(index, e)}
                required
              />
            ))}
          </div>
        </div>

        <button type="submit" className="auth-button">Verify</button>

        <p className="auth-footer">
          <a href="#" className="auth-link">Edit your for code to resent</a>
        </p>
      </form>
    </div>
  );
}

export default VerifyEmail;
