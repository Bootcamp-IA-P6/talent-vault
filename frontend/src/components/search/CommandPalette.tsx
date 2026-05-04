import { useEffect, useState } from 'react';
import { Command } from 'cmdk';
import { useNavigate } from 'react-router-dom';
import { Hash, LayoutDashboard, Search, Users } from 'lucide-react';
import { useDebounced } from '@/hooks/useDebounced';
import { usePersons } from '@/hooks/usePersons';
import { Dialog } from '@/components/ui/Dialog';
import { fallback } from '@/lib/format';

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function CommandPalette({ open, onClose }: Props) {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const debounced = useDebounced(query, 200);
  const { data, isFetching } = usePersons({ search: debounced || undefined, limit: 8 });

  useEffect(() => {
    if (!open) setQuery('');
  }, [open]);

  const goTo = (path: string) => {
    onClose();
    navigate(path);
  };

  const persons = debounced ? data?.items ?? [] : [];

  return (
    <Dialog open={open} onClose={onClose} className="mt-24 max-w-xl overflow-hidden p-0">
      <Command label="Buscar" shouldFilter={false} className="flex flex-col">
        <div className="flex items-center gap-3 border-b border-border px-4 py-3">
          <Search className="h-4 w-4 text-muted" aria-hidden />
          <Command.Input
            value={query}
            onValueChange={setQuery}
            placeholder="Buscar por pasaporte, nombre, email…"
            className="flex-1 bg-transparent text-sm text-text outline-none placeholder:text-muted"
            autoFocus
          />
          {isFetching ? <span className="text-xs text-muted">…</span> : null}
        </div>
        <Command.List className="max-h-[60vh] overflow-y-auto p-2 scrollbar-thin">
          <Command.Empty className="px-3 py-8 text-center text-sm text-muted">
            {debounced ? 'Sin coincidencias.' : 'Empieza a escribir para buscar personas.'}
          </Command.Empty>

          {!debounced ? (
            <Command.Group heading="Navegación">
              <PaletteItem
                value="dashboard"
                icon={<LayoutDashboard className="h-4 w-4" />}
                onSelect={() => goTo('/app/dashboard')}
                label="Ir al Dashboard"
                hint="Métricas globales"
              />
              <PaletteItem
                value="personas"
                icon={<Users className="h-4 w-4" />}
                onSelect={() => goTo('/app/personas')}
                label="Ir a Personas"
                hint="Listado completo"
              />
            </Command.Group>
          ) : null}

          {persons.length > 0 ? (
            <Command.Group heading="Personas">
              {persons.map((p) => (
                <PaletteItem
                  key={p.passport}
                  value={`person-${p.passport}`}
                  icon={<Hash className="h-4 w-4" />}
                  onSelect={() => goTo(`/app/personas/${encodeURIComponent(p.passport)}`)}
                  label={fallback(p.fullname, p.passport)}
                  hint={[fallback(p.city), fallback(p.company), fallback(p.email)]
                    .filter((s) => s !== '—')
                    .join(' · ')}
                />
              ))}
            </Command.Group>
          ) : null}
        </Command.List>
        <div className="border-t border-border px-4 py-2 text-[11px] text-muted">
          ↑ ↓ navegar · ↵ abrir · esc cerrar
        </div>
      </Command>
    </Dialog>
  );
}

function PaletteItem({
  value,
  icon,
  onSelect,
  label,
  hint,
}: {
  value: string;
  icon: React.ReactNode;
  onSelect: () => void;
  label: string;
  hint?: string;
}) {
  return (
    <Command.Item
      value={value}
      onSelect={onSelect}
      className="flex cursor-pointer items-center gap-3 rounded-md px-3 py-2 text-sm aria-selected:bg-surface-2 aria-selected:text-text"
    >
      <span className="text-muted">{icon}</span>
      <span className="flex flex-1 flex-col">
        <span className="text-text">{label}</span>
        {hint ? <span className="text-xs text-muted">{hint}</span> : null}
      </span>
    </Command.Item>
  );
}
