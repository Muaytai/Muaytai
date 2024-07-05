import React from 'react';
import { Card, CardBody, CardTitle, CardText, CardImg, CardSubtitle } from 'reactstrap';
import { Link } from 'react-router-dom';

const HotelList = ({ hotels }) => {
  return (
    <div className="row">
      {hotels.length > 0 ? ( // Проверяем, есть ли отели
        hotels.map((hotel) => (
          <div className="col-md-4 mb-4" key={hotel.id}>
            <Card>
              {hotel.photo && ( // Проверка, есть ли фото
                <CardImg top src={hotel.photo} alt={hotel.name} />
              )}
              {!hotel.photo && ( // Если фото нет, показываем заглушку
                <CardImg top src="https://via.placeholder.com/300x200" alt={hotel.name} />
              )}
              <CardBody>
                <CardTitle tag="h5">
                  <Link to={`/hotels/${hotel.id}`}>{hotel.name}</Link>
                </CardTitle>
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
        ))
      ) : (
        <p>Отелей не найдено</p>
      )}
    </div>
  );
};

export default HotelList;