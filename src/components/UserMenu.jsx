import React, { useState, useEffect } from 'react';
import { Navbar, Nav, NavItem, NavLink } from 'reactstrap';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const UserMenu = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        setUsername(decodedToken.username);
      } catch (error) {
        console.error("Ошибка декодирования токена:", error);
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUsername('');
    navigate('/login');
  };

  return (
    <Navbar className="bg-dark text-white" expand="md">
      <Nav navbar>
        <NavItem>
          {username && (
            <>
              <NavLink className="text-white">Привет, {username}!</NavLink>
              <NavLink className="text-white" onClick={handleLogout}>Выйти</NavLink>
            </>
          )}
        </NavItem>
      </Nav>
    </Navbar>
  );
};

export default UserMenu;