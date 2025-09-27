# Deployment Checklist

## Before Deployment

- [ ] Change `SECRET_KEY` in `.env` to a secure random string
- [ ] Update server URL in `client.py` (CLIENT_CONFIG)
- [ ] Remove database file `plp_chat.db` (will be recreated)
- [ ] Test locally with `python run_server.py` and `python client.py`

## Deploy to Render/Railway

1. **Push to GitHub** (already done if you see this)
2. **Create new web service** on Render or Railway
3. **Environment variables**:
   - `SECRET_KEY`: Generate with `openssl rand -hex 32`
4. **Build/Start commands**:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`

## After Deployment

- [ ] Test server health: `https://your-app.onrender.com/health`
- [ ] Update client with deployed URL
- [ ] Share `client.py` with your partner
- [ ] Both register and set partners: `plp partner username`

## Files Ready for Deployment

✅ Essential files included:
- `server.py` - FastAPI backend
- `client.py` - Terminal client  
- `requirements.txt` - Dependencies
- `Procfile` - Deployment config
- `.env` - Environment template
- `README.md` - Documentation
- `DEPLOYMENT.md` - Deploy guide
- `SETUP.md` - Setup guide
- `.gitignore` - Git ignore rules

🗑️ Test files removed:
- All debug and test scripts cleaned up
- Development dependencies removed
- Logging simplified for production