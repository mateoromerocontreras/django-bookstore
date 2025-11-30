# Django Bookstore - Full Stack E-commerce Application

**Live Application URL:** [https://django-bookstore-frontend.onrender.com/](https://django-bookstore-frontend.onrender.com/)

---

A full-stack e-commerce application for buying and selling used books. The project is containerized with Docker for easy local development and deployed to Render for production.

## 🚀 Deployment & Live API

This project is deployed on Render. The backend API is publicly accessible.

The entire application relies on a multi-service architecture defined via Docker Compose. This setup orchestrates three distinct, containerized services: the Django Backend, the PostgreSQL Database, and the React Frontend—all deployed and networked on Render for a production environment.

![System Architecture: Multi-Service Deployment on Render](diagrams/System_Architecture.png "System Architecture")

**API Base URL:** `https://django-bookstore-ed1i.onrender.com`
*You can test the public endpoint for books here: https://django-bookstore-ed1i.onrender.com/api/books/*

## 🚀 Features

### Backend (Django REST Framework)
- **RESTful API** with Django REST Framework
- **Dockerized** for consistent development and production environments
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
- **Containerized** for development and deployment
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
- Gunicorn (for production)
- django-cors-headers 3.10.1
- PostgreSQL (for development and production)

### Frontend
- React 19
- TypeScript
- Vite
- React Router
- Zustand (state management)
- TanStack Query (data fetching)
- Axios (HTTP client)
- Tailwind CSS (styling)

## 📦 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Local Development with Docker

The entire application (backend, frontend, and database) is containerized using Docker and Docker Compose, which is the recommended way to run it locally.

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/django-bookstore.git
    cd django-bookstore
    ```
    *Note: Remember to replace `your-username` with your actual GitHub username if you forked the repository.*

2.  **Build and Run the Application**
    In the root directory of the project, run the following command:
    ```bash
    docker-compose up -d --build
    ```
    This command will:
    - Build the Docker images for the backend and frontend services.
    - Start the containers for the backend, frontend, and PostgreSQL database.
    - You will see logs from all services in your terminal.

    Once the containers are running, the application will be available at:
    - **Frontend**: `http://localhost:5173`
    - **Backend API**: `http://localhost:8000`

3.  **Run Database Migrations and Other Commands**
    With the containers running, open a **new terminal window** and use `docker-compose exec` to run commands inside the `backend` service.

    - **Apply database migrations:**
      ```bash
      docker-compose exec backend python manage.py migrate
      ```

    - **Create a superuser (for Django Admin access):**
      ```bash
      docker-compose exec backend python manage.py createsuperuser
      ```

    - **Populate the database with sample data (optional):**
      ```bash
      docker-compose exec backend python manage.py populate_db
      ```

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
