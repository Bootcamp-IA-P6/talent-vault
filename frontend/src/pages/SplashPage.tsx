import { useNavigate } from 'react-router-dom';
import { ArrowRight, PlayCircle } from 'lucide-react';
import logoUrl from '@/assets/logo.png';

export default function SplashPage() {
  const navigate = useNavigate();

  return (
    <main className="relative flex h-full min-h-screen w-full flex-col items-center justify-center overflow-hidden bg-bg text-text">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,hsl(var(--accent)/0.18),transparent_65%)]"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,transparent,hsl(var(--bg)/0.95))]"
      />

      <div className="relative z-10 flex flex-col items-center gap-10 animate-fade-in">
        <img
          src={logoUrl}
          alt="Talent Vault"
          className="h-72 w-72 animate-logo-pulse drop-shadow-[0_0_60px_hsl(var(--accent)/0.55)]"
        />

        <h1 className="text-center text-4xl font-semibold tracking-tight text-text">
          Talent <span className="text-accent">Vault</span>
        </h1>

        <button
          type="button"
          onClick={() => navigate('/pitch')}
          className="group inline-flex items-center gap-3 rounded-full bg-accent px-8 py-4 text-base font-semibold text-bg shadow-lg shadow-accent/30 transition hover:bg-accent/90 focus:outline-none focus:ring-2 focus:ring-accent/60"
        >
          <PlayCircle className="h-5 w-5" aria-hidden />
          <span>Entrar</span>
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" aria-hidden />
        </button>

        <p className="text-xs uppercase tracking-[0.3em] text-muted">
          Plataforma corporativa de unificación de datos
        </p>
      </div>
    </main>
  );
}
