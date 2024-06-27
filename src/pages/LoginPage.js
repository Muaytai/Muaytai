import React, { useState } from 'react';
import { Container, Form, FormGroup, Label, Input, Button } from 'reactstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('/api/login', {
        email,
        password,
      });

      console.log(response.data);
      // Очистить поля формы после успешного входа
      setEmail('');
      setPassword('');
      // Перенаправить пользователя на страницу профиля
      navigate('/profile');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container>
      <h2>Вход</h2>
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label for="email">Email</Label>
          <Input
            type="email"
            id="email"
            placeholder="Введите ваш email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="password">Пароль</Label>
          <Input
            type="password"
            id="password"
            placeholder="Введите пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormGroup>
        <Button color="primary" type="submit">
          Войти
        </Button>
      </Form>
    </Container>
  );
};

export default LoginPage;