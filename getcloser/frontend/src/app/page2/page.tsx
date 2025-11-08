'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useFormStore } from '../../store/formStore';
import Modal from '@/components/Modal';
import Cookies from 'js-cookie';

export default function Page2() {
  const { id } = useFormStore();
  const router = useRouter();
  const [inputs, setInputs] = useState<Array<{ id: string; displayName: string }>>(() => {
    const initialInputs = Array(5).fill({ id: '', displayName: '' });
    return initialInputs;
  });
  const [showModal, setShowModal] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null); // Add timeoutRef

  const fetchUserById = useCallback(async (index: number, userId: string) => {
    if (!userId) return; // Don't fetch if ID is empty

    // Prevent adding self as a team member
    if (index !== 0 && id && Number(userId) === Number(id)) { // Check only for other team members, not self
      alert(`자기 자신(${userId})을 팀원으로 추가할 수 없습니다.`);
      const newInputs = [...inputs];
      newInputs[index] = { id: '', displayName: '' }; // Clear the input field
      setInputs(newInputs);
      return;
    }

    try {
      const response = await fetch(`/api/v1/users/${userId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const userData = await response.json();
      // Assuming the API returns an object with a 'data' field which is the display name
      const newInputs = [...inputs];
      newInputs[index] = { id: userId, displayName: userData.data || userId }; // Store both id and display name
      setInputs(newInputs);
    } catch (error) {
      console.error(`Error fetching user ${userId}:`, error);
      const newInputs = [...inputs];
      newInputs[index] = { id: userId, displayName: userId }; // Fallback to just ID if fetch fails
      setInputs(newInputs);
      // Optionally, display an error message to the user
    }
  }, [id, inputs]);

  useEffect(() => {
    const hasSeenModal = Cookies.get('doNotShowModalPage2');
    if (!hasSeenModal) {
      setShowModal(true);
    }
  }, []);

  // Effect to pre-fill the first input if ID is available
  useEffect(() => {
    if (id && inputs[0].id === '') { // Only fetch if ID exists and input is empty
      fetchUserById(0, id);
    }
  }, [id, fetchUserById, inputs]); // Rerun when id changes

  const handleConfirm = () => {
    setShowModal(false);
  };

  const handleDoNotShowAgain = () => {
    Cookies.set('doNotShowModalPage2', 'true', { expires: 365 }); // Cookie expires in 365 days
    setShowModal(false);
  };

  const handleInputChange = (index: number, value: string) => {
    const newInputs = [...inputs];
    newInputs[index] = { id: value, displayName: value }; // Temporarily set display name to ID
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

  const handleSolveProblem = () => {
    console.log('Inputs:', inputs.map(input => input.id));
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

      <div className="mt-8 space-y-4">
        {[...Array(5)].map((_, index) => (
          <div key={index}>
            <Label htmlFor={`team-email-${index}`}>팀원 {index + 1}</Label>
            {index === 0 && <Label> (나)</Label>}
            <Input
              id={`team-id-${index}`}
              type="id"
              placeholder={`팀원 ${index + 1}의 번호`}
              value={inputs[index].displayName}
              onChange={(e) => handleInputChange(index, e.target.value)}
              onBlur={() => {
                if (timeoutRef.current) {
                  clearTimeout(timeoutRef.current); // Clear any pending debounce
                }
                fetchUserById(index, inputs[index].id); // Fetch immediately on blur using the stored ID
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
