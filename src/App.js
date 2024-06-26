// App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardBody, CardTitle, CardText, CardImg, Container, Row, Col } from 'reactstrap';

const App = () => {
  const [hotels, setHotels] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/hotels/');
        setHotels(response.data);
        setIsLoading(false);
      } catch (err) {
        setError(err.message);
        setIsLoading(false);
      }
    };
    fetchHotels();
  }, []);

  return (
    <Container>
      <h1 className="my-4">Список отелей</h1>
      {isLoading ? (
        <p>Загрузка...</p>
      ) : error ? (
        <p>Ошибка: {error}</p>
      ) : (
        <Row>
          {hotels.map((hotel) => (
            <Col md={4} key={hotel.id} className="mb-4">
              <Card>
                {hotel.photo ? (
                  <CardImg top src={`http://127.0.0.1:8000${hotel.photo}`} alt={hotel.name} />
                ) : (
                  <CardImg top src="https://via.placeholder.com/300x200" alt={hotel.name} />
                )}
                <CardBody>
                  <CardTitle tag="h5">{hotel.name}</CardTitle>
                  <CardText>{hotel.description}</CardText>
                  <CardText>
                    <strong>Местоположение:</strong> {hotel.location}
                  </CardText>
                  <CardText>
                    <strong>Цена за ночь:</strong> {hotel.price_per_night} руб.
                  </CardText>
                  <CardText>
                    <strong>Рейтинг:</strong> {hotel.rating}
                  </CardText>
                </CardBody>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </Container>
  );
};

export default App;