import React from 'react';
import { Container, Row, Col } from 'reactstrap';

const SupportPage = () => {
  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <h1 className="text-center mb-4">Служба поддержки</h1>
          <p className="lead text-center">
            Мы здесь, чтобы помочь вам. Если у вас возникли какие-либо вопросы или проблемы, пожалуйста, свяжитесь с нами, и мы сделаем все возможное, чтобы решить их как можно быстрее.
          </p>
          <div className="text-center">
            <h3 className="mb-3">Как с нами связаться:</h3>
            <p>
              Телефон: +7 (123) 456-78-90<br />
              Email: support@ourhotel.com
            </p>
            <p>
              Наши специалисты службы поддержки работают круглосуточно, 7 дней в неделю, чтобы помочь вам в любое время.
            </p>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default SupportPage;