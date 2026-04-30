import { Code2, Globe, Server } from 'lucide-react';
import type { SlideComponent } from '../types';

const layers = [
  {
    icon: Server,
    title: 'FastAPI + Uvicorn',
    role: 'API REST',
    bullets: [
      'Endpoints `/persons`, `/persons/{passport}`, `/stats`',
      'Filtros, paginación y búsqueda fuzzy',
      'Schema OpenAPI automático',
    ],
  },
  {
    icon: Code2,
    title: 'React 18 + Vite',
    role: 'CRM frontend',
    bullets: [
      'TypeScript estricto, Tailwind, shadcn-style UI',
      'TanStack Query para cache y refetch en vivo',
      'Cmd+K, tabs, charts, splash + carousel',
    ],
  },
  {
    icon: Globe,
    title: 'nginx',
    role: 'Edge',
    bullets: [
      'Sirve los assets estáticos compilados',
      'Proxy `/api/*` → `api:8000` (mismo origen, sin CORS)',
      'Fallback SPA para deep-linking',
    ],
  },
];

const Slide04Acceso: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-10 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        Pitch técnico · 4 / 5
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Acceso humano y <span className="text-accent">programático</span>.
      </h2>
      <p className="max-w-2xl text-lg text-text/70">
        El mismo modelo de datos llega a un CRM corporativo y a una API REST documentada.
      </p>
    </header>

    <div className="grid w-full max-w-5xl gap-4 md:grid-cols-3">
      {layers.map(({ icon: Icon, title, role, bullets }) => (
        <div
          key={title}
          className="flex flex-col gap-3 rounded-2xl border border-border/60 bg-surface/60 p-6 backdrop-blur"
        >
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-accent/40 bg-accent/10 text-accent">
            <Icon className="h-5 w-5" aria-hidden />
          </span>
          <div>
            <p className="text-lg font-semibold">{title}</p>
            <p className="text-xs uppercase tracking-wider text-accent">{role}</p>
          </div>
          <ul className="space-y-1.5 text-sm leading-relaxed text-text/70">
            {bullets.map((b) => (
              <li key={b}>· {b}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  </section>
);

Slide04Acceso.meta = { title: 'Acceso', theme: 'dark' };

export default Slide04Acceso;
