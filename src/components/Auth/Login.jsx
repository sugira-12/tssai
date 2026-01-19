import React from 'react';
import AuthForm from './AuthForm';

const Login = ({ 
  formData, 
  errors, 
  loading, 
  onInputChange, 
  onSubmit, 
  onToggleForm 
}) => {
  return (
    <AuthForm
      isLogin={true}
      formData={formData}
      errors={errors}
      loading={loading}
      onInputChange={onInputChange}
      onSubmit={onSubmit}
      onToggleForm={onToggleForm}
    />
  );
};

export default Login;