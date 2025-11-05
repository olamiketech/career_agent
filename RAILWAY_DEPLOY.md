# How to Deploy Your App on Railway

Railway is a cloud platform that makes it easy to deploy applications. Here's a step-by-step guide to deploy your Gradio app.

## Prerequisites

- A Railway account (free tier available)
- Your app files ready
- API keys (OpenAI, Pushover) ready

## Step 1: Create Railway Account

1. Go to https://railway.app
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with GitHub, Google, or email
4. Complete the setup

## Step 2: Install Railway CLI (Optional but Recommended)

While you can deploy via the web interface, the CLI is easier:

```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Or on Mac with Homebrew
brew install railway

# Login to Railway
railway login
```

## Step 3: Prepare Your Project Files

### 3.1: Create a `Procfile`

Railway needs to know how to run your app. Create a `Procfile` in your `1_foundations` directory:

**File: `Procfile`**
```
web: python -m uvicorn app:demo --host 0.0.0.0 --port $PORT
```

**Wait!** Gradio apps don't use uvicorn directly. Let's update this...

Actually, for Gradio, we need a different approach. Let's create a simple runner script.

### 3.2: Create `railway_start.py`

Create a file that Railway will use to start your app:

**File: `railway_start.py`**
```python
from app import create_ui
import os

if __name__ == "__main__":
    demo = create_ui()
    port = int(os.getenv("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )
```

### 3.3: Update `Procfile`

**File: `Procfile`**
```
web: python railway_start.py
```

### 3.4: Verify `requirements.txt`

Make sure your `requirements.txt` includes all dependencies:
```
requests
python-dotenv
gradio
pypdf
openai
openai-agents
```

## Step 4: Deploy to Railway

### Option A: Using Railway CLI (Recommended)

```bash
# Navigate to your project directory
cd /Users/mac/Desktop/projects/agents/1_foundations

# Initialize Railway project
railway init

# This will:
# - Create a new project on Railway
# - Link your local directory to Railway
# - Create a railway.json config file

# Deploy your app
railway up
```

### Option B: Using GitHub Integration (Easiest)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Connect GitHub to Railway:**
   - Go to https://railway.app/dashboard
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your repository
   - Railway will automatically detect it's a Python app

3. **Railway will:**
   - Detect your `requirements.txt`
   - Install dependencies
   - Start your app

### Option C: Using Web Interface

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Empty Project"**
4. Click **"Add Service"** → **"GitHub Repo"** (or **"Local Directory"** for CLI upload)
5. Select your repository

## Step 5: Set Environment Variables

After your project is created, add your secrets:

### Via Web Interface:
1. In your Railway project, click on your service
2. Go to the **"Variables"** tab
3. Click **"New Variable"**
4. Add each variable:

   - **Name:** `OPENAI_API_KEY`
   - **Value:** Your OpenAI API key

   - **Name:** `PUSHOVER_USER`
   - **Value:** `u7uh5eu13yweg5purczxo48vka2zj2`

   - **Name:** `PUSHOVER_TOKEN`
   - **Value:** `aqfb6oyoohir6h5csmm7qukymogtic`

### Via CLI:
```bash
railway variables set OPENAI_API_KEY="your-key-here"
railway variables set PUSHOVER_USER="u7uh5eu13yweg5purczxo48vka2zj2"
railway variables set PUSHOVER_TOKEN="aqfb6oyoohir6h5csmm7qukymogtic"
```

## Step 6: Configure Port and Deployment

Railway automatically sets a `PORT` environment variable. Make sure your app uses it:

- Our `railway_start.py` already handles this ✓

## Step 7: Deploy and Get URL

### Via CLI:
```bash
# Deploy
railway up

# Get your deployment URL
railway domain
```

### Via Web:
- Railway will automatically deploy
- Go to your service → **"Settings"** → **"Generate Domain"**
- Or use the default Railway domain

## Step 8: Verify Deployment

1. Check the **"Deployments"** tab for build logs
2. Check the **"Logs"** tab for runtime logs
3. Visit your Railway URL to test the app

## Troubleshooting

### Common Issues:

1. **Port not set correctly:**
   - Make sure you're reading `$PORT` or `os.getenv("PORT")`
   - Railway provides this automatically

2. **Dependencies not installing:**
   - Check `requirements.txt` has all packages
   - Check build logs in Railway dashboard

3. **App crashes on startup:**
   - Check logs in Railway dashboard
   - Make sure all environment variables are set
   - Verify file paths (Railway uses different paths than local)

4. **"me/" folder not found:**
   - Make sure all files are committed to git
   - Check that files are in the repository

### Check Logs:
```bash
# Via CLI
railway logs

# Or check in web dashboard → Logs tab
```

## File Structure for Railway

Your project should have:
```
1_foundations/
├── app.py              # Main application
├── railway_start.py    # Railway entry point
├── Procfile           # Tells Railway how to run
├── requirements.txt   # Python dependencies
├── README.md          # Documentation
└── me/
    ├── linkedin.pdf
    └── summary.txt
```

## Updating Your App

### Via CLI:
```bash
# Make changes to your code
# Then deploy
railway up
```

### Via GitHub:
- Just push to your repository
- Railway auto-deploys on push (if enabled)

## Railway vs Hugging Face Spaces

| Feature | Railway | Hugging Face Spaces |
|---------|---------|---------------------|
| **Free Tier** | Yes (with limits) | Yes |
| **Auto-deploy** | Yes (GitHub) | Yes |
| **Custom Domain** | Yes | No |
| **Environment Variables** | Easy to manage | Via Secrets |
| **File Upload** | Via Git | Via Git or Web UI |
| **Gradio Support** | Manual setup | Built-in |

## Cost

- **Free tier:** $5 credit/month
- **Paid plans:** Start at $5/month
- Check https://railway.app/pricing for details

## Next Steps

1. Create the `railway_start.py` file
2. Create the `Procfile`
3. Push to GitHub (if using GitHub integration)
4. Deploy to Railway
5. Set environment variables
6. Test your deployed app!



