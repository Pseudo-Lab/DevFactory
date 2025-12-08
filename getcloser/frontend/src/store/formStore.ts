import { create } from 'zustand';

interface FormState {
  email: string;
  id: number;
  accessToken: string;
  question: string;
  answer: string;
  teamId: number;
  memberIds: number[];
  setEmail: (email: string) => void;
  setId: (id: number) => void;
  setAccessToken: (accessToken: string) => void;
  setQuestion: (question: string) => void;
  setAnswer: (answer: string) => void;
  setTeamId: (teamId: number) => void;
  setMemberIds: (memberIds: number[]) => void;
}

export const useFormStore = create<FormState>((set) => ({
  email: '',
  id: 0,
  accessToken: '',
  question: '',
  answer: '',
  teamId: 0,
  memberIds: [],
  setEmail: (email) => set({ email }),
  setId: (id) => set({ id }),
  setAccessToken: (accessToken) => set({ accessToken }),
  setQuestion: (question) => set({ question }),
  setAnswer: (answer) => set({ answer }),
  setTeamId: (teamId) => set({ teamId }),
  setMemberIds: (memberIds) => set({ memberIds }),
}));
