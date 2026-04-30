import { Cpu } from 'lucide-react';
import type { SlideComponent } from '../types';

const Slide01Arquitectura: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-8 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="inline-flex items-center gap-2 rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        <Cpu className="h-3.5 w-3.5" aria-hidden /> Pitch técnico · 1 / 5
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Arquitectura <span className="text-accent">end-to-end</span>.
      </h2>
      <p className="max-w-2xl text-lg text-text/70">
        Un pipeline de eventos que convierte fragmentos crudos en una verdad única consultable.
      </p>
    </header>

    <div className="w-full max-w-5xl rounded-2xl border border-border/60 bg-surface/40 p-8 backdrop-blur">
      <pre className="overflow-x-auto font-mono text-xs leading-relaxed text-text/85 md:text-sm">
{`  ┌─────────┐    ┌──────────┐    ┌─────────┐  raw   ┌────────────┐
  │  Kafka  │ ─> │ Consumer │ ─> │ MongoDB │ ─────> │ Aggregator │
  └─────────┘    └────┬─────┘    └─────────┘        └─────┬──────┘
                      │ fast path                          │ batch
                      ▼                                    ▼
                 ┌─────────┐                        ┌──────────────┐
                 │  Redis  │ ─────────────────────> │  PostgreSQL  │
                 └─────────┘                        └──────┬───────┘
                                                           ▼
                                                ┌─────────────────────┐
                                                │  FastAPI + React UI │
                                                └─────────────────────┘`}
      </pre>
    </div>

    <p className="text-center text-sm text-text/60">
      Cinco capas desacopladas. Cada una hace una sola cosa, bien.
    </p>
  </section>
);

Slide01Arquitectura.meta = { title: 'Arquitectura', theme: 'dark' };

export default Slide01Arquitectura;
