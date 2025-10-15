'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';

export default function Page4() {
  const [result, setResult] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    const isSuccess = Math.random() > 0.5; // 50% chance of success
    setResult(isSuccess ? '성공' : '실패');
  }, []);

  const handleTryAgain = () => {
    router.push('/page2');
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Page 4</h1>
      <p>This is the fourth page.</p>

      <div className="mt-8 text-center">
        {result === '성공' ? (
          <p className="text-green-600 text-3xl font-bold">결과: 성공!</p>
        ) : (
          <>
            <p className="text-red-600 text-3xl font-bold">결과: 실패!</p>
            <Button onClick={handleTryAgain} className="mt-4">다시 도전하기</Button>
          </>
        )}
      </div>
    </div>
  );
}
