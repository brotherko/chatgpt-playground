import axios from 'axios';
import useCookie from 'react-use-cookie';
import { nanoid } from 'nanoid';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';

export const useApi = (baseUrl: string) => {
  const queryClient = useQueryClient();
  const [sessionId, setSessionId] = useCookie('session_id', nanoid());

  useEffect(() => {
    queryClient.invalidateQueries({ queryKey: ['conversations'] });
  }, [queryClient, sessionId])


  const { data } = useQuery({
    queryKey: ['conversations', sessionId],
    queryFn: async () => {
      const { data } = await axios.get(
        `${baseUrl}/api/chat/${sessionId}`
      );
      return data;
    },
  });

  const { mutate, isLoading } = useMutation({
    mutationFn: (message: string) => {
      return axios.post(`${baseUrl}/api/chat/${sessionId}`, {
        message,
      });
    },
    onMutate: async (message) => {
      await queryClient.cancelQueries({ queryKey: ['conversations', sessionId] });
      queryClient.setQueryData(['conversations', sessionId], (old: any) => {
        return [
          ...(old || []),
          {
            sender: 'human',
            message,
          },
        ];
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
  });


  const reset = () => {
    if (isLoading) {
      console.error('Can not reset chat while interacting with server')
    }
    setSessionId(nanoid())
  };

  return {
    data,

    reset,
    post: mutate,
    loading: isLoading,
  };
};