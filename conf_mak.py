import yaml

# Read the YAML data from the configurations.yaml file
with open(r'H:\GIT project\yaml-creator\configurations.yaml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Create a .conf file and write the data
with open(r'H:\GIT project\yaml-creator\configurations.conf', 'w') as conf_file:
    for configuration in yaml_data["configurations"]:
        url = configuration.get('url', 'default_url')  # Use 'url' or provide a default
        conf_file.write(f"[{url}]\n")
        conf_file.write(f"url={url}\n")
        conf_file.write("\n")
