import re
import requests

import requests
import re

# Extract the IP address from the given config
config_str = "trojan://telegram-id-directvpn@13.39.146.155:22222?security=tls&sni=trj.rollingnext.co.uk&type=tcp#💚 M@M 💙"

def find_loc_ss(config_str):
        # Use regular expressions to extract the IP address from the string
        ip_match = re.search(r'(?P<ip>\d+\.\d+\.\d+\.\d+)', config_str)
        if ip_match:
                ip_address = ip_match.group("ip")
                # Use the ip-api.com API to get geolocation information
                api_url = f"http://ip-api.com/json/{ip_address}"
                response = requests.get(api_url)

                if response.status_code == 200:
                    geolocation_data = response.json()
                    city = geolocation_data.get("city")
                    country = geolocation_data.get("country")

                    if city and country:
                        print(f"City: {city}, Country: {country}")
                        return city , country
                    else:
                        print("City and country information not available.")
                else:
                    print("Failed to retrieve geolocation information.")
        else:
            print("No IP address found in the configuration string.")
        return 0 , 0
find_loc_ss(config_str)
