import { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { ChevronLeft, ChevronRight, X } from 'lucide-react';
import { cn } from '@/lib/cn';
import type { SlideComponent } from './types';

type Props = {
  slides: SlideComponent[];
  onExit: () => void;
};

export default function Carousel({ slides, onExit }: Props) {
  const [emblaRef, embla] = useEmblaCarousel({ loop: false, align: 'start' });
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
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        goNext();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goPrev();
      } else if (e.key === 'Escape') {
        onExit();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [goNext, goPrev, onExit]);

  const total = slides.length;
  const Current = slides[selected];
  const theme = Current?.meta?.theme ?? 'dark';
  const themeBg =
    theme === 'accent' ? 'bg-accent text-bg' : theme === 'inverse' ? 'bg-text text-bg' : 'bg-bg text-text';

  return (
    <div className={cn('fixed inset-0 z-40 flex flex-col', themeBg)}>
      <div className="embla flex-1" ref={emblaRef}>
        <div className="embla__container">
          {slides.map((Slide, i) => (
            <div className="embla__slide" key={i}>
              <Slide
                index={i}
                total={total}
                goNext={goNext}
                goPrev={goPrev}
                exitPitch={onExit}
              />
            </div>
          ))}
        </div>
      </div>

      <div className="pointer-events-none absolute inset-x-0 top-0 flex items-center justify-between p-4">
        <span className="pointer-events-auto rounded-full border border-border/60 bg-bg/40 px-3 py-1 text-xs uppercase tracking-widest text-text/70 backdrop-blur">
          {selected + 1} / {total}
        </span>
        <button
          type="button"
          onClick={onExit}
          className="pointer-events-auto inline-flex items-center gap-2 rounded-full border border-border/60 bg-bg/40 px-4 py-2 text-sm text-text/80 backdrop-blur transition hover:border-accent hover:text-text"
        >
          <X className="h-4 w-4" aria-hidden /> Omitir
        </button>
      </div>

      <button
        type="button"
        aria-label="Anterior"
        onClick={goPrev}
        disabled={selected === 0}
        className="absolute left-4 top-1/2 -translate-y-1/2 rounded-full border border-border/60 bg-bg/40 p-3 text-text/80 backdrop-blur transition hover:border-accent hover:text-text disabled:pointer-events-none disabled:opacity-30"
      >
        <ChevronLeft className="h-6 w-6" aria-hidden />
      </button>
      <button
        type="button"
        aria-label="Siguiente"
        onClick={goNext}
        disabled={selected === total - 1}
        className="absolute right-4 top-1/2 -translate-y-1/2 rounded-full border border-border/60 bg-bg/40 p-3 text-text/80 backdrop-blur transition hover:border-accent hover:text-text disabled:pointer-events-none disabled:opacity-30"
      >
        <ChevronRight className="h-6 w-6" aria-hidden />
      </button>

      <div className="absolute inset-x-0 bottom-6 flex items-center justify-center gap-2">
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
