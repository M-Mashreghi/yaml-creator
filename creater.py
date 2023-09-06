import yaml
import re
import base64
import json
import requests
emoji = '\U0001F499'
new_name = "M@M " + emoji

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


def find_location(vmess_url):
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
            return city , country
            if city and country:
                print(f"City: {city}, Country: {country}")
            else:
                print("City and country information not available.")
        else:
            print("Failed to retrieve geolocation information.")
    else:
        print("Server address not found in the VMess configuration.")
    return 0 , 0



# Read the URLs from the text file
with open(r'H:\GIT project\yaml-creator\urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Modify URLs
for i in range(len(urls)):
    url = urls[i]
    if url.startswith("vmess://"):
        city ,country = find_location(url)
        name = new_name  +city + country
        urls[i] = update_vmess_name(url, name)
    else:
        urls[i] = re.sub(r'#.*', f'#{new_name}', url)


# Convert URLs to YAML format
yaml_data = {
    "configurations": [
        {
            "url": url
        }
        for url in urls
    ]
}

# Save the YAML data to a file
with open(r'H:\GIT project\yaml-creator\configurations.yaml', 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file)

# Create a .conf file and write the modified URLs
with open(r'H:\GIT project\yaml-creator\configurations.conf', 'w', encoding='utf-8') as conf_file:
    for modified_url in urls:
        conf_file.write(f"{modified_url}\n\n")
