import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RegistrationPage from './pages/RegistrationPage'
import SupportPage from './pages/SupportPage'
import ReviewsPage from './pages/ReviewsPage'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<RegistrationPage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/contacts" element={<ReviewsPage />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </Router>
  );
};

export default App;