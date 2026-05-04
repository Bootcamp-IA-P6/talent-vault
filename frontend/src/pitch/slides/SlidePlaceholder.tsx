import type { SlideComponent } from '../types';

const SlidePlaceholder: SlideComponent = ({ exitPitch }) => (
  <section className="flex h-full w-full flex-col items-center justify-center gap-6 bg-bg text-text">
    <h1 className="text-5xl font-semibold tracking-tight">Talent Vault</h1>
    <p className="max-w-xl text-center text-lg text-text/70">
      Aquí irán las slides del pitch. Sustituye este placeholder añadiendo tus
      propios componentes en <code className="text-accent">src/pitch/slides/</code> y
      registrándolos en <code className="text-accent">slides/index.ts</code>.
    </p>
    <button
      type="button"
      onClick={exitPitch}
      className="rounded-md bg-accent px-6 py-3 text-sm font-medium text-bg transition hover:bg-accent/90"
    >
      Entrar al CRM
    </button>
  </section>
);

SlidePlaceholder.meta = { title: 'Bienvenida', theme: 'dark' };

export default SlidePlaceholder;
