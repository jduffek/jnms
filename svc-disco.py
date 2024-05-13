# svc-disco.py

import os
import socket
import threading

# Define the default port range in the configuration
DEFAULT_PORTS = "1-100"

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
    host_disco_files = [file for file in os.listdir() if file.startswith("host-disco")]

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
                s.settimeout(1)  # Set timeout for connection attempt
                
                # Attempt to connect to the host and port
                result = s.connect_ex((host, port))
                
                # Check if the port is open
                if result == 0:
                    print(f"Port {port} is open on {host}")
                    open_ports.append((host, port))  # Changed format here
                
                # Close the socket
                s.close()
            except socket.error:
                print(f"Could not connect to {host}")

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

def main():
    # Build the nodes.db file
    build_nodes_db()

    # Read hosts from the nodes.db file
    hosts = []
    with open("nodes.db", 'r') as db_file:
        for line in db_file:
            parts = line.strip().split(":")
            if len(parts) >= 1:
                host = parts[0]
                hosts.append(host)

    # Get user input for ports to scan
    ports = get_user_input()

    # Perform port scanning
    open_ports = port_scan(hosts, ports)

    # Output port scanning results
    if open_ports:
        print("Port scanning results:")
        for host, port in open_ports:
            print(f"{host}:{port}")
            # Update nodes.db with the open port
            with open("nodes.db", 'a') as db_file:
                db_file.write(f"{host}:{port}\n")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
