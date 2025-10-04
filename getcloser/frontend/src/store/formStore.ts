import { create } from 'zustand';

interface FormState {
  email: string;
  question: string;
  answer: string;
  setEmail: (email: string) => void;
  setQuestion: (question: string) => void;
  setAnswer: (answer: string) => void;
}

export const useFormStore = create<FormState>((set) => ({
  email: '',
  question: '',
  answer: '',
  setEmail: (email) => set({ email }),
  setQuestion: (question) => set({ question }),
  setAnswer: (answer) => set({ answer }),
}));
