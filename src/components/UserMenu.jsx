import React, { useState, useEffect } from 'react';
import { Navbar, Nav, NavItem, Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const UserMenu = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [dropdownOpen, setDropdownOpen] = useState(false);

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

  const toggle = () => setDropdownOpen(!dropdownOpen);

  return (
    <Navbar className="bg-dark text-white" expand="md">
      <Nav navbar>
        <NavItem>
          {username && (
            <Dropdown isOpen={dropdownOpen} toggle={toggle}>
              <DropdownToggle nav caret className="text-white">
                Привет, {username}!
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem onClick={handleLogout}>Выйти</DropdownItem>
                <DropdownItem onClick={() => navigate('/profile')}>Профиль</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          )}
        </NavItem>
      </Nav>
    </Navbar>
  );
};

export default UserMenu;