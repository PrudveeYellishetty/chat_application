#!/usr/bin/env python3
"""
Local development server runner for PLP Chat
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_server():
    """Run the FastAPI server"""
    print("🚀 Starting PLP Development Server...")
    print("📝 Server will be available at: http://localhost:8000")
    print("📊 API docs available at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    print("🔧 PLP Development Server Setup")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import fastapi
        print("✅ FastAPI found")
    except ImportError:
        print("📦 FastAPI not found, installing requirements...")
        if not install_requirements():
            sys.exit(1)
    
    # Run server
    run_server()

if __name__ == "__main__":
    main()