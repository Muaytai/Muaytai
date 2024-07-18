import React from 'react';
import { Card, CardBody, CardTitle, CardText, CardImg } from 'reactstrap';
import { Link } from 'react-router-dom';

const HotelCard = ({ hotel }) => {
  return (
    <Link to={`/hotels/${hotel.id}`}>
      <Card>
        <CardImg top width="100%" src={hotel.photo} alt={hotel.name} />
        <CardBody>
          <CardTitle tag="h5">{hotel.name}</CardTitle>
          <CardText>Расположение: {hotel.location}</CardText>
          <CardText>Цена за ночь: {hotel.price_per_night} BYN</CardText>
          <CardText>Рейтинг: {hotel.rating}</CardText>
        </CardBody>
      </Card>
    </Link>
  );
};

export default HotelCard;