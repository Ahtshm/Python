from netmiko import ConnectHandler
import re
import csv

ip_base = "10.28.16."
ip_range = range(41, 50)  # 41 to 49

inventory = []

for i in ip_range:
    ip = f"{ip_base}{i}"

    device = {
        "device_type": "aruba_aoscx",
        "host": ip,
        "username": "admin",
        "password": "ISPL@2024",
        "port": 22,
        "timeout": 10,
    }

    try:
        print(f"\nConnecting to {ip} ...")
        conn = ConnectHandler(**device)

        output = conn.send_command("show system")
        conn.disconnect()

        hostname = re.search(r"Hostname\s*:\s*(.*)", output)
        product  = re.search(r"Product Name\s*:\s*(.*)", output)
        serial   = re.search(r"Chassis Serial Nbr\s*:\s*(.*)", output)
        mac      = re.search(r"Base MAC Address\s*:\s*(.*)", output)

        inventory.append({
            "IP Address": ip,
            "Hostname": hostname.group(1) if hostname else "N/A",
            "Model / Part Number": product.group(1) if product else "N/A",
            "Serial Number": serial.group(1) if serial else "N/A",
            "Base MAC Address": mac.group(1) if mac else "N/A",
            "Status": "Reachable",
        })

        print(f"{ip} → Reachable")

    except Exception:
        inventory.append({
            "IP Address": ip,
            "Hostname": "N/A",
            "Model / Part Number": "N/A",
            "Serial Number": "N/A",
            "Base MAC Address": "N/A",
            "Status": "Not Reachable",
        })

        print(f"{ip} → Not Reachable")

# Write CSV
with open("aruba_inventory_10.28.16.41-49.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "IP Address",
            "Hostname",
            "Model / Part Number",
            "Serial Number",
            "Base MAC Address",
            "Status",
        ],
    )
    writer.writeheader()
    writer.writerows(inventory)

print("\nInventory completed. CSV file created successfully.")
