import React from 'react';
import './RadioGroup.css';

const RadioGroup = ({ label, name, options, value, onChange, error, required = false }) => {
  return (
    <div className="radio-group">
      {label && (
        <div className="radio-label">
          {label} {required && <span className="required">*</span>}
        </div>
      )}
      <div className="radio-options">
        {options.map((option) => (
          <label key={option.value} className="radio-option">
            <input
              type="radio"
              name={name}
              value={option.value}
              checked={value === option.value}
              onChange={onChange}
              className="radio-input"
            />
            <span className="radio-custom"></span>
            <span className="radio-text">{option.label}</span>
          </label>
        ))}
      </div>
      {error && <span className="error-message">{error}</span>}
    </div>
  );
};

export default RadioGroup;