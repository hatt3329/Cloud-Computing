import requests

BASE_URL = "http://127.0.0.1:8000"

# user agent
resp = requests.get(f"{BASE_URL}/user-agent", headers={"User-Agent": "MyTestClient/1.0"})
print("/user-agent:", resp.json())

# set cookie
resp = requests.get(f"{BASE_URL}/set-cookie")
print("/set-cookie:", resp.json())
cookie_jar = resp.cookies

# check cookie
resp = requests.get(f"{BASE_URL}/check-cookie", cookies=cookie_jar)
print("/check-cookie:", resp.json())

# secure header with valid token
resp = requests.get(f"{BASE_URL}/secure-header", headers={"X-Client-Token": "secret123"})
print("/secure-header (valid):", resp.json())

# invalid token
resp = requests.get(f"{BASE_URL}/secure-header", headers={"X-Client-Token": "wrongtoken"})
print("/secure-header (invalid):", resp.json())

# multiple headers and cookies
headers = {
    "Accept-Language": "en-US",
    "Referer": "http://example.com"
}
cookies = {"session_id": "abc123"}
resp = requests.get(f"{BASE_URL}/multi-info", headers=headers, cookies=cookies)
print("/multi-info:", resp.json())
