import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import axios from 'axios';

const ProfilePage = () => {
  const [fullName, setFullName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [address, setAddress] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Токен не найден');
        return;
      }

      try {
        const response = await axios.get('http://127.0.0.1:8000/api/profile/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setFullName(response.data.full_name || '');
        setBirthDate(response.data.birth_date || '');
        setAddress(response.data.address || '');
        setPhoneNumber(response.data.phone_number || '');
      } catch (error) {
        if (error.response && error.response.status === 401) {
          setError('Токен недействителен или отсутствует');
        } else {
          setError('Не удалось загрузить данные профиля');
        }
      }
    };

    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');

    if (!token) {
      setError('Токен не найден');
      return;
    }

    try {
      await axios.put('http://127.0.0.1:8000/api/profile/', {
        full_name: fullName,
        birth_date: birthDate,
        address: address,
        phone_number: phoneNumber,
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setMessage('Профиль успешно сохранен');
      setError(null);
    } catch (error) {
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
        if (error.response.status === 400) {
          setError('Некорректные данные: ' + JSON.stringify(error.response.data));
        } else if (error.response.status === 401) {
          setError('Токен недействителен или отсутствует');
        } else {
          setError('Не удалось сохранить данные профиля');
        }
      } else {
        console.error('Error message:', error.message);
        setError('Не удалось сохранить данные профиля');
      }
      setMessage(null);
    }
  };

  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <h2>Профиль пользователя</h2>
          {message && <Alert color="success">{message}</Alert>}
          {error && <Alert color="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <FormGroup>
              <Label for="fullName">Ф.И.О.</Label>
              <Input
                type="text"
                id="fullName"
                placeholder="Введите полное имя"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </FormGroup>
            <FormGroup>
              <Label for="birthDate">Дата рождения</Label>
              <Input
                type="date"
                id="birthDate"
                placeholder="Введите дату рождения"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
                required
              />
            </FormGroup>
            <FormGroup>
              <Label for="address">Адрес жительства</Label>
              <Input
                type="text"
                id="address"
                placeholder="Введите адрес"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                required
              />
            </FormGroup>
            <FormGroup>
              <Label for="phoneNumber">Номер телефона</Label>
              <Input
                type="text"
                id="phoneNumber"
                placeholder="Введите номер телефона"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                required
              />
            </FormGroup>
            <Button color="primary" type="submit">Сохранить</Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default ProfilePage;
