import api from './api';
import type { Book, BookList } from '../types';

export const bookService = {
  getAllBooks: async (params?: { page?: number; search?: string }): Promise<{ results: BookList[]; count: number; next?: string; previous?: string }> => {
    const response = await api.get('/books/', { params });
    return response.data;
  },

  getBook: async (id: number): Promise<Book> => {
    const response = await api.get<Book>(`/books/${id}/`);
    return response.data;
  },

  createBook: async (data: Partial<Book>): Promise<Book> => {
    const response = await api.post<Book>('/books/', data);
    return response.data;
  },

  updateBook: async (id: number, data: Partial<Book>): Promise<Book> => {
    const response = await api.patch<Book>(`/books/${id}/`, data);
    return response.data;
  },

  deleteBook: async (id: number): Promise<void> => {
    await api.delete(`/books/${id}/`);
  },
};

