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
    nm.scan(hosts=network_range, arguments='-PR -T5 --host-timeout 30s')  # -PR for ARP scan
    # PE is pinging, PR is ARP requests, and increasing the host timeout for more reliable
    # scans. Added T5 for more aggressive scanning

    with app.app_context():
        for host in nm.all_hosts():
            mac_address = nm[host]['addresses'].get('mac', 'N/A')
            # moved the ip field to a variable outside the device dict
            ip_address = nm[host]['addresses'].get('ipv4', '')

            open_ports = []
            # services will be implemented later
            services = []
            # for loop to extract port information from every host
            # A nested for loop is needed because each host can contain multiple open ports
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                # list of ports and services
                for port in lport:
                    open_ports.append(str(port))
                    services.append(nm[host][proto][port]['name'])
            # NOTE: It might be smart to isolate the protocol and port scanning/processing into another function.

            # Prepare the device data
            device_data = {
                'ip_address': ip_address,
                'mac_address': mac_address,
                'hostname': nm[host].hostname(),
                'status': nm[host].state(),
                'open_ports': ','.join(open_ports),
                'services': ','.join(services)
            }

            # existing_device will be an entry from the database if the IP of Device is found
            # in a query of the database. This is to set up for updating existing entries
            existing_device = Device.query.filter_by(ip_address=device_data['ip_address']).first()
            if existing_device:
                # Update the existing device's information
                existing_device.mac_address = device_data['mac_address']
                existing_device.hostname = device_data['hostname']
                existing_device.status = device_data['status']
                existing_device.open_ports = device_data['open_ports']
                existing_device.services = device_data['services']
            else:
                # Add a new device to the database
                new_device = Device(
                    p_address=device_data['ip_address'],
                    mac_address=device_data['mac_address'],
                    hostname=device_data['hostname'],
                    status=device_data['status'],
                    open_ports=device_data['open_ports'],
                    services=device_data['services']
                )
                db.session.add(new_device)
            # commit outside the if else block to commit changes to both existing and new entries
            db.session.commit()
            # NOTE: I combined the scan_network and save to database methods. Probably a bad idea to have
            # a monolithic function like this. Consider changing it.


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

        scan_network(network_range)
