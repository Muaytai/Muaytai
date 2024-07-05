import React from 'react';
import { Card, CardBody, CardTitle, CardText, Button, CardImg } from 'reactstrap';

const HotelCard = ({ hotel }) => {
  return (
    <Card>
      <CardImg top width="100%" src={hotel.photo} alt={hotel.name} /> {/* Добавьте фото */}
      <CardBody>
        <CardTitle tag="h5">{hotel.name}</CardTitle>
        <CardText>Цена: {hotel.price_per_night} BYN</CardText> {/* Добавьте цену */}
        <CardText>{hotel.description}</CardText>
        <Button color="primary" href={`/hotels/${hotel.id}`}>
          Подробнее
        </Button>
      </CardBody>
    </Card>
  );
};

export default HotelCard;