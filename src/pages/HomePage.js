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
  const [filteredHotels, setFilteredHotels] = useState(hotels); // Добавлено состояние для фильтрованных отелей

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/hotels/');
        setHotels(response.data.results); // Используем results из ответа
        setFilteredHotels(response.data.results); // Обновляем filteredHotels
        setIsLoading(false);
      } catch (err) {
        setError(err.message);
        setIsLoading(false);
      }
    };

    fetchHotels();
  }, []);

  // Обработка фильтрации
  const handleFilter = (filterParams) => {
    const filtered = hotels.filter((hotel) => {
      return (
        hotel.name.toLowerCase().includes(filterParams.name.toLowerCase()) &&
        hotel.rating >= filterParams.minRating &&
        hotel.price_per_night <= filterParams.maxPrice
      );
    });
    setFilteredHotels(filtered);
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
        <HotelList hotels={filteredHotels} /> // Используем filteredHotels
      )}
    </Container>
  );
};

export default HomePage;