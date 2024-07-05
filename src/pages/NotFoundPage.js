import React from 'react';
import { Link } from 'react-router-dom'; // Импортируйте Link из react-router-dom

const NotFoundPage = () => {
  return (
    <div className="not-found-page">
      <img src="https://www.freepik.com/free-vector/404-error-page-with-character-concept-illustration_10632468.htm" alt="404" />
      <h1>Страница не найдена</h1>
      <p>Извините, страница, которую вы ищете, не существует.</p>
      <Link to="/" className="btn btn-primary">Вернуться на главную</Link>
    </div>
  );
};

export default NotFoundPage;