import { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { ChevronLeft, ChevronRight, Linkedin } from 'lucide-react';
import { cn } from '@/lib/cn';
import usImg from '@/assets/contact/us.png';
import marImg from '@/assets/contact/mar.png';
import michelleImg from '@/assets/contact/michelle.png';
import robImg from '@/assets/contact/rob.png';

type Slide =
  | { kind: 'thanks'; image: string }
  | { kind: 'person'; image: string; name: string; linkedin: string };

const slides: Slide[] = [
  { kind: 'thanks', image: usImg },
  {
    kind: 'person',
    image: marImg,
    name: 'Mar Izquierdo Vaquer',
    linkedin: 'https://www.linkedin.com/in/mar-izquierdo-vaquer/',
  },
  {
    kind: 'person',
    image: michelleImg,
    name: 'Michelle Gelves',
    linkedin: 'https://www.linkedin.com/in/michellegelves/',
  },
  {
    kind: 'person',
    image: robImg,
    name: 'Roberto Molero',
    linkedin: 'https://www.linkedin.com/in/ruperthlosada/',
  },
];

export default function ContactPage() {
  const [emblaRef, embla] = useEmblaCarousel({ loop: true, align: 'center' });
  const [selected, setSelected] = useState(0);

  const goNext = useCallback(() => embla?.scrollNext(), [embla]);
  const goPrev = useCallback(() => embla?.scrollPrev(), [embla]);
  const goTo = useCallback((i: number) => embla?.scrollTo(i), [embla]);

  useEffect(() => {
    if (!embla) return;
    const onSelect = () => setSelected(embla.selectedScrollSnap());
    onSelect();
    embla.on('select', onSelect);
    embla.on('reInit', onSelect);
    return () => {
      embla.off('select', onSelect);
      embla.off('reInit', onSelect);
    };
  }, [embla]);

  useEffect(() => {
    if (!embla) return;
    const id = window.setInterval(() => embla.scrollNext(), 3000);
    return () => window.clearInterval(id);
  }, [embla]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        goNext();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goPrev();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [goNext, goPrev]);

  return (
    <div className="mx-auto flex w-full max-w-5xl flex-col items-center">
      <div className="relative w-full">
        <div className="embla overflow-hidden" ref={emblaRef}>
          <div className="embla__container">
            {slides.map((slide, i) => (
              <div className="embla__slide flex items-center justify-center px-4 py-6" key={i}>
                {slide.kind === 'thanks' ? (
                  <div className="flex w-full max-w-2xl flex-col items-center gap-8">
                    <div className="overflow-hidden rounded-2xl border border-border bg-surface shadow-2xl">
                      <img
                        src={slide.image}
                        alt="Equipo Talent Vault"
                        className="h-auto w-full object-cover"
                      />
                    </div>
                    <h1 className="animate-logo-pulse text-8xl font-bold tracking-tight text-text drop-shadow-[0_0_40px_hsl(var(--accent)/0.45)] md:text-9xl">
                      Gracias
                    </h1>
                  </div>
                ) : (
                  <a
                    href={slide.linkedin}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="group flex w-full max-w-2xl flex-col items-center gap-5"
                  >
                    <div className="aspect-[3/2] w-full overflow-hidden rounded-2xl border border-border bg-surface shadow-2xl transition group-hover:border-accent">
                      <img
                        src={slide.image}
                        alt={slide.name}
                        className="h-full w-full object-contain transition group-hover:scale-[1.02]"
                      />
                    </div>
                    <div className="flex flex-col items-center gap-2">
                      <h2 className="text-2xl font-semibold text-text">{slide.name}</h2>
                      <span className="inline-flex items-center gap-2 text-sm text-muted transition group-hover:text-accent">
                        <Linkedin className="h-4 w-4" aria-hidden />
                        {slide.linkedin.replace('https://www.', '')}
                      </span>
                    </div>
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>

        <button
          type="button"
          aria-label="Anterior"
          onClick={goPrev}
          className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full border border-border bg-surface/80 p-3 text-text/80 backdrop-blur transition hover:border-accent hover:text-text"
        >
          <ChevronLeft className="h-6 w-6" aria-hidden />
        </button>
        <button
          type="button"
          aria-label="Siguiente"
          onClick={goNext}
          className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full border border-border bg-surface/80 p-3 text-text/80 backdrop-blur transition hover:border-accent hover:text-text"
        >
          <ChevronRight className="h-6 w-6" aria-hidden />
        </button>
      </div>

      <div className="mt-6 flex items-center justify-center gap-2">
        {slides.map((_, i) => (
          <button
            key={i}
            type="button"
            aria-label={`Ir al slide ${i + 1}`}
            onClick={() => goTo(i)}
            className={cn(
              'h-2 rounded-full transition-all',
              i === selected ? 'w-8 bg-accent' : 'w-2 bg-text/30 hover:bg-text/50',
            )}
          />
        ))}
      </div>
    </div>
  );
}
