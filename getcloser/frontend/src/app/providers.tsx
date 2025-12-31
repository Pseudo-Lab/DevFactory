'use client';

import React, { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useNavigationStore } from '../store/navigationStore';
import { authenticatedFetch } from '../lib/api';
import { useFormStore } from '../store/formStore';

const queryClient = new QueryClient();

function StoreInitializer() {
  useEffect(() => {
    const { setProgressStatus, setTeamId, setChallengeId, setId } = useFormStore.getState();

    const fetchUserStatus = async () => {
      try {
        const userMeResponse = await authenticatedFetch('/api/v1/users/me');
        if (!userMeResponse.ok) {
          throw new Error(`HTTP error! status: ${userMeResponse.status}`);
        }
        const userMeResult = await userMeResponse.json();
        console.log('User Me API Response from provider:', userMeResult);

        if (userMeResult.sub) setId(userMeResult.sub);
        if (userMeResult.team_id) setTeamId(userMeResult.team_id);
        if (userMeResult.challenge_id) setChallengeId(userMeResult.challenge_id);
        if (userMeResult.progress_status) setProgressStatus(userMeResult.progress_status);

      } catch (error) {
        console.error('Error fetching user status:', error);
        // Could handle token invalidation here
      }
    };

    // Function to run on initial load
    const initialize = () => {
      if (typeof window !== 'undefined') {
        const { accessToken, progressStatus } = useFormStore.getState();
        const { currentPage, setCurrentPage } = useNavigationStore.getState();
        if (accessToken) {
          if (progressStatus) {
            switch (progressStatus) {
              case 'NONE_TEAM':
              case 'TEAM_WAITING':
                if (currentPage !== 'page2') setCurrentPage('page2');
                break;
              case 'CHALLENGE_ASSIGNED':
                if (currentPage !== 'page3') setCurrentPage('page3');
                break;
              case 'CHALLENGE_SUCCESS':
              case 'CHALLENGE_FAILED':
              case 'REDEEMED':
                if (currentPage !== 'page4') setCurrentPage('page4');
                break;
              default:
                if (currentPage === '' || currentPage === 'page1') {
                  // Potentially stale or unrecognized status, refresh
                  fetchUserStatus();
                }
                break;
            }
          } else {
            // No progressStatus, fetch it
            fetchUserStatus();
          }
        } else {
          // If no accessToken and not already on 'page1', redirect to 'page1'
          if (currentPage !== 'page1') {
            setCurrentPage('page1');
          }
        }
      }
    };

    initialize();

    // Subscribe to formStore for changes
    const unsubscribeFormStore = useFormStore.subscribe(
      (state, prevState) => {
        if (typeof window !== 'undefined') {
          const { accessToken, progressStatus } = state;
          const { setCurrentPage, currentPage } = useNavigationStore.getState();

          // Handle login/logout
          if (!accessToken && prevState.accessToken) {
            // User just logged out
            if (currentPage !== 'page1') {
              setCurrentPage('page1');
            }
          }

          // Handle progressStatus changes
          if (progressStatus && progressStatus !== prevState.progressStatus) {
            switch (progressStatus) {
              case 'NONE_TEAM':
              case 'TEAM_WAITING':
                setCurrentPage('page2');
                break;
              case 'CHALLENGE_ASSIGNED':
                setCurrentPage('page3');
                break;
              case 'CHALLENGE_SUCCESS':
              case 'CHALLENGE_FAILED':
              case 'REDEEMED':
                setCurrentPage('page4');
                break;
            }
          }
        }
      }
    );

    return () => {
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
