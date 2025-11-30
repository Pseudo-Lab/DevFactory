'use client';

import Avatar from 'boring-avatars';
import Cookies from 'js-cookie';
import React, { useState, useEffect, useRef, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Modal from '@/components/Modal';
import { authenticatedFetch } from '../../lib/api';
import { useFormStore } from '../../store/formStore';

type View = 'loading' | 'create' | 'waiting';
type TeamMember = {
  user_id: number;
  is_ready: boolean;
  displayName: string;
};
type InputState = { id: string; displayName: string };

const WaitingView = ({ teamMembers, myId, teamId }: { teamMembers: TeamMember[], myId: number, teamId: number }) => {
  const router = useRouter();

  const handleLeaveTeam = async () => {
    try {
      await authenticatedFetch(`/api/v1/teams/${teamId}/cancel`, {
        method: 'POST',
      });
    } catch (error) {
      console.error('Error canceling team:', error);
      alert('팀을 나가는데 실패했습니다.');
    }
    router.back();
  };

  const me = teamMembers.find(m => m.user_id === myId);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-hidden bg-background-light dark:bg-background-dark p-4">
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-10"></div>
      <main className="relative z-20 w-full max-w-md mx-auto transform -translate-y-16">
        <div className="relative flex h-32 w-32 items-center justify-center mx-auto">
          <div className="absolute h-full w-full rounded-full bg-primary/20 animate-pulse"></div>
          <div className="absolute h-2/3 w-2/3 rounded-full bg-primary/30 animate-pulse [animation-delay:0.2s]"></div>
          <div className="absolute h-1/3 w-1/3 rounded-full bg-primary"></div>
        </div>
        <div className="text-center mt-2">
          <h1 className="text-[#111718] dark:text-white tracking-tight text-3xl font-bold leading-tight">팀원 기다리는 중...</h1>
          <p className="text-zinc-600 dark:text-zinc-400 text-base font-normal leading-normal mt-2 px-4">모든 팀원이 준비되면 퀴즈가 시작됩니다.</p>
        </div>
        <div className="mt-2 space-y-3">
          {teamMembers.map(member => (
            <div key={member.user_id} className="flex items-center gap-4 bg-white/80 dark:bg-white/10 rounded p-3 justify-between backdrop-blur-md">
              <div className="flex items-center gap-4">
                <Avatar size={40} name={String(member.user_id)} variant="beam" colors={['#25e2f4', '#f5f8f8', '#102122', '#FFC700', '#FF8C00']} />
                <p className="text-[#111718] dark:text-white text-base font-medium leading-normal flex-1 truncate">
                  {member.displayName} {member.user_id === myId ? '(나)' : ''}
                </p>
              </div>
              <div className="shrink-0">
                {member.is_ready ? (
                  <span className="material-symbols-outlined filled text-green-500">check_circle</span>
                ) : (
                  <div className="w-6 h-6 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin"></div>
                )}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 text-center">
          <button onClick={handleLeaveTeam} className="text-zinc-600 dark:text-zinc-400 text-sm font-medium leading-normal underline underline-offset-2">팀 나가기</button>
        </div>
      </main>
    </div>
  );
};

const CreateTeamView = ({
  inputs,
  handleInputChange,
  handleCreateTeam,
  fetchUserById
}: {
  inputs: InputState[],
  handleInputChange: (index: number, value: string) => void,
  handleCreateTeam: () => void,
  fetchUserById: (index: number, userId: string) => void
}) => {
  const [showModal, setShowModal] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const hasSeenModal = Cookies.get('doNotShowModalPage2');
    if (!hasSeenModal) {
      setShowModal(true);
    }
  }, []);

  const handleConfirm = () => setShowModal(false);
  const handleDoNotShowAgain = () => {
    Cookies.set('doNotShowModalPage2', 'true', { expires: 365 });
    setShowModal(false);
  };

  return (
    <div className="container mx-auto p-4">
      <Modal
        title="미션 소개"
        content={('1. 참가자들의 코드를 모으세요!<br />   코드는 위에 개인별 다른 코드가 있습니다.<br />2. 5명이 함께 문제 풀기에 도전하세요!<br />   (팁! 문제는 팀원들과 관련된 문제가 나옵니다.)<br />3. 성공 시 부스 방문해주세요.<br />   성공 선물을 드립니다.')}
        onConfirm={handleConfirm}
        onDoNotShowAgain={handleDoNotShowAgain}
        isOpen={showModal}
      />
      <div className="mt-8 space-y-4">
        {[...Array(5)].map((_, index) => (
          <div key={index}>
            <Label htmlFor={`team-id-${index}`}>팀원 {index + 1} {index === 0 && '(나)'}</Label>
            <Input
              id={`team-id-${index}`}
              type="text"
              placeholder={`팀원 ${index + 1}의 번호`}
              value={inputs[index].displayName}
              onChange={(e) => handleInputChange(index, e.target.value)}
              onBlur={() => {
                if (timeoutRef.current) clearTimeout(timeoutRef.current);
                fetchUserById(index, inputs[index].id);
              }}
              disabled={index === 0}
            />
          </div>
        ))}
        <Button onClick={handleCreateTeam} className="w-full">문제 풀기</Button>
      </div>
      <nav className="flex justify-between mt-8">
        <Button asChild className="rounded-full" variant={'outline'}>
          <Link href="/page1">&lt;</Link>
        </Button>
      </nav>
    </div>
  );
};

export default function Page2() {
  const { id: myId, teamId, setTeamId, setMemberIds } = useFormStore();
  const router = useRouter();

  const [view, setView] = useState<View>('loading');
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [inputs, setInputs] = useState<InputState[]>(() => Array(5).fill({ id: '', displayName: '' }));

  const hasCheckedTeamStatus = useRef(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const fetchUserDisplayName = useCallback(async (userId: number | string): Promise<string> => {
    try {
      const response = await authenticatedFetch(`/api/v1/users/${userId}`);
      if (!response.ok) return `User ${userId}`;
      const data = await response.json();
      return data.data || `User ${userId}`;
    } catch (error) {
      console.error(error);
      return `User ${userId}`;
    }
  }, []);

  const fetchUserById = useCallback(async (index: number, userId: string) => {
    if (!userId) return;
    if (index !== 0 && myId && Number(userId) === Number(myId)) {
      alert(`자기 자신(${userId})을 팀원으로 추가할 수 없습니다.`);
      const newInputs = [...inputs];
      newInputs[index] = { id: '', displayName: '' };
      setInputs(newInputs);
      return;
    }
    const displayName = await fetchUserDisplayName(userId);
    const newInputs = [...inputs];
    newInputs[index] = { id: userId, displayName: displayName };
    setInputs(newInputs);
  }, [myId, inputs, fetchUserDisplayName]);

  useEffect(() => {
    if (myId && inputs[0].id === '') {
      fetchUserById(0, String(myId));
    }
  }, [myId, fetchUserById, inputs]);

  useEffect(() => {
    if (!myId || hasCheckedTeamStatus.current) return;

    const checkUserTeam = async () => {
      hasCheckedTeamStatus.current = true;
      try {
        const response = await authenticatedFetch('/api/v1/teams/create');
        if (response.ok) {
          const teamData = await response.json();
          if (teamData && teamData.status === 'PENDING') {
            setTeamId(teamData.team_id);
            setView('waiting');
            return;
          }
        }
        setView('create');
      } catch (error) {
        console.error('Error checking user\'s team status:', error);
        setView('create');
      }
    };
    checkUserTeam();
  }, [myId, setTeamId]);

  useEffect(() => {
    if (view !== 'waiting' || !teamId) return;

    const interval = setInterval(async () => {
      try {
        const response = await authenticatedFetch(`/api/v1/teams/${teamId}/status`);
        if (!response.ok) throw new Error('Failed to fetch team status');
        const memberStatuses: { user_id: number, is_ready: boolean }[] = await response.json();
        const membersWithNames = await Promise.all(memberStatuses.map(async (member) => {
          const existingMember = teamMembers.find(m => m.user_id === member.user_id);
          const displayName = existingMember?.displayName ?? await fetchUserDisplayName(member.user_id);
          return { ...member, displayName };
        }));
        setTeamMembers(membersWithNames);
      } catch (error) {
        console.error('Error polling team status:', error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [view, teamId, fetchUserDisplayName, teamMembers]);

  useEffect(() => {
    if (view === 'waiting' && teamMembers.length > 0 && teamMembers.every(m => m.is_ready)) {
      setMemberIds(teamMembers.map(m => m.user_id));
      router.push('/page3');
    }
  }, [view, teamMembers, router, setMemberIds]);

  const handleInputChange = (index: number, value: string) => {
    const newInputs = [...inputs];
    newInputs[index] = { id: value, displayName: value };
    setInputs(newInputs);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      fetchUserById(index, value);
    }, 1500);
  };

  const handleCreateTeam = async () => {
    if (inputs.some(input => input.id === '')) {
      alert('모든 팀원 ID를 채워주세요.');
      return;
    }
    const memberIds = inputs.slice(1).map(input => Number(input.id));
    const requestBody = { my_id: myId, member_ids: memberIds };

    try {
      const response = await authenticatedFetch('/api/v1/teams/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Team creation failed');
      }
      const responseData = await response.json();
      setTeamId(responseData.team_id);
      setView('waiting');
    } catch (error) {
      console.error('Error creating team:', error);
      alert(`팀 생성에 실패했습니다: ${error}`);
    }
  };

  if (view === 'loading') {
    return (
      <div className="container mx-auto p-4 flex justify-center items-center h-screen">
        <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-primary"></div>
      </div>
    );
  }

  if (view === 'waiting') {
    return <WaitingView teamMembers={teamMembers} myId={myId as number} teamId={teamId as number} />;
  }

  return (
    <CreateTeamView
      inputs={inputs}
      handleInputChange={handleInputChange}
      handleCreateTeam={handleCreateTeam}
      fetchUserById={fetchUserById}
    />
  );
}
