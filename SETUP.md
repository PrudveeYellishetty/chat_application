# 🖥 PLP - Personal Learning Platform

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python run_server.py
```

### 3. Test the System
```bash
python test_system.py
```

### 4. Run the Client
```bash
python client.py
```

## 📋 Usage Examples

Once you run `python client.py`, you'll see the PLP interface:

### Authentication
- Register: Choose 'r' when prompted, create username and password
- Login: Choose 'l' when prompted, enter credentials

### Messaging Commands
```bash
plp send "Code review completed for feature-auth branch"
plp recv
plp hist alice
plp status
plp help
plp exit
```

## 🌐 Deployment

### Deploy to Render.com (Free)

1. Push your code to GitHub
2. Connect GitHub repo to Render
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Set `SECRET_KEY` to a secure random string

4. Update `client.py` line 19:
   ```python
   "server_url": "https://your-app-name.onrender.com"
   ```

### Deploy to Railway (Free)

1. Push code to GitHub
2. Connect to Railway
3. Set environment variable: `SECRET_KEY=your-secret-key`
4. Railway will auto-detect Python and deploy

## 🎭 Stealth Features

The client is designed to look like a development tool:

- **Professional terminal interface** with build-like outputs
- **Git-style command structure** (`plp` prefix)
- **Development terminology** (team updates, communication history)
- **Fake build/compile messages** for camouflage
- **Professional color scheme** and formatting

## 🔧 Configuration

### Server Configuration
Edit `.env` file:
```env
SECRET_KEY=your-super-secret-key
DATABASE_URL=sqlite:///./plp_chat.db
PORT=8000
```

### Client Configuration
Edit `CLIENT_CONFIG` in `client.py`:
```python
CLIENT_CONFIG = {
    "server_url": "https://your-server.onrender.com",
    "websocket_url": "wss://your-server.onrender.com"
}
```

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS in production (automatic with Render/Railway)
- Consider adding rate limiting for production use
- Messages are stored in plaintext (add encryption for sensitive use)

## 🐛 Troubleshooting

### Client won't connect
- Check server is running: `python run_server.py`
- Verify server URL in client.py
- Check firewall/network settings

### WebSocket issues
- Real-time updates require WebSocket support
- Some networks block WebSocket connections
- Client will still work with HTTP-only (polling mode)

### Database issues
- SQLite file is created automatically
- For production, use PostgreSQL (set DATABASE_URL)

## 📚 API Documentation

When server is running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Next Steps

1. **Test locally** with multiple client instances
2. **Deploy server** to cloud platform
3. **Share client.py** with your contacts
4. **Customize stealth features** as needed

---

**Have fun with your stealth terminal chat! 🚀**