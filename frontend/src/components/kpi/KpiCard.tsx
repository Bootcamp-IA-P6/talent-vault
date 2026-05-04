import type { ReactNode } from 'react';
import { cn } from '@/lib/cn';

type Props = {
  label: string;
  value: ReactNode;
  hint?: ReactNode;
  icon?: ReactNode;
  accent?: 'accent' | 'success' | 'danger';
  className?: string;
};

const accents = {
  accent: 'text-accent bg-accent/10 border-accent/30',
  success: 'text-success bg-success/10 border-success/30',
  danger: 'text-danger bg-danger/10 border-danger/30',
};

export function KpiCard({ label, value, hint, icon, accent = 'accent', className }: Props) {
  return (
    <div
      className={cn(
        'flex flex-col gap-3 rounded-lg border border-border bg-surface p-5 shadow-sm',
        className,
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <span className="text-xs uppercase tracking-wide text-muted">{label}</span>
        {icon ? (
          <span className={cn('rounded-md border p-2', accents[accent])}>{icon}</span>
        ) : null}
      </div>
      <div className="text-3xl font-semibold tracking-tight text-text">{value}</div>
      {hint ? <div className="text-xs text-muted">{hint}</div> : null}
    </div>
  );
}
