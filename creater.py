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
