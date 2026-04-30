import { Zap, ShieldCheck, Plug } from 'lucide-react';
import type { SlideComponent } from '../types';

const pillars = [
  {
    icon: Zap,
    title: 'Tiempo real',
    body: 'Los datos se unifican en milisegundos, no en horas. En cuanto llegan todas las piezas, el perfil aparece al instante.',
  },
  {
    icon: ShieldCheck,
    title: 'Cero pérdida',
    body: 'Guardamos cada fragmento original. Auditoría completa, trazabilidad total y nada se cae entre las grietas.',
  },
  {
    icon: Plug,
    title: 'Listo para usar',
    body: 'Dashboard visual para tu equipo y API REST para integrar con cualquier sistema que ya tengas.',
  },
];

const Slide03Diferencial: SlideComponent = () => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-14 bg-bg px-8 text-text">
    <header className="flex flex-col items-center gap-3 text-center">
      <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs uppercase tracking-widest text-accent">
        Por qué elegirnos
      </span>
      <h2 className="max-w-4xl text-5xl font-semibold tracking-tight">
        Tres razones que <span className="text-accent">no tienen competencia</span>.
      </h2>
    </header>

    <div className="grid w-full max-w-6xl grid-cols-1 gap-6 md:grid-cols-3">
      {pillars.map(({ icon: Icon, title, body }) => (
        <article
          key={title}
          className="flex flex-col gap-4 rounded-2xl border border-border/60 bg-surface/60 p-8 backdrop-blur transition hover:border-accent/60"
        >
          <div className="inline-flex w-fit rounded-xl bg-accent/15 p-3 text-accent">
            <Icon className="h-7 w-7" aria-hidden />
          </div>
          <h3 className="text-2xl font-semibold tracking-tight">{title}</h3>
          <p className="text-sm leading-relaxed text-text/70">{body}</p>
        </article>
      ))}
    </div>

    <p className="max-w-2xl text-center text-lg italic text-text/70">
      &ldquo;No reemplazamos tus sistemas. Los hacemos hablar entre sí.&rdquo;
    </p>
  </section>
);

Slide03Diferencial.meta = { title: 'Por qué elegirnos', theme: 'dark' };

export default Slide03Diferencial;
