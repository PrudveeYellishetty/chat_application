#!/usr/bin/env python3
"""
PLP Client - Personal Learning Platform Terminal Interface
A stealth chat client disguised as a development productivity tool.
"""

import os
import sys
import json
import asyncio
import threading
import time
from datetime import datetime
from typing import Optional, List, Dict
import argparse

import requests
import websockets
from colorama import init, Fore, Back, Style
import getpass

# Initialize colorama for Windows support
init(autoreset=True)

# Client Configuration
CLIENT_CONFIG = {
    "server_url": "http://localhost:8000",  # Change this to your deployed server URL
    "websocket_url": "ws://localhost:8000",  # Change this to your deployed WebSocket URL
    "app_name": "PLP - Personal Learning Platform",
    "version": "1.2.0"
}

class PLPClient:
    def __init__(self):
        self.server_url = CLIENT_CONFIG["server_url"]
        self.ws_url = CLIENT_CONFIG["websocket_url"]
        self.token = None
        self.username = None
        self.websocket = None
        self.ws_thread = None
        self.session = requests.Session()
        self.running = True
        
    def print_banner(self):
        """Display professional-looking banner"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}  {CLIENT_CONFIG['app_name']}")
        print(f"{Fore.CYAN}  Version {CLIENT_CONFIG['version']} - Development Environment")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Connected to PLP Development Server")
        print(f"{Fore.GREEN}✓ Terminal Interface Ready")
        print(f"{Fore.YELLOW}📋 Type 'plp help' for available commands{Style.RESET_ALL}\n")

    def print_help(self):
        """Display help information"""
        print(f"\n{Fore.CYAN}PLP Development Commands:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}plp send \"message\"{Style.RESET_ALL}     - Send development update")
        print(f"  {Fore.GREEN}plp recv{Style.RESET_ALL}               - Check for team updates") 
        print(f"  {Fore.GREEN}plp hist [user]{Style.RESET_ALL}        - View project communication history")
        print(f"  {Fore.GREEN}plp status{Style.RESET_ALL}             - Check connection status")
        print(f"  {Fore.GREEN}plp clear{Style.RESET_ALL}              - Clear terminal output")
        print(f"  {Fore.GREEN}plp help{Style.RESET_ALL}               - Show this help menu")
        print(f"  {Fore.GREEN}plp exit{Style.RESET_ALL}               - Exit PLP environment")
        print(f"\n{Fore.YELLOW}Examples:{Style.RESET_ALL}")
        print(f"  plp send \"Code review completed for branch feature-auth\"")
        print(f"  plp send \"Database migration successful - ready for deployment\"")
        print(f"  plp hist alice")
        print()

    def fake_build_output(self):
        """Generate fake build/compile output for stealth"""
        outputs = [
            f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Compiling source files...",
            f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Dependency resolution completed",
            f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Build pipeline executed successfully",
            f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Running automated tests...",
            f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} All tests passed (47/47)",
            f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Generating documentation...",
            f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Documentation updated",
        ]
        import random
        return random.choice(outputs)

    def authenticate(self) -> bool:
        """Handle user authentication"""
        print(f"\n{Fore.YELLOW}🔐 PLP Authentication Required{Style.RESET_ALL}")
        
        while True:
            choice = input("Choose: (l)ogin or (r)egister: ").lower().strip()
            
            if choice in ['l', 'login']:
                return self.login()
            elif choice in ['r', 'register']:
                return self.register()
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 'l' for login or 'r' for register.{Style.RESET_ALL}")

    def login(self) -> bool:
        """Login user"""
        print(f"\n{Fore.CYAN}PLP Developer Login{Style.RESET_ALL}")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        
        try:
            response = self.session.post(
                f"{self.server_url}/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.username = username
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"{Fore.GREEN}✓ Authentication successful{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✓ Connected as: {username}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}✗ Authentication failed: {response.json().get('detail', 'Unknown error')}{Style.RESET_ALL}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}✗ Cannot connect to PLP server. Check your internet connection.{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ Login error: {e}{Style.RESET_ALL}")
            return False

    def register(self) -> bool:
        """Register new user"""
        print(f"\n{Fore.CYAN}PLP Developer Registration{Style.RESET_ALL}")
        username = input("Choose username: ").strip()
        
        if len(username) < 3:
            print(f"{Fore.RED}Username must be at least 3 characters long{Style.RESET_ALL}")
            return False
            
        password = getpass.getpass("Choose password: ")
        password_confirm = getpass.getpass("Confirm password: ")
        
        if password != password_confirm:
            print(f"{Fore.RED}Passwords do not match{Style.RESET_ALL}")
            return False
            
        if len(password) < 6:
            print(f"{Fore.RED}Password must be at least 6 characters long{Style.RESET_ALL}")
            return False
        
        try:
            response = self.session.post(
                f"{self.server_url}/auth/register",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.username = username
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"{Fore.GREEN}✓ Registration successful{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✓ Connected as: {username}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}✗ Registration failed: {response.json().get('detail', 'Unknown error')}{Style.RESET_ALL}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}✗ Cannot connect to PLP server. Check your internet connection.{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ Registration error: {e}{Style.RESET_ALL}")
            return False

    async def websocket_listener(self):
        """Listen for incoming WebSocket messages"""
        try:
            ws_url = self.ws_url.replace("http://", "ws://").replace("https://", "wss://")
            uri = f"{ws_url}/ws/{self.username}"
            
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                while self.running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(message)
                        
                        if data.get("type") == "new_message":
                            self.display_incoming_message(data)
                            
                    except asyncio.TimeoutError:
                        # Send ping to keep connection alive
                        await websocket.send("ping")
                    except websockets.exceptions.ConnectionClosed:
                        print(f"\n{Fore.YELLOW}📡 WebSocket connection lost{Style.RESET_ALL}")
                        break
                        
        except Exception as e:
            print(f"\n{Fore.YELLOW}📡 Real-time notifications unavailable: {e}{Style.RESET_ALL}")

    def start_websocket(self):
        """Start WebSocket in background thread"""
        def run_websocket():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.websocket_listener())
            
        self.ws_thread = threading.Thread(target=run_websocket, daemon=True)
        self.ws_thread.start()

    def display_incoming_message(self, data):
        """Display incoming message with fake build context"""
        timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        formatted_time = timestamp.strftime("%H:%M:%S")
        
        print(f"\n{self.fake_build_output()}")
        print(f"{Fore.CYAN}[{formatted_time}] {Fore.WHITE}New team update from {Fore.YELLOW}{data['sender']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}📝 {data['message']}{Style.RESET_ALL}")
        print(f"{self.fake_build_output()}")
        print(f"\n{Fore.GREEN}plp>{Style.RESET_ALL} ", end="", flush=True)

    def send_message(self, receiver: str, message: str) -> bool:
        """Send a message"""
        try:
            response = self.session.post(
                f"{self.server_url}/messages/send",
                json={"receiver": receiver, "message": message}
            )
            
            if response.status_code == 200:
                data = response.json()
                timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
                formatted_time = timestamp.strftime("%H:%M:%S")
                
                print(f"{self.fake_build_output()}")
                print(f"{Fore.GREEN}[{formatted_time}] ✓ Update sent to {receiver}{Style.RESET_ALL}")
                if data["delivered"]:
                    print(f"{Fore.GREEN}[{formatted_time}] ✓ Delivered successfully{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[{formatted_time}] ⏳ Queued for delivery{Style.RESET_ALL}")
                print(f"{self.fake_build_output()}")
                return True
            else:
                print(f"{Fore.RED}✗ Failed to send message: {response.json().get('detail', 'Unknown error')}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Send error: {e}{Style.RESET_ALL}")
            return False

    def receive_messages(self) -> bool:
        """Fetch unread messages"""
        try:
            response = self.session.get(f"{self.server_url}/messages/unread")
            
            if response.status_code == 200:
                messages = response.json()
                
                if not messages:
                    print(f"{self.fake_build_output()}")
                    print(f"{Fore.BLUE}📭 No new team updates available{Style.RESET_ALL}")
                    print(f"{self.fake_build_output()}")
                    return True
                
                print(f"{self.fake_build_output()}")
                print(f"{Fore.CYAN}📬 Received {len(messages)} new team update(s){Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
                
                for msg in messages:
                    timestamp = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                    formatted_time = timestamp.strftime("%m/%d %H:%M")
                    
                    print(f"{Fore.YELLOW}From: {msg['sender']} {Fore.BLUE}[{formatted_time}]{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}📝 {msg['message']}{Style.RESET_ALL}")
                    print()
                
                print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
                print(f"{self.fake_build_output()}")
                return True
            else:
                print(f"{Fore.RED}✗ Failed to fetch messages: {response.json().get('detail', 'Unknown error')}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Receive error: {e}{Style.RESET_ALL}")
            return False

    def get_history(self, other_user: str) -> bool:
        """Get message history with another user"""
        try:
            response = self.session.get(
                f"{self.server_url}/messages/history",
                params={"other_user": other_user, "limit": 20}
            )
            
            if response.status_code == 200:
                messages = response.json()
                
                if not messages:
                    print(f"{self.fake_build_output()}")
                    print(f"{Fore.BLUE}📭 No communication history with {other_user}{Style.RESET_ALL}")
                    print(f"{self.fake_build_output()}")
                    return True
                
                print(f"{self.fake_build_output()}")
                print(f"{Fore.CYAN}📊 Communication History with {other_user} (last {len(messages)} messages){Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
                
                for msg in messages:
                    timestamp = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                    formatted_time = timestamp.strftime("%m/%d %H:%M")
                    
                    if msg["sender"] == self.username:
                        sender_color = Fore.GREEN
                        prefix = "→ You"
                    else:
                        sender_color = Fore.YELLOW
                        prefix = f"← {msg['sender']}"
                    
                    print(f"{sender_color}{prefix} {Fore.BLUE}[{formatted_time}]{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}   {msg['message']}{Style.RESET_ALL}")
                    print()
                
                print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
                print(f"{self.fake_build_output()}")
                return True
            else:
                print(f"{Fore.RED}✗ Failed to fetch history: {response.json().get('detail', 'Unknown error')}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ History error: {e}{Style.RESET_ALL}")
            return False

    def check_status(self):
        """Check connection status"""
        try:
            response = self.session.get(f"{self.server_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"{Fore.GREEN}✓ PLP Server Status: {data['status'].upper()}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✓ Connection: Active{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✓ User: {self.username}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}📊 Active developers: {data.get('active_connections', 'Unknown')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠ Server responding with status: {response.status_code}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Connection status: OFFLINE{Style.RESET_ALL}")
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

    def parse_command(self, command: str) -> bool:
        """Parse and execute PLP commands"""
        parts = command.strip().split()
        
        if not parts:
            return True
            
        if parts[0] != "plp":
            print(f"{Fore.RED}✗ Unknown command. Use 'plp help' for available commands.{Style.RESET_ALL}")
            return True
        
        if len(parts) == 1:
            print(f"{Fore.YELLOW}PLP command required. Use 'plp help' for available commands.{Style.RESET_ALL}")
            return True
            
        subcommand = parts[1].lower()
        
        if subcommand == "help":
            self.print_help()
            
        elif subcommand == "send":
            if len(parts) < 3:
                print(f"{Fore.RED}Usage: plp send \"message\"{Style.RESET_ALL}")
                return True
                
            # Join all parts after "send" and remove quotes
            message = " ".join(parts[2:]).strip('"\'')
            
            if not message:
                print(f"{Fore.RED}Message cannot be empty{Style.RESET_ALL}")
                return True
            
            # For now, assume sending to a default recipient
            # In a real implementation, you might want to specify recipient
            receiver = input(f"Send to (username): ").strip()
            if not receiver:
                print(f"{Fore.RED}Recipient username required{Style.RESET_ALL}")
                return True
                
            self.send_message(receiver, message)
            
        elif subcommand == "recv":
            self.receive_messages()
            
        elif subcommand == "hist":
            if len(parts) < 3:
                other_user = input("Show history with (username): ").strip()
            else:
                other_user = parts[2]
                
            if not other_user:
                print(f"{Fore.RED}Username required for history{Style.RESET_ALL}")
                return True
                
            self.get_history(other_user)
            
        elif subcommand == "status":
            self.check_status()
            
        elif subcommand == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            
        elif subcommand == "exit":
            print(f"{Fore.CYAN}Shutting down PLP environment...{Style.RESET_ALL}")
            return False
            
        else:
            print(f"{Fore.RED}✗ Unknown PLP command: {subcommand}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Use 'plp help' for available commands.{Style.RESET_ALL}")
            
        return True

    def run(self):
        """Main client loop"""
        self.print_banner()
        
        # Authenticate
        if not self.authenticate():
            return
            
        # Start WebSocket for real-time updates
        self.start_websocket()
        time.sleep(1)  # Give WebSocket time to connect
        
        print(f"\n{Fore.GREEN}🚀 PLP Development Environment Ready{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Real-time team updates: {'✓ Active' if self.ws_thread and self.ws_thread.is_alive() else '✗ Unavailable'}{Style.RESET_ALL}")
        
        # Main command loop
        try:
            while self.running:
                try:
                    command = input(f"\n{Fore.GREEN}plp>{Style.RESET_ALL} ").strip()
                    
                    if not command:
                        continue
                        
                    if not self.parse_command(command):
                        break
                        
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Use 'plp exit' to quit properly.{Style.RESET_ALL}")
                    continue
                except EOFError:
                    break
                    
        finally:
            self.running = False
            print(f"\n{Fore.CYAN}✓ PLP session terminated{Style.RESET_ALL}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="PLP - Personal Learning Platform Terminal Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python client.py                    # Start interactive mode
  python client.py --server URL       # Connect to custom server
        """
    )
    
    parser.add_argument(
        "--server",
        help="PLP server URL (default: localhost:8000)",
        default=CLIENT_CONFIG["server_url"]
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"PLP Client {CLIENT_CONFIG['version']}"
    )
    
    args = parser.parse_args()
    
    # Update configuration
    if args.server != CLIENT_CONFIG["server_url"]:
        CLIENT_CONFIG["server_url"] = args.server
        CLIENT_CONFIG["websocket_url"] = args.server.replace("http://", "ws://").replace("https://", "wss://")
    
    # Start client
    client = PLPClient()
    try:
        client.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}✓ PLP session interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}✗ PLP client error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()