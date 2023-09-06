import yaml
import re

# Read the URLs from the text file
with open(r'H:\GIT project\yaml-creator\urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Modify URLs
modified_urls = [re.sub(r'#.*', '#M@M', url) for url in urls]

# Convert URLs to YAML format
yaml_data = {
    "configurations": [
        {
            "url": url
        }
        for url in modified_urls
    ]
}

# Save the YAML data to a file
with open(r'H:\GIT project\yaml-creator\configurations.yaml', 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file)

# Create a .conf file and write the modified URLs
with open(r'H:\GIT project\yaml-creator\configurations.conf', 'w') as conf_file:
    for modified_url in modified_urls:
        conf_file.write(f"{modified_url}\n\n")
