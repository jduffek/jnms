# snmp.py
# this all works...just need to tie it into the rest?
# if run without switch it will default to sending a SNMP GET to all SNMP nodes in the nodes.db
# python3 snmp.py 10.1.1.1 -g -c public -o 1.3.6.1.2.1.1.1.0
# python3 snmp.py 10.1.1.1 -w -c public
# python3 snmp.py 10.1.1.1 -w -c public -f snmpwalk.txt

import datetime
from pysnmp.hlapi import *

def snmp_get(ip, community, oid):
    print(f"Performing SNMP GET operation on {ip}...")
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
        print(f"SNMP GET error for {ip}: {errorIndication}")
    elif errorStatus:
        print(f"SNMP GET error for {ip}: {errorStatus}")
    else:
        for oid, value in varBinds:
            print(f"{oid} = {value.prettyPrint() if value else 'N/A'}")

def snmp_walk(ip, community, output_file=None):
    print(f"Performing SNMP WALK operation on {ip}...")
    now = datetime.datetime.now()
    if output_file:
        with open(output_file, "w") as f:
            f.write(f"Generated on {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            line_count = 0
            for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1')),  # Starting from the root of the MIB tree
                lexicographicMode=True
            ):
                if errorIndication:
                    print(f"SNMP WALK error for {ip}: {errorIndication}")
                    break
                elif errorStatus:
                    print(f"SNMP WALK error for {ip}: {errorStatus}")
                    break
                else:
                    for oid, value in varBinds:
                        f.write(f"{oid} = {value.prettyPrint() if value else 'N/A'}\n")
                        line_count += 1
            f.write(f"Finished at {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    else:
        for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((ip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1')),  # Starting from the root of the MIB tree
            lexicographicMode=True
        ):
            if errorIndication:
                print(f"SNMP WALK error for {ip}: {errorIndication}")
                break
            elif errorStatus:
                print(f"SNMP WALK error for {ip}: {errorStatus}")
                break
            else:
                for oid, value in varBinds:
                    print(f"{oid} = {value.prettyPrint() if value else 'N/A'}")

def read_nodes_db(file_path):
    snmp_nodes = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2 and parts[1].upper() == 'SNMP':
                ip = parts[0]
                community = parts[2] if len(parts) >= 3 else 'public'  # Default to 'public' if community string is not provided
                snmp_nodes[ip] = community
    return snmp_nodes

def main():
    import argparse
    import os
    default_file_path = os.path.join(os.getcwd(), 'nodes.db')  # Default path is the local directory
    default_oid = '1.3.6.1.2.1'  # Default OID for SNMP GET operation

    parser = argparse.ArgumentParser(description='Perform SNMP operations.')
    parser.add_argument('file_path', type=str, nargs='?', default=default_file_path, help='Path to nodes.db file')
    parser.add_argument('-g', dest='get', action='store_true', help='Perform SNMP GET operation')
    parser.add_argument('-w', dest='walk', action='store_true', help='Perform SNMP WALK operation')
    parser.add_argument('-o', dest='oid', type=str, default=default_oid, help='OID for GET operation')
    parser.add_argument('-f', dest='output_file', type=str, default=None, help='Output file for SNMP WALK operation')
    args = parser.parse_args()

    snmp_nodes = read_nodes_db(args.file_path)

    if args.walk:
        for ip, community in snmp_nodes.items():
            snmp_walk(ip, community, args.output_file)
    else:
        # Default behavior: Perform SNMP GET operation if neither -g nor -w is specified
        for ip, community in snmp_nodes.items():
            snmp_get(ip, community, args.oid)

if __name__ == "__main__":
    main()
