// BookingPage.jsx
import React, { useEffect, useState } from 'react';
import { Container } from 'reactstrap';
import BookingForm from '../components/BookingForm';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

const BookingPage = () => {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  if (!isAuthenticated) {
    return (
      <div>
        <p>Необходимо авторизоваться.</p>
        <Link to="/login">Войти</Link>
      </div>
    );
  }

  return (
    <Container>
      <h2>Бронирование отеля</h2>
      <BookingForm />
    </Container>
  );
};

export default BookingPage;