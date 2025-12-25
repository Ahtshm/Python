from netmiko import ConnectHandler
import csv
import socket

# Device credentials
USERNAME = "admin"
PASSWORD = "ISPL@2024"

# IP range
IP_BASE = "10.28.16."
IP_RANGE = range(41, 50)  # 41–49 inclusive

results = []

for i in IP_RANGE:
    ip = f"{IP_BASE}{i}"
    print(f"\nConnecting to {ip} ...")

    device = {
        "device_type": "aruba_aoscx",
        "host": ip,
        "username": USERNAME,
        "password": PASSWORD,
        "timeout": 10,
    }

    # Default row if device is not reachable
    row = {
        "IP Address": ip,
        "Reachability": "Not Reachable",
        "NTP Status": "N/A"
    }

    try:
        conn = ConnectHandler(**device)
        row["Reachability"] = "Reachable"

        # Run show ntp associations for accurate sync status
        output = conn.send_command("show ntp associations")
        conn.disconnect()

        # Check for '*' symbol → currently synchronized server
        if "*" in output:
            row["NTP Status"] = "Synchronized"
        else:
            row["NTP Status"] = "Not Synchronized"

        print(f"{ip} → {row['NTP Status']}")

    except (socket.timeout, Exception):
        print(f"{ip} → Not Reachable")

    results.append(row)

# Write CSV
with open("ntp_sync_inventory.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["IP Address", "Reachability", "NTP Status"]
    )
    writer.writeheader()
    writer.writerows(results)

print("\nNTP inventory completed. CSV file saved as ntp_sync_inventory.csv")
