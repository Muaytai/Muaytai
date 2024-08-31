'use client';

import axios from 'axios';
import { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const accessToken = Cookies.get('access_token');
    if (!accessToken) {
      setError('No access token');
      setLoading(false);
      return;
    }

    axios.get('http://127.0.0.1:8000/api/profile/me/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(response => {
        setUser(response.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>Profile</h1>
      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
    </div>
  );
}