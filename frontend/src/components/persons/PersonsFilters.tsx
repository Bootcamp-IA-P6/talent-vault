import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';

type Props = {
  search: string;
  city: string;
  company: string;
  onChange: (next: { search?: string; city?: string; company?: string }) => void;
  onClear: () => void;
};

export default function PersonsFilters({ search, city, company, onChange, onClear }: Props) {
  const hasFilters = Boolean(search || city || company);
  return (
    <aside className="flex w-full flex-col gap-4 rounded-lg border border-border bg-surface p-5 lg:max-w-xs">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">Filtros</h2>
        {hasFilters ? (
          <Button variant="ghost" size="sm" onClick={onClear} className="gap-1">
            <X className="h-3 w-3" aria-hidden /> Limpiar
          </Button>
        ) : null}
      </div>

      <label className="flex flex-col gap-1.5 text-xs text-muted">
        Búsqueda
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" aria-hidden />
          <Input
            placeholder="Pasaporte, nombre, email…"
            value={search}
            onChange={(e) => onChange({ search: e.target.value })}
            className="pl-9"
          />
        </div>
      </label>

      <label className="flex flex-col gap-1.5 text-xs text-muted">
        Ciudad (exacta)
        <Input
          placeholder="ej. Madrid"
          value={city}
          onChange={(e) => onChange({ city: e.target.value })}
        />
      </label>

      <label className="flex flex-col gap-1.5 text-xs text-muted">
        Empresa (exacta)
        <Input
          placeholder="ej. Acme S.A."
          value={company}
          onChange={(e) => onChange({ company: e.target.value })}
        />
      </label>
    </aside>
  );
}
