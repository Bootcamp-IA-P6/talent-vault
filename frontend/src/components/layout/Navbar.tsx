import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  Activity,
  BookOpen,
  Database,
  LayoutDashboard,
  Mail,
  Presentation,
  Search,
  Sparkles,
  Users,
} from 'lucide-react';
import logoUrl from '@/assets/logo.png';
import { cn } from '@/lib/cn';
import { Button } from '@/components/ui/Button';
import { Dialog } from '@/components/ui/Dialog';

type Props = {
  onOpenSearch: () => void;
};

const tabs = [
  { to: '/app/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/app/personas', label: 'Personas', icon: Users },
];

const externalTools = [
  {
    href: 'http://localhost:8081',
    label: 'Mongo Express',
    icon: Database,
  },
  {
    href: 'http://localhost:9090/graph?g0.expr=sum%20by%20(type)%20(rate(talent_vault_kafka_messages_consumed_total%5B1m%5D))&g0.tab=0&g0.display_mode=lines&g0.show_exemplars=0&g0.range_input=5m&g1.expr=increase(talent_vault_realtime_persons_assembled_total%5B1m%5D)&g1.tab=0&g1.display_mode=lines&g1.show_exemplars=0&g1.range_input=5m&g2.expr=histogram_quantile(0.9%2C%20rate(talent_vault_pipeline_tick_duration_seconds_bucket%5B5m%5D))&g2.tab=0&g2.display_mode=lines&g2.show_exemplars=0&g2.range_input=5m',
    label: 'Prometheus',
    icon: Activity,
  },
  {
    href: 'http://localhost:8000/docs',
    label: 'API docs',
    icon: BookOpen,
  },
];

export default function Navbar({ onOpenSearch }: Props) {
  const navigate = useNavigate();
  const [contactOpen, setContactOpen] = useState(false);
  const isMac =
    typeof navigator !== 'undefined' && /Mac|iPhone|iPad|iPod/.test(navigator.platform);
  const cmdKey = isMac ? '⌘' : 'Ctrl';

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-surface/80 backdrop-blur">
      <div className="flex h-16 items-center gap-6 px-6">
        <NavLink to="/" className="flex items-center gap-2.5" title="Volver al inicio">
          <img src={logoUrl} alt="" aria-hidden className="h-9 w-9 rounded-md" />
          <span className="text-sm font-semibold tracking-tight text-text">
            Talent<span className="text-accent">Vault</span>
          </span>
        </NavLink>

        <nav className="flex items-center gap-1">
          {tabs.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                cn(
                  'inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-surface-2 text-text'
                    : 'text-muted hover:bg-surface-2/60 hover:text-text',
                )
              }
            >
              <Icon className="h-4 w-4" aria-hidden />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-3">
          <button
            type="button"
            onClick={onOpenSearch}
            className="hidden h-9 items-center gap-3 rounded-md border border-border bg-surface-2 px-3 text-sm text-muted transition hover:border-accent hover:text-text md:inline-flex"
          >
            <Search className="h-4 w-4" aria-hidden />
            <span>Buscar personas…</span>
            <kbd className="ml-2 rounded border border-border bg-surface px-1.5 py-0.5 font-mono text-[10px] text-muted">
              {cmdKey} K
            </kbd>
          </button>

          <div className="hidden items-center gap-1 border-l border-border pl-3 md:flex">
            {externalTools.map(({ href, label, icon: Icon }) => (
              <a
                key={href}
                href={href}
                target="_blank"
                rel="noreferrer noopener"
                title={`${label} (${href})`}
                aria-label={label}
                className="inline-flex h-9 w-9 items-center justify-center rounded-md text-muted transition-colors hover:bg-surface-2 hover:text-text"
              >
                <Icon className="h-4 w-4" aria-hidden />
              </a>
            ))}
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/pitch')}
            className="gap-2"
            title="Pitch comercial"
          >
            <Presentation className="h-4 w-4" aria-hidden />
            Pitch
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate('/pitch/tecnico')}
            className="gap-2"
            title="Pitch técnico (arquitectura y stack)"
          >
            <Sparkles className="h-4 w-4" aria-hidden />
            Pitch técnico
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setContactOpen(true)}
            className="gap-2"
            title="Contacto"
          >
            <Mail className="h-4 w-4" aria-hidden />
            Contacto
          </Button>
        </div>
      </div>

      <Dialog open={contactOpen} onClose={() => setContactOpen(false)}>
        <div className="flex flex-col gap-6 p-6">
          <div className="flex flex-col gap-2">
            <h2 className="text-lg font-semibold text-text">¿Seguro que quieres contactar?</h2>
            <p className="text-sm text-muted">
              Te llevaremos a la pantalla de contacto del equipo.
            </p>
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="ghost" size="sm" onClick={() => setContactOpen(false)}>
              No
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={() => {
                setContactOpen(false);
                navigate('/app/contacto');
              }}
            >
              Sí
            </Button>
          </div>
        </div>
      </Dialog>
    </header>
  );
}
