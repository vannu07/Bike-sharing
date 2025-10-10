#!/usr/bin/env python3
"""
Setup script for Bike Sharing Demand Prediction Project
"""

import os
import sys
import subprocess
import platform

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static', 'logs', 'models']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def run_tests():
    """Run the test suite"""
    print("\nRunning tests...")
    try:
        subprocess.check_call([sys.executable, "-m", "pytest", "test_app.py", "-v"])
        print("✅ All tests passed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Some tests failed: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚴‍♂️ Bike Sharing Demand Prediction Project Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup completed. Check the issues above.")
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  python app.py")
    print("\nTo run tests:")
    print("  python -m pytest test_app.py -v")

if __name__ == "__main__":
    main()
