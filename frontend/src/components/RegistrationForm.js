// components/RegistrationForm.js
import React, { useState } from 'react';
import { Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import axios from 'axios';

const RegistrationForm = ({ onRegistrationSuccess }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Хеширование пароля перед отправкой
      const hashedPassword = await hashPassword(password);

      const response = await axios.post('/api/register', {
        name,
        email,
        password: hashedPassword,
      });

      console.log(response.data);
      // Очистить поля формы после успешной регистрации
      setName('');
      setEmail('');
      setPassword('');
      setError(null);
      // Вызвать функцию обратного вызова для уведомления родительского компонента
      onRegistrationSuccess();
    } catch (error) {
      setError(error.response.data.error);
    }
  };

  const hashPassword = async (password) => {
    // Реализуйте логику хеширования пароля
    // Например, с использованием библиотеки bcrypt
    return password;
  };

  return (
    <Form onSubmit={handleSubmit}>
      <FormGroup>
        <Label for="name">Имя</Label>
        <Input
          type="text"
          id="name"
          placeholder="Введите ваше имя"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </FormGroup>
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
      {error && <Alert color="danger">{error}</Alert>}
      <Button color="primary" type="submit">
        Зарегистрироваться
      </Button>
    </Form>
  );
};

export default RegistrationForm;