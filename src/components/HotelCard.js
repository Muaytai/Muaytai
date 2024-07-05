import React from 'react';
import { Card, CardBody, CardTitle, CardText, CardImg } from 'reactstrap';
import { Link } from 'react-router-dom';

const HotelCard = ({ hotel }) => {
  return (
    <Card>
      <Link to={`/hotels/${hotel.id}`}>
        <CardImg top width="100%" src={hotel.photo} alt={hotel.name} />
      </Link>
      <CardBody>
        <Link to={`/hotels/${hotel.id}`}>
          <CardTitle tag="h5">{hotel.name}</CardTitle>
        </Link>
        <CardText>Расположение: {hotel.location}</CardText>
        <CardText>Цена за ночь: {hotel.price_per_night} BYN</CardText>
        <CardText>Рейтинг: {hotel.rating}</CardText>
      </CardBody>
    </Card>
  );
};

export default HotelCard;