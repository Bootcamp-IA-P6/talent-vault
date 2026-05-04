import { Inbox, Link2, Send } from 'lucide-react';
import type { SlideComponent } from '../types';

const steps = [
  {
    n: '01',
    icon: Inbox,
    title: 'Recibimos',
    body: 'Escuchamos todas tus fuentes en vivo, sin importar el formato ni el orden de llegada.',
  },
  {
    n: '02',
    icon: Link2,
    title: 'Conectamos',
    body: 'Usamos el documento de identidad y matching inteligente por nombre para detectar que distintos fragmentos hablan de la misma persona.',
  },
  {
    n: '03',
    icon: Send,
    title: 'Entregamos',
    body: 'Un perfil único, completo y consistente, listo para buscar, filtrar y exportar.',
  },
];

const Slide05Proceso: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-12 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        Cómo lo hacemos
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        De fragmentos a personas, en <span className="text-accent">3 pasos</span>.
      </h2>
    </header>

    <div className="grid w-full max-w-6xl grid-cols-1 gap-6 md:grid-cols-3">
      {steps.map(({ n, icon: Icon, title, body }) => (
        <article
          key={n}
          className="relative flex flex-col gap-5 rounded-2xl border border-border/60 bg-surface/60 p-8 backdrop-blur"
        >
          <span className="absolute right-6 top-6 font-mono text-5xl text-text/10">{n}</span>
          <div className="inline-flex w-fit rounded-xl bg-accent/15 p-3 text-accent">
            <Icon className="h-7 w-7" aria-hidden />
          </div>
          <h3 className="text-2xl font-semibold tracking-tight">{title}</h3>
          <p className="text-sm leading-relaxed text-text/70">{body}</p>
        </article>
      ))}
    </div>

    <p className="max-w-3xl text-center text-lg text-text/70">
      Si llegan todas las piezas a la vez, el perfil aparece <span className="text-accent">al instante</span>.
      Si no, lo completamos automáticamente. <span className="text-text">Nada se pierde.</span>
    </p>
  </section>
);

Slide05Proceso.meta = { title: 'Cómo tratamos los datos', theme: 'dark' };

export default Slide05Proceso;
