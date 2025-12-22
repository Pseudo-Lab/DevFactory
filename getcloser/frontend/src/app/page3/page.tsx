'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import React, { useEffect } from 'react';
import { useFormStore } from '../../store/formStore';
import { authenticatedFetch } from '../../lib/api';

const questions = [
  { category: '1', keyword: '관심사', problem: '사용자의 관심사를 맞춰주세요. 예: 기술, 예술, 환경 등' },
  { category: '2', keyword: '취미', problem: '사용자의 취미를 맞춰주세요. 예: 등산, 독서, 요리 등' },
  { category: '3', keyword: 'MBTI', problem: '사용자의 MBTI 유형을 맞춰주세요. 예: INFP, ESTJ 등' },
];

export default function Page3() {
  const { question, answer, challengeId, setAnswer, id, teamId, memberIds, setQuestion, setChallengeId, setIsCorrect } = useFormStore(); // Destructure new state
  const router = useRouter();

  useEffect(() => {
    const assignChallenges = async () => {
      if (!teamId || !id || memberIds.length === 0) {
        console.warn('Missing teamId, my_id, or memberIds for challenge assignment.');
        return;
      }

      const requestBody = {
        team_id: teamId,
        my_id: id,
        members_ids: memberIds,
      };

      console.log('Assign Challenges Request Body:', requestBody);

      try {
        const response = await authenticatedFetch('/api/v1/challenges/assign', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || response.statusText}`);
        }

        const responseData = await response.json();
        console.log('Challenge assignment successful:', responseData);
        // Here you might want to update the question in the store based on responseData
        if (responseData.my_assigned && responseData.my_assigned.category) {
          const category = String(responseData.my_assigned.category);
          const questionData = questions.find((q) => q.category === category);
          if (questionData) {
            setQuestion(questionData.problem);
            setChallengeId(responseData.my_assigned.assigned_challenge_id);
          } else {
            console.warn(`No question found for category: ${category}`);
          }
        } else {
          console.warn('Category not found in challenge assignment response.');
        }
      } catch (error: unknown) {
        console.error('Error assigning challenges:', error);
        let errorMessage = '알 수 없는 오류가 발생했습니다.';
        if (error instanceof Error) {
          errorMessage = error.message;
        }
        alert(`챌린지 할당에 실패했습니다: ${errorMessage}`);
      }
    };

    assignChallenges();
  }, [id, teamId, memberIds, setQuestion, setChallengeId]); // Dependencies for useEffect

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const requestBody = {
      user_id: id,
      challenge_id: challengeId,
      submitted_answer: answer,
    };

    console.log(JSON.stringify(requestBody));

    try {
      const response = await authenticatedFetch('/api/v1/challenges/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || response.statusText}`);
      }

      const responseData = await response.json();
      console.log('Challenge submission successful:', responseData);
      setIsCorrect(responseData.is_correct);
      router.push('/page4');
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
        <Button asChild className="bg-background text-emerald-900 rounded-full">
          <Link href="/page2">&lt;</Link>
        </Button>
      </nav>
    </div>
  );
}
