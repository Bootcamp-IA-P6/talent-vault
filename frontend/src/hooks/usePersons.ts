import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { listPersons } from '@/lib/api';
import type { PersonsQuery } from '@/lib/types';

export function usePersons(params: PersonsQuery) {
  return useQuery({
    queryKey: ['persons', params],
    queryFn: ({ signal }) => listPersons(params, signal),
    placeholderData: keepPreviousData,
  });
}
