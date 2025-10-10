#!/usr/bin/env python3
"""
Run script for Bike Sharing Demand Prediction Application
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import pandas
        import numpy
        import sklearn
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_application():
    """Run the Flask application"""
    if not check_dependencies():
        return False
    
    print("🚴‍♂️ Starting Bike Sharing Demand Prediction Application...")
    print("📱 Web Interface: http://localhost:5000")
    print("🔧 API Endpoint: http://localhost:5000/predict")
    print("❤️  Health Check: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Import and run the app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False

if __name__ == "__main__":
    success = run_application()
    sys.exit(0 if success else 1)
