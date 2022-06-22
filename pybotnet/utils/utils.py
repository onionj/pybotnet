import requests
import json
import socket


# Servers to get your public IP


def _get_my_ip_server_1():
    """return global ip V4 and loaction \n
    server 1"""
    takeip = requests.post("https://api.myip.com", timeout=2).text
    ip = str(json.loads(takeip)["ip"])
    country = str(json.loads(takeip)["country"])
    ipaddr = f"{ip}\ncountry: {country}"
    return ipaddr


def _get_my_ip_server_2():
    """return global ip V4 \n
    server 2"""
    return requests.get("https://api.ipify.org", timeout=2).text


def _get_my_ip_server_3():
    """return global ip V4 \n
    server 3"""
    return requests.get("https://ident.me", timeout=2).text


def get_global_ip() -> str:
    """return system ip (3 API server)"""
    for server in [_get_my_ip_server_1, _get_my_ip_server_2, _get_my_ip_server_3]:
        try:
            return server()
        except:
            return None

def get_host_name_ip() -> dict:
    try:
        host_name = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("4.2.2.4", 80))
        host_ip = s.getsockname()[0]
        return {"host_ip": host_ip, "host_name": host_name}
    except:
        return {"host_ip": None, "host_name": None}
