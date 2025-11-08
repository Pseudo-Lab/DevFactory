'use client';

import React, { useState, useEffect } from 'react';
import { useFormStore } from '../store/formStore';

export default function Header() {
  const { id } = useFormStore();
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const fetchUserName = async () => {
        try {
          const response = await fetch(`/api/v1/users/${id}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const userData = await response.json();
          setUserName(userData.data || null);
        } catch (error) {
          console.error(`Error fetching user ${id}:`, error);
          setUserName(null); // Clear user name on error
        }
      };
      fetchUserName();
    } else {
      setUserName(null); // Clear user name if id is empty
    }
  }, [id]);

  return (
    <header className="py-4 bg-background text-foreground border-b border-border">
      <h1 className="text-3xl font-bold">친해지길바라</h1>
      <p className="text-md mt-1 text-center" style={{ margin: 0, padding: 0, lineHeight: '1em' }}>
        Pseudo Lab<br />
        2nd Grand Gathering<br />
        2025. 12. 20
      </p>
      {id && userName && <p className="text-sm mt-2">ID: <strong>{id}</strong>, 이름: <strong>{userName}</strong></p>}
      {id && !userName && <p className="text-sm mt-2">ID: <strong>{id}</strong></p>}
    </header>
  );
}
