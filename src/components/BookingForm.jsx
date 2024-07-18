import React, { useState, useEffect } from 'react';
import { Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import axios from 'axios';

const BookingForm = ({ hotels }) => {
  const [formData, setFormData] = useState({
    hotel: '',
    check_in: '',
    check_out: '',
    guests: 1,
  });
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null); // Добавляем состояние для сообщения об успехе

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

      const response = await axios.post('http://127.0.0.1:8000/api/bookings/', formData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Бронирование успешно создано:', response.data);
      setSuccessMessage('Бронирование успешно создано!'); // Устанавливаем сообщение об успехе
      // Очистите поля формы, покажите сообщение об успехе и т. д.
    } catch (error) {
      setError(error.response.data.detail || 'Ошибка при бронировании');
    }
  };

  // Скрываем сообщение об успехе через 2 секунды
  useEffect(() => {
    if (successMessage) {
      const timeout = setTimeout(() => {
        setSuccessMessage(null);
      }, 2000);

      return () => clearTimeout(timeout);
    }
  }, [successMessage]);

  return (
    <Form onSubmit={handleSubmit}>
      <FormGroup>
        <Label for="hotel">Отель</Label>
        <Input type="select" name="hotel" id="hotel" value={formData.hotel} onChange={handleChange}>
          <option value="">Выберите отель</option>
          {hotels.length > 0 && hotels.map((hotel) => (
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
      {successMessage && <Alert color="success">{successMessage}</Alert>} {/* Отображаем сообщение об успехе */}
      <Button color="primary" type="submit">
        Забронировать
      </Button>
    </Form>
  );
};

export default BookingForm;