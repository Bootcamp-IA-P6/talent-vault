import { ArrowLeft } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { usePerson } from '@/hooks/usePerson';
import PersonDetailTabs from '@/components/persons/PersonDetailTabs';
import { Badge } from '@/components/ui/Badge';
import { Card, CardBody } from '@/components/ui/Card';
import { Skeleton } from '@/components/ui/Skeleton';
import { fallback } from '@/lib/format';

export default function PersonDetailPage() {
  const { passport } = useParams<{ passport: string }>();
  const { data, isLoading, isError, error } = usePerson(passport);

  return (
    <div className="flex flex-col gap-6">
      <Link
        to="/app/personas"
        className="inline-flex w-fit items-center gap-2 text-sm text-muted transition hover:text-text"
      >
        <ArrowLeft className="h-4 w-4" aria-hidden /> Volver al listado
      </Link>

      <Card>
        <CardBody>
          {isLoading ? (
            <div className="flex flex-col gap-3">
              <Skeleton className="h-6 w-48" />
              <Skeleton className="h-4 w-72" />
            </div>
          ) : isError ? (
            <div className="text-sm text-danger">
              {String((error as Error)?.message ?? 'Persona no encontrada')}
            </div>
          ) : data ? (
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-wider text-muted">Persona</p>
                <h1 className="text-2xl font-semibold tracking-tight">
                  {fallback(data.fullname, data.passport)}
                </h1>
                <p className="mt-1 text-sm text-muted">
                  {fallback(data.job)} · {fallback(data.company)} · {fallback(data.city)}
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge variant="accent" className="font-mono">
                  {data.passport}
                </Badge>
                {data.sex ? <Badge>{data.sex}</Badge> : null}
                {data.IPv4 ? (
                  <Badge variant="outline" className="font-mono">
                    {data.IPv4}
                  </Badge>
                ) : null}
              </div>
            </div>
          ) : null}
        </CardBody>
      </Card>

      {data ? <PersonDetailTabs person={data} /> : null}
    </div>
  );
}
