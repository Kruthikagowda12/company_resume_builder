# Deployment Guide: Vercel + Neon

## Prerequisites
- GitHub account (for connecting to Vercel)
- Vercel account
- Neon account

## Step 1: Create Neon Project & Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Sign up/login and create a new project
3. Create a new PostgreSQL database (or use default)
4. Copy your DATABASE_URL connection string (looks like: `postgresql://user:password@ep-xxxxx.neon.tech/dbname`)

## Step 2: Prepare Your Django App

✅ Already done! Your app is configured to:
- Use Neon (PostgreSQL) when `DATABASE_URL` is set
- Use SQLite locally when `DATABASE_URL` is not set
- Serve static files using WhiteNoise
- Run migrations on deployment

## Step 3: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI (if not already installed)
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to your project
cd path/to/resume_builder

# Deploy (first time will link the project)
vercel deploy --prod
```

When prompted, enter your environment variables:
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `SECRET_KEY`: Generate new: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `ALLOWED_HOSTS`: `localhost,127.0.0.1` (will be overridden by VERCEL_URL in production)
- `DEBUG`: `false`

### Option B: Using GitHub Integration

1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Select your GitHub repository
5. Vercel will auto-detect Django
6. Add environment variables in **Settings > Environment Variables**:
   - `DATABASE_URL`: Your Neon connection string
   - `SECRET_KEY`: Generate using the command above
   - `DEBUG`: `false`
7. Click "Deploy"

## Step 4: Verify Deployment

After deployment:
1. Check Vercel dashboard for build logs
2. Visit your deployed URL
3. Test your resume builder app

## Troubleshooting

### Static files not loading
- Run: `python manage.py collectstatic --noinput`
- Ensure `STATIC_ROOT` is set (already configured)

### Database migration errors
- Check Neon database connection in Vercel env variables
- Verify `DATABASE_URL` format

### Connection timeout
- Whitelist Vercel IPs in Neon dashboard (if needed)
- Check database connection limits in Neon settings

## Local Development

To test with Neon locally:
1. Create `.env` file with:
   ```
   DATABASE_URL=your-neon-connection-string
   DEBUG=True
   SECRET_KEY=your-secret-key
   ```
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`

## Important Notes

- Keep `.env` file with production secrets **out of Git** (use `.env.example` for reference)
- Set `DEBUG=False` in production
- Use strong `SECRET_KEY` in production
- Monitor your Neon database usage in the Neon console
