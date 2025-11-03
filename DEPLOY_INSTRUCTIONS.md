# How to Deploy Your App to Hugging Face Spaces

## Step 1: Create the Space Manually

1. Go to https://huggingface.co/spaces
2. Click the **"Create new Space"** button (top right)
3. Fill in the form:
   - **Space name**: `career_conversations`
   - **SDK**: Select **Gradio**
   - **Hardware**: Select **CPU basic** (free)
   - **Visibility**: Choose **Public** or **Private**
4. Click **"Create Space"**

## Step 2: Upload Your Files

After the Space is created, you have two options:

### Option A: Upload via Web Interface (Easiest)

1. In your Space, click on the **"Files and versions"** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload these files one by one:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. For the `me/` folder:
   - Click **"Add file"** → **"Create new file"**
   - File path: `me/linkedin.pdf`
   - Upload the PDF file
   - Repeat for `me/summary.txt`

### Option B: Use Git (Recommended)

1. In your Space, you'll see Git instructions. Copy the repository URL
2. In your terminal, navigate to the `1_foundations` folder:

```bash
cd /Users/mac/Desktop/projects/agents/1_foundations
```

3. Initialize git (if not already done):
```bash
git init
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/career_conversations
```

4. Add and commit files:
```bash
git add app.py requirements.txt README.md me/
git commit -m "Initial commit"
git push origin main
```

## Step 3: Add Secrets (IMPORTANT!)

1. In your Space, go to **Settings** (gear icon on the left sidebar)
2. Scroll down to **"Secrets"** section
3. Add these secrets (click "New secret" for each):

   **Secret 1:**
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key (starts with `sk-proj-...`)

   **Secret 2:**
   - Name: `PUSHOVER_USER`
   - Value: `u7uh5eu13yweg5purczxo48vka2zj2`

   **Secret 3:**
   - Name: `PUSHOVER_TOKEN`
   - Value: `aqfb6oyoohir6h5csmm7qukymogtic`

4. Click **"Save secrets"** for each one

## Step 4: Restart the Space

1. Click the **three dots menu** (⋯) at the top right
2. Select **"Restart this Space"**
3. Wait for it to rebuild (usually 1-2 minutes)

## Step 5: Test Your App

1. Once it's running, click the **"App"** tab
2. You should see your chat interface
3. Try sending a message!

## Troubleshooting

If you see errors:
- Make sure all secrets are added correctly
- Check that all files are uploaded (especially the `me/` folder)
- Restart the Space after adding secrets
- Check the **"Logs"** tab for error messages

## Your Space URL

Once deployed, your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/career_conversations
```

Replace `YOUR_USERNAME` with your actual Hugging Face username!


