# -*- coding: utf-8 -*-
"""detectionclass.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1atcFzpfAAZPbpTX-ZTNPzy0eO0FA0IX6
"""

import socket
import threading

# Function to scan a single port
def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"Port {port} is open")
    sock.close()

# Function to scan multiple ports
def scan_ports(ip, start_port, end_port):
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        thread.start()

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    print(f"Scanning ports {start_port} to {end_port} on {target_ip}...")
    scan_ports(target_ip, start_port, end_port)