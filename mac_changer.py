#!/usr/bin/env python3
"""
mac_changer.py - A simple MAC address changer tool.

Author: Cybernerddd (Ampah Agyarko Emmanuel)
GitHub: https://github.com/cybernerddd

Description:
    This script allows you to spoof your MAC address on Linux-based systems.
    Useful for penetration testing, red team engagements, or privacy.

Usage:
    sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
    sudo python3 mac_changer.py --interface wlan0 --random
    sudo python3 mac_changer.py --interface eth0 --restore

Options:
    -i, --interface   Network interface (e.g., eth0, wlan0)
    -m, --mac         New MAC address to set
    -r, --random      Generate and assign a random MAC address
    --restore         Restore the original MAC address for the interface
"""

import subprocess
import argparse
import re
import random
import sys
import os
import json

ORIG_MAC_FILE = "/tmp/.mac_changer_restore.json"

def get_current_mac(interface):
    """Returns the current MAC address of the interface."""
    try:
        output = subprocess.check_output(
            ["ip", "link", "show", interface], text=True
        )
        mac_address_search = re.search(
            r"link/ether\s+([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})", output
        )
        if mac_address_search:
            return mac_address_search.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        print(f"[!] Could not read MAC address for {interface}")
        sys.exit(1)

def change_mac(interface, new_mac):
    """Change the MAC address of the given interface."""
    print(f"[*] Changing MAC address for {interface} to {new_mac}")
    try:
        subprocess.run(["ip", "link", "set", "dev", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", "dev", interface, "address", new_mac], check=True)
        subprocess.run(["ip", "link", "set", "dev", interface, "up"], check=True)
    except subprocess.CalledProcessError:
        print("[!] Failed to change MAC address.")
        sys.exit(1)

def generate_random_mac():
    """Generate a random MAC address with the locally administered bit set."""
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
    )

def validate_mac(mac):
    """Validate the format of the MAC address."""
    pattern = re.compile(r"^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$")
    return pattern.match(mac) is not None

def store_original_mac(interface, mac):
    """Store the original MAC address to a file for restore."""
    orig_data = {}
    if os.path.exists(ORIG_MAC_FILE):
        try:
            with open(ORIG_MAC_FILE, "r") as f:
                orig_data = json.load(f)
        except Exception:
            orig_data = {}
    if interface not in orig_data:
        orig_data[interface] = mac
        with open(ORIG_MAC_FILE, "w") as f:
            json.dump(orig_data, f)

def restore_mac(interface):
    """Restore the original MAC address from the stored file."""
    if not os.path.exists(ORIG_MAC_FILE):
        print("[!] No original MAC address found to restore.")
        sys.exit(4)
    with open(ORIG_MAC_FILE, "r") as f:
        orig_data = json.load(f)
    if interface not in orig_data:
        print(f"[!] No original MAC address found for interface {interface}.")
        sys.exit(4)
    orig_mac = orig_data[interface]
    change_mac(interface, orig_mac)
    updated_mac = get_current_mac(interface)
    if updated_mac == orig_mac:
        print(f"[+] MAC address for {interface} restored to {updated_mac}")
        # Optionally remove the entry after restore
        del orig_data[interface]
        if orig_data:
            with open(ORIG_MAC_FILE, "w") as f:
                json.dump(orig_data, f)
        else:
            os.remove(ORIG_MAC_FILE)
        sys.exit(0)
    else:
        print("[!] Failed to restore MAC address.")
        sys.exit(5)

def main():
    if os.geteuid() != 0:
        print("[!] You must run this script as root.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Simple MAC Address Changer")
    parser.add_argument("-i", "--interface", required=True, help="Network interface")
    parser.add_argument("-m", "--mac", help="New MAC address")
    parser.add_argument("-r", "--random", action="store_true", help="Set a random MAC address")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done, without making changes")
    parser.add_argument("--restore", action="store_true", help="Restore original MAC address")

    args = parser.parse_args()

    if args.restore:
        restore_mac(args.interface)

    current_mac = get_current_mac(args.interface)
    if current_mac:
        print(f"[+] Current MAC for {args.interface}: {current_mac}")
    else:
        print("[!] Could not read current MAC.")
        sys.exit(1)

    if args.random:
        new_mac = generate_random_mac()
    elif args.mac:
        if not validate_mac(args.mac):
            print("[!] Invalid MAC address format.")
            sys.exit(2)
        new_mac = args.mac
    else:
        print("[!] You must specify either --mac or --random, or use --restore")
        sys.exit(1)

    # Store the original MAC before changing if not already stored
    store_original_mac(args.interface, current_mac)

    if args.dry_run:
        print(f"[DRY RUN] Would change MAC of {args.interface} from {current_mac} to {new_mac}")
        sys.exit(0)

    change_mac(args.interface, new_mac)

    updated_mac = get_current_mac(args.interface)
    if updated_mac == new_mac:
        print(f"[+] MAC address successfully changed to {updated_mac}")
        sys.exit(0)
    else:
        print("[!] MAC address change failed.")
        sys.exit(3)

if __name__ == "__main__":
    main()