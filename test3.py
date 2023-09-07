import requests

# Replace this with the IP address you want to look up
ip_address = "542.outline-vpn.cloud"

# Send a request to ipinfo.io
response = requests.get(f"https://ipinfo.io/{ip_address}/json")

# Check if the response status code indicates success (200 OK)
if response.status_code == 200:
    try:
        # Try to parse the response JSON
        data = response.json()
        
        # Extract the location information
        city = data.get("city", "N/A")
        country = data.get("country", "N/A")

        print(f"City: {city}")
        print(f"Country: {country}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Unable to parse JSON response from the geolocation service.")
else:
    print(f"Error: HTTP status code {response.status_code} received. Unable to retrieve geolocation data.")
