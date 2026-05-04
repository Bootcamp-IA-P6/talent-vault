import { useQuery } from '@tanstack/react-query';
import { getPerson } from '@/lib/api';

export function usePerson(passport: string | undefined) {
  return useQuery({
    queryKey: ['person', passport],
    queryFn: ({ signal }) => getPerson(passport!, signal),
    enabled: Boolean(passport),
  });
}
