'use client';

import Avatar from 'boring-avatars';
import Cookies from 'js-cookie';
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Modal from '@/components/Modal';
import { authenticatedFetch } from '../../lib/api';
import { useFormStore } from '../../store/formStore';
import { useNavigationStore } from '../../store/navigationStore';

type View = 'create' | 'waiting';
type TeamMember = {
  user_id: number;
  is_ready: boolean;
  displayName: string;
};
type InputState = { id: string; displayName: string };
const TEAM_SIZE = process.env.NEXT_PUBLIC_TEAM_SIZE
  ? parseInt(process.env.NEXT_PUBLIC_TEAM_SIZE, 10)
  : 5;

const WaitingView = ({ teamMembers, myId, teamId, setView }: { teamMembers: TeamMember[], myId: number, teamId: number, setView: (view: View) => void }) => {
  const handleLeaveTeam = async () => {
    try {
      await authenticatedFetch(`/api/v1/teams/${String(teamId)}/cancel`, {
        method: 'POST',
      });
    } catch (error) {
      console.error('Error canceling team:', error);
      alert('팀을 나가는데 실패했습니다.');
    }
    setView('create');
  };

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
          <h1 className="text-white tracking-tight text-3xl font-bold leading-tight">팀원 기다리는 중...</h1>
          <p className="text-gray-400 dark:text-zinc-400 text-base font-normal leading-normal mt-2 px-4">모든 팀원이 준비되면 퀴즈가 시작됩니다.</p>
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
          <button onClick={handleLeaveTeam} className="text-zinc-300 hover:text-white text-sm font-medium leading-normal underline underline-offset-2 transition-colors">팀 나가기</button>
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
  const { setCurrentPage } = useNavigationStore();

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
        content={('1. 참가자들의 코드를 모으세요!\n   코드는 위에 개인별 다른 코드가 있습니다.\n2. 5명이 함께 문제 풀기에 도전하세요!\n   (팁! 문제는 팀원들과 관련된 문제가 나옵니다.)\n3. 성공 시 부스 방문해주세요.\n   성공 선물을 드립니다.')}
        onConfirm={handleConfirm}
        onDoNotShowAgain={handleDoNotShowAgain}
        isOpen={showModal}
      />
      <div className="mt-8 space-y-4">
        {[...Array(TEAM_SIZE)].map((_, index) => (
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
        <Button onClick={() => setCurrentPage('page1')} className="rounded-full" variant={'outline'}>
          &lt;
        </Button>
      </nav>
    </div>
  );
};

export default function Page2() {
  const { id: myId, teamId, setTeamId, setMemberIds, progressStatus } = useFormStore();
  const { setCurrentPage } = useNavigationStore();

  const [view, setView] = useState<View>('create');
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [inputs, setInputs] = useState<InputState[]>(() => Array(TEAM_SIZE).fill({ id: '', displayName: '' }));

  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const fetchUserDisplayName = useCallback(async (userId: number | string): Promise<string> => {
    try {
      const response = await authenticatedFetch(`/api/v1/users/${userId}`);
      if (response.status === 404) {
        alert(`존재하지 않는 ID. ${userId}`);
        return '';
      }
      if (!response.ok) return '';
      const json = await response.json();
      return json.data || '';
    } catch (error) {
      console.error(error);
      return '';
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
    const initialize = async () => {
      if (progressStatus === 'NONE_TEAM') {
        setView('create');
      } else if (progressStatus === 'TEAM_WAITING') {
        try {
          const response = await authenticatedFetch('/api/v1/teams/me');
          if (!response.ok) {
            throw new Error('Failed to fetch team data');
          }
          const teamData = await response.json();
          if (teamData && teamData.members) {
            const initialTeamMembers: TeamMember[] = teamData.members.map((member: { id: number; name: string; }) => ({
              user_id: Number(member.id),
              displayName: member.name,
              is_ready: false,
            }));
            setTeamMembers(initialTeamMembers);
          }
          setView('waiting');
        } catch (error) {
          console.error('Error fetching team data for waiting view:', error);
          setView('create'); // Fallback to create view
        }
      }
    };

    initialize();
  }, [progressStatus]);

  useEffect(() => {
    if (myId && inputs[0].id === '') {
      fetchUserById(0, String(myId));
    }
  }, [myId, fetchUserById, inputs]);

  useEffect(() => {
    if (view !== 'waiting' || !teamId) return;

    const interval = setInterval(async () => {
      try {
        const response = await authenticatedFetch(`/api/v1/teams/${String(teamId)}/status`);

        if (!response.ok) {
          if (response.status === 404 || response.status === 403) {
            console.error('Team not found or user not authorized. Returning to create view.');
            setView('create');
            clearInterval(interval);
            return;
          }
          throw new Error(`Failed to fetch team status: ${response.status}`);
        }

        const memberStatuses: { team_id: number, status: string, members_ready: number[] } = await response.json();
        const readyMemberIds = new Set(memberStatuses.members_ready);

        // Per user request, if our ID is not in the list from the server, return to create view.
        if (myId && !readyMemberIds.has(Number(myId))) {
          console.log('User ID not in members_ready list. Returning to create view.', myId, readyMemberIds);
          setView('create');
          clearInterval(interval);
          return;
        }

        setTeamMembers(prevTeamMembers =>
          prevTeamMembers.map(member => ({
            ...member,
            is_ready: readyMemberIds.has(member.user_id),
          }))
        );
      } catch (error) {
        console.error('Error polling team status:', error);
        setView('create');
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [view, teamId, myId, setView]);

  useEffect(() => {
    if (view === 'waiting' && teamMembers.length > 0 && teamMembers.every(m => m.is_ready)) {
      setMemberIds(teamMembers.map(m => m.user_id));
      setCurrentPage('page3');
    }
  }, [view, teamMembers, setCurrentPage, setMemberIds]);

  const handleInputChange = (index: number, value: string) => {
    const newInputs = [...inputs];
    newInputs[index] = { id: value, displayName: value };
    setInputs(newInputs);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      fetchUserById(index, value);
    }, 10000);
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

      const initialTeamMembers = inputs.map(input => ({
        user_id: Number(input.id),
        displayName: input.displayName,
        is_ready: false,
      }));
      setTeamMembers(initialTeamMembers);

      setView('waiting');
    } catch (error) {
      console.error('Error creating team:', error);
      alert(`팀 생성에 실패했습니다: ${error}`);
    }
  };

  if (view === 'waiting') {
    return <WaitingView teamMembers={teamMembers} myId={myId as number} teamId={teamId as number} setView={setView} />;
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
