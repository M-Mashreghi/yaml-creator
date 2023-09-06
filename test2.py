from urllib.parse import urlparse

# Your URL
url = "vless://bfbd0da6-d36b-4e72-8868-96f2eb51b9e3@all.vpncustomize.website:2096?security=tls&sni=uGGkffkuygV2raykufukfkyKuyk-irancel-Mokhabera-Mamad-raitel-MIc.Snapp.monster&type=grpc&serviceName=@VPNCUSTOMIZE#M@M 💙"

# Parse the URL
parsed_url = urlparse(url)

# Extract the hostname (which is the IP address)
ip_address = parsed_url.hostname

print(f"IP Address: {ip_address}")
