'use client';

import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useFormStore } from '../../store/formStore';
import SplitText from './SplitText';

export default function Page1() {
  const { email, setEmail, setId, setAccessToken, setTeamId, setChallengeId, setProgressStatus } = useFormStore();

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
        if (authResponse.status === 404) {
          alert('등록되지 않은 이메일 입니다.');
          return;
        }
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
      if (userMeResult.team_id) {
        setTeamId(userMeResult.team_id);
      }
      if (userMeResult.challenge_id) {
        setChallengeId(userMeResult.challenge_id);
      }
      if (userMeResult.progress_status) {
        setProgressStatus(userMeResult.progress_status);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('정보 제출에 실패했습니다.');
    }
  };

  return (
    <div className="container mx-auto p-4 min-h-screen flex items-center justify-center">
      <main className="max-w-md mx-auto bg-card text-card-foreground p-6 rounded-lg shadow-md">
        <div className="flex justify-center">
          <SplitText
            text='친해지길바라'
            className='text-2xl font-semibold text-center'
            delay={100}
            duration={0.6}
            ease='power3.out'
            splitType='chars'
            from={{ opacity: 0, y: 40 }}
            to={{ opacity: 1, y: 0 }}
            threshold={0.1}
            rootMargin='-100px'
            textAlign='center'
          />
        </div>
        <Image src="/logo.png" alt="Fail" width={52} height={58} style={{ marginTop: 36, marginBottom: 36 }} className="mx-auto block" />
        <div className="items-center text-center" style={{ marginBottom: 36 }}>
          <p className="text-md mt-1">Pseudo Lab</p>
          <p className="text-md">2nd Grand Gathering</p>
          <p className="text-md">2026. 1. 10</p>
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
