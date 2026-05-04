import { createBrowserRouter, Navigate } from 'react-router-dom';
import AppShell from '@/components/layout/AppShell';
import SplashPage from '@/pages/SplashPage';
import PitchPage from '@/pages/PitchPage';
import PitchTecnicoPage from '@/pages/PitchTecnicoPage';
import DashboardPage from '@/pages/DashboardPage';
import PersonsPage from '@/pages/PersonsPage';
import PersonDetailPage from '@/pages/PersonDetailPage';
import ContactPage from '@/pages/ContactPage';
import NotFoundPage from '@/pages/NotFoundPage';

export const router = createBrowserRouter([
  { path: '/', element: <SplashPage /> },
  { path: '/pitch', element: <PitchPage /> },
  { path: '/pitch/tecnico', element: <PitchTecnicoPage /> },
  {
    path: '/app',
    element: <AppShell />,
    children: [
      { index: true, element: <Navigate to="/app/dashboard" replace /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'personas', element: <PersonsPage /> },
      { path: 'personas/:passport', element: <PersonDetailPage /> },
      { path: 'contacto', element: <ContactPage /> },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
]);
