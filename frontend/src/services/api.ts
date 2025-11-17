import axios from 'axios';
import type { ApiError } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

// Function to get CSRF token from cookies
function getCsrfToken(): string | null {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) {
      return decodeURIComponent(value);
    }
  }
  return null;
}

// Function to ensure CSRF token is available
let csrfTokenPromise: Promise<string> | null = null;

async function ensureCsrfToken(): Promise<string> {
  // Check if token exists in cookies
  let token = getCsrfToken();
  if (token) {
    return token;
  }

  // If no promise exists, create one
  if (!csrfTokenPromise) {
    csrfTokenPromise = axios
      .get(`${API_BASE_URL}/csrf-token/`, {
        withCredentials: true,
      })
      .then((response) => {
        const token = response.data.csrfToken || getCsrfToken();
        if (!token) {
          throw new Error('Failed to obtain CSRF token');
        }
        csrfTokenPromise = null; // Reset promise
        return token;
      })
      .catch((error) => {
        csrfTokenPromise = null; // Reset promise on error
        throw error;
      });
  }

  return csrfTokenPromise;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for session-based auth
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add CSRF token
api.interceptors.request.use(
  async (config) => {
    // Add CSRF token for POST, PUT, PATCH, DELETE requests
    if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase() || '')) {
      try {
        const token = await ensureCsrfToken();
        if (token) {
          config.headers['X-CSRFToken'] = token;
        }
      } catch (error) {
        console.error('Failed to get CSRF token:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      const apiError: ApiError = error.response.data || { error: 'An error occurred' };
      return Promise.reject(apiError);
    } else if (error.request) {
      // Request made but no response
      return Promise.reject({ error: 'Network error. Please check your connection.' });
    } else {
      // Something else happened
      return Promise.reject({ error: error.message });
    }
  }
);

export default api;

