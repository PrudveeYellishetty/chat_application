# 🚀 PLP Chat - Daily Use Deployment Guide

## Quick Deploy to Render.com (FREE - Recommended)

### Step 1: Prepare Repository
1. **Create GitHub Repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial PLP chat deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/plp-chat.git
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `plp-chat-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:
- **SECRET_KEY**: `generate-a-secure-32-character-random-string`
- **DATABASE_URL**: `sqlite:///./plp_chat.db`

### Step 4: Update Client Configuration
After deployment, you'll get a URL like `https://plp-chat-server.onrender.com`

Update your `client.py`:
```python
CLIENT_CONFIG = {
    "server_url": "https://YOUR-APP-NAME.onrender.com",
    "websocket_url": "wss://YOUR-APP-NAME.onrender.com",
    "app_name": "PLP - Personal Learning Platform",
    "version": "1.2.0",
    "partner_file": Path.home() / ".plp_partner"
}
```

## 🔥 Alternative: Railway.app (Also FREE)

1. Go to [railway.app](https://railway.app)
2. Click **"Deploy from GitHub"**
3. Select your repository
4. Railway will auto-deploy using your `Procfile`
5. Add environment variable: `SECRET_KEY`

## 🎯 For Daily Use Setup

### You (Primary User):
1. Deploy server using above steps
2. Update `client.py` with your server URL
3. Share the updated `client.py` with your friend

### Your Friend:
1. Install Python and dependencies:
   ```bash
   pip install requests websockets colorama
   ```
2. Run the client:
   ```bash
   python client.py
   ```

## 🔐 Security Setup

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📱 Daily Usage Workflow

1. **Server**: Runs 24/7 on cloud (no maintenance needed)
2. **You & Friend**: Just run `python client.py` anytime to chat
3. **Stealth Mode**: Looks like a development tool to anyone watching

## 🛠 Troubleshooting

**If deployment fails:**
- Check build logs in Render/Railway dashboard
- Ensure all files are committed to GitHub
- Verify `requirements.txt` includes all dependencies

**If client can't connect:**
- Check server URL in `client.py`
- Ensure server is running (check Render/Railway dashboard)
- Try `https://` instead of `http://`

## ✅ Success Checklist

- [ ] Server deployed and running
- [ ] Environment variables set
- [ ] Client updated with server URL
- [ ] Both users can register/login
- [ ] Messages send/receive successfully
- [ ] Partner persistence works across sessions

Your PLP chat is now ready for daily use! 🎉