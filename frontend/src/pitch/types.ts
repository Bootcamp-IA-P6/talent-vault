import type { FC } from 'react';

export type SlideProps = {
  index: number;
  total: number;
  goNext: () => void;
  goPrev: () => void;
  exitPitch: () => void;
};

export type SlideMeta = {
  title?: string;
  theme?: 'dark' | 'accent' | 'inverse';
};

export type SlideComponent = FC<SlideProps> & { meta?: SlideMeta };
