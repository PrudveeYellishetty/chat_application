#!/usr/bin/env python3
"""
PLP Server - Personal Learning Platform Chat Backend
A secure chat server disguised as a development tool backend.
"""

import os
import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # 30 days

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./plp_chat.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True, nullable=False)
    receiver = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    delivered = Column(Boolean, default=False)
    read = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    receiver: str
    message: str

class MessageResponse(BaseModel):
    id: int
    sender: str
    receiver: str
    message: str
    timestamp: datetime
    delivered: bool
    read: bool

class Token(BaseModel):
    access_token: str
    token_type: str

# FastAPI app
app = FastAPI(
    title="PLP Server",
    description="Personal Learning Platform - Development Tool Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Ensure password doesn't exceed bcrypt's 72 byte limit
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def get_current_user(db: Session = Depends(get_db), username: str = Depends(verify_token)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        logger.info(f"User {username} connected via WebSocket")

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
            logger.info(f"User {username} disconnected from WebSocket")

    async def send_personal_message(self, message: dict, username: str):
        if username in self.active_connections:
            try:
                await self.active_connections[username].send_text(json.dumps(message))
                return True
            except Exception as e:
                logger.error(f"Error sending message to {username}: {e}")
                self.disconnect(username)
        return False

manager = ConnectionManager()

# API Routes
@app.get("/")
async def root():
    return {
        "service": "PLP Development Server",
        "version": "1.0.0",
        "status": "active",
        "endpoints": ["/auth", "/messages", "/ws"]
    }

@app.post("/auth/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"New user registered: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/messages/send", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create message
    db_message = Message(
        sender=current_user.username,
        receiver=message_data.receiver,
        message=message_data.message,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Try to deliver via WebSocket
    message_dict = {
        "id": db_message.id,
        "sender": db_message.sender,
        "receiver": db_message.receiver,
        "message": db_message.message,
        "timestamp": db_message.timestamp.isoformat(),
        "type": "new_message"
    }
    
    delivered = await manager.send_personal_message(message_dict, message_data.receiver)
    if delivered:
        db_message.delivered = True
        db.commit()
    
    logger.info(f"Message sent from {current_user.username} to {message_data.receiver}")
    
    return MessageResponse(
        id=db_message.id,
        sender=db_message.sender,
        receiver=db_message.receiver,
        message=db_message.message,
        timestamp=db_message.timestamp,
        delivered=db_message.delivered,
        read=db_message.read
    )

@app.get("/messages/unread", response_model=List[MessageResponse])
async def get_unread_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    messages = db.query(Message).filter(
        Message.receiver == current_user.username,
        Message.read == False
    ).order_by(Message.timestamp).all()
    
    # Mark as read
    for message in messages:
        message.read = True
    db.commit()
    
    logger.info(f"Retrieved {len(messages)} unread messages for {current_user.username}")
    
    return [MessageResponse(
        id=msg.id,
        sender=msg.sender,
        receiver=msg.receiver,
        message=msg.message,
        timestamp=msg.timestamp,
        delivered=msg.delivered,
        read=msg.read
    ) for msg in messages]

@app.get("/messages/history", response_model=List[MessageResponse])
async def get_message_history(
    other_user: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    messages = db.query(Message).filter(
        ((Message.sender == current_user.username) & (Message.receiver == other_user)) |
        ((Message.sender == other_user) & (Message.receiver == current_user.username))
    ).order_by(Message.timestamp.desc()).limit(limit).all()
    
    # Reverse to get chronological order
    messages.reverse()
    
    logger.info(f"Retrieved {len(messages)} history messages between {current_user.username} and {other_user}")
    
    return [MessageResponse(
        id=msg.id,
        sender=msg.sender,
        receiver=msg.receiver,
        message=msg.message,
        timestamp=msg.timestamp,
        delivered=msg.delivered,
        read=msg.read
    ) for msg in messages]

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for ping/pong
            await websocket.send_text(f"pong: {data}")
    except WebSocketDisconnect:
        manager.disconnect(username)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_connections": len(manager.active_connections)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )