# Django Bookstore - Render Deployment Guide

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier available)

## Deployment Steps

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Configure for Render deployment"
git push origin master
```

### 2. Create a New Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name:** `django-bookstore-backend`
- **Region:** Choose closest to your users
- **Branch:** `master`
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn bookstore.wsgi:application`

### 3. Add Environment Variables

In the Render dashboard, add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.10.4` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a strong random key |
| `ALLOWED_HOSTS` | Your Render URL (e.g., `django-bookstore-backend.onrender.com`) |
| `CORS_ALLOWED_ORIGINS` | Your frontend URL (e.g., `https://your-frontend.com`) |
| `CSRF_TRUSTED_ORIGINS` | Same as CORS (e.g., `https://your-frontend.com`) |

### 4. Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name:** `bookstore-db`
3. **Database:** `bookstore`
4. **User:** `bookstore_user`
5. **Region:** Same as your web service
6. Click **"Create Database"**

### 5. Connect Database to Web Service

1. Go to your web service settings
2. Add environment variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Internal Database URL from your PostgreSQL database

### 6. Deploy

Click **"Create Web Service"** or **"Deploy"**

The deployment will:
- Install dependencies
- Collect static files
- Run migrations
- Populate the database (first time only)
- Start Gunicorn server

### 7. Update Frontend API URL

Update your frontend to use the Render backend URL:
```typescript
// In src/services/api.ts
const API_URL = import.meta.env.VITE_API_URL || 'https://your-backend.onrender.com';
```

## Environment Variables Explained

- **SECRET_KEY:** Django secret (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- **DEBUG:** Always `False` in production
- **ALLOWED_HOSTS:** Comma-separated domains that can access your backend
- **CORS_ALLOWED_ORIGINS:** Comma-separated frontend URLs that can make API requests
- **CSRF_TRUSTED_ORIGINS:** Same as CORS, for CSRF protection
- **DATABASE_URL:** Automatically provided by Render PostgreSQL

## Important Notes

1. **Free Tier Limitations:**
   - Service spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - 750 hours/month free

2. **Database Persistence:**
   - Free PostgreSQL expires after 90 days
   - Data is lost if database is deleted
   - Backup regularly for production

3. **Static Files:**
   - Served via WhiteNoise (no separate CDN needed)
   - Automatically collected during build

4. **Security:**
   - HTTPS enabled by default
   - Environment variables encrypted
   - Database in private network

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure `build.sh` has execute permissions: `chmod +x build.sh`
- Verify all requirements are in `requirements.txt`

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check database is in same region as web service
- Ensure database is not suspended (free tier)

### CORS Errors
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Include protocol (https://)
- No trailing slash

### Static Files Not Loading
- Check `STATIC_ROOT` is set in settings
- Verify `collectstatic` runs in build script
- Ensure WhiteNoise is in MIDDLEWARE

## Alternative: Using render.yaml

Instead of manual configuration, you can use the included `render.yaml`:

1. Push code to GitHub
2. Go to Render Dashboard
3. Click **"New +"** → **"Blueprint"**
4. Select your repository
5. Render will automatically create services from `render.yaml`

## Monitoring

- **Logs:** Available in Render dashboard
- **Metrics:** CPU, Memory, Request count
- **Health Checks:** Automatic ping to keep service alive

## Upgrading from Free Tier

For production, consider:
- **Starter plan** ($7/month): No spin-down, better performance
- **Standard plan** ($25/month): Auto-scaling, more resources
- **PostgreSQL Standard** ($7/month): No expiration, automated backups
