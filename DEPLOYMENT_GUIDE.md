# Deployment Comparison: Docker vs Render

## Current Setup

Your project now supports **BOTH** local Docker development AND Render deployment.

### For Local Development (Docker)
```bash
docker-compose up -d
```
- Uses `docker-compose.yml`
- Uses `entrypoint.sh`
- PostgreSQL 15 in container
- DEBUG = True (unless you set DEBUG=False env var)
- Development server (runserver)

### For Render Deployment
```bash
# Render automatically runs:
./build.sh
gunicorn bookstore.wsgi:application
```
- Uses `render.yaml` (optional)
- Uses `build.sh`
- Managed PostgreSQL database
- DEBUG = False (production)
- Gunicorn production server

## Key Files for Render

✅ **requirements.txt** - Updated with production dependencies
✅ **build.sh** - Build script for Render
✅ **render.yaml** - Infrastructure as Code (optional)
✅ **settings.py** - Environment-aware configuration
✅ **.env.example** - Template for environment variables
✅ **RENDER_DEPLOYMENT.md** - Complete deployment guide

## What Changed

### settings.py
- ✅ SECRET_KEY from environment variable
- ✅ DEBUG from environment variable (default: False)
- ✅ ALLOWED_HOSTS from environment variable
- ✅ DATABASE_URL support (dj-database-url)
- ✅ WhiteNoise for static files
- ✅ CORS_ALLOWED_ORIGINS from environment variable
- ✅ Security headers enabled in production
- ✅ Backwards compatible with Docker

### requirements.txt
- ✅ Added `gunicorn` - Production WSGI server
- ✅ Added `whitenoise` - Static file serving
- ✅ Added `dj-database-url` - Parse DATABASE_URL

### New Files
- ✅ `build.sh` - Render build commands
- ✅ `render.yaml` - Auto-deployment config
- ✅ `.env.example` - Environment variables template
- ✅ `RENDER_DEPLOYMENT.md` - Deployment instructions

## Quick Start Guide

### Local Development
```bash
# 1. Start Docker
docker-compose up -d

# 2. Check logs
docker-compose logs -f web

# 3. Access API
http://localhost:8000/api/books/
```

### Deploy to Render
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for Render"
git push

# 2. In Render Dashboard:
- Create Web Service
- Connect GitHub repo
- Set build command: ./build.sh
- Set start command: gunicorn bookstore.wsgi:application
- Add environment variables (see RENDER_DEPLOYMENT.md)
- Create PostgreSQL database
- Link database to web service
- Deploy!

# 3. Access your API
https://your-app.onrender.com/api/books/
```

## Environment Variables for Render

**Required:**
- `SECRET_KEY` - Generate new one (NOT the default!)
- `DATABASE_URL` - Provided by Render PostgreSQL
- `ALLOWED_HOSTS` - Your Render domain (e.g., `yourapp.onrender.com`)

**Recommended:**
- `CORS_ALLOWED_ORIGINS` - Your frontend URL
- `CSRF_TRUSTED_ORIGINS` - Your frontend URL
- `DEBUG` - Leave as `False` or omit

**Optional:**
- `PYTHON_VERSION` - `3.10.4`

## Testing Before Deployment

Test production settings locally:
```bash
# Set environment variables
export DEBUG=False
export SECRET_KEY="test-secret-key-change-in-production"
export ALLOWED_HOSTS="localhost,127.0.0.1"
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"

# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn bookstore.wsgi:application
```

## Differences Between Environments

| Feature | Docker (Dev) | Render (Prod) |
|---------|-------------|---------------|
| Server | runserver | gunicorn |
| DEBUG | True | False |
| Database | Docker PostgreSQL | Managed PostgreSQL |
| Static Files | Django serves | WhiteNoise serves |
| HTTPS | No | Yes (automatic) |
| Domain | localhost:8000 | yourapp.onrender.com |
| CORS | All origins | Specific origins |
| Secrets | In docker-compose | Environment variables |

## Important Security Notes

🔒 **For Production (Render):**
- Never use the default SECRET_KEY
- Always set DEBUG=False
- Specify exact ALLOWED_HOSTS
- Limit CORS_ALLOWED_ORIGINS to your frontend
- Use HTTPS URLs only
- Keep environment variables secret

🔓 **For Development (Docker):**
- Can use default SECRET_KEY
- DEBUG=True is fine
- CORS_ALLOW_ALL_ORIGINS is OK
- HTTP is acceptable

## Next Steps

1. **Test locally** with Docker to ensure everything works
2. **Read RENDER_DEPLOYMENT.md** for detailed instructions
3. **Generate a new SECRET_KEY** for production
4. **Push to GitHub**
5. **Deploy on Render**
6. **Update frontend** to use your Render backend URL

## Troubleshooting

### Docker not working?
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Render deployment failing?
- Check Render logs in dashboard
- Verify all environment variables are set
- Ensure build.sh has correct line endings (use `dos2unix build.sh` if needed)
- Check DATABASE_URL is connected

### Static files not loading on Render?
- Verify WhiteNoise is in MIDDLEWARE
- Check STATIC_ROOT is set
- Ensure collectstatic runs in build.sh
