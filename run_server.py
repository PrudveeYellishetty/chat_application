#!/usr/bin/env python3
"""
PLP Server Runner
"""

import subprocess
import sys

def main():
    print("🚀 Starting PLP Server...")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()