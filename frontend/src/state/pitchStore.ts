import { create } from 'zustand';

type PitchState = {
  pitchSeen: boolean;
  markSeen: () => void;
  reset: () => void;
};

export const usePitchStore = create<PitchState>((set) => ({
  pitchSeen: false,
  markSeen: () => set({ pitchSeen: true }),
  reset: () => set({ pitchSeen: false }),
}));
