'use client';

import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useFormStore } from '../../store/formStore';

import { useRouter } from 'next/navigation';

export default function Page1() {
  const { email, setEmail, setId, setAccessToken } = useFormStore();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form Submitted:', { email });

    try {
      const authResponse = await fetch('/api/v1/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!authResponse.ok) {
        throw new Error(`HTTP error! status: ${authResponse.status}`);
      }

      const authResult = await authResponse.json();
      const newAccessToken = authResult.accessToken;

      if (!newAccessToken) {
        throw new Error('Access token not received from auth API.');
      }
      setAccessToken(newAccessToken); // Store the new access token

      const userMeResponse = await fetch('/api/v1/users/me', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${newAccessToken}`, // Use the new access token
        },
      });

      if (!userMeResponse.ok) {
        throw new Error(`HTTP error! status: ${userMeResponse.status}`);
      }

      const userMeResult = await userMeResponse.json();
      console.log('User Me API Response:', userMeResult);

      if (userMeResult.sub) {
        setId(userMeResult.sub);
      }
      alert('정보가 제출되었습니다!');
      router.push('/page2');
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('정보 제출에 실패했습니다.');
    }
  };

  return (
    <div className="container mx-auto p-4 min-h-screen flex items-center justify-center">
      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md">
        <h1 className="text-5xl font-bold">친해지길바라</h1>
        <Image src="/logo.png" alt="Fail" width={52} height={58} style={{ marginTop: 36, marginBottom: 36 }} className="mx-auto block" />
        <div className="items-center text-center" style={{ marginBottom: 36 }}>
          <p className="text-md mt-1">Pseudo Lab</p>
          <p className="text-md">2nd Grand Gathering</p>
          <p className="text-md">2025. 12. 20</p>
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
          <Button type="submit" className="w-full">정보 제출</Button>
          
        </form>
      </main>
    </div>
  );
}
