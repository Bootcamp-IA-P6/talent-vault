import { Database, HardDrive } from 'lucide-react';
import type { SlideComponent } from '../types';

const Slide03Datos: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-10 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        Pitch técnico · 3 / 5
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Dos almacenes, <span className="text-accent">cada uno con su trabajo</span>.
      </h2>
    </header>

    <div className="grid w-full max-w-5xl gap-6 md:grid-cols-2">
      <div className="flex flex-col gap-4 rounded-2xl border border-border/60 bg-surface/60 p-8 backdrop-blur">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl border border-accent/40 bg-accent/10 text-accent">
            <HardDrive className="h-6 w-6" aria-hidden />
          </span>
          <div>
            <p className="text-xl font-semibold">MongoDB</p>
            <p className="text-xs uppercase tracking-widest text-accent">Histórico raw</p>
          </div>
        </div>
        <ul className="space-y-2 text-sm text-text/75">
          <li>· Persiste cada mensaje original sin transformar.</li>
          <li>· Inmutable: trazabilidad y auditoría completas.</li>
          <li>· Permite reprocesar el pipeline si cambian las reglas.</li>
        </ul>
        <p className="mt-auto rounded-md border border-border/60 bg-bg/40 px-3 py-2 font-mono text-xs text-text/60">
          collection: <span className="text-accent">raw_messages</span>
        </p>
      </div>

      <div className="flex flex-col gap-4 rounded-2xl border border-border/60 bg-surface/60 p-8 backdrop-blur">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl border border-accent/40 bg-accent/10 text-accent">
            <Database className="h-6 w-6" aria-hidden />
          </span>
          <div>
            <p className="text-xl font-semibold">PostgreSQL</p>
            <p className="text-xs uppercase tracking-widest text-accent">Fuente única de verdad</p>
          </div>
        </div>
        <ul className="space-y-2 text-sm text-text/75">
          <li>· Esquema relacional con 32 campos por persona.</li>
          <li>· Índices en pasaporte, fullname y city para consultas instantáneas.</li>
          <li>· Lo que ven la API y el CRM.</li>
        </ul>
        <p className="mt-auto rounded-md border border-border/60 bg-bg/40 px-3 py-2 font-mono text-xs text-text/60">
          table: <span className="text-accent">persons</span>
        </p>
      </div>
    </div>

    <p className="text-center text-sm text-text/60">
      Crudo + curado en paralelo. Nunca pierdes el original; siempre consultas el limpio.
    </p>
  </section>
);

Slide03Datos.meta = { title: 'Datos', theme: 'dark' };

export default Slide03Datos;
