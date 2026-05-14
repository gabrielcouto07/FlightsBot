import { Bell, Plane, Sliders, Users, Zap } from 'lucide-react';

export const navItems = [
  {
    path: '/',
    label: 'Ofertas',
    title: 'Explorador de Ofertas',
    description: 'Pesquise primeiro, compare rapido e reserve com o link mais direto disponivel.',
    icon: Plane,
  },
  {
    path: '/alerts-lab',
    label: 'Alertas',
    title: 'Laboratorio de Alertas',
    description: 'Teste cobertura de alertas, limites de preco e listas de monitoramento.',
    icon: Bell,
  },
  {
    path: '/route-monitor',
    label: 'Rotas',
    title: 'Monitor de Rotas',
    description: 'Acompanhe rotas monitoradas, limites de disparo e saude das buscas.',
    icon: Zap,
  },
  {
    path: '/users',
    label: 'Viajantes',
    title: 'Viajantes',
    description: 'Gerencie viajantes de teste e os planos ligados a cada um.',
    icon: Users,
  },
  {
    path: '/filter-lab',
    label: 'Diagnostico',
    title: 'Diagnostico',
    description: 'Area tecnica para validar filtros, matching e inspecao de resultados.',
    icon: Sliders,
  },
];
