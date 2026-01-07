'use client';

import { authenticatedFetch } from '../lib/api';
import React, { useState, useEffect } from 'react';
import { useFormStore } from '../store/formStore';
import SplitText from '@/app/pages/SplitText';

export default function Header() {
  const { id } = useFormStore();
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const fetchUserName = async () => {
        try {
          const response = await authenticatedFetch(`/api/v1/users/${id}`);
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
    <header className="py-4 bg-background text-foreground border-b border-border text-center flex flex-col items-center">
      <SplitText
        text='친해지길바라'
        className='text-2xl font-semibold text-center'
        delay={100}
        duration={0.6}
        ease='power3.out'
        splitType='chars'
        from={{ opacity: 0, y: 40 }}
        to={{ opacity: 1, y: 0 }}
        threshold={0.1}
        rootMargin='-100px'
        textAlign='center'
      />
      <p className="text-sm mt-2 text-center" style={{ margin: 0, padding: 0, lineHeight: '1.2em' }}>
        Pseudo Lab 2nd Grand Gathering<br />2026. 1. 10
      </p>
      {id && userName && <p className="text-lg mt-4"><strong className="text-emerald-400 text-xl">{userName}</strong></p>}
      {id && !userName && <p className="text-lg mt-4"><strong className="text-emerald-400 text-xl">{id}</strong></p>}
    </header>
  );
}
