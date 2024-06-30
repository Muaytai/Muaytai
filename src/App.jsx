import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RegistrationPage from './pages/RegistrationPage';
import SupportPage from './pages/SupportPage';
import ReviewsPage from './pages/ReviewsPage';
import NotFoundPage from './pages/NotFoundPage';
import HotelDetailsPage from './pages/HotelDetailsPage';
import BookingPage from './pages/BookingPage';
import Header from './components/Header';
import UserMenu from './components/UserMenu';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<Header />} /> {/* Заголовок будет на всех страницах */}
        <Route path="/login" element={<RegistrationPage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/contacts" element={<ReviewsPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/hotels/:id" element={<HotelDetailsPage />} />
        <Route path="/booking" element={<BookingPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default App;