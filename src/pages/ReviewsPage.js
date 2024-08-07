import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { Row, Col } from 'reactstrap';

const ReviewsPage = () => {
  const reviews = [
    {
      id: 1,
      author: 'Андрей Иванов',
      city: 'Москва',
      text: 'Я недавно останавливался в отеле "Лазурный берег" и был приятно удивлен. Номера чистые и уютные, персонал очень вежливый и внимательный. Расположение отеля просто идеальное - в нескольких минутах ходьбы от пляжа. Я обязательно вернусь сюда в следующий раз!',
    },
    {
      id: 2,
      author: 'Ольга Петрова',
      city: 'Санкт-Петербург',
      text: 'Отель "Гранд Палас" превзошел все мои ожидания. Роскошные интерьеры, великолепный ресторан с изысканной кухней, а бассейн на крыше с панорамным видом на город - это просто сказка Персонал работает на высшем уровне, создавая по-настоящему незабываемый отдых. Рекомендую всем, кто ценит комфорт и качество.',
    },
    {
      id: 3,
      author: 'Максим Сидоров',
      city: 'Екатеринбург',
      text: 'Отель "Уральские Самоцветы" - отличный выбор для тех, кто хочет совместить деловую поездку с приятным отдыхом. Современные номера, удобное расположение в центре города и вкусная кухня в ресторане - все это делает пребывание в отеле комфортным и приятным.',
    },
    {
      id: 4,
      author: 'Елена Кузнецова',
      city: 'Казань',
      text: 'Отель "Кул Шариф" - это настоящая жемчужина Казани. Великолепная архитектура, продуманный интерьер и высокий уровень сервиса создают атмосферу роскоши и комфорта. Особенно впечатляет панорамный вид на мечеть Кул Шариф с террасы ресторана. Рекомендую всем, кто ценит красоту и качество.',
    },
    {
      id: 5,
      author: 'Дмитрий Смирнов',
      city: 'Нижний Новгород',
      text: 'Отель "Волга" - отличный вариант для семейного отдыха. Просторные номера, детская игровая комната и анимация делают пребывание с детьми комфортным и увлекательным. Расположение отеля на берегу Волги позволяет наслаждаться прекрасными видами и свежим воздухом.',
    },
    {
      id: 6,
      author: 'Анна Соколова',
      city: 'Ростов-на-Дону',
      text: 'Отель "Дон-Плаза" - это идеальное сочетание комфорта, качества и гостеприимства. Номера оборудованы всем необходимым, а персонал всегда готов помочь и ответить на любые вопросы. Расположение отеля в самом центре города позволяет легко добраться до основных достопримечательностей.',
    },
    {
      id: 7,
      author: 'Сергей Петров',
      city: 'Новосибирск',
      text: 'Отель "Сибирь" - это отличный выбор для деловых поездок. Современные конференц-залы, быстрый интернет и удобное расположение рядом с бизнес-центром делают пребывание в отеле максимально комфортным и продуктивным. Также стоит отметить вкусную кухню в ресторане и приветливый персонал.',
    },
    {
      id: 8,
      author: 'Мария Иванова',
      city: 'Владивосток',
      text: 'Отель "Версаль" - это настоящий оазис комфорта и спокойствия во Владивостоке. Номера оформлены в элегантном стиле, а панорамные окна открывают захватывающие виды на бухту Золотой Рог. Особенно впечатляет SPA-центр отеля с бассейном, саунами и массажными кабинетами.',
    },
    {
      id: 9,
      author: 'Александр Кузьмин',
      city: 'Калининград',
      text: 'Отель "Балтика" - это идеальный выбор для тех, кто хочет познакомиться с Калининградом. Расположенный в историческом центре города, отель позволяет легко добраться до основных достопримечательностей. Номера оборудованы всем необходимым, а завтраки в ресторане отеля отличаются большим разнообразием и высоким качеством.',
    },
    {
      id: 10,
      author: 'Татьяна Смирнова',
      city: 'Ярославль',
      text: 'Отель "Золотое кольцо" - это идеальное место для знакомства с Ярославлем. Расположенный в самом центре города, отель позволяет легко добраться до основных достопримечательностей. Номера оформлены в классическом стиле, а завтраки в ресторане отеля отличаются большим разнообразием и высоким качеством.',
    }
  ];

  return (
    <Container>
      <Title>Отзывы об отелях</Title>
      <ReviewsContainer>
        {reviews.map((review) => (
          <ReviewContainer key={review.id}>
              <ReviewContent>
              <ReviewAuthor>{review.author}</ReviewAuthor>
              <ReviewText>{review.city}: {review.text}</ReviewText>
            </ReviewContent>
          </ReviewContainer>
        ))}
      </ReviewsContainer>
      <Row className="mt-4">
        <Col>
          <Link to="/" className="btn btn-danger btn-block">
            Вернуться на главную
          </Link>
        </Col>
      </Row>
    </Container>
  );
};

export default ReviewsPage;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
  background-color: #f5f5f5;
`;

const Title = styled.h1`
  text-align: center;
  margin-bottom: 40px;
  color: #007bff;
  font-size: 36px;
  font-weight: bold;
`;

const ReviewsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  grid-gap: 40px;
`;

const ReviewContainer = styled.div`
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const ReviewContent = styled.div`
  padding: 20px;
`;

const ReviewAuthor = styled.h3`
  color: #007bff;
  margin-bottom: 10px;
  font-size: 20px;
  font-weight: bold;
`;

const ReviewText = styled.p`
  color: #555;
  line-height: 1.6;
  font-size: 16px;
`;