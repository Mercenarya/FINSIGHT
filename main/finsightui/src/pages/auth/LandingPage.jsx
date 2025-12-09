import React from 'react';
import { useNavigate } from 'react-router-dom';
import "./LandingPage.css";

function LandingPage() {
    const navigate = useNavigate();

    const handleTryDemo = () => {
        navigate('/login');
    };

    const handleLearnMore = () => {
        const featuresSection = document.getElementById('features');
        if (featuresSection) {
            featuresSection.scrollIntoView({ behavior: 'smooth' });
        }
    };

    return (
        <div className="landing-page">
            {/* Header/Navbar */}
            <header className="landing-header">
                <div className="landing-logo">FinSight</div>
                <nav className="landing-nav">
                    <a href="#features" className="nav-link">Features</a>
                    <a href="#contact" className="nav-link">Contact</a>
                </nav>
            </header>

            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <h1 className="hero-title">
                        Understand &<br />
                        Forecast Financial<br />
                        Performance with<br />
                        <span className="highlight">FinSight AI</span>
                    </h1>
                    <p className="hero-subtitle">
                        Upload your reports. Analyze instantly. Predict smarter.
                    </p>
                    <div className="hero-buttons">
                        <button className="btn-primary" onClick={handleTryDemo}>
                            Try Demo
                        </button>
                        <button className="btn-secondary" onClick={handleLearnMore}>
                            Learn More
                        </button>
                    </div>
                </div>

                <div className="hero-dashboard">
                    <div className="dashboard-mockup">
                        <div className="dashboard-cards">
                            <div className="stat-card">
                                <span className="stat-label">Revenue</span>
                                <span className="stat-value">$2.4M</span>
                                <span className="stat-change positive">↑ 23.5%</span>
                            </div>
                            <div className="stat-card">
                                <span className="stat-label">Profit</span>
                                <span className="stat-value">$840K</span>
                                <span className="stat-change positive">↑ 18.2%</span>
                            </div>
                        </div>
                        <div className="dashboard-chart">
                            <svg viewBox="0 0 300 100" className="line-chart">
                                <defs>
                                    <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                        <stop offset="0%" stopColor="#00D4AA" stopOpacity="0.3" />
                                        <stop offset="100%" stopColor="#00D4AA" stopOpacity="0" />
                                    </linearGradient>
                                </defs>
                                <path
                                    d="M0,80 L30,75 L60,70 L90,65 L120,60 L150,55 L180,45 L210,40 L240,30 L270,25 L300,20 L300,100 L0,100 Z"
                                    fill="url(#chartGradient)"
                                />
                                <path
                                    d="M0,80 L30,75 L60,70 L90,65 L120,60 L150,55 L180,45 L210,40 L240,30 L270,25 L300,20"
                                    fill="none"
                                    stroke="#00D4AA"
                                    strokeWidth="2"
                                />
                                <circle cx="0" cy="80" r="3" fill="#00D4AA" />
                                <circle cx="60" cy="70" r="3" fill="#00D4AA" />
                                <circle cx="120" cy="60" r="3" fill="#00D4AA" />
                                <circle cx="180" cy="45" r="3" fill="#00D4AA" />
                                <circle cx="240" cy="30" r="3" fill="#00D4AA" />
                                <circle cx="300" cy="20" r="3" fill="#00D4AA" />
                            </svg>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="features-section">
                <h2 className="section-title">Why Choose FinSight?</h2>
                <div className="features-grid">
                    {/* Feature 1: AI Financial Analysis */}
                    <div className="feature-card">
                        <div className="feature-icon">
                            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="6" y="20" width="8" height="22" rx="2" fill="#FF6B6B" />
                                <rect x="20" y="12" width="8" height="30" rx="2" fill="#4ECDC4" />
                                <rect x="34" y="6" width="8" height="36" rx="2" fill="#45B7D1" />
                            </svg>
                        </div>
                        <h3 className="feature-title">AI Financial Analysis</h3>
                        <p className="feature-description">
                            Automatically calculates key ratios and performance metrics.
                        </p>
                    </div>

                    {/* Feature 2: Forecasting Models */}
                    <div className="feature-card">
                        <div className="feature-icon">
                            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="24" cy="28" r="14" fill="url(#crystalGradient)" />
                                <ellipse cx="24" cy="42" rx="10" ry="3" fill="rgba(138, 43, 226, 0.3)" />
                                <circle cx="24" cy="28" r="10" fill="rgba(255, 255, 255, 0.2)" />
                                <path d="M20 10L24 4L28 10" stroke="#FFD700" strokeWidth="2" fill="none" />
                                <circle cx="24" cy="4" r="2" fill="#FFD700" />
                                <circle cx="16" cy="14" r="1.5" fill="#FFD700" />
                                <circle cx="32" cy="14" r="1.5" fill="#FFD700" />
                                <defs>
                                    <radialGradient id="crystalGradient" cx="50%" cy="30%" r="70%">
                                        <stop offset="0%" stopColor="#E8D5F2" />
                                        <stop offset="100%" stopColor="#8A2BE2" />
                                    </radialGradient>
                                </defs>
                            </svg>
                        </div>
                        <h3 className="feature-title">Forecasting Models</h3>
                        <p className="feature-description">
                            Predicts revenue, profit, and cash flow using machine learning.
                        </p>
                    </div>

                    {/* Feature 3: Cross-Company Comparison */}
                    <div className="feature-card">
                        <div className="feature-icon">
                            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="4" y="36" width="40" height="2" fill="#3498db" opacity="0.3" />
                                <rect x="4" y="28" width="40" height="2" fill="#3498db" opacity="0.2" />
                                <rect x="4" y="20" width="40" height="2" fill="#3498db" opacity="0.1" />
                                <path d="M6 34L14 28L22 32L30 22L38 18L44 14" stroke="#00D4AA" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                                <circle cx="14" cy="28" r="3" fill="#00D4AA" />
                                <circle cx="30" cy="22" r="3" fill="#00D4AA" />
                                <circle cx="44" cy="14" r="3" fill="#00D4AA" />
                            </svg>
                        </div>
                        <h3 className="feature-title">Cross-Company Comparison</h3>
                        <p className="feature-description">
                            Benchmark different companies or industries.
                        </p>
                    </div>

                    {/* Feature 4: Visual Dashboard */}
                    <div className="feature-card">
                        <div className="feature-icon">
                            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="4" y="36" width="40" height="2" fill="#e74c3c" opacity="0.3" />
                                <rect x="4" y="28" width="40" height="2" fill="#e74c3c" opacity="0.2" />
                                <rect x="4" y="20" width="40" height="2" fill="#e74c3c" opacity="0.1" />
                                <path d="M6 14L14 22L22 18L30 28L38 24L44 34" stroke="#FF6B6B" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                                <circle cx="14" cy="22" r="3" fill="#FF6B6B" />
                                <circle cx="30" cy="28" r="3" fill="#FF6B6B" />
                                <circle cx="44" cy="34" r="3" fill="#FF6B6B" />
                            </svg>
                        </div>
                        <h3 className="feature-title">Visual Dashboard</h3>
                        <p className="feature-description">
                            Generate interactive charts, KPIs, and exportable reports.
                        </p>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section id="demo" className="how-it-works-section">
                <h2 className="section-title">How It Works</h2>
                <div className="steps-container">
                    {/* Step 1 */}
                    <div className="step-item">
                        <div className="step-number">
                            <span>01</span>
                        </div>
                        <h3 className="step-title">Upload Financial Data</h3>
                        <p className="step-description">
                            Import your Excel/CSV files with financial statements.
                        </p>
                    </div>

                    {/* Step 2 */}
                    <div className="step-item">
                        <div className="step-number">
                            <span>02</span>
                        </div>
                        <h3 className="step-title">AI Analysis</h3>
                        <p className="step-description">
                            FinSight AI analyzes and visualizes the results instantly.
                        </p>
                    </div>

                    {/* Step 3 */}
                    <div className="step-item">
                        <div className="step-number">
                            <span>03</span>
                        </div>
                        <h3 className="step-title">Get Insights</h3>
                        <p className="step-description">
                            Receive forecasts and downloadable reports.
                        </p>
                    </div>
                </div>
            </section>

            {/* Target Users Section */}
            <section className="target-users-section">
                <h2 className="section-title">Target Users</h2>
                <div className="users-container">
                    {/* Businesses (SMEs) */}
                    <div className="user-card">
                        <div className="user-icon">
                            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="12" y="20" width="40" height="36" rx="2" fill="#5B9BD5" />
                                <rect x="16" y="24" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="28" y="24" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="40" y="24" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="16" y="34" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="28" y="34" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="40" y="34" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="16" y="44" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="28" y="44" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="40" y="44" width="8" height="6" rx="1" fill="#A5C8ED" />
                                <rect x="24" y="8" width="16" height="12" rx="2" fill="#7BAFD4" />
                                <rect x="28" y="12" width="3" height="4" rx="0.5" fill="#A5C8ED" />
                                <rect x="33" y="12" width="3" height="4" rx="0.5" fill="#A5C8ED" />
                            </svg>
                        </div>
                        <h3 className="user-title">Businesses (SMEs)</h3>
                        <p className="user-description">
                            Simplify decision-making and financial planning.
                        </p>
                    </div>

                    {/* Investors */}
                    <div className="user-card">
                        <div className="user-icon">
                            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="14" y="24" width="36" height="28" rx="3" fill="#8B6F47" />
                                <rect x="14" y="24" width="36" height="8" rx="2" fill="#A0825C" />
                                <rect x="26" y="28" width="12" height="6" rx="1" fill="#D4B896" />
                                <rect x="18" y="36" width="28" height="2" fill="#6B5839" />
                                <rect x="18" y="42" width="28" height="2" fill="#6B5839" />
                                <rect x="18" y="48" width="28" height="2" fill="#6B5839" />
                            </svg>
                        </div>
                        <h3 className="user-title">Investors</h3>
                        <p className="user-description">
                            Identify growth opportunities using predictive analytics.
                        </p>
                    </div>

                    {/* Students & Lecturers */}
                    <div className="user-card">
                        <div className="user-icon">
                            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                                {/* Graduation Cap - clearer design */}
                                <polygon points="32,8 4,24 32,40 60,24" fill="#1a1a2e" />
                                <polygon points="32,40 4,24 4,28 32,44 60,28 60,24" fill="#16213e" />
                                <rect x="30" y="24" width="4" height="4" fill="#0f3460" />
                                {/* Tassel pole */}
                                <rect x="52" y="22" width="3" height="22" fill="#F39C12" />
                                {/* Tassel */}
                                <circle cx="53.5" cy="44" r="3" fill="#F39C12" />
                                <path d="M50 47 L53.5 44 L57 47 L53.5 54 Z" fill="#F39C12" />
                                {/* Cap button */}
                                <circle cx="32" cy="26" r="3" fill="#F39C12" />
                            </svg>
                        </div>
                        <h3 className="user-title">Students & Lecturers</h3>
                        <p className="user-description">
                            Learn real-world financial analysis with AI tools.
                        </p>
                    </div>
                </div>
            </section>

            {/* Technology Stack Section */}
            <section className="tech-stack-section">
                <h2 className="section-title">Technology Stack</h2>
                <p className="tech-subtitle">Powered by Modern Technologies</p>
                <div className="tech-container">
                    <div className="tech-badge">ReactJS</div>
                    <div className="tech-badge">Python</div>
                    <div className="tech-badge">TensorFlow</div>
                    <div className="tech-badge">MongoDB</div>
                    <div className="tech-badge">Plotly</div>
                    <div className="tech-badge">Figma</div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="testimonials-section">
                <h2 className="section-title">Testimonials</h2>
                <div className="testimonials-container">
                    <div className="testimonial-card">
                        <p className="testimonial-quote">
                            "FinSight makes financial analysis simple and powerful."
                        </p>
                        <p className="testimonial-author">— Sarah Chen, CFO</p>
                    </div>

                    <div className="testimonial-card">
                        <p className="testimonial-quote">
                            "AI forecasting helps us plan with confidence."
                        </p>
                        <p className="testimonial-author">— Michael Nguyen, Investor</p>
                    </div>

                    <div className="testimonial-card">
                        <p className="testimonial-quote">
                            "Perfect for both investors and students."
                        </p>
                        <p className="testimonial-author">— Dr. Tran, Finance Professor</p>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <h2 className="cta-title">Start Smarter Financial Decisions Today</h2>
                <p className="cta-subtitle">FinSight brings AI clarity to complex financial data.</p>
                <button className="cta-button" onClick={handleTryDemo}>
                    Get Started for Free
                </button>
            </section>
        </div>
    );
}

export default LandingPage;