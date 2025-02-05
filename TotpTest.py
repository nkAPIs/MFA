import requests
from constants import Constants
constants = Constants()

# Step 1: Get the JWT token
token_url = "http://127.0.0.1:8000/token"
credentials = {
    "username": constants.user,
    "password": constants.password
}

response = requests.post(token_url, data=credentials)

if response.status_code == 200:
    token = response.json().get("access_token")
    print("✅ Token received:", token)
else:
    print("❌ Failed to get token:", response.text)
    exit()

# Step 2: Use the token to call the /getsecret endpoint
secret = "WOZPWOU3MATTHZK5"  # Replace with actual secret key
headers = {
    "Authorization": f"Bearer {token}"
}

get_secret_url = f"http://127.0.0.1:8000/getsecret?secret={secret}"
response = requests.get(get_secret_url, headers=headers)

if response.status_code == 200:
    print("🔑 TOTP Token:", response.json())
else:
    print("❌ Failed to get TOTP token:", response.text)

