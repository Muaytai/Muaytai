import React, { useState } from 'react';
import { Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import axios from 'axios';

const RegistrationForm = ({ onRegistrationSuccess }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('/api/register/', {
        username, // Используем 'username' вместо 'name'
        email,
        password, // Пароль хешируется на бэкенде
      });

      console.log('Пользователь успешно зарегистрирован:', response.data);
      onRegistrationSuccess();
      setUsername('');
      setEmail('');
      setPassword('');
      setError(null);
    } catch (error) {
      setError(error.response.data.error || 'Произошла ошибка при регистрации');
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <FormGroup>
        <Label for="username">Имя пользователя</Label>
        <Input
          type="text"
          id="username"
          placeholder="Введите имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </FormGroup>
      {/* ... (Поля ввода для email и пароля) */}
      {error && <Alert color="danger">{error}</Alert>}
      <Button color="primary" type="submit">
        Зарегистрироваться
      </Button>
    </Form>
  );
};

export default RegistrationForm;