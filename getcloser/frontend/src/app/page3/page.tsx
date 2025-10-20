'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useFormStore } from '../../store/formStore';
import React from 'react';

export default function Page3() {
  const { question, answer, setAnswer } = useFormStore();
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Question:', question, 'Answer:', answer);
    // Here you would typically send this data to an API
    router.push('/page4');
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Page 3</h1>
      <p>This is the third page.</p>

      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md mt-8">
        <h2 className="text-xl font-semibold mb-4">Page 1에서 입력된 질문:</h2>
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
        <Button asChild>
          <Link href="/page2">이전 페이지 (Page 2)</Link>
        </Button>
        {/* Removed '다음 페이지 (Page 4)' button */}
      </nav>
    </div>
  );
}
