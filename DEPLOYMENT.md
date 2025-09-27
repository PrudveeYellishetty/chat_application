# 🚀 PLP Chat - Cloud Deployment Guide

## Option 1: Deploy to Render.com (Recommended - Free Tier)

### Step 1: Prepare Your Repository
1. Push all files to a GitHub repository
2. Make sure these files are included:
   - `server.py`
   - `requirements.txt`
   - `Procfile`
   - `.env` (optional, set via Render dashboard)

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `plp-chat-server` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
In Render dashboard, add these environment variables:
- `SECRET_KEY`: Generate a secure random string (e.g., using `openssl rand -hex 32`)
- `DATABASE_URL`: `sqlite:///./plp_chat.db` (or use PostgreSQL for production)

### Step 4: Deploy
- Click "Create Web Service"
- Wait for deployment (usually 2-3 minutes)
- Note your app URL: `https://your-app-name.onrender.com`

### Step 5: Update Client
Edit `client.py` line 19-20:
```python
CLIENT_CONFIG = {
    "server_url": "https://your-app-name.onrender.com",
    "websocket_url": "wss://your-app-name.onrender.com",
    # ... rest of config
}
```

---

## Option 2: Deploy to Railway (Alternative Free Option)

### Step 1: Prepare Repository
Same as Render - push to GitHub with all necessary files.

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy

### Step 3: Set Environment Variables
In Railway dashboard:
- `SECRET_KEY`: Your secure random string
- `PORT`: Railway sets this automatically

### Step 4: Get URL and Update Client
- Railway will provide your app URL
- Update `client.py` with your Railway URL

---

## Option 3: Deploy to Heroku (Paid but Reliable)

### Step 1: Install Heroku CLI
Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-plp-chat-app

# Set environment variables
heroku config:set SECRET_KEY=your-super-secret-key

# Deploy
git push heroku main
```

### Step 3: Update Client
Update `client.py` with your Heroku URL: `https://your-plp-chat-app.herokuapp.com`

---

## 🧪 Testing Your Deployment

### Test Server Health
Visit your deployed URL in browser:
```
https://your-app-name.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-27T...",
  "active_connections": 0
}
```

### Test API Documentation
Visit:
```
https://your-app-name.onrender.com/docs
```

You should see the FastAPI interactive documentation.

---

## 📱 Distributing the Client

### Option 1: Simple Distribution
1. Update `client.py` with your server URL
2. Send the updated `client.py` file to your contact
3. They just need to run: `pip install -r requirements.txt` then `python client.py`

### Option 2: Standalone Executable (Advanced)
Create a standalone executable using PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile client.py
```

This creates a single executable file that doesn't require Python installation.

---

## 🔒 Production Security Checklist

- [ ] Change `SECRET_KEY` to a random 32+ character string
- [ ] Use PostgreSQL instead of SQLite for production
- [ ] Enable HTTPS (automatic with Render/Railway/Heroku)
- [ ] Add rate limiting to prevent spam
- [ ] Consider adding message encryption
- [ ] Monitor server logs for suspicious activity
- [ ] Set up backup for database

---

## 🐛 Troubleshooting Deployment

### Common Issues

**Build fails with "requirements not found"**
- Make sure `requirements.txt` is in root directory
- Check file has correct dependencies

**Server starts but crashes immediately**
- Check environment variables are set correctly
- Look at deployment logs for error messages
- Ensure `SECRET_KEY` is set

**Client can't connect**
- Verify server URL is correct in `client.py`
- Check if server is actually running (visit `/health` endpoint)
- Ensure firewall/network allows HTTPS traffic

**WebSocket connection fails**
- Some networks block WebSocket connections
- App will still work without real-time updates
- Check if WSS (WebSocket Secure) is properly configured

### Getting Help
- Check deployment platform documentation
- Look at server logs in platform dashboard
- Test API endpoints directly in browser

---

## 🎯 Quick Deployment Summary

1. **Push code to GitHub**
2. **Connect to Render/Railway**
3. **Set SECRET_KEY environment variable**
4. **Deploy (usually takes 2-5 minutes)**
5. **Update client.py with your server URL**
6. **Test with /health endpoint**
7. **Share client.py with your contact**

Your stealth chat system is now running in the cloud! 🚀