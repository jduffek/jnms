# svc-disco.py
#
# Port scan and save info to nodes.db
#
# Usage:
# python3 svc-disco2.py      # Scans default range:ports, and nodes listed in nodes.db for open ports
# python3 svc-disco2.py -new          # Runs a guided menu for network range input and port scan
# python3 svc-disco2.py -scan my_nets.txt  # Scans IP ranges listed in my_nets.txt for open ports   !need a port config line at top
# python3 svc-disco2.py -scan my_nets.txt -p 1-1024 # Scans IP ranges listed in my_nets.txt for open ports with specified port range
#
# Script behavior:
# - Builds nodes.db with discovered hosts
# - Reads nodes.db to find active hosts for port scanning
# - Supports guided menu for user-defined network ranges
# - Supports scanning IP ranges from a specified file
# - Supports specifying port range in command line arguments
# - Supports port range configuration in the my_nets.txt file
# - Saves port scan results to nodes.db and a timestamped disco file

import os
import sys
import socket
import threading
import argparse
import datetime

# Define the default port range in the configuration
DEFAULT_PORTS = "1-100"
DEFAULT_RANGE = "10.1.1.1-10.1.1.20"  # You can adjust this as needed

def build_nodes_db():
    existing_entries = set()

    # Read existing entries from the nodes.db file
    try:
        with open("nodes.db", 'r') as db_file:
            for line in db_file:
                existing_entries.add(line.strip())
    except FileNotFoundError:
        pass  # If nodes.db does not exist yet, ignore the error

    # Scan for all host-discoX files
    host_disco_files = [file for file in os.listdir() if file.startswith("disco/host-disco")]

    # Parse host information from each host-disco file
    new_entries = set()
    for file_name in host_disco_files:
        with open(file_name, 'r') as file:
            for line in file:
                if "alive" in line:
                    parts = line.strip().split()
                    if len(parts) >= 1:
                        host = parts[0]
                        # Ensure the host is a valid IP address
                        try:
                            socket.inet_aton(host)
                            entry = host
                            if len(parts) == 2:
                                entry += f":{parts[1]}"
                            if entry not in existing_entries:
                                new_entries.add(entry)
                        except socket.error:
                            pass  # Skip invalid host entries

    # Write the new entries to the nodes.db file
    with open("nodes.db", 'a') as db_file:
        for entry in new_entries:
            db_file.write(f"{entry}\n")

def port_scan(hosts, ports):
    open_ports = []
    lock = threading.Lock()

    # Parse ports input
    if '-' in ports:
        start_port, end_port = map(int, ports.split('-'))
        ports_to_scan = range(start_port, end_port + 1)
    else:
        ports_to_scan = [int(ports)]

    # Define a function to scan ports for a single host
    def scan_ports_single_host(host):
        for port in ports_to_scan:
            try:
                # Create a socket object
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)  # Set timeout for connection attempt
                
                # Attempt to connect to the host and port
                result = s.connect_ex((host, port))
                
                # Check if the port is open
                if result == 0:
                    with lock:
                        open_ports.append((host, port))
                
                # Close the socket
                s.close()
            except socket.error:
                pass  # Could not connect to host

    # Create threads to scan ports for each host concurrently
    threads = []
    for host in hosts:
        thread = threading.Thread(target=scan_ports_single_host, args=(host,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return open_ports

def get_user_input():
    user_input = input("Do you want to specify ports to scan? (yes/no): ").lower()
    if user_input == 'yes':
        ports = input("Enter port(s) to scan (e.g., 8080 or 8000-8100): ")
        return ports
    else:
        return DEFAULT_PORTS  # Use default ports specified in the configuration

def parse_port_config(file_path):
    port_config = {}
    current_port_range = DEFAULT_PORTS
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("1-") or line.startswith("0-") or line.startswith("1024"):
                current_port_range = line
            elif line:
                port_config[line] = current_port_range
    return port_config

def main():
    print("Discovery started.")

    # Create a timestamp for the log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    log_file_name = f"disco/svc-disco_{timestamp}.txt"

    # Open the log file for writing
    with open(log_file_name, 'w') as log_file:
        log_file.write("Discovery started.\n")

        parser = argparse.ArgumentParser(description="Network and Port Scanner")
        parser.add_argument('-new', action='store_true', help="Run in guided mode")
        parser.add_argument('-scan', type=str, help="Scan using the specified file")
        parser.add_argument('-p', '--port', type=str, help="Specify port range")
        args = parser.parse_args()
        
        # Write the command-line arguments to the log file
        log_file.write(f"Command-line arguments: {sys.argv}\n")

        if args.new:
            ports = get_user_input()
            build_nodes_db()
            discovered_hosts = set()
            try:
                with open("nodes.db", 'r') as db_file:
                    for line in db_file:
                        discovered_hosts.add(line.strip().split(":")[0])
            except FileNotFoundError:
                log_file.write("nodes.db file not found.\n")
                print("nodes.db file not found.")
                return

            open_ports = port_scan(discovered_hosts, ports)

            if open_ports:
                log_file.write("Port scanning complete.\n")
                with open("nodes.db", 'r+') as db_file:
                    existing_entries = set(line.strip() for line in db_file)
                    for host, port in open_ports:
                        result = f"{host}:{port}"
                        if result not in existing_entries:
                            db_file.write(f"{result}\n")
                for host, port in open_ports:
                    log_file.write(f"{host}:{port}\n")
                    print(f"{host}:{port}")
            else:
                log_file.write("No open ports found.\n")
                print("No open ports found.")

            log_file.write("Discovery complete.\n")
            print("Discovery complete.")

        elif args.scan:
            port_config = parse_port_config(args.scan)
            if not port_config:
                log_file.write("Port configuration not found in the specified file.\n")
                print("Port configuration not found in the specified file.")
                return

            try:
                with open(args.scan, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        line = line.strip()
                        if "-" in line:
                            log_file.write(f"Scanning port range: {line}\n")
                            print(f"Scanning port range: {line}")
                        elif line:
                            log_file.write(f"Scanning network range: {line}\n")
                            print(f"Scanning network range: {line}")
                            ports = port_config.get(line, DEFAULT_PORTS)
                            discovered_hosts = port_scan([line], ports)
                            if not discovered_hosts:
                                log_file.write("No open ports found.\n")
                                print("No open ports found.")
                            else:
                                log_file.write("Port scanning complete.\n")
                                print("Port scanning complete.")
                                for host, port in discovered_hosts:
                                    log_file.write(f"{host}:{port}\n")
                                    print(f"{host}:{port}")
            except FileNotFoundError:
                log_file.write(f"File {args.scan} not found.\n")
                print(f"File {args.scan} not found.")
                return

            log_file.write("Discovery complete.\n")
            print("Discovery complete.")

        else:
            # If no option is specified, proceed with default behavior
            try:
                with open("nodes.db", 'r') as db_file:
                    discovered_hosts = set(line.strip().split(":")[0] for line in db_file)
            except FileNotFoundError:
                log_file.write("nodes.db file not found.\n")
                print("nodes.db file not found.")
                return

            open_ports = port_scan(discovered_hosts, DEFAULT_PORTS)

            if open_ports:
                log_file.write("Port scanning complete.\n")
                for host, port in open_ports:
                    log_file.write(f"{host}:{port}\n")
                    print(f"{host}:{port}")
            else:
                log_file.write("No open ports found.\n")
                print("No open ports found.")

            log_file.write("Discovery complete.\n")
            print("Discovery complete.")

if __name__ == "__main__":
    main()
