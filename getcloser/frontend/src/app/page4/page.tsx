'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';

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
      <div className="mt-8 text-center">
        {result === '성공' ? (
          <>
            <p className="text-3xl font-bold">성공!</p>
            <Image
              src="/free-icon-success.png"
              alt="Success"
              width={100}
              height={100}
              className="mx-auto block"
            />
            <p>DevFactory 부스에 방문하여 해당 화면을 보여주세요.<br />부스 방문 시 선물 드립니다!</p>
          </>
        ) : (
          <>
            <p className="text-red-600 text-3xl font-bold">실패!</p>
            <Image src="/free-icon-failure.png" alt="Fail" width={100} height={100} className="mx-auto block" />
            <Button onClick={handleTryAgain} className="mt-4">다시 도전하기</Button>
          </>
        )}
      </div>
    </div>
  );
}
