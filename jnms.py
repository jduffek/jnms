# jnms.py
# daddy

import subprocess

def main():
    # Execute host discovery script
    subprocess.run(["python3", "host-disco.py"])

    # Execute service discovery script
    subprocess.run(["python3", "svc-disco.py"])

    # Execute service discovery script...soon.
    #subprocess.run(["python3", "snmp.py"])

    # Execute service discovery script
    subprocess.run(["python3", "monitors.py"])

if __name__ == "__main__":
    main()