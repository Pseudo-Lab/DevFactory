'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useFormStore } from '../../store/formStore';
import Modal from '@/components/Modal';
import Cookies from 'js-cookie';

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
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const hasSeenModal = Cookies.get('doNotShowModalPage2');
    if (!hasSeenModal) {
      setShowModal(true);
    }
  }, []);

  const handleConfirm = () => {
    setShowModal(false);
  };

  const handleDoNotShowAgain = () => {
    Cookies.set('doNotShowModalPage2', 'true', { expires: 365 }); // Cookie expires in 365 days
    setShowModal(false);
  };

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
      <Modal
        title="미션 소개"
        content={(
          `1. 참가자들의 코드를 모으세요!<br />` +
          `   코드는 위에 개인별 다른 코드가 있습니다.<br />` +
          `2. 5명이 함께 문제 풀기에 도전하세요!<br />` +
          `   (팁! 문제는 팀원들과 관련된 문제가 나옵니다.)<br />` +
          `3. 성공 시 부스 방문해주세요.<br />` +
          `   성공 선물을 드립니다.`
        )}
        onConfirm={handleConfirm}
        onDoNotShowAgain={handleDoNotShowAgain}
        isOpen={showModal}
      />
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
        <Button asChild className="rounded-full" variant={ 'outline' }>
          <Link href="/page1">&lt;</Link>
        </Button>
      </nav>
    </div>
  );
}
