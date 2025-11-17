import api from './api';
import type { User, LoginCredentials, RegisterData } from '../types';

export const authService = {
  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post<User>('/auth/register/', data);
    return response.data;
  },

  login: async (credentials: LoginCredentials): Promise<User> => {
    const response = await api.post<User>('/auth/login/', credentials);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout/');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/user/');
    return response.data;
  },
};

