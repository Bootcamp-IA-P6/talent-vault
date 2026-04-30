import { Activity, Layers, Zap } from 'lucide-react';
import type { SlideComponent } from '../types';

const items = [
  {
    icon: Zap,
    title: 'Apache Kafka',
    role: 'Backbone de eventos',
    detail:
      'Topic único `testing` que recibe fragmentos de los 5 sistemas fuente. Particionado, replicado, sin pérdida.',
  },
  {
    icon: Layers,
    title: 'Consumer (Python)',
    role: 'Clasifica y enruta',
    detail:
      'Detecta el tipo de mensaje (personal/banco/profesional/localización/red), lo persiste en MongoDB raw y dispara el ensamblado.',
  },
  {
    icon: Activity,
    title: 'Redis',
    role: 'Buffer en caliente',
    detail:
      'Mantiene el estado de cada pasaporte en memoria mientras llegan sus 5 fragmentos. Cuando completa, sale al SQL loader.',
  },
];

const Slide02Ingesta: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-10 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        Pitch técnico · 2 / 5
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Ingesta en <span className="text-accent">tiempo real</span>.
      </h2>
      <p className="max-w-2xl text-lg text-text/70">
        Eventos entran por Kafka, se clasifican y se ensamblan en caliente sin esperar batch nocturno.
      </p>
    </header>

    <div className="grid w-full max-w-5xl gap-4 md:grid-cols-3">
      {items.map(({ icon: Icon, title, role, detail }) => (
        <div
          key={title}
          className="flex flex-col gap-3 rounded-2xl border border-border/60 bg-surface/60 p-6 backdrop-blur"
        >
          <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-accent/40 bg-accent/10 text-accent">
            <Icon className="h-5 w-5" aria-hidden />
          </span>
          <div>
            <p className="text-lg font-semibold text-text">{title}</p>
            <p className="text-xs uppercase tracking-wider text-accent">{role}</p>
          </div>
          <p className="text-sm leading-relaxed text-text/70">{detail}</p>
        </div>
      ))}
    </div>

    <p className="text-center text-sm text-text/60">
      Resultado: latencia de fragmento → persona unificada en{' '}
      <span className="font-mono text-accent">segundos</span>, no horas.
    </p>
  </section>
);

Slide02Ingesta.meta = { title: 'Ingesta', theme: 'dark' };

export default Slide02Ingesta;
