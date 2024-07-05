import React from 'react';
import { Container, Row, Col, Card, CardBody, Button } from 'reactstrap';
import { useSpring, animated } from 'react-spring';
import Header from '../components/Header';
import HotelList from '../components/HotelList';
import HotelFilter from '../components/HotelFilter';

const partners = [
  {
    name: 'OVERONE',
    url: 'https://overone.by/'
  }
];

const HomePage = () => {
  const randomPartner = partners[0];

  const [springProps] = useSpring(() => ({
    from: { opacity: 0, transform: 'translateY(50px)' },
    to: { opacity: 1, transform: 'translateY(0)' },
    config: { duration: 1000 }
  }));

  return (
    <Container>
      <Header />
      <animated.div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '300px',
          pointerEvents: 'none',
          overflow: 'hidden',
          display: 'flex',
          justifyContent: 'space-between'
        }}
      >
        <div
          style={{
            width: '400px',
            height: '300px',
            backgroundImage: 'url("https://i.gifer.com/7SYx.gif")',
            backgroundSize: 'contain',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'left center',
            animation: 'fireworks 2s ease-in-out infinite'
          }}
        />
        <div
          style={{
            width: '400px',
            height: '300px',
            backgroundImage: 'url("https://i.gifer.com/7SYx.gif")',
            backgroundSize: 'contain',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'right center',
            animation: 'fireworks 2s ease-in-out infinite'
          }}
        />
      </animated.div>
      <HotelFilter />
      <HotelList />
      <animated.div style={springProps}>
        <Row className="mt-5">
          <Col md={{ size: 8, offset: 2 }}>
            <Card
              className="border-danger animate__animated animate__fadeInUp"
              style={{
                backgroundColor: '#ff69b4',
                backgroundImage: 'url("https://i.gifer.com/Nv2.gif")',
                backgroundSize: 'contain',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center',
                boxShadow: '0 0 20px rgba(255, 105, 180, 0.5)',
                borderRadius: '10px'
              }}
            >
              <CardBody>
                <div className="text-center">
                  <p className="text-white mb-3">Наши партнеры лучшая компания</p>
                  <Button
                    color="danger"
                    tag="a"
                    href={randomPartner.url}
                    target="_blank"
                    className="animate__animated animate__pulse animate__infinite"
                    style={{
                      fontFamily: 'Permanent Marker, cursive',
                      fontSize: '1.5rem',
                      backgroundImage: 'url("https://i.gifer.com/Nv2.gif")',
                      backgroundSize: 'contain',
                      backgroundRepeat: 'no-repeat',
                      backgroundPosition: 'center'
                    }}
                  >
                    {randomPartner.name}
                  </Button>
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </animated.div>
    </Container>
  );
};

export default HomePage;