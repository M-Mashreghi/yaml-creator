import requests
import time

def test_custom_download_speed(ip_address, port, file_url):
    # Construct the full URL with IP address and port
    url = f"http://{ip_address}:{port}/{file_url}"
    
    start_time = time.time()
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    end_time = time.time()
    
    download_speed = len(response.content) / (end_time - start_time) / 10**6  # Convert to Mbps
    return download_speed

if __name__ == "__main__":
    ip_address = "3.71.252.84"
    port = 22222 # Replace with the port your server uses
    file_url = 'H:\GIT project\yaml-creator\configurations.conf'  # Replace with the file URL you want to test
    
    download_speed = test_custom_download_speed(ip_address, port, file_url)
    
    if download_speed is not None:
        print(f"Download Speed to {ip_address}:{port}: {download_speed:.2f} Mbps")
