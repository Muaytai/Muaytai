import React from 'react';
import { Card, CardBody, CardTitle, CardText, Button } from 'reactstrap';

const HotelCard = ({ hotel }) => {
  return (
    <Card>
      <CardBody>
        <CardTitle tag="h5">{hotel.name}</CardTitle>
        <CardText>{hotel.description}</CardText>
        <Button color="primary" href={`/hotels/${hotel.id}`}>
          Подробнее
        </Button>
      </CardBody>
    </Card>
  );
};

export default HotelCard;