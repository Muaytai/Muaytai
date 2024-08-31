'use client';

import axios from 'axios';
import { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import Link from 'next/link';

export default function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const accessToken = Cookies.get('access_token');
    if (!accessToken) {
      setError('No access token');
      setLoading(false);
      return;
    }

    axios.get('http://127.0.0.1:8000/api/products/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(response => {
        setProducts(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="flex justify-center items-center h-screen text-lg">Loading...</p>;
  if (error) return <p className="flex justify-center items-center h-screen text-lg text-red-500">Error: {error.message}</p>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold text-center mb-6">Products</h1>
      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map(product => (
          <li key={product.id} className="border p-4 rounded-lg shadow-md">
            <Link href={`/products/${product.id}`} className="block hover:text-blue-500">
              <h2 className="text-2xl font-semibold">{product.name}</h2>
            </Link>
            <p className="text-gray-600">{product.description}</p>
            <p className="text-lg font-medium mt-2">${product.price}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}