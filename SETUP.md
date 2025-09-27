# PLP Setup Guide

## Local Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Server**
   ```bash
   python run_server.py
   ```

3. **Run Client**
   ```bash
   python client.py
   ```

## Usage

1. **Register/Login** when prompted
2. **Set Partner**: `plp partner username`
3. **Send Messages**: `plp send "message"`
4. **Receive**: `plp recv`
5. **History**: `plp hist`

## Configuration

**Server** (`.env`):
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./plp_chat.db
```

**Client** (`client.py` line 25):
```python
"server_url": "https://your-deployed-server.com"
```

## Deployment

See `DEPLOYMENT.md` for cloud deployment instructions.