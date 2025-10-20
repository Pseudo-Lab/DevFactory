'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useFormStore } from '../../store/formStore';
import { Rows } from 'lucide-react';

export default function Page1() {
  const { email, setEmail } = useFormStore();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form Submitted:', { email });
    // Here you would typically send this data to an API
    alert('정보가 제출되었습니다! 콘솔을 확인해주세요.');
  };

  return (
    <div className="container mx-auto p-4 min-h-screen flex items-center justify-center">
      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md">
        <h1 className="text-5xl font-bold">친해지길바라</h1>
        <Image src="/logo.png" alt="Fail" width={52} height={58} style={{marginTop: 36, marginBottom: 36}} className="mx-auto block" />
        <div className="items-center text-center" style={{marginBottom: 36}}>
          <p className="text-md mt-1">Pseudo Lab</p>
          <p className="text-md">2nd Grand Gathering</p>
          <p className="text-md">2025. 11. 15</p>
        </div>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className='items-center text-center'>
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
          <Link href="/page2"><Button type="submit" className="w-full">정보 제출</Button></Link>
          
        </form>
      </main>
    </div>
  );
}
