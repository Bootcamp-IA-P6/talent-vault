import { ArrowDown } from 'lucide-react';
import type { SlideComponent } from '../types';

const Slide01Hook: SlideComponent = ({ goNext }) => (
  <section className="relative flex h-full w-full flex-col items-center justify-center gap-10 overflow-hidden bg-bg text-text">
    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_30%,hsl(var(--accent)/0.18),transparent_60%)]" />
    <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,transparent,hsl(var(--bg))_85%)]" />

    <span className="relative rounded-full border border-border/60 bg-surface/40 px-4 py-1.5 text-xs uppercase tracking-[0.3em] text-text/60 backdrop-blur">
      Plataforma de unificación de datos de RRHH
    </span>

    <h1 className="relative text-7xl font-semibold tracking-tight md:text-8xl">
      Talent <span className="text-accent">Vault</span>
    </h1>

    <p className="relative max-w-2xl text-center text-2xl font-light text-text/80">
      Tus empleados, en un solo lugar.
      <br />
      <span className="text-text">En tiempo real.</span>
    </p>

    <button
      type="button"
      onClick={goNext}
      className="relative mt-6 inline-flex items-center gap-2 rounded-full border border-border/60 bg-surface/40 px-5 py-2.5 text-sm text-text/80 backdrop-blur transition hover:border-accent hover:text-text"
    >
      Comenzar el recorrido
      <ArrowDown className="h-4 w-4 animate-bounce" aria-hidden />
    </button>
  </section>
);

Slide01Hook.meta = { title: 'Bienvenida', theme: 'dark' };

export default Slide01Hook;
