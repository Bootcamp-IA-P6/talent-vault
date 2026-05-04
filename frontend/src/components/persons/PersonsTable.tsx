import { useNavigate } from 'react-router-dom';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/Table';
import { Badge } from '@/components/ui/Badge';
import { Skeleton } from '@/components/ui/Skeleton';
import { fallback } from '@/lib/format';
import type { Person } from '@/lib/types';

type Props = {
  rows: Person[];
  loading?: boolean;
};

export default function PersonsTable({ rows, loading }: Props) {
  const navigate = useNavigate();

  if (loading && rows.length === 0) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full" />
        ))}
      </div>
    );
  }

  if (!loading && rows.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-border bg-surface px-6 py-16 text-center text-sm text-muted">
        Sin resultados con esos filtros.
      </div>
    );
  }

  return (
    <Table>
      <THead>
        <TR className="hover:bg-surface-2">
          <TH>Pasaporte</TH>
          <TH>Nombre completo</TH>
          <TH>Ciudad</TH>
          <TH>Empresa</TH>
          <TH>Puesto</TH>
          <TH>Email</TH>
          <TH>IPv4</TH>
        </TR>
      </THead>
      <TBody>
        {rows.map((p) => (
          <TR
            key={p.passport}
            onClick={() => navigate(`/app/personas/${encodeURIComponent(p.passport)}`)}
            className="cursor-pointer"
          >
            <TD className="font-mono text-xs text-accent">{p.passport}</TD>
            <TD className="font-medium">{fallback(p.fullname)}</TD>
            <TD>{fallback(p.city)}</TD>
            <TD>{fallback(p.company)}</TD>
            <TD>{fallback(p.job)}</TD>
            <TD className="text-muted">{fallback(p.email)}</TD>
            <TD>
              {p.IPv4 ? (
                <Badge variant="outline" className="font-mono">
                  {p.IPv4}
                </Badge>
              ) : (
                '—'
              )}
            </TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
