import { useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { usePersons } from '@/hooks/usePersons';
import { useDebounced } from '@/hooks/useDebounced';
import PersonsFilters from '@/components/persons/PersonsFilters';
import PersonsTable from '@/components/persons/PersonsTable';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { formatNumber } from '@/lib/format';

export default function PersonsPage() {
  const [search, setSearch] = useState('');
  const [city, setCity] = useState('');
  const [company, setCompany] = useState('');
  const [limit, setLimit] = useState(50);
  const [offset, setOffset] = useState(0);

  const debouncedSearch = useDebounced(search, 300);
  const debouncedCity = useDebounced(city, 300);
  const debouncedCompany = useDebounced(company, 300);

  const params = useMemo(
    () => ({
      search: debouncedSearch || undefined,
      city: debouncedCity || undefined,
      company: debouncedCompany || undefined,
      limit,
      offset,
    }),
    [debouncedSearch, debouncedCity, debouncedCompany, limit, offset],
  );

  const { data, isLoading, isFetching } = usePersons(params);

  const total = data?.total ?? 0;
  const showingFrom = total === 0 ? 0 : offset + 1;
  const showingTo = Math.min(offset + limit, total);

  const update = (next: { search?: string; city?: string; company?: string }) => {
    if (next.search !== undefined) setSearch(next.search);
    if (next.city !== undefined) setCity(next.city);
    if (next.company !== undefined) setCompany(next.company);
    setOffset(0);
  };

  return (
    <div className="flex flex-col gap-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">Personas</h1>
        <p className="text-sm text-muted">Listado completo con filtros y paginación.</p>
      </header>

      <div className="flex flex-col gap-6 lg:flex-row">
        <PersonsFilters
          search={search}
          city={city}
          company={company}
          onChange={update}
          onClear={() => {
            setSearch('');
            setCity('');
            setCompany('');
            setOffset(0);
          }}
        />

        <div className="flex flex-1 flex-col gap-4">
          <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-muted">
            <span>
              Mostrando <span className="text-text">{formatNumber(showingFrom)}</span>–
              <span className="text-text">{formatNumber(showingTo)}</span> de{' '}
              <span className="text-text">{formatNumber(total)}</span>
              {isFetching ? <span className="ml-2 animate-pulse text-accent">·</span> : null}
            </span>
            <label className="flex items-center gap-2 text-xs">
              Por página
              <Select
                value={limit}
                onChange={(e) => {
                  setLimit(Number(e.target.value));
                  setOffset(0);
                }}
                className="h-8 w-20"
              >
                {[25, 50, 100, 200].map((n) => (
                  <option key={n} value={n}>
                    {n}
                  </option>
                ))}
              </Select>
            </label>
          </div>

          <PersonsTable rows={data?.items ?? []} loading={isLoading} />

          <div className="flex items-center justify-end gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={offset === 0}
              onClick={() => setOffset(Math.max(0, offset - limit))}
            >
              <ChevronLeft className="h-4 w-4" aria-hidden /> Anterior
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={offset + limit >= total}
              onClick={() => setOffset(offset + limit)}
            >
              Siguiente <ChevronRight className="h-4 w-4" aria-hidden />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
