# app/models.py
# The purpose of this file is to define the database models that will
# be used by other functions and for persistent storage
from flask_sqlalchemy import SQLAlchemy
# moved the database declaration from __init__.py to this file
db = SQLAlchemy()


# Device class used when detecting devices on the network and storing in database
class Device(db.Model):
    # TODO: add history or last connected column
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False, unique=True)
    mac_address = db.Column(db.String(17), nullable=False)
    hostname = db.Column(db.String(255))
    status = db.Column(db.String(50))
    # new fields to store data from additional functionality
    open_ports = db.Column(db.String(255))
    services = db.Column(db.String(255))

    def __repr__(self):
        return f'<Device {self.ip_address}>'


# Class for storing statistics about bandwidth usage in database
# this is for each sniff (which lasts about a minute) and should
# be expanded so the data is more meaningful (ie. ongoing total bandwidth usage by an IP)
class TrafficStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    bytes_transferred = db.Column(db.Integer, default=0)
    packets_transferred = db.Column(db.Integer, default=0)
    # New field to indicate a device that's part of internal network traffic
    is_internal = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<TrafficStat {self.ip_address}>'
