export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Author {
  id: number;
  name: string;
  bio?: string;
  birth_date?: string;
  nationality?: string;
  created_at: string;
  updated_at: string;
}

export interface Editorial {
  id: number;
  name: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  created_at: string;
  updated_at: string;
}

export interface Book {
  id: number;
  title: string;
  isbn: string;
  description?: string;
  publication_date?: string;
  price: string;
  condition: 'new' | 'like_new' | 'good' | 'fair' | 'poor';
  pages?: number;
  language: string;
  author: Author;
  author_id?: number;
  editorial: Editorial;
  editorial_id?: number;
  seller: User;
  seller_id?: number;
  quantity: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface BookList {
  id: number;
  title: string;
  isbn: string;
  price: string;
  condition: string;
  quantity: number;
  is_available: boolean;
  author_name: string;
  editorial_name: string;
  seller_username: string;
  created_at: string;
}

export interface CartItem {
  id: number;
  book: Book;
  book_id?: number;
  quantity: number;
  subtotal: string;
  created_at: string;
  updated_at: string;
}

export interface Cart {
  id: number;
  user: number;
  items: CartItem[];
  total: string;
  created_at: string;
  updated_at: string;
}

export interface CheckoutResponse {
  message: string;
  purchased_items: {
    book: string;
    quantity: number;
    price: string;
    subtotal: string;
  }[];
  total: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface ApiError {
  error?: string;
  errors?: string[];
  [key: string]: any;
}

