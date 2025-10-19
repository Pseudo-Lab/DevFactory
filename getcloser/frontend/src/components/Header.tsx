'use client';

import React from 'react';
import { useFormStore } from '../store/formStore';

export default function Header() {
  const { email } = useFormStore();

  return (
    <header className="py-4 bg-background text-foreground border-b border-border">
      <h1 className="text-3xl font-bold">친해지길바라</h1>
      <p className="text-md mt-1 text-center" style={{ margin: 0, padding: 0, lineHeight: '1em' }}>
        Pseudo Lab<br />
        2nd Grand Gathering<br />
        2025. 11. 15
      </p>
      {email && <p className="text-sm mt-2"><strong>{email}</strong></p>}
    </header>
  );
}
