import React from 'react';
import { Card, CardBody, CardTitle, CardText, CardImg } from 'reactstrap';

const HotelDetails = ({ hotel }) => {
  return (
    <Card>
      <CardImg top width="100%" src={hotel.photo} alt={hotel.name} />
      <CardBody>
        <CardTitle tag="h2">{hotel.name}</CardTitle>
        <CardText>
          <strong>Описание:</strong> {hotel.description}
        </CardText>
        <CardText>
          <strong>Местоположение:</strong> {hotel.location}
        </CardText>
        <CardText>
          <strong>Цена за ночь:</strong> {hotel.price_per_night} BYN
        </CardText>
        <CardText>
          <strong>Рейтинг:</strong> {hotel.rating}
        </CardText>
      </CardBody>
    </Card>
  );
};

export default HotelDetails;