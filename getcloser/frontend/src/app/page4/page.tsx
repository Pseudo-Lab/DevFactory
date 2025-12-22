'use client';

import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { authenticatedFetch } from '../../lib/api';
import { useFormStore } from '../../store/formStore';

// Assuming a TeamMember interface for better typing
interface TeamMember {
  id: number;
  name: string;
  email: string;
  github_url?: string; // Optional
  linkedin_url?: string; // Optional
}

interface TeamData {
    id: number;
    name: string;
    members: TeamMember[];
}

export default function Page4() {
  const { id, isCorrect } = useFormStore(); // Added isCorrect

  const [result, setResult] = useState<string>('');
  const [teamData, setTeamData] = useState<TeamData | null>(null); // State to store team data
  const [clickCount, setClickCount] = useState<number>(0);
  const [lastClickTime, setLastClickTime] = useState<number>(0);
  const router = useRouter();

  // This useEffect will set the initial success/failure based on isCorrect from the store
  useEffect(() => {
    if (isCorrect === null) {
      console.warn('isCorrect is not set, defaulting to 실패');
      setResult('실패');
    } else {
      setResult(isCorrect ? '성공' : '실패');
    }
  }, [isCorrect]); // Depend on isCorrect from the store

  // New useEffect to fetch team data when result is '성공'
  useEffect(() => {
    if (result === '성공') {
      const fetchTeamData = async () => {
        try {
          const response = await authenticatedFetch('/api/v1/teams/me', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || response.statusText}`);
          }

          const data = await response.json();
          setTeamData(data);
        } catch (error: unknown) {
          console.error('Error fetching team data:', error);
          // Handle error, e.g., show a message to the user
        }
      };

      fetchTeamData();
    }
  }, [result]); // Depend on result

  const handleTryAgain = () => {
    router.push('/page2');
  };

  const handleSuccessClick = async () => {
    const currentTime = new Date().getTime();
    if (currentTime - lastClickTime < 2000) { // 2 seconds window
      setClickCount(prevCount => prevCount + 1);
    } else {
      setClickCount(1);
    }
    setLastClickTime(currentTime);

    if (clickCount + 1 >= 5) { // Check if this click makes it 5
      setClickCount(0); // Reset after alert
      setLastClickTime(0); // Reset time as well

      const response = await authenticatedFetch('/api/v1/challenges/redeem', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: id }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      alert('수령 완료!');

    }
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
              onClick={handleSuccessClick}
            />
            <p>DevFactory 부스에 방문하여 해당 화면을 보여주세요.<br />부스 방문 시 선물 드립니다!</p>

            {/* Display Team Members */}
            {teamData && teamData.members && teamData.members.length > 0 && (
              <div className="mt-8 text-left">
                <h3 className="text-2xl font-bold mb-4">우리 팀원들</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {teamData.members.map((member) => (
                    <div key={member.id} className="bg-muted p-4 rounded-lg shadow-md">
                      <p className="text-lg font-semibold">{member.name}</p>
                      <p className="text-sm text-gray-600">Email: {member.email}</p>
                      {member.github_url && (
                        <p className="text-sm text-gray-600">
                          GitHub: <a href={member.github_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">{member.github_url}</a>
                        </p>
                      )}
                      {member.linkedin_url && (
                        <p className="text-sm text-gray-600">
                          LinkedIn: <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">{member.linkedin_url}</a>
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
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
