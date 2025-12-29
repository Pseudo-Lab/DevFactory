'use client';

import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import React, { useEffect } from 'react';
import { useFormStore } from '../../store/formStore';
import { authenticatedFetch } from '../../lib/api';
import { useNavigationStore } from '../../store/navigationStore';

interface TeamMember {
  id: number;
  user_id: number;
  name: string;
  email: string;
  github_url?: string;
  linkedin_url?: string;
}

const questions = [
  { category: '1', keyword: '관심사', problem: '사용자의 관심사를 맞춰주세요. 예: 기술, 예술, 환경 등' },
  { category: '2', keyword: '취미', problem: '사용자의 취미를 맞춰주세요. 예: 등산, 독서, 요리 등' },
  { category: '3', keyword: 'MBTI', problem: '사용자의 MBTI 유형을 맞춰주세요. 예: INFP, ESTJ 등' },
];

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

export default function Page3() {
  const { question, answer, challengeId, setAnswer, id, teamId, memberIds, setQuestion, setChallengeId, setIsCorrect, reset } = useFormStore(); // Destructure new state
  const { setCurrentPage } = useNavigationStore();

  useEffect(() => {
    const CHALLENGE_DATA_KEY = 'challengeData';

    const initializeChallenge = async () => {
      if (!question && id && teamId) {
        // Fetch team members to get their names
        let members: TeamMember[] = [];
        try {
          const teamResponse = await authenticatedFetch('/api/v1/teams/me', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
          });
          if (teamResponse.ok) {
            const teamData = await teamResponse.json();
            if (teamData && teamData.members) {
              members = teamData.members;
            }
          } else {
            console.error('Failed to fetch team data');
          }
        } catch (error) {
          console.error('Error fetching team members:', error);
        }

        const findMemberName = (userId: number): string => {
          const member = members.find((m) => m.user_id === userId);
          return member ? member.name : String(userId); // Fallback to user_id as string
        };

        // 1. Try to restore challenge from localStorage
        const savedChallengeJSON = localStorage.getItem(CHALLENGE_DATA_KEY);
        if (savedChallengeJSON) {
          console.log('Restoring challenge from localStorage...');
          try {
            const savedChallenge = JSON.parse(savedChallengeJSON);
            if (savedChallenge.category && savedChallenge.assigned_challenge_id) {
              const questionInfo = questions.find((q) => q.category === String(savedChallenge.category));
              if (questionInfo) {
                const memberName = findMemberName(savedChallenge.user_id);
                setQuestion([memberName, questionInfo.problem].join(' '));
                setChallengeId(savedChallenge.assigned_challenge_id);
                return; // Challenge successfully restored
              }
            }
          } catch (e) {
            console.error('Failed to parse challenge data from localStorage', e);
            localStorage.removeItem(CHALLENGE_DATA_KEY); // Clear corrupted data
          }
        }

        // 2. If no valid saved data, assign a new challenge
        console.log('No valid saved challenge found. Assigning a new one...');
        try {
          const assignResponse = await authenticatedFetch('/api/v1/challenges/assign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ team_id: teamId, my_id: id, members_ids: memberIds.filter((memberId) => memberId !== Number(id)) }),
          });

          if (!assignResponse.ok) {
            const errorData = await getJsonFromResponse(assignResponse);
            throw new Error(`Failed to assign challenge: ${errorData.detail}`);
          }

          const newChallengeData = await assignResponse.json();
          console.log('Successfully assigned new challenge:', newChallengeData);

          if (newChallengeData.my_assigned && newChallengeData.my_assigned.category && newChallengeData.my_assigned.assigned_challenge_id) {
            const dataToSave = {
              category: String(newChallengeData.my_assigned.category),
              assigned_challenge_id: newChallengeData.my_assigned.assigned_challenge_id,
              user_id: newChallengeData.my_assigned.user_id,
            };

            // Save to localStorage for future restoration
            localStorage.setItem(CHALLENGE_DATA_KEY, JSON.stringify(dataToSave));
            console.log('Saved new challenge to localStorage.');

            // Set state from the new challenge data
            const questionInfo = questions.find((q) => q.category === dataToSave.category);
            if (questionInfo) {
              const memberName = findMemberName(dataToSave.user_id);
              setQuestion([memberName, questionInfo.problem].join(' '));
              setChallengeId(dataToSave.assigned_challenge_id);
            }
          } else {
            throw new Error('Assigned challenge data is incomplete or malformed.');
          }
        } catch (error) {
          console.error('Error assigning challenge:', error);
          // General error handling: leave team, reset state, clear local storage
          if (teamId && teamId > 0) {
            try {
              console.log(`Attempting to leave team ${teamId} due to error...`);
              await authenticatedFetch(`/api/v1/teams/${teamId}/cancel`, { method: 'POST' });
              console.log(`Successfully left team ${teamId}.`);
            } catch (cancelError) {
              console.error(`Failed to leave team ${teamId}:`, cancelError);
            }
          }
          localStorage.removeItem(CHALLENGE_DATA_KEY);
          reset();

          setCurrentPage('page1');
        }
      } else if (question) {
        console.log('Question already exists, skipping initialization.');
      } else {
        console.log('Missing id or teamId, cannot initialize challenge. Resetting.');
        localStorage.removeItem(CHALLENGE_DATA_KEY);
        reset();

        setCurrentPage('page1');
      }
    };

    initializeChallenge();
  }, [id, teamId, question, memberIds, setQuestion, setChallengeId, reset, setCurrentPage]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const requestBody = {
      user_id: id,
      challenge_id: challengeId,
      submitted_answer: answer,
    };

    try {
      const response = await authenticatedFetch('/api/v1/challenges/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await getJsonFromResponse(response);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
      }

      const responseData = await response.json();
      console.log('Challenge submission successful:', responseData);
      setIsCorrect(responseData.is_correct);
      setCurrentPage('page4');
    } catch (error: unknown) {
      console.error('Error submitting challenge:', error);
      let errorMessage = '알 수 없는 오류가 발생했습니다.';
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      alert(`챌린지 제출에 실패했습니다: ${errorMessage}`);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md mt-8">
        <h2 className="text-xl font-semibold mb-4">질문:</h2>
        <p className="mb-4 p-2 border rounded bg-muted">{question || '질문이 입력되지 않았습니다.'}</p>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <Label htmlFor="answer">답변 입력</Label>
            <Textarea
              id="answer"
              placeholder="질문에 대한 답변을 입력해주세요."
              required
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          </div>
          <Button type="submit" className="w-full">제출 하기</Button>
        </form>
      </main>

      <nav className="flex justify-between mt-8">
        <Button onClick={() => setCurrentPage('page2')} className="bg-background text-emerald-900 rounded-full">
          &lt;
        </Button>
      </nav>
    </div>
  );
}
