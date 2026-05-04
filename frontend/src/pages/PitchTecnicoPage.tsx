import { useNavigate } from 'react-router-dom';
import Carousel from '@/pitch/Carousel';
import { slidesTech } from '@/pitch/slides-tech';

export default function PitchTecnicoPage() {
  const navigate = useNavigate();
  return <Carousel slides={slidesTech} onExit={() => navigate('/app/dashboard')} />;
}
