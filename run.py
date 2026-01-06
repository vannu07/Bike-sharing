#!/usr/bin/env python3
"""
Run script for Bike Sharing Demand Prediction Application
"""

import sys

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask  # pylint: disable=unused-import,import-outside-toplevel
        import pandas  # pylint: disable=unused-import,import-outside-toplevel
        import numpy  # pylint: disable=unused-import,import-outside-toplevel
        import sklearn  # pylint: disable=unused-import,import-outside-toplevel
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_application():
    """Run the Flask application"""
    if not check_dependencies():
        sys.exit(1)

    print("🚴‍♂️ Starting Bike Sharing Demand Prediction Application...")
    print("📱 Web Interface: http://localhost:5000")
    print("🔧 API Endpoint: http://localhost:5000/predict")
    print("❤️  Health Check: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)

    try:
        # Import and run the app
        from app import app  # pylint: disable=import-outside-toplevel
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ Error running application: {e}")
        return False

if __name__ == "__main__":
    run_application()
