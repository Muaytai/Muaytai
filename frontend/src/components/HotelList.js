import React from 'react';
import { Card, CardBody, CardTitle, CardText, CardImg, CardSubtitle } from 'reactstrap';

const HotelList = ({ hotels }) => {
  return (
    <div className="row">
      {hotels.map((hotel) => (
        <div className="col-md-4 mb-4" key={hotel.id}>
           <Card>
                {hotel.photo ? (
                  <CardImg top src={`http://127.0.0.1:8000${hotel.photo}`} alt={hotel.name} />
                ) : (
                  <CardImg top src="https://via.placeholder.com/300x200" alt={hotel.name} />
                )}
            <CardBody>
              <CardTitle tag="h5">{hotel.name}</CardTitle>
              <CardSubtitle tag="h6" className="mb-2 text-muted">
                {hotel.location}
              </CardSubtitle>
              <CardText>{hotel.description}</CardText>
              <CardText>
                Цена за ночь: {hotel.price_per_night} BYN | Рейтинг: {hotel.rating}
              </CardText>
            </CardBody>
          </Card>
        </div>
      ))}
    </div>
  );
};

export default HotelList;