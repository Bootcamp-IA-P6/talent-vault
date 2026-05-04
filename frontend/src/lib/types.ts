export type Person = {
  passport: string;
  name: string | null;
  last_name: string | null;
  fullname: string | null;
  email: string | null;
  telfnumber: string | null;
  sex: string | null;
  IBAN: string | null;
  salary: number | null;
  company: string | null;
  company_address: string | null;
  company_email: string | null;
  company_telfnumber: string | null;
  job: string | null;
  city: string | null;
  address: string | null;
  IPv4: string | null;
};

export type PersonsResponse = {
  total: number;
  limit: number;
  offset: number;
  items: Person[];
};

export type StatBucket = {
  city?: string;
  company?: string;
  job?: string;
  sex?: string;
  count: number;
};

export type Stats = {
  total_persons: number;
  top_cities: StatBucket[];
  top_companies: StatBucket[];
  top_jobs: StatBucket[];
  sex_distribution: StatBucket[];
};

export type PersonsQuery = {
  city?: string;
  company?: string;
  search?: string;
  limit?: number;
  offset?: number;
};
