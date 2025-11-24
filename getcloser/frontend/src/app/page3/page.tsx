'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import React, { useEffect } from 'react';
import { useFormStore } from '../../store/formStore';
import { authenticatedFetch } from '../../lib/api';

export default function Page3() {
  const { question, answer, setAnswer, id, teamId, memberIds } = useFormStore(); // Destructure new state
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
        // setQuestion(responseData.challenge_question);
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
  }, [id, teamId, memberIds]); // Dependencies for useEffect

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Question:', question, 'Answer:', answer);
    // Here you would typically send this data to an API
    router.push('/page4');
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
