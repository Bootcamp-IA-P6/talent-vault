import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import type { StatBucket } from '@/lib/types';

const COLORS = ['hsl(217 91% 60%)', 'hsl(199 89% 60%)', 'hsl(142 70% 45%)', 'hsl(38 92% 55%)'];

export function SexPie({ data }: { data: StatBucket[] }) {
  const rows = data.map((d) => ({ name: d.sex ?? 'Sin dato', value: d.count }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie
          data={rows}
          dataKey="value"
          nameKey="name"
          innerRadius={60}
          outerRadius={90}
          paddingAngle={2}
          stroke="hsl(222 40% 11%)"
        >
          {rows.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
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
        <Legend wrapperStyle={{ color: 'hsl(210 20% 92%)', fontSize: 12 }} />
      </PieChart>
    </ResponsiveContainer>
  );
}
