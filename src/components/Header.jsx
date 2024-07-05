import React from 'react';
import { Container, Nav, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';
import UserMenu from './UserMenu';

const Header = () => {
  return (
    <Container fluid className="bg-primary text-white py-4">
      <div className="d-flex flex-column align-items-center">
        <h1 className="display-4 mb-3 animate__animated animate__fadeInDown" style={{
          color: '#db7093',
          fontWeight: 'bold'
        }}>
          Добро пожаловать в наш отель!
        </h1>
        <Nav className="mb-4">
          <NavItem>
            <Link to="/" className="btn btn-lg btn-danger text-white animate__animated animate__bounce animate__delay-1s animate__repeat-2" style={{ fontSize: 20 }}>
              Главная
            </Link>
          </NavItem>
          <NavItem>
            <Link to="/contacts" className="btn btn-lg btn-success text-white animate__animated animate__bounce animate__delay-2s animate__repeat-2" style={{ fontSize: 20 }}>
              Отзывы
            </Link>
          </NavItem>
          <NavItem>
            <Link to="/booking" className="btn btn-lg btn-warning text-white animate__animated animate__bounce animate__delay-3s animate__repeat-2" style={{ fontSize: 20 }}>
              Бронирование
            </Link>
          </NavItem>
          <NavItem>
            <Link to="/login" className="btn btn-lg btn-info text-white animate__animated animate__bounce animate__delay-4s animate__repeat-2" style={{ fontSize: 20 }}>
              Регистрация/Войти
            </Link>
          </NavItem>
          <NavItem>
            <Link to="/support" className="btn btn-lg btn-secondary text-white animate__animated animate__bounce animate__delay-5s animate__repeat-2" style={{ fontSize: 20 }}>
              Служба поддержки
            </Link>
          </NavItem>
        </Nav>
        <p className="lead animate__animated animate__fadeInUp" style={{
          color: '#ffd700', // Золотистый цвет
          textShadow: '0 0 10px #ffd700, 0 0 20px #ffd700, 0 0 30px #ffd700, 0 0 40px #ffd700'
        }}>
          Забронируйте номер прямо сейчас и насладитесь незабываемым отдыхом.
        </p>
      </div>
    </Container>
  );
};

export default Header;