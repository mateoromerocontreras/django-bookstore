import { create } from 'zustand';
import type { Cart } from '../types';
import { cartService } from '../services/cartService';

interface CartState {
  cart: Cart | null;
  isLoading: boolean;
  error: string | null;
  fetchCart: () => Promise<void>;
  addToCart: (bookId: number, quantity: number) => Promise<void>;
  updateCartItem: (bookId: number, quantity: number) => Promise<void>;
  removeFromCart: (bookId: number) => Promise<void>;
  clearCart: () => Promise<void>;
  checkout: () => Promise<void>;
  getCartItemCount: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  isLoading: false,
  error: null,

  fetchCart: async () => {
    set({ isLoading: true, error: null });
    try {
      const cart = await cartService.getCart();
      set({ cart, isLoading: false });
    } catch (error: any) {
      set({ error: error.error || 'Failed to fetch cart', isLoading: false });
    }
  },

  addToCart: async (bookId: number, quantity: number) => {
    set({ isLoading: true, error: null });
    try {
      await cartService.addItem(bookId, quantity);
      await get().fetchCart();
    } catch (error: any) {
      set({ error: error.error || 'Failed to add item to cart', isLoading: false });
      throw error;
    }
  },

  updateCartItem: async (bookId: number, quantity: number) => {
    set({ isLoading: true, error: null });
    try {
      await cartService.updateItem(bookId, quantity);
      await get().fetchCart();
    } catch (error: any) {
      set({ error: error.error || 'Failed to update cart item', isLoading: false });
      throw error;
    }
  },

  removeFromCart: async (bookId: number) => {
    set({ isLoading: true, error: null });
    try {
      await cartService.removeItem(bookId);
      await get().fetchCart();
    } catch (error: any) {
      set({ error: error.error || 'Failed to remove item from cart', isLoading: false });
      throw error;
    }
  },

  clearCart: async () => {
    set({ isLoading: true, error: null });
    try {
      await cartService.clearCart();
      await get().fetchCart();
    } catch (error: any) {
      set({ error: error.error || 'Failed to clear cart', isLoading: false });
      throw error;
    }
  },

  checkout: async () => {
    set({ isLoading: true, error: null });
    try {
      await cartService.checkout();
      await get().fetchCart();
    } catch (error: any) {
      set({ error: error.error || 'Failed to checkout', isLoading: false });
      throw error;
    }
  },

  getCartItemCount: () => {
    const cart = get().cart;
    if (!cart || !cart.items) return 0;
    return cart.items.reduce((sum, item) => sum + item.quantity, 0);
  },
}));

