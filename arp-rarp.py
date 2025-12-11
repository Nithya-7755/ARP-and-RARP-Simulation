import random
import os
import platform
import re
from time import sleep

# ---------- Preloaded ARP Cache ----------
arp_cache = {
    "192.168.1.1": "3C:F0:11:9B:2A:11",
    "192.168.1.2": "98:5F:D3:4A:77:22",
    "192.168.1.3": "B4:6D:83:1F:23:33",
    "192.168.1.4": "54:2A:1B:7C:99:44",
    "192.168.1.5": "70:85:C2:3B:56:55",
    "192.168.1.6": "28:92:A4:6F:88:66",
    "192.168.1.7": "40:B8:37:9D:1A:77",
    "192.168.1.8": "A0:32:99:4E:9C:88",
    "192.168.1.9": "18:AF:61:2C:4E:99",
    "192.168.1.10": "9C:3D:CF:7B:54:AA",
    "192.168.1.11": "F4:6B:EF:88:1D:BB",
    "192.168.1.12": "5C:CF:7F:9E:AA:CC",
    "192.168.1.13": "B8:8A:EC:1F:CB:DD",
    "192.168.1.14": "84:C5:A6:4B:76:EE",
    "192.168.1.15": "00:1A:2B:3C:4D:5E"
}

# ---------- Utility Functions ----------
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def random_mac():
    """Generate a realistic random unicast MAC address."""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02X" % x, mac))

def validate_ip(ip):
    """Check if an IP address is in correct format."""
    pattern = re.compile(
        r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return re.match(pattern, ip)

def validate_mac(mac):
    """Check if a MAC address is in correct format."""
    pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")
    return re.match(pattern, mac)

# ---------- ARP Process ----------
def arp_request(ip):
    print(f"\n[*] Checking ARP cache for IP {ip}...")
    sleep(0.7)

    if not validate_ip(ip):
        print(f"[!] Invalid IP address format. Please enter a valid IP (e.g., 192.168.1.10).")
        return

    if ip in arp_cache:
        print(f"[+] Entry found in cache.")
        print(f"[#] MAC Address of {ip} is {arp_cache[ip]}")
        return

    print(f"[!] IP {ip} not found in cache.")
    sleep(0.6)
    print("[*] Broadcasting ARP Request on LAN...")
    sleep(1.2)
    print(f"[+] Reply received from {ip}.")
    sleep(0.5)

    mac = random_mac()
    arp_cache[ip] = mac
    print(f"[#] MAC Address of {ip} is {mac}")
    print("[*] Entry added to ARP cache.")

# ---------- RARP Process ----------
def rarp_request(mac):
    print(f"\n[*] Searching ARP cache for MAC {mac}...")
    sleep(0.7)

    if not validate_mac(mac):
        print(f"[!] Invalid MAC address format. Please enter a valid MAC (e.g., 00:1A:2B:3C:4D:5E).")
        return

    for ip, mac_addr in arp_cache.items():
        if mac_addr.lower() == mac.lower():
            print(f"[+] Reply received.")
            sleep(0.5)
            print(f"[#] IP Address of {mac} is {ip}")
            return

    print(f"[!] MAC {mac} not found in cache.")
    sleep(0.6)
    print("[*] Sending RARP Request to network server...")
    sleep(1.2)

    ip = f"192.168.1.{random.randint(16, 99)}"
    arp_cache[ip] = mac.upper()

    print(f"[+] Reply received from RARP Server.")
    sleep(0.5)
    print(f"[#] IP Address of {mac} is {ip}")
    print("[*] Entry added to ARP cache.")

# ---------- Display Cache ----------
def display_cache():
    print("\n========== ARP CACHE TABLE ==========")
    if not arp_cache:
        print("Cache is empty.")
        return
    print(f"{'IP Address':<20} {'MAC Address'}")
    print("-" * 40)
    for ip, mac in arp_cache.items():
        print(f"{ip:<20} {mac}")
    print("=====================================")

# ---------- Main Menu ----------
while True:
    print("\n=========== ARP / RARP MENU ===========")
    print("1. ARP (Find MAC Address from IP)")
    print("2. RARP (Find IP Address from MAC)")
    print("3. Display ARP Cache Table")
    print("4. Exit")
    print("=======================================")

    try:
        choice = int(input("Enter your choice (1-4): ").strip())
    except ValueError:
        print("Invalid input! Please enter 1–4.")
        continue

    if choice == 1:
        target_ip = input("Enter Target IP Address (e.g., 192.168.1.10): ").strip()
        arp_request(target_ip)

    elif choice == 2:
        target_mac = input("Enter MAC Address (e.g., 00:1A:2B:3C:4D:5E): ").strip()
        rarp_request(target_mac)

    elif choice == 3:
        display_cache()

    elif choice == 4:
        print("\nExiting... Goodbye!")
        break

    else:
        print("Invalid choice! Please select between 1 and 4.")
