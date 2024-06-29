
import React, { useState } from 'react';
import { Form, FormGroup, Label, Input, Button } from 'reactstrap';

const HotelFilter = ({ onFilter }) => {
  const [filterParams, setFilterParams] = useState({
    name: '',
    minRating: 0,
    maxPrice: 1000,
  });

  const handleInputChange = (e) => {
    setFilterParams({
      ...filterParams,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onFilter(filterParams);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <FormGroup>
        <Label for="name">Название</Label>
        <Input type="text" name="name" id="name" value={filterParams.name} onChange={handleInputChange} />
      </FormGroup>
      <FormGroup>
        <Label for="minRating">Минимальный рейтинг</Label>
        <Input type="number" name="minRating" id="minRating" value={filterParams.minRating} onChange={handleInputChange} />
      </FormGroup>
      <FormGroup>
        <Label for="maxPrice">Максимальная цена</Label>
        <Input type="number" name="maxPrice" id="maxPrice" value={filterParams.maxPrice} onChange={handleInputChange} />
      </FormGroup>
      <Button color="primary" type="submit">Фильтровать</Button>
    </Form>
  );
};

export default HotelFilter;