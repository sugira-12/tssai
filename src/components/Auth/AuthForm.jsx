import React from 'react';
import Input from '../../UI/Input';
import RadioGroup from '../../UI/RadioGroup';
import Button from '../../UI/Button';
import './AuthForm.css';

const AuthForm = ({ 
  isLogin, 
  formData, 
  errors, 
  loading, 
  onInputChange, 
  onSubmit,
  onToggleForm 
}) => {
  const userTypeOptions = [
    { label: '👨‍🎓 I am a Student', value: 'student' },
    { label: '👨‍🏫 I am a Teacher', value: 'teacher' },
  ];

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <img src="https://cdn-icons-png.flaticon.com/512/2282/2282188.png" alt="TSS.AI Logo" className="logo" />
          <h1 className="auth-title">{isLogin ? 'Welcome Back to TSS.AI' : 'Join TSS.AI'}</h1>
          <p className="auth-subtitle">
            {isLogin 
              ? 'Enter your credentials to access your account' 
              : 'Create your account to get started'}
          </p>
        </div>

        <form onSubmit={onSubmit} className="auth-form">
          {!isLogin && (
            <Input
              label="Username"
              type="text"
              name="username"
              value={formData.username}
              onChange={onInputChange}
              placeholder="Enter your username"
              error={errors.username}
              required
            />
          )}

          <Input
            label="Email Address"
            type="email"
            name="email"
            value={formData.email}
            onChange={onInputChange}
            placeholder="Enter your email"
            error={errors.email}
            required
          />

          <Input
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={onInputChange}
            placeholder="Enter your password"
            error={errors.password}
            required
          />

          {!isLogin && (
            <RadioGroup
              label="Select your role"
              name="userType"
              options={userTypeOptions}
              value={formData.userType}
              onChange={onInputChange}
              error={errors.userType}
              required
            />
          )}

          {isLogin && (
            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" name="remember" />
                <span>Remember me</span>
              </label>
              <a href="#forgot" className="forgot-link">Forgot password?</a>
            </div>
          )}

          <Button 
            type="submit" 
            variant="primary" 
            fullWidth 
            disabled={loading}
          >
            {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Create Account')}
          </Button>

          <div className="auth-divider">
            <span>or continue with</span>
          </div>

          <Button type="button" variant="outline" fullWidth>
            <img src="https://cdn-icons-png.flaticon.com/512/2991/2991148.png" alt="Google" className="social-icon" />
            Continue with Google
          </Button>
        </form>

        <div className="auth-footer">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button type="button" onClick={onToggleForm} className="toggle-link">
              {isLogin ? 'Sign up' : 'Sign in'}
            </button>
          </p>
          <p className="terms-text">
            By continuing, you agree to our 
            <a href="#terms"> Terms of Service</a> and 
            <a href="#privacy"> Privacy Policy</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;