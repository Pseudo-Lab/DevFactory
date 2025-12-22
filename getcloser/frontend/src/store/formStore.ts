import { create } from 'zustand';

interface FormState {
  email: string;
  id: number;
  accessToken: string;
  question: string;
  challengeId: number;
  answer: string;
  teamId: number;
  memberIds: number[];
  isCorrect: boolean | null;
  setEmail: (email: string) => void;
  setId: (id: number) => void;
  setAccessToken: (accessToken: string) => void;
  setQuestion: (question: string) => void;
  setChallengeId: (challengeId: number) => void;
  setAnswer: (answer: string) => void;
  setTeamId: (teamId: number) => void;
  setMemberIds: (memberIds: number[]) => void;
  setIsCorrect: (isCorrect: boolean) => void;
}

export const useFormStore = create<FormState>((set) => ({
  email: '',
  id: 0,
  accessToken: '',
  question: '',
  challengeId: 0,
  answer: '',
  teamId: 0,
  memberIds: [],
  isCorrect: null,
  setEmail: (email) => set({ email }),
  setId: (id) => set({ id }),
  setAccessToken: (accessToken) => set({ accessToken }),
  setQuestion: (question) => set({ question }),
  setChallengeId: (challengeId) => set({ challengeId }),
  setAnswer: (answer) => set({ answer }),
  setTeamId: (teamId) => set({ teamId }),
  setMemberIds: (memberIds) => set({ memberIds }),
  setIsCorrect: (isCorrect) => set({ isCorrect }),
}));
