import requests
import json

# Test the analysis API
url = "http://127.0.0.1:8001/api/analysis/"
params = {
    "company": "VIC",
    "year": "2024", 
    "period": "Quarter 1",
    "metrics": "cash_ratio,quick_ratio,current_ratio"
}

try:
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
