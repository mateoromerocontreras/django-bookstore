import api from './api';
import type { Cart, CartItem, CheckoutResponse } from '../types';

export const cartService = {
  getCart: async (): Promise<Cart> => {
    const response = await api.get<Cart>('/cart/');
    return response.data;
  },

  addItem: async (bookId: number, quantity: number): Promise<CartItem> => {
    const response = await api.post<CartItem>('/cart/add_item/', {
      book_id: bookId,
      quantity,
    });
    return response.data;
  },

  updateItem: async (bookId: number, quantity: number): Promise<CartItem> => {
    const response = await api.put<CartItem>('/cart/update_item/', {
      book_id: bookId,
      quantity,
    });
    return response.data;
  },

  removeItem: async (bookId: number): Promise<void> => {
    await api.delete(`/cart/remove_item/?book_id=${bookId}`);
  },

  clearCart: async (): Promise<void> => {
    await api.post('/cart/clear/');
  },

  checkout: async (): Promise<CheckoutResponse> => {
    const response = await api.post<CheckoutResponse>('/cart/checkout/');
    return response.data;
  },
};

