# jnms.py
# daddy

import subprocess

def main():
    # Execute host discovery script
    subprocess.run(["python3", "host-disco.py"])

    # Execute service discovery script
    subprocess.run(["python3", "svc-disco.py"])

    # Start SNMP script as a background process
    snmp_process = subprocess.Popen(["python3", "snmp.py"])

    # Execute service discovery script
    subprocess.run(["python3", "monitors.py"])

    # Wait for the SNMP script to finish before exiting (optional)
    snmp_process.wait()

if __name__ == "__main__":
    main()
