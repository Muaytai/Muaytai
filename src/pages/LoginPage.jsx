import React, { useState } from 'react';
import { Form, FormGroup, Label, Input, Button, Alert, TabContent, TabPane, Nav, NavItem, NavLink, Container, Row, Col, Card, CardBody } from 'reactstrap';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const LoginPage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('1'); // Начальная вкладка

  const toggle = (tab) => {
    if (activeTab !== tab) setActiveTab(tab);
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/token/', {
        username,
        password,
      });

      // Сохраняем токен в localStorage
      localStorage.setItem('token', response.data.access);

      setUsername('');
      setPassword('');
      setError(null);
      navigate('/'); // Перенаправление на главную страницу
    } catch (error) {
      setError(error.response.data.detail || 'Неверное имя пользователя или пароль');
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/register/', {
        username,
        email,
        password,
      });

      console.log('Пользователь успешно зарегистрирован:', response.data);
      setActiveTab('1'); // Переключиться на вкладку "Вход" после регистрации
      setUsername('');
      setEmail('');
      setPassword('');
      setError(null);
    } catch (error) {
      setError(error.response.data.error || 'Произошла ошибка при регистрации');
    }
  };

  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <Card className="bg-primary text-white shadow-lg" style={{ borderRadius: '20px' }}>
            <CardBody>
              <Nav tabs>
                <NavItem>
                  <NavLink
                    className={activeTab === '1' ? 'active' : ''}
                    onClick={() => {
                      toggle('1');
                    }}
                    style={{
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      backgroundColor: activeTab === '1' ? '#ffc107' : '#007bff',
                      color: 'white',
                      padding: '10px 20px',
                      borderRadius: '10px 10px 0 0'
                    }}
                  >
                    Войти
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink
                    className={activeTab === '2' ? 'active' : ''}
                    onClick={() => {
                      toggle('2');
                    }}
                    style={{
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      backgroundColor: activeTab === '2' ? '#28a745' : '#007bff',
                      color: 'white',
                      padding: '10px 20px',
                      borderRadius: '10px 10px 0 0'
                    }}
                  >
                    Регистрация
                  </NavLink>
                </NavItem>
              </Nav>
              <TabContent activeTab={activeTab}>
                <TabPane tabId="1">
                  <Form onSubmit={handleLoginSubmit}>
                    <FormGroup>
                      <Label for="username" className="text-white">
                        Имя пользователя
                      </Label>
                      <Input
                        type="text"
                        id="username"
                        placeholder="Введите имя пользователя"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={{ borderRadius: '10px', padding: '10px' }}
                      />
                    </FormGroup>
                    <FormGroup>
                      <Label for="password" className="text-white">
                        Пароль
                      </Label>
                      <Input
                        type="password"
                        id="password"
                        placeholder="Введите пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ borderRadius: '10px', padding: '10px' }}
                      />
                    </FormGroup>
                    {error && <Alert color="danger">{error}</Alert>}
                    <Button
                      color="warning"
                      block
                      style={{
                        fontSize: '1.5rem',
                        fontWeight: 'bold',
                        padding: '10px 20px',
                        borderRadius: '10px'
                      }}
                    >
                      Войти
                    </Button>
                  </Form>
                </TabPane>
                <TabPane tabId="2">
                  <Form onSubmit={handleRegisterSubmit}>
                    <FormGroup>
                      <Label for="username" className="text-white">
                        Имя пользователя
                      </Label>
                      <Input
                        type="text"
                        id="username"
                        placeholder="Введите имя пользователя"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={{ borderRadius: '10px', padding: '10px' }}
                      />
                    </FormGroup>
                    <FormGroup>
                      <Label for="email" className="text-white">
                        Email
                      </Label>
                      <Input
                        type="email"
                        id="email"
                        placeholder="Введите email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{ borderRadius: '10px', padding: '10px' }}
                      />
                    </FormGroup>
                    <FormGroup>
                      <Label for="password" className="text-white">
                        Пароль
                      </Label>
                      <Input
                        type="password"
                        id="password"
                        placeholder="Введите пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ borderRadius: '10px', padding: '10px' }}
                      />
                    </FormGroup>
                    {error && <Alert color="danger">{error}</Alert>}
                    <Button
                      color="success"
                      block
                      style={{
                        fontSize: '1.5rem',
                        fontWeight: 'bold',
                        padding: '10px 20px',
                        borderRadius: '10px'
                      }}
                    >
                      Зарегистрироваться
                    </Button>
                  </Form>
                </TabPane>
              </TabContent>
              <Row className="mt-4">
                <Col>
                  <Link to="/" className="btn btn-danger btn-block">
                    Вернуться на главную
                  </Link>
                </Col>
              </Row>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginPage;