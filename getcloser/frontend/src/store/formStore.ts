import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

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
  progressStatus: string;
  setEmail: (email: string) => void;
  setId: (id: number) => void;
  setAccessToken: (accessToken: string) => void;
  setQuestion: (question: string) => void;
  setChallengeId: (challengeId: number) => void;
  setAnswer: (answer: string) => void;
  setTeamId: (teamId: number) => void;
  setMemberIds: (memberIds: number[]) => void;
  setIsCorrect: (isCorrect: boolean) => void;
  setProgressStatus: (progressStatus: string) => void;
  reset: () => void;
}

const initialState = {
  email: '',
  id: 0,
  accessToken: '',
  question: '',
  challengeId: 0,
  answer: '',
  teamId: 0,
  memberIds: [],
  isCorrect: null,
  progressStatus: '',
};

export const useFormStore = create<FormState>()(
  persist(
    (set, get) => ({
      ...initialState,
      setEmail: (email) => set({ email }),
      setId: (id) => set({ id }),
      setAccessToken: (accessToken) => set({ accessToken }),
      setQuestion: (question) => set({ question }),
      setChallengeId: (challengeId) => set({ challengeId }),
      setAnswer: (answer) => set({ answer }),
      setTeamId: (teamId) => set({ teamId }),
      setMemberIds: (memberIds) => set({ memberIds }),
      setIsCorrect: (isCorrect) =>
        set({
          isCorrect,
          progressStatus: isCorrect ? 'CHALLENGE_SUCCESS' : 'CHALLENGE_FAILED',
        }),
      setProgressStatus: (progressStatus) => set({ progressStatus }),
      reset: () => {
        const { email, id, accessToken, teamId, memberIds } = get();
        set({
          ...initialState,
          email,
          id,
          accessToken,
          teamId,
          memberIds,
        });
      },
    }),
    {
      name: 'form-storage', // name of the item in the storage (must be unique)
      storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
      partialize: (state) => ({ email: state.email, id: state.id, accessToken: state.accessToken, teamId: state.teamId, memberIds: state.memberIds }),
    },
  ),
);
