# scripts/capture.py

from scapy.all import sniff
# defaultdict is the data structure used to store traffic statistics
# better than a regular dictionary because keys that are new are automatically
# assigned a default value
from collections import defaultdict
# database model used to populate the database with the data retrieved later in the script
from app.models import TrafficStat
# database operations require app context
from app import db, create_app

# Dictionary to store traffic statistics
traffic_stats = defaultdict(lambda: {'bytes': 0, 'packets': 0})


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


# packet capture function. listens on an ethernet interface for a minute, recording traffic
def start_packet_capture(interface='eth0', duration=60):
    print(f"Starting packet capture on {interface}")
    # Scapy method to sniff traffic
    sniff(iface=interface, prn=packet_callback, store=False, timeout=duration)

    print("\nTraffic Statistics:")
    for ip, stats in traffic_stats.items():
        print(f"IP: {ip}, Bytes: {stats['bytes']}, Packets: {stats['packets']}")


def save_traffic_stats_to_db():
    # similar to network_map.py, we need app context for database operations
    with app.app_context():
        for ip, stats in traffic_stats.items():
            existing_stat = TrafficStat.query.filter_by(ip_address=ip).first()
            # above and below code is checking for duplicate IPs in the sniff data
            # if they are found, then we just update the database number of bytes and packets
            if existing_stat:
                existing_stat.bytes_transferred += stats['bytes']
                existing_stat.packets_transferred += stats['packets']
            else:
                # New IP in traffic sniff data so create a new entry to the database
                new_stat = TrafficStat(
                    ip_address=ip,
                    bytes_transferred=stats['bytes'],
                    packets_transferred=stats['packets']
                )
                db.session.add(new_stat)
            db.session.commit()


if __name__ == "__main__":
    # same as network_map.py
    # Why? Why the app = create_app() with app.app_context()? Because we make calls to the database
    # using Flask_SQLAlchemy which needs the application context to know which database we are working with.
    app = create_app()
    # database operations require the app context
    # Adjust the network interface as needed, Might need to expand this later to more interfaces
    start_packet_capture(interface='eth0', duration=60)
    save_traffic_stats_to_db()
