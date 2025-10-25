'use client';

import React, { useState, useEffect, useRef } from 'react';
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
  const timeoutRef = useRef<NodeJS.Timeout | null>(null); // Add timeoutRef

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

    // Clear any existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set a new timeout to fetch user data after 3 seconds
    timeoutRef.current = setTimeout(() => {
      fetchUserById(index, value);
    }, 3000);
  };

  const fetchUserById = async (index: number, id: string) => {
    if (!id) return; // Don't fetch if ID is empty
    try {
      const response = await fetch(`${process.env.APP_HOST}/v1/users/${id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const userData = await response.json();
      // Assuming the API returns an object with a 'detail' field as per user's confirmation
      const newInputs = [...inputs];
      newInputs[index] = userData.detail || id; // Use fetched detail, or original ID if not found
      setInputs(newInputs);
    } catch (error) {
      console.error(`Error fetching user ${id}:`, error);
      // Optionally, display an error message to the user
    }
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
            {index === 0 && <Label> (나)</Label>}
            <Input
              id={`team-id-${index}`}
              type="id"
              placeholder={`팀원 ${index + 1}의 번호`}
              value={inputs[index]}
              onChange={(e) => handleInputChange(index, e.target.value)}
              onBlur={(e) => {
                if (timeoutRef.current) {
                  clearTimeout(timeoutRef.current); // Clear any pending debounce
                }
                fetchUserById(index, e.target.value); // Fetch immediately on blur
              }}
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
