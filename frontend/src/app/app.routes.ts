
import { Routes } from '@angular/router';

import { Inicio } from './pages/inicio/inicio';
import { Catalogo } from './pages/catalogo/catalogo';
import { Contato } from './pages/contato/contato';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'inicio',
    pathMatch: 'full'
  },
  {
    path: 'inicio',
    component: Inicio
  },
  {
    path: 'servicos',
    component: Catalogo
  },
  {
    path: 'contato',
    component: Contato
  },
  {
    path: '**',
    redirectTo: 'inicio'
  }
];
