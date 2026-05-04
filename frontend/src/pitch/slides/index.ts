import type { SlideComponent } from '../types';
import Slide01Hook from './Slide01Hook';
import Slide02Problema from './Slide02Problema';
import Slide03Diferencial from './Slide03Diferencial';
import Slide04Empresa from './Slide04Empresa';
import Slide05Proceso from './Slide05Proceso';
// Slide06Tecnico ("Bajo el capó") reservado para un pitch técnico dedicado.
// import Slide06Tecnico from './Slide06Tecnico';
import Slide07Cierre from './Slide07Cierre';

export const slides: SlideComponent[] = [
  Slide01Hook,
  Slide02Problema,
  Slide03Diferencial,
  Slide04Empresa,
  Slide05Proceso,
  Slide07Cierre,
];
