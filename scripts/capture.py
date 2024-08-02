# scripts/capture.py

from scapy.all import sniff

def packet_callback(packet):
    if packet.haslayer('IP'):
        ip_src = packet['IP'].src
        ip_dst = packet['IP'].dst
        print(f"Packet: {ip_src} -> {ip_dst}")

def start_packet_capture(interface='eth0'):
    print(f"Starting packet capture on {interface}")
    sniff(iface=interface, prn=packet_callback, store=False)

if __name__ == "__main__":
    # Adjust the network interface as needed
    start_packet_capture(interface='eth0')
