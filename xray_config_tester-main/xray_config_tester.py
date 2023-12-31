import json
import subprocess
from typing import Tuple
import socket
import time
import requests   # --> pip install requests , pip install pysocks
import os
import base64


# v1.4

# xray_path = "xray-windows-1.8.3.exe"
xray_path = "./xray-linux-amd64-1.8.3"

n_try = 1
timeout= 3 #sec


default_config_alias = "Mahsa Network"


def wait_for_port(port: int,host: str = 'localhost',timeout: float = 5.0) -> None:
    #Wait until a port starts accepting TCP connections.
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(f'Timeout exceeded for the port {port} on host {host} to start accepting connections.') from ex






def start_xray_service(proxy_conf_path: str, binary_path: str, timeout=5) -> Tuple[subprocess.Popen, dict]:
    #starts the proxy (v2ray/xray) service and waits for the respective port to open

    with open(proxy_conf_path, "r") as infile:
        proxy_conf = json.load(infile)

    proxy_listen = "127.0.0.1" #proxy_conf["inbounds"][0]["listen"]
    # proxy_port = proxy_conf["inbounds"][0]["port"]  # Socks port
    proxy_port = proxy_conf["inbounds"][1]["port"]  # HTTPS port
    proxy_process = subprocess.Popen([binary_path, "-c", proxy_conf_path],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)    
    try:
        wait_for_port(host=proxy_listen, port=proxy_port, timeout=timeout)
    except Exception as e:
        proxy_process.kill()
        raise TimeoutError(str(e)) from e 
    # proxies = dict(http=f"socks5://{proxy_listen}:{proxy_port}",https=f"socks5://{proxy_listen}:{proxy_port}")
    proxies = dict(http=f"{proxy_listen}:{proxy_port}",https=f"{proxy_listen}:{proxy_port}")

    return proxy_process, proxies




def download_speed_test(n_bytes: int, proxies: dict, timeout: int) -> Tuple[float, float]:
    #tests the download speed using cloudflare servers
    if(proxies==None):
        raise TimeoutError("No Xray service available")
    
    start_time = time.perf_counter()
    r = requests.get(url="https://speed.cloudflare.com/__down", params={"bytes": n_bytes}, timeout=timeout, proxies=proxies )
    total_time = time.perf_counter() - start_time
    cf_time = float(r.headers.get("Server-Timing").split("=")[1]) / 1000
    latency = r.elapsed.total_seconds() - cf_time
    download_time = total_time - latency

    mb = n_bytes * 8 / (10 ** 6)
    download_speed = mb / download_time

    return download_speed, latency





def extract_config_alias_and_hash(txt=""):
    txt_list = txt.split("\r\n")
    config_alias = ""
    config_hash = ""
    for x in txt_list:
        if(x.startswith("b64_of_alias_config----->$$$$$$") and x.endswith("$$$$$$$")):
            config_alias = base64.b64decode(x[31:-7]).decode("utf-8")
        if(x.startswith("hash_of_outbnd_config--->$$$$$$") and x.endswith("$$$$$$$")):
            config_hash = x[31:-7]
    return (config_alias , config_hash)





