# Bookstore Frontend

A modern React TypeScript frontend for the Django Bookstore backend.

## Features

- 📚 Book catalog with search and filters
- 🛒 Shopping cart functionality
- 👤 User authentication (login/register)
- 💳 Checkout process
- 📱 Responsive design
- 🎨 Modern UI with Tailwind CSS

## Tech Stack

- React 19
- TypeScript
- Vite
- React Router
- Zustand (state management)
- TanStack Query (data fetching)
- Axios (HTTP client)
- Tailwind CSS (styling)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Django backend running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── services/      # API service functions
├── stores/        # Zustand state stores
├── types/         # TypeScript type definitions
└── utils/         # Utility functions
```

## API Integration

The frontend connects to the Django REST API at `http://localhost:8000/api/`.

### Endpoints Used

- `/api/auth/` - Authentication
- `/api/books/` - Books CRUD
- `/api/authors/` - Authors
- `/api/editorials/` - Editorials
- `/api/cart/` - Shopping cart operations

## Environment Variables

Create a `.env` file if you need to change the API URL:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Features Overview

### Authentication
- User registration
- Login/logout
- Protected routes
- Session-based authentication

### Book Catalog
- Browse all books
- Search functionality
- Filter by author, condition, price
- Book details page

### Shopping Cart
- Add/remove items
- Update quantities
- View cart total
- Checkout process

## Development Notes

- The app uses session-based authentication (cookies)
- CORS is configured in Django backend for `localhost:5173`
- State is persisted using Zustand with localStorage
- React Query handles server state and caching
