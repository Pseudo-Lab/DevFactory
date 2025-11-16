import { create } from 'zustand';

interface FormState {
  email: string;
  id: string;
  accessToken: string;
  question: string;
  answer: string;
  teamId: string;
  memberIds: string[];
  setEmail: (email: string) => void;
  setId: (id: string) => void;
  setAccessToken: (accessToken: string) => void;
  setQuestion: (question: string) => void;
  setAnswer: (answer: string) => void;
  setTeamId: (teamId: string) => void;
  setMemberIds: (memberIds: string[]) => void;
}

export const useFormStore = create<FormState>((set) => ({
  email: '',
  id: '',
  accessToken: '',
  question: '',
  answer: '',
  teamId: '',
  memberIds: [],
  setEmail: (email) => set({ email }),
  setId: (id) => set({ id }),
  setAccessToken: (accessToken) => set({ accessToken }),
  setQuestion: (question) => set({ question }),
  setAnswer: (answer) => set({ answer }),
  setTeamId: (teamId) => set({ teamId }),
  setMemberIds: (memberIds) => set({ memberIds }),
}));
