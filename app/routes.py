# app/routes.py

from flask import current_app as app
from flask import jsonify
# The application will need to be able to generate JSON
from .models import Device, TrafficStat, db
from sqlalchemy.orm import aliased
# aliased is needed for join clarity


# route for landing page
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Network Monitoring Tool!"})


# Endpoint for retrieving data on devices
@app.route('/devices', methods=['GET'])
def list_devices():
    # Alias TrafficStat for better join clarity
    tsalias = aliased(TrafficStat)

    # Perform a left join to include all devices and order by traffic data
    devices = db.session.query(Device, tsalias).outerjoin(
        tsalias, Device.ip_address == tsalias.ip_address
    ).order_by(tsalias.bytes_transferred.desc().nullslast()).all()

    # format the resulting data from the query above into a list with useful tags
    device_list = [
        {
            'ip': d.ip_address,
            'mac': d.mac_address,
            'hostname': d.hostname,
            'status': d.status,
            'open_ports': d.open_ports,
            'services': d.services,
            'traffic_bytes': traffic.bytes_transferred if traffic else 0,
            'traffic_packets': traffic.packets_transferred if traffic else 0
        }for d, traffic in devices
    ]
    return jsonify(device_list)


# Endpoint for retrieving traffic stats in the database
@app.route('/traffic', methods=['GET'])
def get_traffic_stats():
    # Query traffic stats and prioritize internal network traffic
    stats = TrafficStat.query.order_by(TrafficStat.is_internal.desc().nullslast(),
                                       TrafficStat.bytes_transferred.desc()).all()

    traffic_data = [
        {
            'ip': stat.ip_address,
            'bytes': stat.bytes_transferred,
            'packets': stat.packets_transferred,
            'is_internal': stat.is_internal
        } for stat in stats
    ]
    return jsonify(traffic_data)
