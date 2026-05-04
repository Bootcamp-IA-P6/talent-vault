import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/Button';

export default function NotFoundPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-bg px-6 text-center text-text">
      <p className="text-xs uppercase tracking-widest text-muted">Error 404</p>
      <h1 className="text-4xl font-semibold tracking-tight">Página no encontrada</h1>
      <p className="max-w-md text-sm text-muted">
        La ruta a la que intentas acceder no existe o ha sido movida.
      </p>
      <Link to="/">
        <Button variant="primary">Volver al inicio</Button>
      </Link>
    </main>
  );
}
