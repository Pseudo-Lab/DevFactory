import { useFormStore } from '../store/formStore';

export async function authenticatedFetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  const { accessToken } = useFormStore.getState();

  const headers = new Headers(init?.headers);

  if (accessToken) {
    headers.set('Authorization', `Bearer ${accessToken}`);
  }

  const newInit: RequestInit = {
    ...init,
    headers,
  };

  return fetch(input, newInit);
}
