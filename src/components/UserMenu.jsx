import React, { useState } from 'react';
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import { useNavigate } from 'react-router-dom';

const UserMenu = ({ username }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const toggle = () => setDropdownOpen(!dropdownOpen);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <div style={{ position: 'absolute', top: 10, right: 10, zIndex: 999 }}>
      <Dropdown isOpen={dropdownOpen} toggle={toggle}>
        <DropdownToggle caret>
          {username}
        </DropdownToggle>
        <DropdownMenu right>
          <DropdownItem onClick={() => navigate('/profile')}>Профиль</DropdownItem>
          <DropdownItem divider />
          <DropdownItem onClick={handleLogout}>Выйти</DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </div>
  );
};

export default UserMenu;
