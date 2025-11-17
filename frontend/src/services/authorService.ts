import api from './api';
import type { Author } from '../types';

export const authorService = {
  getAllAuthors: async (): Promise<Author[]> => {
    const response = await api.get('/authors/');
    // Handle paginated response or direct array
    if (Array.isArray(response.data)) {
      return response.data;
    } else if (response.data.results && Array.isArray(response.data.results)) {
      // Paginated response
      return response.data.results;
    } else {
      console.error('Unexpected authors response format:', response.data);
      return [];
    }
  },

  getAuthor: async (id: number): Promise<Author> => {
    const response = await api.get<Author>(`/authors/${id}/`);
    return response.data;
  },

  createAuthor: async (data: Partial<Author>): Promise<Author> => {
    const response = await api.post<Author>('/authors/', data);
    return response.data;
  },
};

