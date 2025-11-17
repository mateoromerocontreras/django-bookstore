import { create } from 'zustand';
import type { Author } from '../types';

interface BookFilters {
  search: string;
  author: number | null;
  condition: string | null;
  minPrice: number | null;
  maxPrice: number | null;
}

interface BookState {
  filters: BookFilters;
  authors: Author[];
  setFilter: (key: keyof BookFilters, value: any) => void;
  resetFilters: () => void;
  setAuthors: (authors: Author[]) => void;
}

const initialFilters: BookFilters = {
  search: '',
  author: null,
  condition: null,
  minPrice: null,
  maxPrice: null,
};

export const useBookStore = create<BookState>((set) => ({
  filters: initialFilters,
  authors: [],

  setFilter: (key, value) => {
    set((state) => ({
      filters: { ...state.filters, [key]: value },
    }));
  },

  resetFilters: () => {
    set({ filters: initialFilters });
  },

  setAuthors: (authors) => {
    set({ authors });
  },
}));

