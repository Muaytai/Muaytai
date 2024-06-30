import React, { useState, useEffect } from 'react';
import { Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import axios from 'axios';

const BookingForm = () => {
  const [hotels, setHotels] = useState([]);
  const [formData, setFormData] = useState({
    hotel: '',
    check_in: '',
    check_out: '',
    guests: 1,
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await axios.get('/api/hotels/');
        setHotels(response.data);
      } catch (error) {
        console.error('Ошибка при получении списка отелей:', error);
      }
    };

    fetchHotels();
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token'); // Получаем токен

      const response = await axios.post('/api/bookings/', formData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Бронирование успешно создано:', response.data);
      // Очистите поля формы, покажите сообщение об успехе и т. д.
    } catch (error) {
      setError(error.response.data.detail || 'Ошибка при бронировании');
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <FormGroup>
        <Label for="hotel">Отель</Label>
        <Input type="select" name="hotel" id="hotel" value={formData.hotel} onChange={handleChange}>
          <option value="">Выберите отель</option>
          {hotels.map((hotel) => (
            <option key={hotel.id} value={hotel.id}>
              {hotel.name}
            </option>
          ))}
        </Input>
      </FormGroup>
      <FormGroup>
        <Label for="check_in">Дата заезда</Label>
        <Input type="date" name="check_in" id="check_in" value={formData.check_in} onChange={handleChange} />
      </FormGroup>
      <FormGroup>
        <Label for="check_out">Дата выезда</Label>
        <Input type="date" name="check_out" id="check_out" value={formData.check_out} onChange={handleChange} />
      </FormGroup>
      <FormGroup>
        <Label for="guests">Количество гостей</Label>
        <Input type="number" name="guests" id="guests" value={formData.guests} onChange={handleChange} min="1" />
      </FormGroup>
      {error && <Alert color="danger">{error}</Alert>}
      <Button color="primary" type="submit">
        Забронировать
      </Button>
    </Form>
  );
};

export default BookingForm;