import os
import socket
import time
import ipaddress

def get_broadcast_address(ip, subnet_mask):
    try:
        network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
        return str(network.broadcast_address)
    except Exception as e:
        print(f"Error calculating broadcast address: {e}")
        return "255.255.255.255"  # Default to global broadcast if calculation fails


def broadcast_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 0))
    while True:
        try:
            ip = os.getenv("HOST_IP", "127.0.0.1")
            subnet_mask = os.getenv("SUBNET_MASK", "255.255.255.0")

            broadcast_address = get_broadcast_address(ip, subnet_mask)

            message = f"flask_backend:{ip}:5000"
            s.sendto(message.encode('utf-8'), (broadcast_address, 5000))
            time.sleep(5)
        except Exception as e:
            print(f"Broadcasting error: {e}")
