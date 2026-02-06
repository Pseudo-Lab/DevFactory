'use client';

import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';
import { useFormStore } from '../../store/formStore';
import { authenticatedFetch } from '../../lib/api';
import { useNavigationStore } from '../../store/navigationStore';
import { questions } from '@/lib/constants';

interface TeamMember {
  id: number;
  user_id: number;
  name: string;
  email: string;
  github_url?: string;
  linkedin_url?: string;
}

interface QuestionInfo {
  category: string;
  keyword: string;
  problem: string;
  options: string[];
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

export default function Page3() {
  const { question, challengeId, setAnswer, id, teamId, memberIds, setQuestion, setChallengeId, setProgressStatus, reset } = useFormStore(); // Destructure new state
  const { setCurrentPage } = useNavigationStore();
  const [currentQuestionInfo, setCurrentQuestionInfo] = useState<QuestionInfo | null>(null);

  useEffect(() => {
    const initializeChallenge = async () => {
      // If a question is already loaded, do nothing.
      if (question) {
        // Still need to set the question info for rendering options
        if (!currentQuestionInfo) {
          const loadedQuestionCategory = questions.find(q => question.includes(q.problem));
          if (loadedQuestionCategory) {
            setCurrentQuestionInfo(loadedQuestionCategory as QuestionInfo); // Cast to QuestionInfo
          }
        }
        console.log('Question already exists, skipping initialization.');
        return;
      }

      // If we are on page3, we should have the necessary IDs.
      // If not, something is wrong, but providers.tsx should redirect.
      if (id && teamId) {
        console.log('No question found in store. Fetching/assigning challenge from server...');

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

        try {
          // This endpoint will assign a new challenge if one doesn't exist,
          // or it should ideally return the existing one.
          const assignResponse = await authenticatedFetch('/api/v1/challenges/assign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ team_id: teamId, my_id: id, members_ids: memberIds.filter((memberId) => memberId !== Number(id)) }),
          });

          if (!assignResponse.ok) {
            const errorData = await getJsonFromResponse(assignResponse);
            throw new Error(`Failed to assign/fetch challenge: ${errorData.detail}`);
          }

          const newChallengeData = await assignResponse.json();
          console.log('Successfully assigned/fetched challenge:', newChallengeData);

          if (newChallengeData.my_assigned && newChallengeData.my_assigned.category && newChallengeData.my_assigned.assigned_challenge_id) {
            const { user_id: userId, category, assigned_challenge_id } = newChallengeData.my_assigned;

            // Set state from the challenge data
            const questionInfo = questions.find((q) => q.category === String(category));
            if (questionInfo) {
              const memberName = findMemberName(userId);
              setQuestion([memberName, questionInfo.problem].join(' '));
              setChallengeId(assigned_challenge_id);
              setCurrentQuestionInfo(questionInfo as QuestionInfo); // Cast to QuestionInfo
            } else {
              throw new Error(`Could not find question for category: ${category}`);
            }
          } else {
            throw new Error('Assigned challenge data is incomplete or malformed.');
          }
        } catch (error) {
          console.error('Error in challenge initialization:', error);
          // Attempt to recover by going back to team formation
          reset();
          setCurrentPage('page2');
        }
      }
    };

    initializeChallenge();
    // Added challengeId to dependency array to react to changes if needed,
    // though the main trigger is the absence of `question`.
  }, [id, teamId, question, memberIds, setQuestion, setChallengeId, reset, setCurrentPage, challengeId, currentQuestionInfo]);

  const submitAnswer = async (submittedAnswer: string) => {
    const requestBody = {
      user_id: id,
      challenge_id: challengeId,
      submitted_answer: submittedAnswer,
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
      setProgressStatus(responseData.is_correct ? 'CHALLENGE_SUCCESS' : 'CHALLENGE_FAILED');
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

  const handleOptionClick = async (option: string) => {
    setAnswer(option); // Update the store
    await submitAnswer(option); // Submit the answer immediately
  };

  return (
    <div className="container mx-auto p-4">
      <main className={`mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md ${currentQuestionInfo?.category === '3' ? 'max-w-3xl' : 'max-w-md'}`}>
        <h2 className="text-xl font-semibold mb-4">질문:</h2>
        <p className="mb-4 p-2 border rounded bg-muted">{question || '질문이 입력되지 않았습니다.'}</p>

        {currentQuestionInfo && currentQuestionInfo.options && (
          <div className={`grid gap-2 mt-4 ${currentQuestionInfo.category === '3' ? 'grid-cols-4' : 'grid-cols-2'}`}>
            {currentQuestionInfo.options.map((option) => (
              <Button
                key={option}
                onClick={() => handleOptionClick(option)}
                variant="outline"
                className="justify-center text-center h-auto py-2 px-1 text-sm whitespace-normal break-words"
              >
                {option}
              </Button>
            ))}
          </div>
        )}
        <p className="text-red-400 text-xl font-bold mt-8">기회는 두번 뿐! (틀리면 팀 새로 구성)</p>
      </main>
    </div>
  );
}