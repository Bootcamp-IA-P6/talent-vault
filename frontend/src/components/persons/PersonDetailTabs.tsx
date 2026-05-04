import { useState } from 'react';
import {
  AtSign,
  Banknote,
  Briefcase,
  Building2,
  Globe2,
  Hash,
  Home,
  Mail,
  MapPin,
  Phone,
  PiggyBank,
  User,
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import { fallback, formatCurrency, formatIBAN } from '@/lib/format';
import type { Person } from '@/lib/types';

type Props = { person: Person };

function Field({
  label,
  value,
  icon,
}: {
  label: string;
  value: React.ReactNode;
  icon: React.ReactNode;
}) {
  return (
    <div className="flex items-start gap-3 rounded-md border border-border bg-surface-2/40 p-4">
      <span className="mt-0.5 rounded-md border border-border bg-surface p-2 text-accent">
        {icon}
      </span>
      <div className="flex min-w-0 flex-col">
        <span className="text-[10px] uppercase tracking-wider text-muted">{label}</span>
        <span className="break-all text-sm text-text">{value}</span>
      </div>
    </div>
  );
}

export default function PersonDetailTabs({ person }: Props) {
  const [tab, setTab] = useState('contacto');

  return (
    <Tabs value={tab} onChange={setTab}>
      <TabsList>
        <TabsTrigger value="contacto">Contacto</TabsTrigger>
        <TabsTrigger value="trabajo">Trabajo</TabsTrigger>
        <TabsTrigger value="finanzas">Finanzas</TabsTrigger>
        <TabsTrigger value="localizacion">Localización</TabsTrigger>
      </TabsList>

      <TabsContent value="contacto">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Nombre" value={fallback(person.name)} icon={<User className="h-4 w-4" />} />
          <Field
            label="Apellidos"
            value={fallback(person.last_name)}
            icon={<User className="h-4 w-4" />}
          />
          <Field
            label="Nombre completo"
            value={fallback(person.fullname)}
            icon={<User className="h-4 w-4" />}
          />
          <Field
            label="Sexo"
            value={fallback(person.sex)}
            icon={<AtSign className="h-4 w-4" />}
          />
          <Field
            label="Email"
            value={fallback(person.email)}
            icon={<Mail className="h-4 w-4" />}
          />
          <Field
            label="Teléfono"
            value={fallback(person.telfnumber)}
            icon={<Phone className="h-4 w-4" />}
          />
        </div>
      </TabsContent>

      <TabsContent value="trabajo">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field
            label="Empresa"
            value={fallback(person.company)}
            icon={<Building2 className="h-4 w-4" />}
          />
          <Field
            label="Puesto"
            value={fallback(person.job)}
            icon={<Briefcase className="h-4 w-4" />}
          />
          <Field
            label="Email empresa"
            value={fallback(person.company_email)}
            icon={<Mail className="h-4 w-4" />}
          />
          <Field
            label="Tel. empresa"
            value={fallback(person.company_telfnumber)}
            icon={<Phone className="h-4 w-4" />}
          />
          <Field
            label="Dirección empresa"
            value={fallback(person.company_address)}
            icon={<Home className="h-4 w-4" />}
          />
        </div>
      </TabsContent>

      <TabsContent value="finanzas">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field
            label="IBAN"
            value={<span className="font-mono">{formatIBAN(person.IBAN)}</span>}
            icon={<Banknote className="h-4 w-4" />}
          />
          <Field
            label="Salario"
            value={formatCurrency(person.salary)}
            icon={<PiggyBank className="h-4 w-4" />}
          />
        </div>
      </TabsContent>

      <TabsContent value="localizacion">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Ciudad" value={fallback(person.city)} icon={<MapPin className="h-4 w-4" />} />
          <Field label="Dirección" value={fallback(person.address)} icon={<Home className="h-4 w-4" />} />
          <Field
            label="IPv4"
            value={
              <span className="font-mono text-accent">{fallback(person.IPv4)}</span>
            }
            icon={<Globe2 className="h-4 w-4" />}
          />
          <Field
            label="Pasaporte"
            value={<span className="font-mono">{person.passport}</span>}
            icon={<Hash className="h-4 w-4" />}
          />
        </div>
      </TabsContent>
    </Tabs>
  );
}
