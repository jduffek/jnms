# monitors.py
#
# ICMP and TCP, etc, monitors with added functionality to beep once a minute when a node is down.
# Also includes email alerting functionality using smtp.py

import subprocess
import socket
import time
import sys
from smtp import send_email, sender_email, receiver_email, smtp_server, smtp_port, password

# Define constants
BEEP_ENABLED = False  # Set to True to enable beep, False to disable
SMTP_ENABLED = True  # Set to True to enable email alerts, False to disable
SMS_ENABLED = False  # Set to True to enable SMS alerts, False to disable

BEEP_DELAY = 60  # Delay for beeping in seconds
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
        message += f"- {node}\n"
    message += "Please check."
    return subject, message

def main():
    last_email_time = 0
    last_beep_time = 0

    while True:
        try:
            with open('nodes.db', 'r') as file:
                hosts = file.read().splitlines()
        except FileNotFoundError:
            print("Error: nodes.db file not found")
            time.sleep(60)
            continue

        down_nodes = []

        for host_entry in hosts:
            if ':ICMP' in host_entry:
                host = host_entry.split(':')[0]
                if not icmp_monitor(host):
                    down_nodes.append(host)
            elif ':SNMP' in host_entry:
                # Ignore SNMP entries
                continue
            else:
                parts = host_entry.split(':')
                if len(parts) == 2:
                    host, port = parts
                    try:
                        port = int(port)
                        if not tcp_monitor(host, port):
                            down_nodes.append(f"{host}:{port}")
                    except ValueError:
                        print(f"Invalid port {port} specified for host {host}")
                else:
                    print(f"Invalid format specified for host {host_entry}")

        current_time = time.time()
        if down_nodes:
            if current_time - last_beep_time >= BEEP_DELAY:
                beep()
                last_beep_time = current_time
            if SMTP_ENABLED and current_time - last_email_time >= EMAIL_DELAY:
                subject, message = generate_alert_message(down_nodes)
                send_alert_email(subject, message)
                last_email_time = current_time

        # Delay before the next check
        time.sleep(10)

if __name__ == "__main__":
    main()
