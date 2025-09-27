# PLP (Personal Learning Platform) - Terminal Chat Tool

A stealth terminal-based chat application disguised as a coding productivity tool.

## 🚀 Quick Start

### Server Setup (Deploy Once)
1. Deploy server to cloud (Render/Railway)
2. Update `CLIENT_CONFIG` in `client.py` with your server URL

### Client Usage
```bash
python client.py
```

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `plp send "message"` | Send a message | `plp send "Hello there!"` |
| `plp recv` | Fetch unread messages | `plp recv` |
| `plp hist` | View chat history | `plp hist` |
| `plp status` | Check connection status | `plp status` |
| `plp clear` | Clear terminal history | `plp clear` |
| `plp exit` | Exit application | `plp exit` |

## 🎭 Stealth Features

- Looks like a development tool (PLP - Personal Learning Platform)
- Git-style command outputs
- Fake compiler/build messages
- Professional terminal interface

## 🏗️ Architecture

```
Client (Terminal) ←→ Cloud Server ←→ Database
     ↓                    ↓              ↓
  Python CLI          FastAPI       SQLite/PostgreSQL
  WebSocket           WebSocket         Messages
  HTTP Requests       REST API          User Auth
```

## 🔒 Security

- HTTPS/WSS encryption
- User authentication
- Message persistence
- Cross-platform support

## 🌟 Features

- ✅ Real-time messaging
- ✅ Persistent chat history
- ✅ Cross-network support
- ✅ Stealth mode interface
- ✅ Multi-user support
- ✅ Cloud deployment ready

Built for secure, professional communication disguised as development tooling.