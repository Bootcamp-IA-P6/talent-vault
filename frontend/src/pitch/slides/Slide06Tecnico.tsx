import type { SlideComponent } from '../types';

const stack = [
  { name: 'Apache Kafka', role: 'Ingesta en tiempo real' },
  { name: 'Redis', role: 'Ensamblado instantáneo' },
  { name: 'MongoDB', role: 'Archivo histórico (raw)' },
  { name: 'PostgreSQL', role: 'Fuente única de verdad' },
  { name: 'FastAPI + React', role: 'Acceso humano y por API' },
  { name: 'Prometheus', role: 'Monitoreo y métricas' },
];

const Slide06Tecnico: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-10 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-border/60 bg-surface/60 px-3 py-1 text-xs uppercase tracking-widest text-text/60">
        Bajo el capó
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Construido sobre tecnologías de <span className="text-accent">nivel enterprise</span>.
      </h2>
    </header>

    <div className="w-full max-w-5xl rounded-2xl border border-border/60 bg-surface/40 p-8 backdrop-blur">
      <pre className="overflow-x-auto font-mono text-xs leading-relaxed text-text/80 md:text-sm">
{`  ┌─────────┐    ┌──────────┐    ┌─────────┐  raw  ┌──────────┐
  │  Kafka  │ ─> │ Consumer │ ─> │ MongoDB │ ────> │ Aggregator│
  └─────────┘    └────┬─────┘    └─────────┘       └─────┬────┘
                      │ fast path                         │ batch
                      ▼                                   ▼
                 ┌─────────┐                      ┌──────────────┐
                 │  Redis  │ ───────────────────> │  PostgreSQL  │
                 └─────────┘                      └──────┬───────┘
                                                         ▼
                                              ┌─────────────────────┐
                                              │  FastAPI + React UI │
                                              └─────────────────────┘`}
      </pre>
    </div>

    <div className="grid w-full max-w-5xl grid-cols-2 gap-3 md:grid-cols-3">
      {stack.map(({ name, role }) => (
        <div
          key={name}
          className="flex flex-col gap-1 rounded-xl border border-border/60 bg-surface/60 px-4 py-3 backdrop-blur"
        >
          <p className="text-sm font-semibold text-text">{name}</p>
          <p className="text-xs text-text/60">{role}</p>
        </div>
      ))}
    </div>

    <p className="text-center text-sm text-text/60">
      Stack robusto, escalable a millones de mensajes, listo para producción.
    </p>
  </section>
);

Slide06Tecnico.meta = { title: 'Parte técnica', theme: 'dark' };

export default Slide06Tecnico;
