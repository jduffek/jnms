# snmp.py
# 
# if run without switch it will default to sending a SNMP GET to all SNMP nodes in the nodes.db
# python3 snmp.py 10.1.1.1 -g -c public -o 1.3.6.1.2.1.1.1.0
# python3 snmp.py 10.1.1.1 -w -c public
# python3 snmp.py 10.1.1.1 -w -c public -f snmpwalk.txt
#
# this specifies oid file:
# python3 snmp.py -m -i 30 -l qnap_monitor.log -of oids.txt
#
# this will use default and/or oid file specified in nodes.db config:
# python3 snmp.py -m -i 30 -l qnap_monitor.log
#
# nodes.db file example:
# 10.1.1.147:SNMP:string:qnap.txt
#
# and/else it will use oids.txt by default

import datetime
import time
import argparse
import os
from pysnmp.hlapi import *

def snmp_get(ip, community, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((ip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
    )
    
    if errorIndication:
        return f"SNMP GET error for {ip}: {errorIndication}"
    elif errorStatus:
        return f"SNMP GET error for {ip}: {errorStatus}"
    else:
        for oid, value in varBinds:
            return f"{oid} = {value.prettyPrint() if value else 'N/A'}"

def monitor_device(ip, community, default_oids, custom_oids, interval, log_file):
    with open(log_file, 'a') as f:
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for oid in default_oids + custom_oids:
                result = snmp_get(ip, community, oid)
                log_entry = f"{now} - {result}\n"
                print(log_entry.strip())
                f.write(log_entry)
                f.flush()  # Ensure data is written to the file immediately
            time.sleep(interval)

def read_nodes_db(file_path):
    snmp_nodes = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2 and parts[1].upper() == 'SNMP':
                ip = parts[0]
                community = parts[2] if len(parts) >= 3 else 'public'
                custom_oid_file = parts[3] if len(parts) >= 4 else None
                snmp_nodes[ip] = (community, custom_oid_file)
    return snmp_nodes

def read_oids(file_path):
    oids = []
    if file_path:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignore empty lines and comments
                    oid = line.split()[0]  # Take the first part of the line, before any comment
                    oids.append(oid)
    return oids

def main():
    default_file_path = os.path.join(os.getcwd(), 'nodes.db')
    default_oid_file = 'oids.txt'
    default_interval = 60
    default_log_file = 'snmp_monitor.log'

    parser = argparse.ArgumentParser(description='Perform SNMP operations.')
    parser.add_argument('file_path', type=str, nargs='?', default=default_file_path, help='Path to nodes.db file')
    parser.add_argument('-m', dest='monitor', action='store_true', help='Monitor device using SNMP')
    parser.add_argument('-i', dest='interval', type=int, default=default_interval, help='Interval for SNMP monitoring in seconds')
    parser.add_argument('-l', dest='log_file', type=str, default=default_log_file, help='Log file for SNMP monitoring')
    args = parser.parse_args()

    snmp_nodes = read_nodes_db(args.file_path)

    for ip, (community, custom_oid_file) in snmp_nodes.items():
        default_oids = read_oids(default_oid_file)
        custom_oids = read_oids(custom_oid_file) if custom_oid_file else []
        monitor_device(ip, community, default_oids, custom_oids, args.interval, args.log_file)

if __name__ == "__main__":
    main()
