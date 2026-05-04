import { useNavigate } from 'react-router-dom';
import Carousel from '@/pitch/Carousel';
import { slides } from '@/pitch/slides';
import { usePitchStore } from '@/state/pitchStore';

export default function PitchPage() {
  const navigate = useNavigate();
  const markSeen = usePitchStore((s) => s.markSeen);

  const exit = () => {
    markSeen();
    navigate('/app/dashboard');
  };

  return <Carousel slides={slides} onExit={exit} />;
}
