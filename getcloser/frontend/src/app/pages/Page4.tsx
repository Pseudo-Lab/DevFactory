'use client';

import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { authenticatedFetch } from '../../lib/api';
import { useFormStore } from '../../store/formStore';
import { useNavigationStore } from '../../store/navigationStore';
import Modal from '@/components/Modal';

// Assuming a TeamMember interface for better typing
interface TeamMember {
  id: number;
  user_id: number;
  name: string;
  email: string;
  github_url?: string; // Optional
  linkedin_url?: string; // Optional
}

interface TeamData {
    id: number;
    team_id: number;
    name: string;
    members: TeamMember[];
}

interface ChallengeResult {
  user_id: number;
  question: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
}

const getJsonFromResponse = async (response: Response) => {
  try {
    const text = await response.text();
    if (text) {
      return JSON.parse(text);
    }
  } catch (e) {
    console.error('Failed to parse response JSON', e);
  }
  return { detail: response.statusText || 'An unknown error occurred' };
};

export default function Page4() {
  const { id, progressStatus, teamId, memberIds, reset, setTeamId, setProgressStatus } = useFormStore(); // Use progressStatus
  const { setCurrentPage } = useNavigationStore();

  const [result, setResult] = useState<string>('');
  const [teamData, setTeamData] = useState<TeamData | null>(null); // State to store team data
  const [clickCount, setClickCount] = useState<number>(0);
  const [lastClickTime, setLastClickTime] = useState<number>(0);
  const [selectedMemberChallenge, setSelectedMemberChallenge] = useState<ChallengeResult | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isRedeemed, setIsRedeemed] = useState(false);

  // This useEffect will set the initial success/failure based on progressStatus from the store
  useEffect(() => {
    if (progressStatus === 'CHALLENGE_SUCCESS') {
      setResult('성공');
      setIsRedeemed(false);
    } else if (progressStatus === 'REDEEMED') {
      setResult('성공');
      setIsRedeemed(true);
    } else if (progressStatus === 'CHALLENGE_FAILED') {
      setResult('실패');
    } else {
      console.warn('progressStatus is not set to a known success/failure state, defaulting to 실패');
      setResult('실패');
    }
  }, [progressStatus]); // Depend on progressStatus from the store

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

  const handleTryAgain = async () => {
    try {
      // First, reset the form store to clear previous challenge data.
      // This preserves the user session while clearing challenge-specific state.
      reset();

      // Call assign API to get a new challenge
      const assignResponse = await authenticatedFetch('/api/v1/challenges/assign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ team_id: teamId, my_id: id, members_ids: memberIds.filter((memberId) => memberId !== Number(id)) }),
      });

      if (!assignResponse.ok) {
        const errorData = await getJsonFromResponse(assignResponse);
        throw new Error(`Failed to assign new challenge: ${errorData.detail}`);
      }

      const newChallengeData = await assignResponse.json();
      console.log('Successfully assigned new challenge:', newChallengeData);

      // Navigate to page3 to start the new challenge. Page3's useEffect will handle populating the question.
      setCurrentPage('page3');
    } catch (error: unknown) {
      console.error('Error trying again:', error);
      let errorMessage = '새로운 챌린지를 할당하는 데 실패했습니다.';
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      alert('재도전 실패');

      reset();
      setTeamId(0);
      setProgressStatus('NONE_TEAM');

      setCurrentPage('page2'); // Fallback to page2 if something goes wrong
    }
  };

  const handleSuccessClick = async () => {
    if (isRedeemed) return;

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
      setIsRedeemed(true);
    }
  };

  const handleMemberClick = async (memberUserId: number) => {
    if (!teamData) return;
    try {
      const response = await authenticatedFetch(`/api/v1/teams/${teamData.team_id}/members/${memberUserId}/challenge`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || response.statusText}`);
      }

      const data: ChallengeResult = await response.json();
      setSelectedMemberChallenge(data);
      setIsModalOpen(true);
    } catch (error: unknown) {
      console.error('Error fetching challenge data:', error);
      if (error instanceof Error) {
        alert(`Error: ${error.message}`);
      } else {
        alert('An unknown error occurred.');
      }
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="mt-8 text-center">
        {result === '성공' ? (
          <>
            <p className="text-3xl font-bold">성공!</p>
            <Image
              src={isRedeemed ? '/redeemed-gift.svg' : '/free-icon-success.png'}
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
                  {teamData.members
                    .filter(member => member.user_id !== Number(id)) // Filter out current user's info, and use correct id
                    .map((member) => (
                      <div key={member.user_id} className="bg-muted p-4 rounded-lg shadow-md cursor-pointer hover:bg-muted/80" onClick={() => handleMemberClick(member.user_id)}>
                        <p className="text-lg font-semibold">{member.name}</p>
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
      <Modal
        isOpen={isModalOpen}
        title="Challenge Result"
        content={
          selectedMemberChallenge
            ? `
              <p class="mb-2"><strong>Question:</strong> ${selectedMemberChallenge.question}</p>
              <p class="mb-1"><strong>Your Answer:</strong> <span class="${selectedMemberChallenge.is_correct ? 'text-green-400' : 'text-red-400'}">${selectedMemberChallenge.user_answer}</span></p>
              ${!selectedMemberChallenge.is_correct ? `<p class="mb-2"><strong>Correct Answer:</strong> <span class="text-green-400">${selectedMemberChallenge.correct_answer}</span></p>` : ''}
            `
            : ''
        }
        onConfirm={() => setIsModalOpen(false)}
        onDoNotShowAgain={() => setIsModalOpen(false)}
      />
    </div>
  );
}
