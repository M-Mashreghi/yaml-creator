import yaml

# Read the URLs from the text file
with open(r'H:\GIT project\yaml-creator\urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Change the name for each URL to "love M.M"
for index, url in enumerate(urls):
    urls[index] = url.replace("name:", "love M.M:")

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


# # Create a .conf file and write the data
# with open('configurations.conf', 'w') as conf_file:
#     for configuration in yaml_data["configurations"]:
#         conf_file.write(f"[{configuration['name']}]\n")
#         conf_file.write(f"url={configuration['url']}\n")
#         conf_file.write("\n")
# your link goes here
link = "https://github.com/M-Mashreghi/yaml-creator/blob/main/configurations.conf"

# note: this will break if a repo/organization or subfolder is named "blob" -- would be ideal to use a fancy regex
# to be more precise here
print(link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/"))