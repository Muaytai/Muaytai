import React from 'react';
import { Container, Nav, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';


const Header = () => {
  const [springProps] = useSpring(() => ({
    from: { opacity: 0, transform: 'translateY(-50px)' },
    to: { opacity: 1, transform: 'translateY(0)' },
    config: { duration: 1000 }
  }));

  return (
    <Container fluid className="bg-primary text-white py-4">
      <div className="d-flex flex-column align-items-center">
        <animated.div style={springProps}>
          <h1 className="display-4 mb-3" style={{
            color: '#db7093',
            fontWeight: 'bold'
          }}>
            Добро пожаловать в наш отель!
          </h1>
        </animated.div>
        <Nav className="mb-4">
          <NavItem>
            <NavLink tag={Link} to="/" className="btn btn-lg btn-danger text-white animate__animated animate__bounce animate__delay-1s animate__repeat-2" style={{ fontSize: 20 }}>
              Главная
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink tag={Link} to="/contacts" className="btn btn-lg btn-success text-white animate__animated animate__bounce animate__delay-2s animate__repeat-2" style={{ fontSize: 20 }}>
              Отзывы
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink tag={Link} to="/booking" className="btn btn-lg btn-warning text-white animate__animated animate__bounce animate__delay-3s animate__repeat-2" style={{ fontSize: 20 }}>
              Бронирование
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink tag={Link} to="/login" className="btn btn-lg btn-info text-white animate__animated animate__bounce animate__delay-4s animate__repeat-2" style={{ fontSize: 20 }}>
              Регистрация/Войти
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink tag={Link} to="/support" className="btn btn-lg btn-secondary text-white animate__animated animate__bounce animate__delay-5s animate__repeat-2" style={{ fontSize: 20 }}>
              Служба поддержки
            </NavLink>
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