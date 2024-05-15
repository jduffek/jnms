# host-disco.py
#
# auto discovery using nets.txt, and default ranges if file is not found.
# python3 disc-auto.py        # will scan default/network_ranges and nodes in nodes.db
# python3 disc-auto.py -new   # this will run a new ICMP discovery and build a new nodes.db if not already there
# 
# basic ICMP discovery of the specified network.
#
# if you use file method, do it like this for multiple ranges:
# 10.1.1.1-10.1.1.10
# 10.2.2.1-10.2.2.5

import subprocess
import datetime
from concurrent.futures import ThreadPoolExecutor
import argparse

DEFAULT_RANGES = ["10.1.1.1-10.1.1.10", "1.0.0.1"]  # Default ranges

def icmp_discovery(network_range):
    discovered_hosts = []

    if '-' in network_range:
        start_ip, end_ip = network_range.split('-')
        start_ip_parts = list(map(int, start_ip.split('.')))
        end_ip_parts = list(map(int, end_ip.split('.')))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(start_ip_parts[3], end_ip_parts[3] + 1):
                ip_address = f"{start_ip_parts[0]}.{start_ip_parts[1]}.{start_ip_parts[2]}.{i}"
                command = ["ping", "-c", "1", "-W", "1", ip_address]
                futures.append(executor.submit(ping_host, ip_address, command))

            for future in futures:
                result = future.result()
                if result:
                    discovered_hosts.append(result)
    else:
        ip_address = network_range
        command = ["ping", "-c", "1", "-W", "1", ip_address]
        result = ping_host(ip_address, command)
        if result:
            discovered_hosts.append(result)

    return discovered_hosts

def ping_host(ip_address, command):
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode == 0:
        print(f"{ip_address} is alive")
        return f"{ip_address}:ICMP"

def new_discovery():
    choice = input("Would you like to input a network range(s)? (yes/file/no): ").lower()
    
    if choice == "yes":
        ranges_input = input("Enter the network range(s) (e.g., 192.168.1.1-192.168.1.254): ")
        network_ranges = ranges_input.split(",")
        discovered_hosts = []
        for network_range in network_ranges:
            discovered_hosts.extend(icmp_discovery(network_range))
    elif choice == "file":
        file_name = input("What is the name of the file?: ")
        try:
            with open(file_name, 'r') as file:
                network_ranges = [line.strip() for line in file.readlines()]
                discovered_hosts = []
                for network_range in network_ranges:
                    discovered_hosts.extend(icmp_discovery(network_range))
        except FileNotFoundError:
            print("File not found.")
            return
    elif choice == "no":
        network_ranges = DEFAULT_RANGES  # Default ranges
        discovered_hosts = []
        for network_range in network_ranges:
            discovered_hosts.extend(icmp_discovery(network_range))
    else:
        print("Invalid choice.")
        return

    return discovered_hosts

def default_discovery():
    file_name = "nets.txt"
    try:
        with open(file_name, 'r') as file:
            network_ranges = [line.strip() for line in file.readlines()]
            discovered_hosts = []
            for network_range in network_ranges:
                discovered_hosts.extend(icmp_discovery(network_range))
    except FileNotFoundError:
        print("nets.txt file not found. Using default ranges.")
        discovered_hosts = []
        for network_range in DEFAULT_RANGES:
            discovered_hosts.extend(icmp_discovery(network_range))

    return discovered_hosts

def main():
    parser = argparse.ArgumentParser(description="ICMP network discovery")
    parser.add_argument("-new", action="store_true", help="Enable new discovery")
    args = parser.parse_args()

    if args.new:
        discovered_hosts = new_discovery()
    else:
        discovered_hosts = default_discovery()

    if not discovered_hosts:
        return

    filename = "disco/host-disco_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open(filename, 'w') as f:
        for host in discovered_hosts:
            f.write(host + '\n')

    print(f"Discovery results saved to {filename}")

    # Read existing hosts from nodes.db file into a set
    existing_hosts = set()
    try:
        with open("nodes.db", 'r') as nodes_file:
            existing_hosts = {line.strip() for line in nodes_file.readlines()}
    except FileNotFoundError:
        pass  # If nodes.db doesn't exist, proceed without existing hosts

    # Write to nodes.db file in append mode, avoiding duplicates
    written_hosts = set(existing_hosts)  # Initialize with existing hosts
    with open("nodes.db", 'a') as nodes_file:
        for host in discovered_hosts:
            if host not in written_hosts:
                nodes_file.write(host + '\n')
                written_hosts.add(host)

    print("Results also saved to nodes.db")

if __name__ == "__main__":
    main()
