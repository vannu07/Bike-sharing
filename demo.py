#!/usr/bin/env python3
"""
Demonstration script for Bike Sharing Demand Prediction Application
This script shows how to use the API programmatically
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running!")
        return False

def test_prediction():
    """Test the prediction endpoint with sample data"""
    print("\n🚴‍♂️ Testing prediction endpoint...")
    
    # Sample data for different scenarios
    test_cases = [
        {
            "name": "Summer Clear Day",
            "data": {
                "year": 1,
                "month": "Jul",
                "weekday": "Mon",
                "temperature": 28.0,
                "humidity": 55.0,
                "windspeed": 8.0,
                "weather": "Clear",
                "season": "Summer",
                "holiday": 0,
                "workingday": 1
            }
        },
        {
            "name": "Winter Storm Day",
            "data": {
                "year": 0,
                "month": "Jan",
                "weekday": "Sun",
                "temperature": -5.0,
                "humidity": 90.0,
                "windspeed": 20.0,
                "weather": "Thunderstrom",
                "season": "Winter",
                "holiday": 1,
                "workingday": 0
            }
        },
        {
            "name": "Spring Rainy Day",
            "data": {
                "year": 1,
                "month": "Apr",
                "weekday": "Fri",
                "temperature": 15.0,
                "humidity": 75.0,
                "windspeed": 12.0,
                "weather": "Light_rainfall",
                "season": "Spring",
                "holiday": 0,
                "workingday": 1
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        print(f"   Data: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction']
                print(f"   ✅ Prediction: {prediction} bike rentals")
                
                # Add some interpretation
                if prediction > 1000:
                    print("   📈 High demand expected!")
                elif prediction > 500:
                    print("   📊 Moderate demand expected")
                else:
                    print("   📉 Low demand expected")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_error_handling():
    """Test error handling with invalid data"""
    print("\n🚨 Testing error handling...")
    
    # Test with missing fields
    print("   Testing missing fields...")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"temperature": 25.0},  # Missing required fields
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 400:
            print("   ✅ Correctly handled missing fields")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
    
    # Test with invalid JSON
    print("   Testing invalid JSON...")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 400:
            print("   ✅ Correctly handled invalid JSON")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")

def main():
    """Main demonstration function"""
    print("🚴‍♂️ Bike Sharing Demand Prediction - API Demonstration")
    print("=" * 60)
    
    # Test health endpoint
    if not test_health():
        print("\n❌ Server is not running. Please start the application first:")
        print("   python app.py")
        return
    
    # Test predictions
    test_prediction()
    
    # Test error handling
    test_error_handling()
    
    print("\n🎉 Demonstration completed!")
    print("\nTo use the web interface, open:")
    print(f"   {BASE_URL}")
    print("\nTo make API calls programmatically:")
    print("   import requests")
    print("   response = requests.post('http://localhost:5000/predict', json=your_data)")

if __name__ == "__main__":
    main()
