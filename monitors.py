# monitors.py
#
# ICMP and TCP, etc, monitors with added functionality to beep once a minute when a node is down.
# Also includes email alerting functionality using smtp.py

import subprocess
import socket
import time
import sys
import importlib.util
from smtp import send_email, sender_email, receiver_email, smtp_server, smtp_port, password

# Define constants
BEEP_ENABLED = True  # Set to True to enable beep, False to disable
SMTP_ENABLED = True    # Set to True to enable email alerts, False to disable
SMS_ENABLED = False    # Set to True to enable SMS alerts, False to disable
#####
BEEP_DELAY = 10  # Delay for beeping in seconds
EMAIL_DELAY = 60  # Delay for sending email alerts in seconds


def icmp_monitor(host):
    try:
        subprocess.run(['ping', '-c', '1', host], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{host}: ICMP OK")
        return True
    except subprocess.CalledProcessError:
        print(f"{host}: ICMP Failed")
        return False

def tcp_monitor(host, port):
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"{host}:{port} TCP OK")
            return True
    except (socket.timeout, ConnectionRefusedError):
        print(f"{host}:{port} TCP Failed")
        return False

def beep():
    if BEEP_ENABLED:
        sys.stdout.write('\a')
        sys.stdout.flush()

def send_alert_email(subject, message):
    if SMTP_ENABLED:
        send_email(subject, message)

def generate_alert_message(down_nodes):
    subject = "[ALERT] Node(s) Down"
    message = "The following node(s) are down:\n"
    for node in down_nodes:
        message += f"- {node}\n"   #################something broken here body is gross.
    message += "Please check."
    return subject, message

def main():
    while True:
        with open('nodes.db', 'r') as file:
            hosts = file.read().splitlines()

        nodes_down = False

        for host in hosts:
            if ':' in host:
                host, port = host.split(':')
                try:
                    port = int(port)
                    if not tcp_monitor(host, port):
                        nodes_down = True
                except ValueError:
                    print(f"Invalid port {port} specified for host {host}")
                    nodes_down = True
            else:
                if not icmp_monitor(host):
                    nodes_down = True

        if nodes_down:
            beep()
            if SMTP_ENABLED:
                subject, message = generate_alert_message(hosts)
                send_alert_email(subject, message)

        # Add a delay for beeping
        time.sleep(BEEP_DELAY)

        # Add a separate delay for sending email alerts
        time.sleep(EMAIL_DELAY - BEEP_DELAY)

if __name__ == "__main__":
    main()
