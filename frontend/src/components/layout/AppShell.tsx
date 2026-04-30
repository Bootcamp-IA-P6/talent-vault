import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { useHotkeys } from 'react-hotkeys-hook';
import Navbar from './Navbar';
import CommandPalette from '@/components/search/CommandPalette';

export default function AppShell() {
  const [paletteOpen, setPaletteOpen] = useState(false);

  useHotkeys('mod+k', (e) => {
    e.preventDefault();
    setPaletteOpen(true);
  });

  return (
    <div className="flex min-h-screen flex-col bg-bg text-text">
      <Navbar onOpenSearch={() => setPaletteOpen(true)} />
      <main className="flex-1 px-6 py-8">
        <Outlet />
      </main>
      <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} />
      <footer className="border-t border-border px-6 py-4 text-xs text-muted">
        Talent Vault · API status: <span className="text-success">●</span> conectado
      </footer>
    </div>
  );
}
