// HotelDetailsPage.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Container } from 'reactstrap';
import HotelDetails from '../components/HotelDetails';

const HotelDetailsPage = () => {
  const { id } = useParams();
  const [hotel, setHotel] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotelDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/hotels/${id}`);
        setHotel(response.data);
        setIsLoading(false);
      } catch (err) {
        setError(err.message);
        setIsLoading(false);
      }
    };

    fetchHotelDetails();
  }, [id]);

  return (
    <Container>
      {isLoading ? (
        <p>Загрузка...</p>
      ) : error ? (
        <p>Ошибка: {error}</p>
      ) : (
        <HotelDetails hotel={hotel} />
      )}
    </Container>
  );
};

export default HotelDetailsPage;