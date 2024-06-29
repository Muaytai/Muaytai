import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RegistrationPage from './pages/RegistrationPage';
import SupportPage from './pages/SupportPage';
import ReviewsPage from './pages/ReviewsPage';
import NotFoundPage from './pages/NotFoundPage';
import HotelDetailsPage from './pages/HotelDetailsPage'; // Импортируйте HotelDetailsPage
import BookingPage from './pages/BookingPage'; // Предполагая, у вас есть страница бронирования

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<RegistrationPage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/contacts" element={<ReviewsPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/hotels/:id" element={<HotelDetailsPage />} /> {/* Добавлен маршрут для HotelDetailsPage */}
        <Route path="/booking" element={<BookingPage />} /> {/* Предполагая, у вас есть страница бронирования */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default App;