def do_test(http_port="10809" , config_filename="config.json" , config_link=""):    
    min_dl_speed = 20 * 1024  # 20KBps
    max_dl_time = 3  # sec
    
    n_bytes =  min_dl_speed * max_dl_time
    is_test_ok = False

    if( config_link.startswith("vmess://") or
        config_link.startswith("vless://") or
        config_link.startswith("trojan://") or
        config_link.startswith("ss://") or
        config_link.startswith("socks://") or
        config_link.startswith("wireguard://") 
        ):        
        pass
    else:
        print("invalid argument in calling do_test()")
        return (False, -1, -1) 


    try:
        # Run the JAR file as a subprocess
        process_java = subprocess.Popen(["java", "-jar", "Link2Json.jar", "-p", http_port, "-o", config_filename, config_link] , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the process to finish and get the output
        stdout, stderr = process_java.communicate()
        

        config_alias = ""
        config_hash = ""
        if(len(stdout)!=0):
            output = stdout.decode("utf-8")
        else:
            output = stderr.decode("utf-8")                
        # print(output)  # print the output of Link2Json which include config alias and config hash
        (config_alias , config_hash) = extract_config_alias_and_hash(output)
        
        if(config_alias==""):
            config_alias = default_config_alias
        if(len(config_hash)>16):
            config_hash = config_hash[:16]

        
        process_java.kill()
    except Exception as e:
        print("failed to start Link2json "+str(e))

    proxies=None
    process_xray = None
    try:
        process_xray, proxies = start_xray_service(config_filename, xray_path, timeout)
    except Exception as e:
        print("Could not start xray service "+str(e))

    count = 0
    Ave_speed = 0
    Ave_latency = 0
    for try_idx in range(n_try):
        try:            
            dl_speed, dl_latency = download_speed_test(n_bytes,proxies,timeout)
            Ave_speed = Ave_speed + dl_speed
            Ave_latency = Ave_latency + dl_latency
            count = count + 1
        except Exception as e:
            # print("download timeout exceeded? -> "+str(e))
            pass
    
    if(process_xray!=None):
        process_xray.kill()

    if(count > 0):
        Ave_speed = round(Ave_speed/count,2)
        Ave_latency = round(Ave_latency/count,2)
        print(f"successful    DL_speed={Ave_speed} Mbps    Latency={Ave_latency} sec --> alias={config_alias} , hash={config_hash} , file={config_filename}") 
        is_test_ok = True
        return (is_test_ok, Ave_speed , Ave_latency , config_alias , config_hash )
    else:
        print(f"test failed --> alias={config_alias} , hash={config_hash} , file={config_filename}")
        is_test_ok = False
        return (is_test_ok, -1, -1 , config_alias , config_hash)
    
    
        
    


def check_working_directory():
    current_dir = os.getcwd()
    actual_file_dir = os.path.dirname(os.path.realpath(__file__))
    if(current_dir != actual_file_dir):
        os.chdir(actual_file_dir)




if __name__ == '__main__':
    # check_working_directory()    
    do_test(config_link="vmess://eyJhZGQiOiIxNTYuMjI1LjY3LjQ3IiwiYWlkIjoiNjQiLCJob3N0IjoiIiwiaWQiOiIzY2E5MTJkYS02YWMyLTQxOGYtYjljZi00NWI2ZjY5NDU3OWIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5MjI0IiwicHMiOiLwn5KaIE1ATSDwn5KZIFdhc2hpbmd0b24gVW5pdGVkIFN0YXRlcyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==")
    do_test("vmess://eyJhZGQiOiIxNTYuMjI1LjY3LjQ3IiwiYWlkIjoiNjQiLCJob3N0IjoiIiwiaWQiOiIzY2E5MTJkYS02YWMyLTQxOGYtYjljZi00NWI2ZjY5NDU3OWIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5MjI0IiwicHMiOiLwn5KaIE1ATSDwn5KZIFdhc2hpbmd0b24gVW5pdGVkIFN0YXRlcyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==")

    # do_test(config_link="vmess://eyJhZGQiOiIxNTYuMjI1LjY3LjQ3IiwiYWlkIjoiNjQiLCJob3N0IjoiIiwiaWQiOiIzY2E5MTJkYS02YWMyLTQxOGYtYjljZi00NWI2ZjY5NDU3OWIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjQ5MjI0IiwicHMiOiLwn5KaIE1ATSDwn5KZIFdhc2hpbmd0b24gVW5pdGVkIFN0YXRlcyIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiIiwidiI6IjIifQ==")
    # do_test("4500","ali.json","vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogInRlc3QxIiwNCiAgImFkZCI6ICJ3ZWIuZ29vZ2xlLmNvbSIsDQogICJwb3J0IjogIjQ0MyIsDQogICJpZCI6ICI2MjBjNjAzMS03MDE4LTQ4ODAtOGI3Ny0wOGY4NDY5ZDlmNmQiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogInRjcCIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJnb29nbGUuY29tIiwNCiAgInBhdGgiOiAiIiwNCiAgInRscyI6ICJ0bHMiLA0KICAic25pIjogInNuaS5nb29nbGUuY29tIiwNCiAgImFscG4iOiAiaDIiLA0KICAiZnAiOiAiYW5kcm9pZCINCn0=")
    # do_test("27000","ali2.json","vless://fa0e6e80-7ede-4c01-b9aa-aa2f43e0afe8@web.yahoo.com:2087?encryption=none&flow=xtls-rprx-vision&security=reality&sni=sni.yahoo.com&fp=firefox&pbk=sCCsXQbQP5Dcw8Ab3Yv-G5wdLZIT0qYCJdU3hSk-mQk&sid=385efdba&type=grpc#test2")    


    