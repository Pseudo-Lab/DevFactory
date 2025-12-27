'use client';

import React, { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useNavigationStore } from '../store/navigationStore';
import { useFormStore } from '../store/formStore';

const queryClient = new QueryClient();

function StoreInitializer() {
  useEffect(() => {
    // Function to run on initial load
    const initialize = () => {
      if (typeof window !== 'undefined') {
        const savedPage = localStorage.getItem('lastPage');
        if (savedPage) {
          useNavigationStore.getState().setCurrentPage(savedPage);
        }

        const accessToken = useFormStore.getState().accessToken;
        const currentPage = useNavigationStore.getState().currentPage;

        // If no accessToken and not already on 'page1', redirect to 'page1'
        if (!accessToken && currentPage !== 'page1') {
          useNavigationStore.getState().setCurrentPage('page1');
          localStorage.removeItem('lastPage'); // Clear lastPage on auth redirect
        }
      }
    };

    initialize();

    // Subscribe to store changes and save to localStorage
    const unsubscribe = useNavigationStore.subscribe(
      (state) => {
        if (typeof window !== 'undefined') {
          localStorage.setItem('lastPage', state.currentPage);
        }
      }
    );

    // Also subscribe to formStore for accessToken changes
    const unsubscribeFormStore = useFormStore.subscribe(
      (state, prevState) => {
        if (typeof window !== 'undefined') {
          const accessToken = state.accessToken;
          const currentPage = useNavigationStore.getState().currentPage;
          // If the access token is cleared and we are not on page1, navigate to page1
          if (!accessToken && prevState.accessToken && currentPage !== 'page1') {
            useNavigationStore.getState().setCurrentPage('page1');
            localStorage.removeItem('lastPage'); // Clear lastPage on auth redirect
          }
        }
      }
    );

    return () => {
      unsubscribe();
      unsubscribeFormStore();
    };
  }, []);

  return null; // This component does not render anything
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <StoreInitializer />
      {children}
    </QueryClientProvider>
  );
}
