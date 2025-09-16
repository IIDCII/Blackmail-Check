# Railway Deployment Guide

## Prerequisites
1. [Railway.app](https://railway.app) account
2. GitHub repository with the Flask app
3. GROQ API key from [console.groq.com](https://console.groq.com)

## Deployment Steps

### 1. Connect Repository
1. Login to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `Blackmail-Check` repository
5. Select the `Blackmail-Scanner-Flask-Web` directory as root

### 2. Configure Environment Variables
In Railway dashboard, go to Variables tab and add:
```
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=production
```

### 3. Deploy
- Railway will automatically detect the `railway.toml` and `requirements.txt`
- The build will use the Nixpacks builder
- Start command: `gunicorn blackmail_file_scanner_frontend:app`

### 4. Custom Domain (Optional)
- In Settings tab, you can add a custom domain
- Railway provides a default domain like `yourapp.railway.app`

## Files Created for Railway

- `requirements.txt` - Python dependencies
- `Procfile` - Process definition for deployment
- `railway.toml` - Railway configuration
- `.gitignore` - Ignore unnecessary files
- Health check endpoint at `/health`

## Environment Variables Needed

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq vision model | Yes (for AI scanning) |
| `FLASK_ENV` | Set to `production` for production | No (defaults to development) |
| `PORT` | Port number (Railway sets automatically) | No |

## Testing the Deployment

After deployment, test these endpoints:
- `/` - Main application dashboard
- `/health` - Health check (returns JSON)
- `/scan` - Trigger new scan (requires GROQ_API_KEY)

## Monitoring

Railway provides:
- Real-time logs
- Metrics dashboard
- Automatic HTTPS
- Custom domains
- Environment management

## Troubleshooting

1. **Build fails**: Check `requirements.txt` for correct dependencies
2. **App won't start**: Verify `Procfile` and `railway.toml` configuration
3. **AI scanning fails**: Ensure GROQ_API_KEY is set correctly
4. **Database errors**: SQLite works on Railway, no additional setup needed