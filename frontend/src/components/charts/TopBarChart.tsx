import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import type { StatBucket } from '@/lib/types';

type Props = {
  data: StatBucket[];
  labelKey: 'city' | 'company' | 'job' | 'sex';
};

export function TopBarChart({ data, labelKey }: Props) {
  const rows = data.map((d) => ({
    label: (d[labelKey] ?? '—') as string,
    count: d.count,
  }));

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={rows} layout="vertical" margin={{ left: 4, right: 16, top: 8, bottom: 8 }}>
        <CartesianGrid horizontal={false} stroke="hsl(222 30% 20%)" />
        <XAxis
          type="number"
          stroke="hsl(215 16% 60%)"
          tick={{ fill: 'hsl(215 16% 60%)', fontSize: 11 }}
        />
        <YAxis
          dataKey="label"
          type="category"
          width={120}
          stroke="hsl(215 16% 60%)"
          tick={{ fill: 'hsl(210 20% 92%)', fontSize: 12 }}
          interval={0}
        />
        <Tooltip
          cursor={{ fill: 'hsl(217 91% 60% / 0.08)' }}
          contentStyle={{
            background: 'hsl(222 40% 11%)',
            border: '1px solid #ffffff',
            borderRadius: 8,
            color: '#ffffff',
            fontSize: 12,
          }}
          itemStyle={{ color: '#ffffff' }}
          labelStyle={{ color: '#ffffff' }}
        />
        <Bar dataKey="count" fill="hsl(217 91% 60%)" radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
