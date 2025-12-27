import { create } from 'zustand';

type NavigationState = {
  currentPage: string;
  setCurrentPage: (page: string) => void;
};

export const useNavigationStore = create<NavigationState>((set) => ({
  currentPage: 'page1', // Default page
  setCurrentPage: (page) => set({ currentPage: page }),
}));
