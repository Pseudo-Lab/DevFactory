'use client';

import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';
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
  { category: '1', keyword: '관심사', problem: '님의 관심사를 맞춰주세요.', options: [ 'Agentic AI', 'AI Ethics', 'AI Security', 'Causal Inference', 'Computer Graphics', 'Computer Vision', 'Efficient AI', 'LLM/Multimodal', 'Physical AI', 'XAI' ] },
  { category: '2', keyword: '계절', problem: '님이 좋아하는 계절을 맞춰주세요.', options: ['봄', '여름', '가을', '겨울'] },
  { category: '3', keyword: 'MBTI', problem: '님의 MBTI 유형을 맞춰주세요.', options: ['INFP', 'ENFP', 'INFJ', 'ENFJ', 'INTJ', 'ENTJ', 'INTP', 'ENTP', 'ISFP', 'ESFP', 'ISTP', 'ESTP', 'ISFJ', 'ESFJ', 'ISTJ', 'ESTJ'] },
];

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
          if(loadedQuestionCategory) {
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
      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md mt-8">
        <h2 className="text-xl font-semibold mb-4">질문:</h2>
        <p className="mb-4 p-2 border rounded bg-muted">{question || '질문이 입력되지 않았습니다.'}</p>

        {currentQuestionInfo && currentQuestionInfo.options && (
          <div className="grid grid-cols-2 gap-4 mt-4">
            {currentQuestionInfo.options.map((option) => (
              <Button
                key={option}
                onClick={() => handleOptionClick(option)}
                variant="outline"
                className="justify-start text-left h-auto py-3"
              >
                {option}
              </Button>
            ))}
          </div>
        )}
      </main>

      <nav className="flex justify-between mt-8">
        <Button onClick={() => setCurrentPage('page2')} className="bg-background text-emerald-900 rounded-full">
          &lt;
        </Button>
      </nav>
    </div>
  );
}