import { ArrowRight, Cloud, Database, FileSpreadsheet, Server, Boxes } from 'lucide-react';
import type { SlideComponent } from '../types';

const incoming = [
  { icon: Database, label: 'Bases de datos' },
  { icon: Cloud, label: 'Servicios en la nube' },
  { icon: FileSpreadsheet, label: 'Archivos y exports' },
  { icon: Server, label: 'Sistemas internos' },
  { icon: Boxes, label: 'APIs externas' },
];

const Slide04Empresa: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-12 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        Qué hacemos
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Toda tu organización en un <span className="text-accent">único perfil</span>.
      </h2>
    </header>

    <div className="flex w-full max-w-6xl items-center gap-8">
      <div className="flex flex-1 flex-col gap-3">
        {incoming.map(({ icon: Icon, label }) => (
          <div
            key={label}
            className="flex items-center gap-3 rounded-xl border border-border/60 bg-surface/60 px-4 py-3 text-sm backdrop-blur"
          >
            <Icon className="h-5 w-5 text-accent" aria-hidden />
            <span className="text-text/80">{label}</span>
          </div>
        ))}
      </div>

      <ArrowRight className="h-10 w-10 shrink-0 text-accent" aria-hidden />

      <div className="flex flex-[2] flex-col gap-5 rounded-2xl border border-accent/40 bg-surface/80 p-8 backdrop-blur">
        <div className="flex items-baseline justify-between">
          <p className="text-sm uppercase tracking-widest text-text/60">Perfil unificado</p>
          <p className="text-xs text-accent">100% completo</p>
        </div>
        <div className="space-y-3">
          {['Contacto', 'Trabajo', 'Finanzas', 'Ubicación', 'Identidad'].map((cat) => (
            <div key={cat} className="flex items-center justify-between rounded-md border border-border/40 bg-bg/40 px-3 py-2.5">
              <span className="text-sm text-text/80">{cat}</span>
              <span className="h-2 w-24 overflow-hidden rounded-full bg-bg/60">
                <span className="block h-full w-full rounded-full bg-accent" />
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>

    <p className="max-w-3xl text-center text-lg text-text/70">
      Recibimos datos de cualquier fuente, los matcheamos por identidad, y te entregamos
      un perfil completo, organizado y listo para consultar.
    </p>
  </section>
);

Slide04Empresa.meta = { title: 'Qué hacemos', theme: 'dark' };

export default Slide04Empresa;
