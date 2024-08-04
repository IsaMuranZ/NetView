# app/routes.py

from flask import current_app as app
from flask import jsonify
# The application will need to be able to generate JSON
from .models import Device, TrafficStat


# route for landing page
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Network Monitoring Tool!"})


# Endpoint for retrieving data on devices
@app.route('/devices', methods=['GET'])
def list_devices():
    # query the entire list of devices
    devices = Device.query.all()

    # format the resulting data from the query above into a list with useful tags
    device_list = [
        {
            'ip': d.ip_address,
            'mac': d.mac_address,
            'hostname': d.hostname,
            'status': d.status,
            'ports': d.open_ports,
            'services': d.services
        }for d in devices
    ]
    return jsonify(device_list)


# Endpoint for retrieving traffic stats in the database
@app.route('/traffic', methods=['GET'])
def get_traffic_stats():
    # query the entire list of traffic statistics
    stats = TrafficStat.query.all()
    traffic_data = [
        {
            'ip': stat.ip_address,
            'bytes': stat.bytes_transferred,
            'packets': stat.packets_transferred,
            'is_internal': stat.is_internal
        } for stat in stats
    ]
    return jsonify(traffic_data)
