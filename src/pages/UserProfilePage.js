// UserProfileForm.js
import React, { useState } from 'react';
import { Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import axios from 'axios';
import { REGISTRATION_API } from './api/api_route';

const UserProfileForm = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Хеширование пароля перед отправкой
      const hashedPassword = await hashPassword(password);

      const response = await axios.post(REGISTRATION_API, {
        name,
        password: hashedPassword,
      });

      console.log(response.data);
      // Очистить поля формы после успешного сохранения
      setName('');
      setPassword('');
      setError(null);
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
      <div className="d-flex justify-content-end">
        <Button color="primary" type="submit" className="mr-2">
          Сохранить
        </Button>
        <Button color="secondary" type="button">
          Отмена
        </Button>
      </div>
    </Form>
  );
};

export default UserProfileForm;