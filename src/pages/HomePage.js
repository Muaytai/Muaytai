import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container } from 'reactstrap';
import Header from '../components/Header';
import HotelList from '../components/HotelList';
import HotelFilter from '../components/HotelFilter';

const HomePage = () => {
  const [hotels, setHotels] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/hotels/');
        console.log('Полученные данные:', response.data); // Для отладки
        setHotels(response.data.results); // Используем results из ответа
        setIsLoading(false);
      } catch (err) {
        setError(err.message);
        setIsLoading(false);
      }
    };

    fetchHotels();
  }, []);

  // Обработка фильтрации (не используется, если фильтрация не нужна)
  const handleFilter = (filterParams) => {
    if (!Array.isArray(hotels)) {
      console.error('Ошибка: hotels не является массивом', hotels);
      return;
    }

    const filtered = hotels.filter((hotel) => {
      return (
        hotel.name.toLowerCase().includes(filterParams.name.toLowerCase()) &&
        hotel.rating >= filterParams.minRating &&
        hotel.price_per_night <= filterParams.maxPrice
      );
    });
    // setFilteredHotels(filtered); // Удалено, если фильтрация не нужна
  };

  return (
    <Container>
      <Header />
      {/* Отображаем HotelFilter, если не загружается и нет ошибок */}
      {!isLoading && !error && <HotelFilter onFilter={handleFilter} />}
      {isLoading ? (
        <p>Загрузка...</p>
      ) : error ? (
        <p>Ошибка: {error}</p>
      ) : (
        <HotelList hotels={hotels} />
      )}
    </Container>
  );
};

export default HomePage;