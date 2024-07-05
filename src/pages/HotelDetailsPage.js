import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Container, Button } from 'reactstrap';
import HotelDetails from '../components/HotelDetails';

const HotelDetailsPage = () => {
  const { id } = useParams();
  const [hotel, setHotel] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHotelDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/hotels/${id}`);
        setHotel(response.data);
        setIsLoading(false);
      } catch (err) {
        if (err.response && err.response.status === 404) {
          setError('Отель не найден');
          setIsLoading(false);
          // Перенаправление на главную страницу
          navigate('/');
        } else {
          setError(err.message);
          setIsLoading(false);
        }
      }
    };

    fetchHotelDetails();
  }, [id, navigate]); // Добавьте navigate в зависимости useEffect

  return (
    <Container>
      {isLoading ? (
        <p>Загрузка...</p>
      ) : error ? (
        <p>Ошибка: {error}</p>
      ) : (
        <>
          <HotelDetails hotel={hotel} />
          <Button color="primary" onClick={() => navigate('/booking')}>Забронировать</Button>
        </>
      )}
    </Container>
  );
};

export default HotelDetailsPage;