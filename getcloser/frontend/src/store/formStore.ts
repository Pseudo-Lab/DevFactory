import { create } from 'zustand';

interface FormState {
  email: string;
  id: string;
  question: string;
  answer: string;
  setEmail: (email: string) => void;
  setId: (id: string) => void;
  setQuestion: (question: string) => void;
  setAnswer: (answer: string) => void;
}

export const useFormStore = create<FormState>((set) => ({
  email: '',
  id: '',
  question: '',
  answer: '',
  setEmail: (email) => set({ email }),
  setId: (id) => set({ id }),
  setQuestion: (question) => set({ question }),
  setAnswer: (answer) => set({ answer }),
}));
