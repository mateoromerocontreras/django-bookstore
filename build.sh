#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Only populate database if it's empty
python manage.py shell -c "from books.models import Book; exit(0 if Book.objects.count() > 0 else 1)" 2>/dev/null || python manage.py populate_db
