import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Row, Col } from 'reactstrap';
import HotelCard from './HotelCard';

// Убрали ненужный импорт Link

const HotelList = () => {
  const [hotels, setHotels] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/hotels/');
        setHotels(response.data.results);
        setIsLoading(false);
      } catch (err) {
        setError(err.message);
        setIsLoading(false);
      }
    };

    fetchHotels();
  }, []);

  return (
    <Row>
      {isLoading ? (
        <p>Загрузка...</p>
      ) : error ? (
        <p>Ошибка: {error}</p>
      ) : (
        hotels.map((hotel) => (
          <Col md={4} key={hotel.id}>
            {/* Убрали Link отсюда */}
            <HotelCard hotel={hotel} />
          </Col>
        ))
      )}
    </Row>
  );
};

export default HotelList;