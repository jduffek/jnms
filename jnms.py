# jnms.py
# daddy

import subprocess
import sys

def main():
    # Check if the '-new' switch is provided
    if "-new" in sys.argv:
        # Remove the '-new' switch from sys.argv
        sys.argv.remove("-new")

        # Execute host discovery script with -new switch
        subprocess.run(["python3", "host-disco.py", "-new"])
    else:
        # Execute host discovery script
        subprocess.run(["python3", "host-disco.py"])

    # Execute service discovery script
    subprocess.run(["python3", "svc-disco.py"])

    # Start SNMP script as a background process
    snmp_process = subprocess.Popen(["python3", "snmp.py"])

    # Execute service discovery script
    subprocess.run(["python3", "moni.py"])

    # Wait for the SNMP script to finish before exiting (optional)
    snmp_process.wait()

if __name__ == "__main__":
    main()
