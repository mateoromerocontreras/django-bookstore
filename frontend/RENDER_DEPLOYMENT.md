# Django Bookstore Frontend - Render Deployment

## Prerequisites
- Backend deployed on Render (see `/RENDER_DEPLOYMENT.md`)
- GitHub repository with frontend code

## Quick Deployment Steps

### 1. Push Code to GitHub

```bash
cd frontend
git add .
git commit -m "Configure frontend for Render deployment"
git push
```

### 2. Create Static Site on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `django-bookstore-frontend`
   - **Branch:** `render-deployment` (or `master`)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

### 3. Add Environment Variable

Add this environment variable in Render dashboard:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://your-backend-name.onrender.com/api` |

**Important:** Replace `your-backend-name` with your actual backend service name.

### 4. Deploy

Click **"Create Static Site"** and Render will:
- Install dependencies
- Build the React app
- Deploy to global CDN
- Provide HTTPS URL automatically

### 5. Update Backend CORS

After getting your frontend URL (e.g., `https://django-bookstore-frontend.onrender.com`), update your backend environment variables:

**In Backend Render Service:**
- `CORS_ALLOWED_ORIGINS`: `https://django-bookstore-frontend.onrender.com`
- `CSRF_TRUSTED_ORIGINS`: `https://django-bookstore-frontend.onrender.com`
- `ALLOWED_HOSTS`: `your-backend.onrender.com`

Then redeploy the backend.

## Configuration Files

✅ **Created:**
- `frontend/.env.example` - Environment variable template
- `frontend/render.yaml` - Optional Render configuration
- `frontend/_redirects` - SPA routing support
- Updated `src/services/api.ts` - Dynamic API URL

## Environment Variables

### Development (.env)
```bash
VITE_API_URL=http://localhost:8000/api
```

### Production (Render)
```bash
VITE_API_URL=https://your-backend-name.onrender.com/api
```

## SPA Routing

The `_redirects` file ensures all routes redirect to `index.html` for client-side routing with React Router.

## Testing Locally

Test with production-like settings:

```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000/api" > .env

# Build
npm run build

# Preview production build
npm run preview
```

## Deployment Checklist

- ✅ API URL uses environment variable
- ✅ Build command configured
- ✅ Publish directory set to `dist`
- ✅ Environment variable added on Render
- ✅ Backend CORS updated with frontend URL
- ✅ SPA redirects configured

## Alternative: Using render.yaml

If you prefer infrastructure-as-code:

1. Ensure `render.yaml` is in the frontend directory
2. In Render Dashboard: **New +** → **Blueprint**
3. Select your repository
4. Render auto-creates the static site

## Common Issues

### API requests fail with CORS error
- Check `VITE_API_URL` is set correctly
- Verify backend has frontend URL in `CORS_ALLOWED_ORIGINS`
- Ensure both use `https://` (not `http://`)

### 404 on page refresh
- Verify `_redirects` file exists
- Check publish directory is `dist`
- Ensure redirects are deployed

### Build fails
- Check Node.js version compatibility
- Run `npm install` and `npm run build` locally first
- Review build logs in Render dashboard

### Environment variable not working
- Environment variables must start with `VITE_`
- Restart deployment after adding env vars
- Check spelling and casing

## Free Tier Benefits

- ✅ **100GB bandwidth/month** (plenty for most apps)
- ✅ **Global CDN** (fast worldwide)
- ✅ **Auto SSL/HTTPS**
- ✅ **No cold starts** (instant loading)
- ✅ **Auto deploys** on git push
- ✅ **Custom domains** supported

## Production Best Practices

1. **Use HTTPS URLs only** - Both frontend and backend
2. **Set proper CORS** - Specific origins, not wildcard
3. **Monitor bandwidth** - Check Render dashboard
4. **Enable auto-deploy** - Deploy on push to main branch
5. **Test build locally** - Before pushing to production

## URLs After Deployment

You'll get URLs like:
- Frontend: `https://django-bookstore-frontend.onrender.com`
- Backend: `https://django-bookstore-backend.onrender.com`

Update these in respective environment variables!

## Next Steps

1. Deploy backend first (see `/RENDER_DEPLOYMENT.md`)
2. Get backend URL
3. Deploy frontend with backend URL in env var
4. Update backend CORS with frontend URL
5. Test the full application

## Troubleshooting

View logs in Render dashboard:
- Build logs show npm install/build output
- Access logs show static file requests
- Backend logs for API errors
