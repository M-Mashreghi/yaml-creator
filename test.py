import base64
import json

def update_vmess_name(vmess_url, new_name):
    # Decode the VMess URL
    vmess_url = vmess_url.strip()
    config_base64 = vmess_url.split("://")[1]
    config_json = base64.b64decode(config_base64).decode()

    # Parse the JSON configuration
    config = json.loads(config_json)

    # Update the name field
    config["ps"] = new_name

    # Encode the updated configuration as base64
    updated_config_json = json.dumps(config)
    updated_config_base64 = base64.b64encode(updated_config_json.encode()).decode()

    # Create the new VMess URL
    new_vmess_url = f"vmess://{updated_config_base64}"

    return new_vmess_url

# List of VMess URLs with their respective new names
vmess_urls = [
    "vmess://eyJhZGQiOiIxMzcuMTc1LjIyLjE4NyIsImFpZCI6IjY0IiwiaG9zdCI6IiIsImlkIjoiNDE4MDQ4YWYtYTI5My00Yjk5LTliMGMtOThjYTM1ODBkZDI0IiwibmV0IjoidGNwIiwicGF0aCI6IiIsInBvcnQiOiI1Mzk5OSIsInBzIjoi8J+fpSBTZXJ2ZXIgMDYiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6IiIsInYiOiIyIn0=",
    "vmess://eyJhZGQiOiIxNTYuMjI1LjY3LjQ3IiwiYWlkIjoiNjQiLCJob3N0IjoiIiwiaWQiOiIzY2E5MTJkYS02YWMyLTQxOGYtYjljZi00NWI2ZjY5NDU3OWIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5MjI0IiwicHMiOiLwn5+lIFNlcnZlciAxNyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ=="
]

new_name = "M@M"

# Update the names and print the new VMess URLs
for url in vmess_urls:
    updated_url = update_vmess_name(url, new_name)
    print(updated_url)
