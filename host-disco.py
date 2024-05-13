# host-disco.py
# basic ICMP discovery of the specified network.
#
# if you use file method, do it like this for multiple ranges:
# 10.1.1.1-10.1.1.10
# 10.2.2.1-10.2.2.5
#
#

import subprocess
import datetime

def icmp_discovery(network_ranges):
    discovered_hosts = []

    for network_range in network_ranges:
        # Check if the input is a single IP address
        if '-' not in network_range:
            # If it's a single IP address, treat it as a range with the same start and end IP
            start_ip = end_ip = network_range
        else:
            # Split the network range into start IP address and end IP address
            start_ip, end_ip = network_range.split('-')

        start_ip_parts = list(map(int, start_ip.split('.')))
        end_ip_parts = list(map(int, end_ip.split('.')))
        
        # Iterate over all IP addresses in the range and ping each one
        for i in range(start_ip_parts[3], end_ip_parts[3] + 1):
            ip_address = f"{start_ip_parts[0]}.{start_ip_parts[1]}.{start_ip_parts[2]}.{i}"
            command = ["ping", "-c", "1", "-W", "1", ip_address]
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Check the return code to determine success or failure
            if process.returncode == 0:
                print(f"{ip_address} is alive")
                discovered_hosts.append(f"{ip_address} is alive")
            else:
                print(f"{ip_address} is unreachable")
                discovered_hosts.append(f"{ip_address} is unreachable")

    return discovered_hosts

def main():
    choice = input("Would you like to input a network range(s)? (yes/file/no): ").lower()
    
    if choice == "yes":
        ranges_input = input("Enter the network range(s) (e.g., 192.168.1.1-192.168.1.254): ")
        network_ranges = ranges_input.split(",")
        discovered_hosts = icmp_discovery(network_ranges)
    elif choice == "file":
        file_name = input("What is the name of the file?: ")
        try:
            with open(file_name, 'r') as file:
                network_ranges = [line.strip() for line in file.readlines()]
                discovered_hosts = icmp_discovery(network_ranges)
        except FileNotFoundError:
            print("File not found.")
            return
    elif choice == "no":
        network_ranges = ["10.1.1.1-10.1.1.10", "10.1.1.145-10.1.1.148"]  # Default ranges
        discovered_hosts = icmp_discovery(network_ranges)
    else:
        print("Invalid choice.")
        return

# Save the results to a file with current date and time
    filename = "host-disco_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open(filename, 'w') as f:
        for host in discovered_hosts:
            f.write(host + '\n')

    print(f"Discovery results saved to {filename}")

if __name__ == "__main__":
    main()





