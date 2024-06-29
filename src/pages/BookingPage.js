import React from 'react';
import { Container } from 'reactstrap';
import BookingForm from '../components/BookingForm';

const BookingPage = () => {
  return (
    <Container>
      <h2>Бронирование отеля</h2>
      <BookingForm />
    </Container>
  );
};

export default BookingPage;