import React from 'react';
import './Button.css';

const Button = ({ children, type = 'button', variant = 'primary', onClick, disabled = false, fullWidth = false }) => {
  return (
    <button
      type={type}
      className={`btn btn-${variant} ${fullWidth ? 'btn-full' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;