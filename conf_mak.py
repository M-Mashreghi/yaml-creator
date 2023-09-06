import yaml

# Read the YAML data from the configurations.yaml file
with open('configurations.yaml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Create a .conf file and write the URLs with the name "M.M" from YAML
with open('configurations.conf', 'w') as conf_file:
    for configuration in yaml_data["configurations"]:
        url = configuration.get('url', '')  # Use 'url' or provide a default
        modified_url = url.replace("name=", "name=M.M")
        conf_file.write(f"{modified_url}\n\n")
