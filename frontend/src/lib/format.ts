const numberES = new Intl.NumberFormat('es-ES');
const currencyES = new Intl.NumberFormat('es-ES', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 0,
});

export function formatNumber(n: number | null | undefined): string {
  if (n == null) return '—';
  return numberES.format(n);
}

export function formatCurrency(n: number | null | undefined): string {
  if (n == null) return '—';
  return currencyES.format(n);
}

export function formatIBAN(iban: string | null | undefined): string {
  if (!iban) return '—';
  return iban.replace(/\s+/g, '').replace(/(.{4})/g, '$1 ').trim();
}

export function formatPhone(phone: string | null | undefined): string {
  if (!phone) return '—';
  return phone;
}

export function fallback(value: string | null | undefined, dash = '—'): string {
  if (value == null || value === '') return dash;
  return value;
}

export function cls(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ');
}
