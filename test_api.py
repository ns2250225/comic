import requests
import json

url = "http://localhost:8000/api/story"
data = {
    "character": "一只勇敢的小猫",
    "plot": "在森林里寻找丢失的铃铛"
}

try:
    print("Sending request...")
    response = requests.post(url, json=data, timeout=60)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
