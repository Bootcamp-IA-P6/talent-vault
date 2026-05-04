import type { HTMLAttributes } from 'react';
import { cn } from '@/lib/cn';

type Variant = 'default' | 'accent' | 'success' | 'danger' | 'outline';

const variants: Record<Variant, string> = {
  default: 'bg-surface-2 text-text border-border',
  accent: 'bg-accent/15 text-accent border-accent/30',
  success: 'bg-success/15 text-success border-success/30',
  danger: 'bg-danger/15 text-danger border-danger/30',
  outline: 'bg-transparent text-text border-border',
};

export function Badge({
  className,
  variant = 'default',
  ...props
}: HTMLAttributes<HTMLSpanElement> & { variant?: Variant }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium',
        variants[variant],
        className,
      )}
      {...props}
    />
  );
}
