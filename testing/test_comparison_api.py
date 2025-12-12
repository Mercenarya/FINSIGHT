"""
Test script for Financial Comparison API
Run this to test the comparison endpoint
"""
import requests
import json

# API Configuration
BASE_URL = "http://localhost:8001"
COMPARE_ENDPOINT = f"{BASE_URL}/api/v1/compare/"

def test_compare_api_post():
    """Test POST request to comparison API"""
    print("=" * 60)
    print("Testing POST Request to Comparison API")
    print("=" * 60)
    
    payload = {
        "ticker1": "VIC",
        "ticker2": "VNM",
        "quarter": "Third_quarter"
    }
    
    try:
        response = requests.post(
            COMPARE_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"\nResponse:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to server")
        print("Make sure Django server is running on port 8001")
    except Exception as e:
        print(f"\nError: {e}")


def test_compare_api_get():
    """Test GET request to comparison API"""
    print("\n" + "=" * 60)
    print("Testing GET Request to Comparison API")
    print("=" * 60)
    
    params = {
        "ticker1": "VIC",
        "ticker2": "VNM",
        "quarter": "Third_quarter"
    }
    
    try:
        response = requests.get(COMPARE_ENDPOINT, params=params)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"\nResponse:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to server")
        print("Make sure Django server is running on port 8001")
    except Exception as e:
        print(f"\nError: {e}")


def test_error_handling():
    """Test error handling with missing parameters"""
    print("\n" + "=" * 60)
    print("Testing Error Handling (Missing Parameters)")
    print("=" * 60)
    
    payload = {
        "ticker1": "VIC"
        # ticker2 is missing
    }
    
    try:
        response = requests.post(
            COMPARE_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"\nResponse:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")
        print("Make sure Django server is running on port 8001")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    print("\n🚀 Starting API Tests...")
    print("Make sure:")
    print("1. Django server is running (python manage.py runserver 8001)")
    print("2. MongoDB is running and contains data")
    print("3. Environment variables are configured\n")
    
    # Run tests
    test_compare_api_post()
    test_compare_api_get()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    print("=" * 60)
