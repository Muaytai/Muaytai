import React, { useState, useEffect } from 'react';
import { Container } from 'reactstrap';
import BookingForm from '../components/BookingForm';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BookingPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hotels, setHotels] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        // Проверяем, авторизован ли пользователь
        if (isAuthenticated) {
          const token = localStorage.getItem('token'); // Получаем токен из localStorage
          const response = await axios.get('http://127.0.0.1:8000/api/hotels/', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          setHotels(response.data.results);
        }
      } catch (error) {
        console.error('Ошибка при получении списка отелей:', error);
      }
    };

    // Вызываем fetchHotels только при изменении isAuthenticated
    fetchHotels();
  }, [isAuthenticated]);

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
      <BookingForm hotels={hotels} />
    </Container>
  );
};

export default BookingPage;