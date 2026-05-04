import { Boxes, LineChart, ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { SlideComponent } from '../types';

const ops = [
  {
    icon: LineChart,
    title: 'Prometheus',
    detail: 'Métricas custom: mensajes consumidos, latencia API, ratios de match. Scrape cada 15 s.',
  },
  {
    icon: Boxes,
    title: 'Docker Compose',
    detail: '11 servicios orquestados, volúmenes persistentes, restart policies. Un `make build` y arriba.',
  },
  {
    icon: ShieldCheck,
    title: 'Loguru + tests',
    detail: 'Logs estructurados a stdout y archivo. Suite pytest sobre clasificador y agregador.',
  },
];

const Slide05Operacion: SlideComponent = ({ exitPitch }) => {
  const navigate = useNavigate();
  return (
    <section className="relative flex h-full w-full flex-col items-center justify-center gap-10 overflow-hidden bg-bg px-8 text-text">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_70%,hsl(var(--accent)/0.15),transparent_60%)]" />

      <header className="relative flex flex-col items-center gap-3 text-center">
        <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
          Pitch técnico · 5 / 5
        </span>
        <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
          Operable y <span className="text-accent">listo para escalar</span>.
        </h2>
      </header>

      <div className="relative grid w-full max-w-5xl gap-4 md:grid-cols-3">
        {ops.map(({ icon: Icon, title, detail }) => (
          <div
            key={title}
            className="flex flex-col gap-3 rounded-2xl border border-border/60 bg-surface/60 p-6 backdrop-blur"
          >
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-accent/40 bg-accent/10 text-accent">
              <Icon className="h-5 w-5" aria-hidden />
            </span>
            <p className="text-lg font-semibold">{title}</p>
            <p className="text-sm leading-relaxed text-text/70">{detail}</p>
          </div>
        ))}
      </div>

      <div className="relative flex flex-wrap items-center justify-center gap-3">
        <button
          type="button"
          onClick={exitPitch}
          className="inline-flex items-center gap-2 rounded-full bg-accent px-6 py-3 text-sm font-semibold text-bg shadow-lg shadow-accent/30 transition hover:bg-accent/90"
        >
          Volver al CRM
        </button>
        <button
          type="button"
          onClick={() => navigate('/pitch')}
          className="inline-flex items-center gap-2 rounded-full border border-border/60 bg-surface/60 px-6 py-3 text-sm font-medium text-text/80 backdrop-blur transition hover:border-accent hover:text-text"
        >
          Ver pitch comercial
        </button>
      </div>

      <p className="relative text-xs uppercase tracking-widest text-text/40">
        Talent Vault · Todos los derechos reservados {new Date().getFullYear()}
      </p>
    </section>
  );
};

Slide05Operacion.meta = { title: 'Operación', theme: 'dark' };

export default Slide05Operacion;
