import speedtest
import re
import base64

# Decode the provided configuration
config_base64 = "ss://YWVzLTI1Ni1nY206cEtFVzhKUEJ5VFZUTHRN@51.77.53.200:4444#%F0%9F%92%9A%20M@M%20%F0%9F%92%99%20Warsaw%20Poland"
ip_match = re.search(r'@(\d+\.\d+\.\d+\.\d+)', config_base64)
port_match = re.search(r':(\d+)', config_base64)
ip_address = ip_match.group(1)
port = port_match.group(1)
print(ip_address)


# Initialize the speedtest client
st = speedtest.Speedtest()

# Set the server to the provided IP and port
st.get_best_server(ip_address, int(port))

# Get latency (ping) and download speed
ping_result = st.results.ping
download_speed = st.download() / 1_000_000  # Convert to Mbps

print(f"Latency (Ping): {ping_result} ms")
print(f"Download Speed: {download_speed:.2f} Mbps")
