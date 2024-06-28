import React, { useState } from 'react';
import { Container, Alert, Modal, ModalHeader, ModalBody } from 'reactstrap';
import RegistrationForm from '../components/RegistrationForm';
import { useNavigate } from 'react-router-dom';

const RegistrationPage = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const handleRegistrationSuccess = (errorMessage) => {
    if (errorMessage) {
      setError(errorMessage);
    } else {
      setShowSuccessModal(true);
      setTimeout(() => {
        setShowSuccessModal(false);
        navigate('/login');
      }, 3000);
    }
  };

  return (
    <Container>
      <h2>Регистрация</h2>
      {error && <Alert color="danger">{error}</Alert>}
      <RegistrationForm onRegistrationSuccess={handleRegistrationSuccess} />
      <Modal isOpen={showSuccessModal}>
        <ModalHeader>Регистрация успешна!</ModalHeader>
        <ModalBody>
          Вы успешно зарегистрировались. Сейчас вы будете перенаправлены на страницу входа.
        </ModalBody>
      </Modal>
    </Container>
  );
};

export default RegistrationPage;