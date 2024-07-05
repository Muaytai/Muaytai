import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, CardBody, Alert } from 'reactstrap';
import BookingForm from '../components/BookingForm';
import { Link } from 'react-router-dom';
import axios from 'axios';

const BookingPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hotels, setHotels] = useState([]);
  const [error, setError] = useState(null);

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
        setError('Ошибка при получении списка отелей');
        console.error('Ошибка при получении списка отелей:', error);
      }
    };

    // Вызываем fetchHotels только при изменении isAuthenticated
    fetchHotels();
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <Container className="my-5">
        <Row className="justify-content-center">
          <Col md={6}>
            <Card className="bg-primary text-white">
              <CardBody>
                <h2 className="text-center mb-4">Необходимо авторизоваться</h2>
                {error && <Alert color="danger">{error}</Alert>}
                <Link to="/login" className="btn btn-warning btn-block">
                  Войти
                </Link>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </Container>
    );
  }

  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <Card className="bg-success text-white">
            <CardBody>
              <h2 className="text-center mb-4">Бронирование отеля</h2>
              <BookingForm hotels={hotels} />
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default BookingPage;