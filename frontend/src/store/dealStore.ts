import { create } from 'zustand';
import { Deal } from '../api/search';

interface DealStore {
  deals: Deal[];
  isLoading: boolean;
  error: string | null;
  setDeals: (deals: Deal[]) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearDeals: () => void;
}

export const useDealStore = create<DealStore>((set) => ({
  deals: [],
  isLoading: false,
  error: null,

  setDeals: (deals: Deal[]) => set({ deals }),

  setIsLoading: (loading: boolean) => set({ isLoading: loading }),

  setError: (error: string | null) => set({ error }),

  clearDeals: () => set({ deals: [], error: null }),
}));
