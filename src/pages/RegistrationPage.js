import React, { useState } from 'react';
import { Container, Alert, Modal, ModalHeader, ModalBody, Button } from 'reactstrap';
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
    }
  };

  const handleCloseModal = () => {
    setShowSuccessModal(false);
    navigate('/');
  };

  return (
    <Container>
      <h2>Регистрация</h2>
      {error && <Alert color="danger">{error}</Alert>}
      <RegistrationForm onRegistrationSuccess={handleRegistrationSuccess} />
      <Modal isOpen={showSuccessModal}>
        <ModalHeader>Регистрация успешна!</ModalHeader>
        <ModalBody>
          Вы успешно зарегистрировались. Сейчас вы будете перенаправлены на главную страницу.
          <Button color="primary" onClick={handleCloseModal}>Закрыть</Button>
        </ModalBody>
      </Modal>
    </Container>
  );
};

export default RegistrationPage;