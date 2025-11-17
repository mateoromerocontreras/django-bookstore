# Django Bookstore - Full Stack E-commerce Application

A complete full-stack web application for buying and selling used books, built with Django REST Framework backend and React TypeScript frontend.

## 🚀 Features

### Backend (Django REST Framework)
- **RESTful API** with Django REST Framework
- **User Authentication** (register, login, logout)
- **Book Management** (CRUD operations)
- **Shopping Cart** functionality
- **Inventory Tracking** (quantity management)
- **Checkout Process** with automatic inventory reduction
- **CORS** configured for frontend integration
- **CSRF Protection** for secure requests

### Frontend (React + TypeScript + Vite)
- **Modern UI** with Tailwind CSS
- **Book Catalog** with search and filters
- **Shopping Cart** with real-time updates
- **User Authentication** pages
- **Responsive Design** (mobile-friendly)
- **Book Covers** from Open Library API
- **State Management** with Zustand
- **Data Fetching** with TanStack Query

## 📁 Project Structure

```
django-bookstore/
├── backend/              # Django backend
│   ├── bookstore/        # Django project settings
│   ├── books/            # Main app (models, views, serializers)
│   ├── manage.py
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── stores/       # Zustand stores
│   │   └── types/        # TypeScript types
│   └── package.json
└── README.md
```

## 🛠️ Tech Stack

### Backend
- Django 3.2.25
- Django REST Framework 3.14.0
- django-cors-headers 3.10.1
- SQLite (development)

### Frontend
- React 19
- TypeScript
- Vite
- React Router
- Zustand (state management)
- TanStack Query (data fetching)
- Axios (HTTP client)
- Tailwind CSS (styling)

## 📦 Installation

### Prerequisites
- Python 3.6+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd django-bookstore
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Populate database with sample data (optional)**
```bash
python manage.py populate_db
```

7. **Run development server**
```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/user/` - Get current user

### Books
- `GET /api/books/` - List all books
- `GET /api/books/{id}/` - Book details
- `POST /api/books/` - Create book (authenticated)
- `PUT/PATCH /api/books/{id}/` - Update book (owner only)
- `DELETE /api/books/{id}/` - Delete book (owner only)

### Authors
- `GET /api/authors/` - List authors
- `GET /api/authors/{id}/` - Author details
- `POST /api/authors/` - Create author

### Editorials
- `GET /api/editorials/` - List editorials
- `GET /api/editorials/{id}/` - Editorial details
- `POST /api/editorials/` - Create editorial

### Cart
- `GET /api/cart/` - View cart
- `POST /api/cart/add_item/` - Add item to cart
- `PUT /api/cart/update_item/` - Update item quantity
- `DELETE /api/cart/remove_item/` - Remove item
- `POST /api/cart/clear/` - Clear cart
- `POST /api/cart/checkout/` - Process checkout

## 🗄️ Database Models

- **Author**: name, bio, birth_date, nationality
- **Editorial**: name, address, phone, email, website
- **Book**: title, ISBN, description, price, condition, quantity, author, editorial, seller
- **Cart**: user's shopping cart
- **CartItem**: items in the cart with quantities

## 🎨 Features Overview

- **Book Catalog**: Browse books with search and filters (author, condition, price)
- **Book Details**: View detailed information about each book
- **Shopping Cart**: Add, update, and remove items
- **Checkout**: Process purchases with inventory management
- **User Authentication**: Secure login and registration
- **Book Covers**: Automatic book cover images from Open Library API

## 🔧 Configuration

### CORS Settings
The backend is configured to allow requests from:
- `http://localhost:3000`
- `http://localhost:5173` (Vite default)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

### Environment Variables
Create a `.env` file in the backend root for production settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

## 📝 Management Commands

- `python manage.py populate_db` - Populate database with sample classic books

## 🧪 Testing

### Backend
```bash
python manage.py test
```

### Frontend
```bash
cd frontend
npm run build  # Test production build
```

## 📄 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue in the repository.

