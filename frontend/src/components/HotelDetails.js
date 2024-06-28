import React from 'react';
import { Row, Col, Card, CardBody, CardTitle, CardText } from 'reactstrap';

const HotelDetails = () => {
  // Здесь вы можете получить данные о выбранном отеле из URL или состояния
  const hotel = {
    id: 1,
    name: 'Отель Гранд',
    description: 'Роскошный отель в центре города',
    price: 150,
    rating: 4.5,
    amenities: ['Бассейн', 'Фитнес-центр', 'Ресторан']
  };

  return (
    <Row>
      <Col md={8}>
        <Card>
          <CardBody>
            <CardTitle tag="h3">{hotel.name}</CardTitle>
            <CardText>{hotel.description}</CardText>
            <CardText>Цена: {hotel.price} руб. за ночь</CardText>
            <CardText>Рейтинг: {hotel.rating}</CardText>
            <h4>Удобства:</h4>
            <ul>
              {hotel.amenities.map((amenity, index) => (
                <li key={index}>{amenity}</li>
              ))}
            </ul>
          </CardBody>
        </Card>
      </Col>
    </Row>
  );
};

export default HotelDetails;