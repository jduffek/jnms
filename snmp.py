# snmp.py
# this all works...just need to tie it into the rest?
# python3 snmp.py 10.1.1.1 -g -c public -o 1.3.6.1.2.1.1.1.0
# python3 snmp.py 10.1.1.1 -w -c public
# python3 snmp.py 10.1.1.1 -w -c public -f snmpwalk.txt

import datetime
from pysnmp.hlapi import *

def snmp_get(ip, community, oid):
    print("Performing SNMP GET operation...")

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
            print(f"{oid} = {value.prettyPrint() if value else 'N/A'}")  # Print OID and its value

def snmp_walk(ip, community, output_file=None):
    print("Performing SNMP WALK operation...")
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
                        f.write(f"{oid} = {value.prettyPrint() if value else 'N/A'}\n")  # Write OID and its value to file
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
                    print(f"{oid} = {value.prettyPrint() if value else 'N/A'}")  # Print OID and its value

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Perform SNMP operations.')
    parser.add_argument('ip', type=str, help='IP address of the SNMP agent')
    parser.add_argument('-c', dest='community', type=str, default='public', help='SNMP community string')
    parser.add_argument('-g', dest='get', action='store_true', help='Perform SNMP GET operation')
    parser.add_argument('-w', dest='walk', action='store_true', help='Perform SNMP WALK operation')
    parser.add_argument('-o', dest='oid', type=str, help='OID for GET operation')
    parser.add_argument('-f', dest='output_file', type=str, default=None, help='Output file for SNMP WALK operation')
    args = parser.parse_args()

    if args.get:
        if not args.oid:
            print("Please provide an OID with -o option for SNMP GET operation.")
            return
        snmp_get(args.ip, args.community, args.oid)
    elif args.walk:
        snmp_walk(args.ip, args.community, args.output_file)
    else:
        print("Please specify either -g (get) or -w (walk) option.")

if __name__ == "__main__":
    main()