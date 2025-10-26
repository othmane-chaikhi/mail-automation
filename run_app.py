#!/usr/bin/env python3
"""
Email Automation App Launcher
Simple launcher for the email automation app.
"""

import subprocess
import sys
import os

def main():
    """Launch the email automation app."""
    print("🚀 Starting Email Automation Pro...")
    print("📧 Opening in your default browser...")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_new.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

if __name__ == "__main__":
    main()
