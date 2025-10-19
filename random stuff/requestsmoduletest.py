import requests

url = "https://www.roblox.com/home"
headers = {"User-Agent": "Mozilla/5.0 (compatible)"}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # raises for 4xx/5xx
    print("Status:", response.status_code)
    print("Body (first 500 chars):")
    print(response.text[:500])
except requests.exceptions.RequestException as e:
    print("Request failed:", e)