'use client';

import axios from 'axios';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

export default function ProductDetail({ params }) {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/products/${params.id}/`)
      .then(response => {
        setProduct(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, [params.id]);

  const addToCart = async () => {
    const accessToken = Cookies.get('access_token');
    if (!accessToken) {
      router.push('/login');
      return;
    }

    try {
      await axios.post('http://127.0.0.1:8000/api/cart/add_to_cart/', {
        product_id: product.id,
        quantity: 1,
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      alert('Product added to cart');
    } catch (error) {
      console.error('Failed to add product to cart', error);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <button onClick={() => router.back()}>Back</button>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>${product.price}</p>
      <button onClick={addToCart}>Add to Cart</button>
    </div>
  );
}