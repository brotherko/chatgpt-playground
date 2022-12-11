import axios from 'axios';
import useCookie from 'react-use-cookie';
import { nanoid } from 'nanoid';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';

export const useApi = (baseUrl: string) => {
  const queryClient = useQueryClient();
  const [sessionId, setSessionId] = useCookie('session_id');

  useEffect(() => {
    if (!sessionId) {
      reset()
    }
  }, [sessionId, setSessionId])

  useEffect(() => {
    queryClient.invalidateQueries({ queryKey: ['conversations'] });
  }, [queryClient, sessionId])


  const { data } = useQuery({
    queryKey: ['conversations', sessionId],
    queryFn: async () => {
      const { data } = await axios.get(
        `${baseUrl}/chat/${sessionId}`
      );
      return data;
    },
    refetchInterval: 30 * 1000
  });

  const { mutate, isLoading } = useMutation({
    mutationFn: (message: string) => {
      return axios.post(`${baseUrl}/chat/${sessionId}`, {
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
    setSessionId(nanoid())
  };

  return {
    data,

    reset,
    post: mutate,
    loading: isLoading,
  };
};