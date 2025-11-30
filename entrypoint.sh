#!/bin/bash

# For local Docker development only
# Render uses build.sh and gunicorn directly

echo "Waiting for PostgreSQL to be ready..."
python << END
import sys
import time
import psycopg2

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            dbname="bookstore",
            user="bookstore_user",
            password="securepassword",
            host="db",
            port="5432"
        )
        conn.close()
        print("PostgreSQL is ready!")
        sys.exit(0)
    except psycopg2.OperationalError:
        retry_count += 1
        time.sleep(1)

print("Failed to connect to PostgreSQL after 30 attempts")
sys.exit(1)
END

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking if database needs population..."
python manage.py shell -c "from books.models import Book; exit(0 if Book.objects.count() > 0 else 1)" 2>/dev/null
if [ $? -eq 1 ]; then
  echo "Populating database with initial data..."
  python manage.py populate_db
else
  echo "Database already populated, skipping..."
fi

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
