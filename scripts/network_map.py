# scripts/network_map.py

import nmap
# This is for function calls to the database and the endpoints
from app import create_app, db
# We need the device class to format data from scans to a format for databases
from app.models import Device


# This function uses nmap to return a list of devices on a network range and their details and
# returns them.
def scan_network(network_range):
    nm = nmap.PortScanner()

    # TODO: make the script run faster and fix the sudo issues that make it run slow.
    # Perform an ARP scan for better MAC address detection on the local network
    nm.scan(hosts=network_range, arguments='-sn -PE -PR --host-timeout 30s')  # -PR for ARP scan
    # PE is pinging, PR is ARP requests, and increasing the host timeout for more reliable
    # scans.

    # list to retrieve devices and return info on them
    devices = []
    print(nm.all_hosts())
    for host in nm.all_hosts():
        # Ensure that 'mac' is a key in the host's addresses
        mac_address = nm[host]['addresses'].get('mac', 'N/A')
        # either this variable is the mac address found by the scan or N/A

        device_info = {
            'ip': nm[host]['addresses'].get('ipv4', ''),
            'mac': mac_address,
            'name': nm[host].hostname(),
            'status': nm[host].state()
        }
        devices.append(device_info)

    return devices


# Function that takes formatted data, updates existing database entries,
# and creates new database entries.
def save_devices_to_db(devices):
    # loop through the list of formatted data
    for device in devices:
        # existing_device will be an entry from the database if the IP of Device is found
        # in a query of the database. This is to set up for updating existing entries
        existing_device = Device.query.filter_by(ip_address=device['ip']).first()
        if existing_device:
            # Update the existing device's information
            existing_device.mac_address = device['mac']
            existing_device.hostname = device['name']
            existing_device.status = device['status']
        else:
            # Add a new device to the database
            new_device = Device(
                ip_address=device['ip'],
                mac_address=device['mac'],
                hostname=device['name'],
                status=device['status']
            )
            db.session.add(new_device)
        # commit outside the if else block to commit changes to both existing and new entries
        db.session.commit()


if __name__ == "__main__":
    # Why? Why the app = create_app() with app.app_context()? Because we make calls to the database
    # using Flask_SQLAlchemy needs the application context to know which database we are working with.
    app = create_app()
    # database operations require the app context
    with app.app_context():
        # Currently the network range is hardcoded for my network
        # TODO: implement identifying the network range automatically
        network_range = '192.168.1,88.0/23'
        # The string has to do with how nmap scans hosts.
        # all the addresses in 192.168.88.0/23 and 192.168.1.0/23 will be scanned
        # this is to support both my home network and my work network

        devices = scan_network(network_range)
        save_devices_to_db(devices)
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}, Name: {device['name']}, Status: {device['status']}")
