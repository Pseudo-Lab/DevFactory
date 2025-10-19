'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useFormStore } from '../../store/formStore';

export default function Page1() {
  const { email, question, answer, setEmail, setQuestion, setAnswer } = useFormStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form Submitted:', { email, question, answer });
    // Here you would typically send this data to an API
    alert('정보가 제출되었습니다! 콘솔을 확인해주세요.');
  };

  return (
    <div className="container mx-auto p-4">
      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">참가 정보 입력</h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <Label htmlFor="email">이메일 주소</Label>
            <Input
              id="email"
              type="email"
              placeholder="your@example.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="question">나만의 질문</Label>
            <Textarea
              id="question"
              placeholder="행사 미션에서 사용 할 나만의 질문을 입력해주세요."
              required
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="answer">답변</Label>
            <Textarea
              id="answer"
              placeholder="질문에 대한 답변을 입력해주세요."
              required
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />
          </div>
          <Link href="/page2"><Button type="submit" className="w-full">정보 제출</Button></Link>
          
        </form>
      </main>
    </div>
  );
}
