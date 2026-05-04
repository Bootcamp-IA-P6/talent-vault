import { ArrowRight, Zap, ShieldCheck, Plug } from 'lucide-react';
import { useStats } from '@/hooks/useStats';
import type { SlideComponent } from '../types';

const recap = [
  { icon: Zap, label: 'Tiempo real' },
  { icon: ShieldCheck, label: 'Cero pérdida' },
  { icon: Plug, label: 'Listo para usar' },
];

const Slide07Cierre: SlideComponent = ({ exitPitch }) => {
  const { data } = useStats();
  const total = data?.total_persons;

  return (
    <section className="relative flex h-full w-full flex-col items-center justify-center gap-10 overflow-hidden bg-bg px-8 text-text">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_60%,hsl(var(--accent)/0.18),transparent_60%)]" />

      <header className="relative flex flex-col items-center gap-4 text-center">
        <h2 className="max-w-4xl text-6xl font-semibold tracking-tight">
          Tu gente, <span className="text-accent">sin fricción</span>.
        </h2>
      </header>

      <div className="relative flex flex-wrap items-center justify-center gap-3">
        {recap.map(({ icon: Icon, label }) => (
          <div
            key={label}
            className="flex items-center gap-2 rounded-full border border-border/60 bg-surface/60 px-4 py-2 backdrop-blur"
          >
            <Icon className="h-4 w-4 text-accent" aria-hidden />
            <span className="text-sm text-text/80">{label}</span>
          </div>
        ))}
      </div>

      {typeof total === 'number' && (
        <div className="relative flex flex-col items-center gap-1">
          <p className="font-mono text-5xl font-semibold text-accent">
            {total.toLocaleString('es-ES')}
          </p>
          <p className="text-xs uppercase tracking-widest text-text/60">
            personas unificadas en este sistema
          </p>
        </div>
      )}

      <button
        type="button"
        onClick={exitPitch}
        className="group relative inline-flex items-center gap-3 rounded-full bg-accent px-8 py-4 text-base font-semibold text-bg shadow-lg shadow-accent/30 transition hover:bg-accent/90"
      >
        Entrar al CRM
        <ArrowRight className="h-5 w-5 transition group-hover:translate-x-1" aria-hidden />
      </button>

      <p className="relative text-xs uppercase tracking-widest text-text/40">
        Talent Vault · Todos los derechos reservados {new Date().getFullYear()}
      </p>
    </section>
  );
};

Slide07Cierre.meta = { title: 'Cierre', theme: 'dark' };

export default Slide07Cierre;
