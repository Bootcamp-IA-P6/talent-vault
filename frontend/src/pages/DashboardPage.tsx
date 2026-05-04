import { Activity, Briefcase, Building2, MapPin, Users } from 'lucide-react';
import { useStats } from '@/hooks/useStats';
import { Card, CardBody, CardHeader, CardTitle } from '@/components/ui/Card';
import { KpiCard } from '@/components/kpi/KpiCard';
import { TopBarChart } from '@/components/charts/TopBarChart';
import { SexPie } from '@/components/charts/SexPie';
import { Skeleton } from '@/components/ui/Skeleton';
import { formatNumber } from '@/lib/format';

export default function DashboardPage() {
  const { data, isLoading, isError, error } = useStats();

  return (
    <div className="flex flex-col gap-6">
      <header className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted">Visión global del registro de personas.</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted">
          <Activity className="h-4 w-4 text-success" aria-hidden />
          Métricas en vivo
        </div>
      </header>

      {isError ? (
        <Card>
          <CardBody className="text-sm text-danger">
            Error cargando estadísticas: {String((error as Error)?.message ?? 'desconocido')}
          </CardBody>
        </Card>
      ) : null}

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          label="Personas registradas"
          value={isLoading ? <Skeleton className="h-8 w-32" /> : formatNumber(data?.total_persons)}
          hint="Total en Postgres"
          icon={<Users className="h-4 w-4" aria-hidden />}
        />
        <KpiCard
          label="Ciudades únicas (top)"
          value={isLoading ? <Skeleton className="h-8 w-20" /> : formatNumber(data?.top_cities.length ?? 0)}
          hint="Ciudades con más personas"
          icon={<MapPin className="h-4 w-4" aria-hidden />}
        />
        <KpiCard
          label="Empresas únicas (top)"
          value={
            isLoading ? <Skeleton className="h-8 w-20" /> : formatNumber(data?.top_companies.length ?? 0)
          }
          hint="Distribución empresarial"
          icon={<Building2 className="h-4 w-4" aria-hidden />}
        />
        <KpiCard
          label="Roles únicos (top)"
          value={isLoading ? <Skeleton className="h-8 w-20" /> : formatNumber(data?.top_jobs.length ?? 0)}
          hint="Variedad de jobs"
          icon={<Briefcase className="h-4 w-4" aria-hidden />}
        />
      </section>

      <section className="grid gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top ciudades</CardTitle>
          </CardHeader>
          <CardBody>
            {isLoading ? (
              <Skeleton className="h-[260px] w-full" />
            ) : (
              <TopBarChart data={data?.top_cities ?? []} labelKey="city" />
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top empresas</CardTitle>
          </CardHeader>
          <CardBody>
            {isLoading ? (
              <Skeleton className="h-[260px] w-full" />
            ) : (
              <TopBarChart data={data?.top_companies ?? []} labelKey="company" />
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top roles</CardTitle>
          </CardHeader>
          <CardBody>
            {isLoading ? (
              <Skeleton className="h-[260px] w-full" />
            ) : (
              <TopBarChart data={data?.top_jobs ?? []} labelKey="job" />
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Distribución por sexo</CardTitle>
          </CardHeader>
          <CardBody>
            {isLoading ? (
              <Skeleton className="h-[260px] w-full" />
            ) : (
              <SexPie data={data?.sex_distribution ?? []} />
            )}
          </CardBody>
        </Card>
      </section>
    </div>
  );
}
