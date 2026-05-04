import type { Person, PersonsQuery, PersonsResponse, Stats } from './types';

const BASE = '/api';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { Accept: 'application/json', ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`API ${res.status} ${res.statusText} on ${path}${body ? ` — ${body}` : ''}`);
  }
  return res.json() as Promise<T>;
}

export function listPersons(params: PersonsQuery, signal?: AbortSignal): Promise<PersonsResponse> {
  const qs = new URLSearchParams();
  if (params.city) qs.set('city', params.city);
  if (params.company) qs.set('company', params.company);
  if (params.search) qs.set('search', params.search);
  if (params.limit != null) qs.set('limit', String(params.limit));
  if (params.offset != null) qs.set('offset', String(params.offset));
  const tail = qs.toString();
  return request<PersonsResponse>(`/persons${tail ? `?${tail}` : ''}`, { signal });
}

export function getPerson(passport: string, signal?: AbortSignal): Promise<Person> {
  return request<Person>(`/persons/${encodeURIComponent(passport)}`, { signal });
}

export function getStats(signal?: AbortSignal): Promise<Stats> {
  return request<Stats>(`/stats`, { signal });
}

export function getHealth(signal?: AbortSignal): Promise<{ status: string }> {
  return request<{ status: string }>(`/health`, { signal });
}
