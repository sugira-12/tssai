import React, { useState, useMemo } from 'react';
import './App.css';

function App() {
  const [isLogin, setIsLogin] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    userType: 'student',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(isLogin ? 'Login Successful' : 'Welcome to TSS.AI 🚀');
  };

  // Generate automation elements
  const automationElements = useMemo(() => {
    return Array.from({ length: 40 }).map((_, i) => {
      const size = Math.random() * 60 + 20;
      const duration = Math.random() * 15 + 10;
      const delay = Math.random() * 5;
      const opacity = Math.random() * 0.15 + 0.05;
      
      return (
        <div
          key={i}
          className="automation-element"
          style={{
            left: `${Math.random() * 100}%`,
            fontSize: `${Math.random() * 10 + 10}px`,
            animationDuration: `${duration}s`,
            animationDelay: `${delay}s`,
            opacity: opacity,
            filter: `blur(${Math.random() * 2}px)`,
          }}
        >
          {Math.random() > 0.5 ? 'TSS' : 'AI'}
        </div>
      );
    });
  }, []);

  return (
    <div className="app">
      {/* Automation Background */}
      <div className="automation-background">
        {automationElements}
        
        {/* Grid Lines */}
        <div className="grid-line horizontal"></div>
        <div className="grid-line vertical"></div>
        
        {/* Moving Dots */}
        <div className="moving-dots">
          {Array.from({ length: 15 }).map((_, i) => (
            <div 
              key={i}
              className="dot"
              style={{
                left: `${(i * 7) % 100}%`,
                animationDelay: `${i * 0.5}s`
              }}
            />
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="content-wrapper">
        <div className="container">
          <header className="header">
            <div className="logo">
              <span className="logo-text">TSS</span>
              <span className="logo-dot">.</span>
              <span className="logo-text">AI</span>
            </div>
            <p className="subtitle">
              {isLogin ? 'Welcome Back' : 'Intelligent Learning Platform'}
            </p>
          </header>

          <div className="form-card">
            <h2 className="form-title">
              {isLogin ? 'Sign In' : 'Create Account'}
            </h2>

            <form onSubmit={handleSubmit} className="form">
              {!isLogin && (
                <div className="input-group">
                  <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    className="form-input"
                    value={formData.username}
                    onChange={handleChange}
                    required
                  />
                </div>
              )}

              <div className="input-group">
                <input
                  type="email"
                  name="email"
                  placeholder="Email address"
                  className="form-input"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  className="form-input"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </div>

              {!isLogin && (
                <div className="role-selection">
                  <div className="role-title">Select your role:</div>
                  <div className="role-buttons">
                    <button
                      type="button"
                      className={`role-btn ${formData.userType === 'student' ? 'active' : ''}`}
                      onClick={() => setFormData({...formData, userType: 'student'})}
                    >
                      <span className="role-icon">👨‍🎓</span>
                      <span className="role-text">Student</span>
                    </button>
                    <button
                      type="button"
                      className={`role-btn ${formData.userType === 'teacher' ? 'active' : ''}`}
                      onClick={() => setFormData({...formData, userType: 'teacher'})}
                    >
                      <span className="role-icon">👨‍🏫</span>
                      <span className="role-text">Teacher</span>
                    </button>
                  </div>
                </div>
              )}

              <button type="submit" className="submit-btn">
                <span className="btn-text">
                  {isLogin ? 'Sign In' : 'Create Account'}
                </span>
                <span className="btn-arrow">→</span>
              </button>

              <div className="divider">
                <span>or</span>
              </div>

              <div className="switch-section">
                <span className="switch-text">
                  {isLogin ? "Don't have an account?" : "Already have an account?"}
                </span>
                <button 
                  type="button" 
                  className="switch-btn"
                  onClick={() => setIsLogin(!isLogin)}
                >
                  {isLogin ? 'Sign Up' : 'Sign In'}
                </button>
              </div>
            </form>

            <p className="terms">
              By continuing, you agree to our 
              <a href="#terms"> Terms</a> and 
              <a href="#privacy"> Privacy Policy</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;