# scripts/network_map.py

import nmap


# This function uses nmap to return a list of devices on a network range and their details and
# returns them.
def scan_network(network_range):
    nm = nmap.PortScanner()

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


if __name__ == "__main__":
    # Currently the network range is hardcoded for my network
    # TODO: implement identifying the network range automatically
    network_range = '192.168.1,88.0/23'
    # The string has to do with how nmap scans hosts.
    # all the addresses in 192.168.88.0/23 and 192.168.1.0/23 will be scanned
    # this is to support both my home network and my work network

    devices = scan_network(network_range)
    print(devices)
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}, Name: {device['name']}, Status: {device['status']}")
