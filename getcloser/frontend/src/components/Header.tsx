'use client';

import React from 'react';
import { useFormStore } from '../store/formStore';

export default function Header() {
  const { email } = useFormStore();

  return (
    <header className="text-center py-4 bg-background text-foreground border-b border-border">
      <h1 className="text-2xl font-bold">행사명: 미정</h1>
      <p className="text-md mt-1">일정: 미정</p>
      <p className="text-md">장소: 미정</p>
      {email && <p className="text-sm mt-2">참가 이메일: <strong>{email}</strong></p>}
    </header>
  );
}
