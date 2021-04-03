import React, { useState } from 'react';

import axios from 'axios';
import { Formik } from 'formik';
import { Button, Col, Form, Row } from 'react-bootstrap';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';

function Search ({ search }) {
  const [isLoading, setLoading] = useState(false);
  const [options, setOptions] = useState([]);

  const wineSearchWord = async query => {
    if (query.length < 3) {
      setLoading(false);
      setOptions([]);
    } else {
      setLoading(true);
      try {
        const response = await axios({
          method: 'get',
          url: 'http://localhost:8003/api/v1/catalog/wine-search-words/',
          params: {
            query: query
          }
        });
        setOptions(response.data);
      } catch(error) {
        console.error(error);
        setOptions([]);
      } finally {
        setLoading(false);
      }
    }
  };

  const onSubmit = async (values, actions) => {
    await search(
      values.country,
      values.points,
      values.priceMax,
      values.priceMin,
      values.query
    );
  };

  return (
    <Formik
      initialValues={{
        country: '',
        points: '',
        priceMax: '',
        priceMin: '',
        query: ''
      }}
      onSubmit={onSubmit}
    >
      {({
        handleChange,
        handleSubmit,
        setFieldValue,
        values
      }) => (
        <Form noValidate onSubmit={handleSubmit}>
          <Form.Group controlId="country">
            <Form.Label>Country</Form.Label>
            <Col>
              <Form.Control
                type="text"
                name="country"
                placeholder="Enter a country (e.g. US)"
                value={values.country}
                onChange={handleChange}
              />
              <Form.Text className="text-muted">
                Filters search results by country.
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="points">Points</Form.Label>
            <Col>
              <Form.Control
                id="points"
                type="number"
                min="1"
                max="100"
                name="points"
                placeholder="Enter points (e.g. 92)"
                value={values.points}
                onChange={handleChange}
              />
              <Form.Text className="text-muted">
                Filters search results by points.
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="priceMin">Minimum Price</Form.Label>
            <Col>
              <Form.Control
                id="priceMin"
                type="number"
                name="priceMin"
                placeholder="Enter minimum price (e.g. 30)"
                value={values.priceMin}
                onChange={handleChange}
              />
              <Form.Text className="text-muted">
                Filters search results by minimum price.
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="priceMax">Maximum Price</Form.Label>
            <Col>
              <Form.Control
                id="priceMax"
                type="number"
                name="priceMax"
                placeholder="Enter maximum price (e.g. 40)"
                value={values.priceMax}
                onChange={handleChange}
              />
              <Form.Text className="text-muted">
                Filters search results by maximum price.
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group controlId='query'>
            <Form.Label>Query</Form.Label>
            <Col>
              <AsyncTypeahead
                filterBy={() => true}
                id="query"
                isLoading={isLoading}
                labelKey="word"
                name="query"
                onChange={selected => {
                  const value = selected.length > 0 ? selected[0].word : '';
                  setFieldValue('query', value);
                }}
                onInputChange={value => setFieldValue('query', value)}
                onSearch={wineSearchWord}
                options={options}
                placeholder="Enter a search term (e.g. cabernet)"
                type="text"
                value={values.query}
              />
              <Form.Text className='text-muted'>
                Searches for query in variety, winery, and description.
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group as={Row}>
            <Col>
              <Button type='submit' variant='primary'>Search</Button>
            </Col>
          </Form.Group>
        </Form>
      )}
    </Formik>
  );
}

export default Search;
