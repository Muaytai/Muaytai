'use client';

import axios from 'axios';
import { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';

export default function Cart() {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const accessToken = Cookies.get('access_token');
    if (!accessToken) {
      setError('No access token');
      setLoading(false);
      return;
    }

    axios.get('http://127.0.0.1:8000/api/cart/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(response => {
        setCart(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  const createOrder = async () => {
    const accessToken = Cookies.get('access_token');
    if (!accessToken) {
      router.push('/login');
      return;
    }

    try {
      await axios.post('http://127.0.0.1:8000/api/orders/create_order/', {}, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      alert('Order created successfully');
      router.push('/profile');
    } catch (error) {
      console.error('Failed to create order', error);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>Cart</h1>
      <ul>
        {cart.items.map(item => (
          <li key={item.product.id}>
            <h2>{item.product.name}</h2>
            <p>{item.product.description}</p>
            <p>${item.product.price}</p>
            <p>Quantity: {item.quantity}</p>
          </li>
        ))}
      </ul>
      <button onClick={createOrder}>Create Order</button>
    </div>
  );
}