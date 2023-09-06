import yaml
import re
import base64
import json
import requests
emoji1 = '\U0001F49A'
emoji2 = '\U0001F499'
new_name = emoji1 + " M@M " + emoji2 + " "

def update_vmess_name(vmess_url, replace_name):
    # Decode the VMess URL
    vmess_url = vmess_url.strip()
    config_base64 = vmess_url.split("://")[1]
    config_json = base64.b64decode(config_base64).decode()

    # Parse the JSON configuration
    config = json.loads(config_json)

    # Update the name field
    config["ps"] = replace_name

    # Encode the updated configuration as base64
    updated_config_json = json.dumps(config)
    updated_config_base64 = base64.b64encode(updated_config_json.encode()).decode()

    # Create the new VMess URL
    new_vmess_url = f"vmess://{updated_config_base64}"

    return new_vmess_url


def find_location_vmess(vmess_url,new_name):
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
            name =new_name  + city + ' ' + country
            return name
            if city and country:
                print(f"City: {city}, Country: {country}")
            else:
                print("City and country information not available.")
        else:
            print("Failed to retrieve geolocation information.")
    else:
        print("Server address not found in the VMess configuration.")
    return new_name

def find_loc_ss(config_str,new_name):
        # Use regular expressions to extract the IP address from the string
        ip_match = re.search(r'@(\d+\.\d+\.\d+\.\d+)', config_str)
        if ip_match:
                ip_address = ip_match.group(1)
                # Use the ip-api.com API to get geolocation information
                api_url = f"http://ip-api.com/json/{ip_address}"
                response = requests.get(api_url)

                if response.status_code == 200:
                    geolocation_data = response.json()
                    city = geolocation_data.get("city")
                    country = geolocation_data.get("country")
                    name =new_name  + city + ' ' + country
                    return name
                    if city and country:
                        print(f"City: {city}, Country: {country}")
                        return city , country
                    else:
                        print("City and country information not available.")
                else:
                    print("Failed to retrieve geolocation information.")
        else:
            print("No IP address found in the configuration string.")
        return new_name


# Read the URLs from the text file
with open(r'H:\GIT project\yaml-creator\urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Modify URLs
for i in range(len(urls)):
    url = urls[i]
    if url.startswith("vmess://"):
        urls[i] = update_vmess_name(url, new_name)
        #find_location_vmess(url,new_name)
    elif url.startswith("ss://"):
        try:
            name_ss = find_loc_ss(url,new_name)
        except:
            name_ss = new_name
        urls[i] = re.sub(r'#.*', f'#{name_ss}', url)
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
