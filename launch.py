#!/usr/bin/env python3
"""
Email Automation Pro - Launcher
Simple launcher for the email automation application.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import pandas
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
        return True

def main():
    """Launch the email automation application."""
    print("🚀 Starting Email Automation Pro...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Check if main app exists
    if not Path("email_automation.py").exists():
        print("❌ Main application file not found")
        return
    
    print("📧 Email Automation Pro")
    print("🔗 Opening in your default browser...")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "email_automation.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
