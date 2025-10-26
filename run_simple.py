#!/usr/bin/env python3
"""
Simple Email Automation - Launcher
"""

import subprocess
import sys

def main():
    """Launch the simple email automation app."""
    print("🚀 Starting Simple Email Automation...")
    print("📧 Opening in your default browser...")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "simple_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
