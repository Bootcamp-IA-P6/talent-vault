import { Database, FileQuestion, Files, Server, HelpCircle } from 'lucide-react';
import type { SlideComponent } from '../types';

const fragments = [
  { icon: Database, label: 'Sistemas dispersos' },
  { icon: Files, label: 'Datos duplicados' },
  { icon: FileQuestion, label: 'Información incompleta' },
  { icon: Server, label: 'Fuentes desconectadas' },
];

const Slide02Problema: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-12 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-danger/40 bg-danger/10 px-3 py-1 text-xs uppercase tracking-widest text-danger">
        El problema
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Tus datos llegan <span className="text-danger">fragmentados</span>.
        <br />
        Tu equipo paga el costo.
      </h2>
    </header>

    <div className="relative grid w-full max-w-5xl grid-cols-2 gap-6 md:grid-cols-4">
      {fragments.map(({ icon: Icon, label }) => (
        <div
          key={label}
          className="flex flex-col items-center gap-3 rounded-2xl border border-border/60 bg-surface/60 p-6 text-center backdrop-blur"
        >
          <div className="rounded-full bg-bg/60 p-3 text-accent">
            <Icon className="h-6 w-6" aria-hidden />
          </div>
          <p className="text-sm font-semibold text-text">{label}</p>
        </div>
      ))}

      <div className="absolute left-1/2 top-1/2 -z-0 hidden -translate-x-1/2 -translate-y-1/2 md:block">
        <div className="flex h-20 w-20 items-center justify-center rounded-full border-2 border-dashed border-danger/60 bg-bg text-danger">
          <HelpCircle className="h-9 w-9" aria-hidden />
        </div>
      </div>
    </div>

    <p className="max-w-2xl text-center text-lg text-text/70">
      Cada sistema guarda una pieza distinta. Reconstruir la foto completa de una persona
      es lento, manual y propenso a errores.
    </p>
  </section>
);

Slide02Problema.meta = { title: 'El problema', theme: 'dark' };

export default Slide02Problema;
