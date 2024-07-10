import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import HomePage from './pages/HomePage';
import HotelDetailsPage from './pages/HotelDetailsPage';
import BookingPage from './pages/BookingPage';
import LoginPage from './pages/LoginPage';
import UserMenu from './components/UserMenu';
import ReviewsPage from './pages/ReviewsPage';
import SupportPage from './pages/SupportPage';

function App() {
  return (
    <Router>
      <div className="App">
        <UserMenu />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/hotels/:id" element={<HotelDetailsPage />} />
          <Route path="/booking" element={<BookingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/contacts" element={<ReviewsPage />} />
          <Route path="/support" element={<SupportPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;