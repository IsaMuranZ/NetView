# app/routes.py

from flask import current_app as app
from flask import jsonify
# The application will need to be able to generate JSON
from .models import Device

# route for landing page
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Network Monitoring Tool!"})

# Endpoint for retrieving data on devices
@app.route('/devices')
def list_devices():
    # Placeholder for device listing
    devices = Device.query.all()
    device_list = [{'ip': d.ip_address, 'mac': d.mac_address, 'hostname': d.hostname, 'status': d.status} for d in devices]
    return jsonify(device_list)
