# scripts/continuous_monitoring.py
# Up until now, the application has 2 scripts for retrieving devices on the network and monitoring traffic
# from those devices. The scripts had to be manually run and, in the application, would have to run by a user
# This file extends the detection of devices and monitoring of traffic by doing it continuously without
# manually running scripts.

# on my machine RUN WITH: `sudo PYTHONPATH=$PYTHONPATH:/home/user/Workspace/NetView/
#                           /home/user/Workspace/NetView/.venv/bin/python
#                           scripts/continuous_monitoring.py`

import time
# time module is for scheduling the scripts at some time interval
import nmap
# module for detecting devices
from scapy.all import sniff
from app import create_app, db
from app.models import Device, TrafficStat
from collections import defaultdict
# the above modules are used in .capture.py and .network_map.py. See those files for details.

# Initialize network scanner and traffic statistics dictionary
nm = nmap.PortScanner()
traffic_stats = defaultdict(lambda: {'bytes': 0, 'packets': 0})
# these are declared in global scope so multiple functions can use these modules


# check if IP is part of internal network. Currently hardcoded for a certain range.
# Needs to be extended
def is_internal_network(ip_address):
    return ip_address.startswith('192.168.1.')


# This function uses nmap to return a list of devices on a network range and their details and
# returns them.
def scan_network(network_range):
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
                'services': ','.join(services),
                'is_internal': is_internal_network(ip_address)
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


# Callback function used by scapy sniff method to capture data like bytes and # of packets.
def packet_callback(packet):
    if packet.haslayer('IP'):
        ip_src = packet['IP'].src
        ip_dst = packet['IP'].dst
        packet_size = len(packet)

        # Update traffic stats for source and destination
        # this is the running total
        traffic_stats[ip_src]['bytes'] += packet_size
        traffic_stats[ip_src]['packets'] += 1

        traffic_stats[ip_dst]['bytes'] += packet_size
        traffic_stats[ip_dst]['packets'] += 1


def save_traffic_stats_to_db():
    with app.app_context():
        for ip, stats in traffic_stats.items():
            existing_stat = TrafficStat.query.filter_by(ip_address=ip).first()
            # above and below code is checking for duplicate IPs in the sniff data
            # if they are found, then we just update the database number of bytes and packets
            if existing_stat:
                existing_stat.bytes_transferred += stats['bytes']
                existing_stat.packets_transferred += stats['packets']
                existing_stat.is_internal = is_internal_network(ip)
            else:
                # New IP in traffic sniff data so create a new entry to the database
                new_stat = TrafficStat(
                    ip_address=ip,
                    bytes_transferred=stats['bytes'],
                    packets_transferred=stats['packets'],
                    is_internal=is_internal_network(ip)
                )
                db.session.add(new_stat)
            db.session.commit()


# function that runs indefinetly to add any new devices/traffic and update existing records
def continuous_monitoring(network_range, interface, scan_interval=300):
    print(f"Starting continuous monitoring on interface {interface} for network {network_range}")

    while True:
        # Perform a network scan
        scan_network(network_range)

        # Start packet capture for a duration equal to half the scan interval
        sniff(iface=interface, prn=packet_callback, store=False, timeout=scan_interval / 2)

        # Save traffic statistics to the database
        save_traffic_stats_to_db()
        print(f"Scan Complete with no errors at time {time.ctime()}")
        # Wait for the remainder of the interval before the next scan
        time.sleep(scan_interval / 2)


if __name__ == "__main__":
    app = create_app()
    # Adjust network range and interface to match your setup
    network_range = '192.168.1.0/24'
    interface = 'eth0'
    continuous_monitoring(network_range, interface)
