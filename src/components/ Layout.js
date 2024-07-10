import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './components/Header';
import UserMenu from './components/UserMenu';
const Layout = () => {
  return (
    <>
      <Header />
      <UserMenu />
      <Container>
        <Outlet />
      </Container>
    </>
  );
};

export default App;