import React from 'react';
import { Container } from 'reactstrap';
import RegistrationForm from '../components/RegistrationForm';
import { useNavigate } from 'react-router-dom';

const RegistrationPage = () => {
  const navigate = useNavigate();

  const handleRegistrationSuccess = () => {
    // Перенаправить пользователя на страницу входа после успешной регистрации
    navigate('/login');
  };

  return (
    <Container>
      <h2>Регистрация</h2>
      <RegistrationForm onRegistrationSuccess={handleRegistrationSuccess} />
    </Container>
  );
};

export default RegistrationPage;