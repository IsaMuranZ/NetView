# app/routes.py

from flask import current_app as app
from flask import jsonify

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Network Monitoring Tool!"})

@app.route('/devices')
def list_devices():
    # Placeholder for device listing
    return jsonify({"devices": "List of devices will be shown here."})
