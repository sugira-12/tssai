import React from 'react';
import AuthForm from './AuthForm';

const Signup = ({ 
  formData, 
  errors, 
  loading, 
  onInputChange, 
  onSubmit, 
  onToggleForm 
}) => {
  return (
    <AuthForm
      isLogin={false}
      formData={formData}
      errors={errors}
      loading={loading}
      onInputChange={onInputChange}
      onSubmit={onSubmit}
      onToggleForm={onToggleForm}
    />
  );
};

export default Signup;