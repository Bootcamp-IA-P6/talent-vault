import { createContext, useContext, useId, type ReactNode } from 'react';
import { cn } from '@/lib/cn';

type TabsCtx = {
  value: string;
  onChange: (v: string) => void;
  baseId: string;
};

const Ctx = createContext<TabsCtx | null>(null);

function useTabsCtx(): TabsCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('Tabs components must be used inside <Tabs>');
  return ctx;
}

export function Tabs({
  value,
  onChange,
  children,
  className,
}: {
  value: string;
  onChange: (v: string) => void;
  children: ReactNode;
  className?: string;
}) {
  const baseId = useId();
  return (
    <Ctx.Provider value={{ value, onChange, baseId }}>
      <div className={cn('flex flex-col', className)}>{children}</div>
    </Ctx.Provider>
  );
}

export function TabsList({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div
      role="tablist"
      className={cn(
        'inline-flex items-center gap-1 rounded-md border border-border bg-surface p-1',
        className,
      )}
    >
      {children}
    </div>
  );
}

export function TabsTrigger({
  value,
  children,
  className,
}: {
  value: string;
  children: ReactNode;
  className?: string;
}) {
  const ctx = useTabsCtx();
  const active = ctx.value === value;
  return (
    <button
      type="button"
      role="tab"
      id={`${ctx.baseId}-tab-${value}`}
      aria-selected={active}
      aria-controls={`${ctx.baseId}-panel-${value}`}
      onClick={() => ctx.onChange(value)}
      className={cn(
        'rounded-md px-3 py-1.5 text-sm font-medium transition-colors',
        active ? 'bg-accent text-bg shadow-sm' : 'text-muted hover:bg-surface-2 hover:text-text',
        className,
      )}
    >
      {children}
    </button>
  );
}

export function TabsContent({
  value,
  children,
  className,
}: {
  value: string;
  children: ReactNode;
  className?: string;
}) {
  const ctx = useTabsCtx();
  if (ctx.value !== value) return null;
  return (
    <div
      role="tabpanel"
      id={`${ctx.baseId}-panel-${value}`}
      aria-labelledby={`${ctx.baseId}-tab-${value}`}
      className={cn('animate-fade-in pt-4', className)}
    >
      {children}
    </div>
  );
}
