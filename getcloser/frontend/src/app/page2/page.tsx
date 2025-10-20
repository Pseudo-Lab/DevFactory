'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useFormStore } from '../../store/formStore';
import React, { useState } from 'react';

export default function Page2() {
  const { email } = useFormStore();
  const router = useRouter();
  const [inputs, setInputs] = useState<string[]>(() => {
    const initialInputs = Array(5).fill('');
    if (email) {
      initialInputs[0] = email;
    }
    return initialInputs;
  });

  const handleInputChange = (index: number, value: string) => {
    const newInputs = [...inputs];
    newInputs[index] = value;
    setInputs(newInputs);
  };

  const handleSolveProblem = () => {
    console.log('Inputs:', inputs);
    // You can add logic here to process the inputs before navigating
    router.push('/page3');
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Page 2</h1>
      <p>This is the second page.</p>
      {email && <p className="mt-4">이메일: <strong>{email}</strong></p>}

      <div className="mt-8 space-y-4">
        {[...Array(5)].map((_, index) => (
          <div key={index}>
            <Label htmlFor={`team-email-${index}`}>팀원 {index + 1}</Label>
            <Input
              id={`team-email-${index}`}
              type="email"
              placeholder={`팀원 ${index + 1}의 이메일 주소`}
              value={inputs[index]}
              onChange={(e) => handleInputChange(index, e.target.value)}
              disabled={index === 0}
            />
          </div>
        ))}
        <Button onClick={handleSolveProblem} className="w-full">문제 풀기</Button>
      </div>

      <nav className="flex justify-between mt-8">
        <Button asChild>
          <Link href="/page1">이전 페이지 (Page 1)</Link>
        </Button>
        {/* Removed '다음 페이지 (Page 3)' button */}
      </nav>
    </div>
  );
}
