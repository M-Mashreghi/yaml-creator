import base64
import json
import requests

vmess_url = "vmess://eyJhZGQiOiIxNTYuMjI1LjY3LjQ3IiwiYWlkIjoiNjQiLCJob3N0IjoiIiwiaWQiOiIzY2E5MTJkYS02YWMyLTQxOGYtYjljZi00NWI2ZjY5NDU3OWIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5MjI0IiwicHMiOiLwn5+lIFNlcnZlciAxNyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ=="

# Decode the VMess URL
vmess_config_base64 = vmess_url.split("://")[1]
vmess_config_json = base64.b64decode(vmess_config_base64).decode()
vmess_config = json.loads(vmess_config_json)

# Extract the server address (location)
server_address = vmess_config.get("add")

if server_address:
    # Use the ip-api.com API to get geolocation information
    api_url = f"http://ip-api.com/json/{server_address}"
    response = requests.get(api_url)

    if response.status_code == 200:
        geolocation_data = response.json()
        city = geolocation_data.get("city")
        country = geolocation_data.get("country")

        if city and country:
            print(f"City: {city}, Country: {country}")
        else:
            print("City and country information not available.")
    else:
        print("Failed to retrieve geolocation information.")
else:
    print("Server address not found in the VMess configuration.")
