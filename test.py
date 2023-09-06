import re

# List of server URLs
servers = [
    "trojan://telegram-id-privatevpns@3.71.252.84:22222?security=tls&sni=trj.rollingnext.co.uk&type=tcp#(S449)%F0%9F%87%A9%F0%9F%87%AAt.me/PrivateVPNs",
    "trojan://telegram-id-directvpn@13.39.146.155:22222?security=tls&sni=trj.rollingnext.co.uk&type=tcp#Our%20Channel%20:%20@DirectVPN",
    "vless://bfbd0da6-d36b-4e72-8868-96f2eb51b9e3@all.vpncustomize.website:2096?security=tls&sni=uGGkffkuygV2raykufukfkyKuyk-irancel-Mokhabera-Mamad-raitel-MIc.Snapp.monster&type=grpc&serviceName=@VPNCUSTOMIZE#%F0%9F%9F%A3all@oneclickvpnkeys",
    "vless://c688395a-b36b-4071-974b-bc91ac2ad2c4@986join.outline-vpn.cloud:443?security=tls&sni=edtunnel-b6t.pages.dev&type=ws&path=/&host=edtunnel-b6t.pages.dev#%F0%9F%9F%A3986@oneclickvpnkeys",
    "vless://884f9b2c-f0c5-44dd-a68e-3e39ce93bb39@cf-wkrs-pages-vless-aoy.pages.dev:443?security=tls&sni=cf-wkrs-pages-vless-aoy.pages.dev&type=ws&path=/?ed%3D2048&host=cf-wkrs-pages-vless-aoy.pages.dev#%F0%9F%9F%A3cf@oneclickvpnkeys",
    "ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpkNTZmZDA0YS01ODAyLTQ3ODgtYmJhZi0zZWExNDE0MmU1OTc=@ru-04.feitucloud.com:10103#%F0%9F%9F%A3704@oneclickvpnkeys",
    "vmess://eyJhZGQiOiI0czQuYWxsYWFuc2VsbC5vbmxpbmUiLCJhaWQiOiIwIiwiaG9zdCI6InRlbGV3ZWJpb24uY29tIiwiaWQiOiIwZDZiYTY2Zi0zYjUxLTQzMjUtODRkMC00ZDlkZDUzMWYwZTkiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiLyIsInBvcnQiOiI4NDQzIiwicHMiOiJTVEFSLdit2YXYp9uM2KogQHN0YXJ2MnJheW4iLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Imh0dHAiLCJ2IjoiMiJ9"
]

# Define a function to change the name for each server URL
def change_server_name(server_url):
    # Use regular expressions to remove everything after '#' and replace with '#M@M'
    new_server_url = re.sub(r'#.*', '#M@M', server_url)
    return new_server_url

# Iterate through the list of servers and change the names
for i, server_url in enumerate(servers):
    new_server_url = change_server_name(server_url)
    print(f"Server {i + 1}: {new_server_url}")
