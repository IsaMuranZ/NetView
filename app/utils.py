# app/utils.py
# this is where utility functions will be stored that scripts and other project files will import from.

# module for retrieving default gateway
import netifaces
import os
from scapy.layers.inet import traceroute


# retrieves the default gateway of the network
def get_default_gateway():
    gateways = netifaces.gateways()
    default_gateway = gateways.get('default', {}).get(netifaces.AF_INET)
    if default_gateway:
        return default_gateway[0]  # The IP address of the gateway
    return None


# parses the system ARP tables to gain information about IP/MAC addresses
def get_arp_table():
    arp_t = {}
    # Execute the arp command (works on Linux systems)
    with os.popen('arp -n') as arp_output:
        for line in arp_output:
            if 'incomplete' not in line:
                fields = line.split()
                if len(fields) >= 4:
                    ip_address = fields[0]
                    mac_address = fields[2]
                    arp_t[ip_address] = mac_address
    return arp_t


# traces the path packets take to get to the destination IP.
# This is useful for creating network topology maps
# dport is the destination port for TCP packets
# this function returns a list of IP addresses that packets take
def perform_tcp_traceroute(target_ip, dport=80):

    # Perform traceroute using TCP packets
    res, _ = traceroute(target_ip, dport=dport, l4='TCP', maxttl=20, verbose=1)

    path = []
    for snd, rcv in res:
        if rcv:
            path.append(rcv.src)

    return path


# Example: Traceroute to a target IP
target_ip = '192.168.88.109'
path = perform_tcp_traceroute(target_ip)
print(f"Traceroute to {target_ip}: {path}")
