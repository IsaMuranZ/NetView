# app/models.py
# The purpose of this file is to define the database models that will
# be used by other functions and for persistent storage
from . import db


# Device class used when detecting devices on the network and storing in database
class Device(db.Model):
    # TODO: add history or last connected column
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False)
    hostname = db.Column(db.String(255))
    status = db.Column(db.String(50))


# Class for storing statistics about bandwidth usage in database
# this is for each sniff (which lasts about a minute) and should
# be expanded so the data is more meaningful (ie. ongoing total bandwidth usage by an IP)
class TrafficStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    bytes_transferred = db.Column(db.Integer, default=0)
    packets_transferred = db.Column(db.Integer, default=0)


def __repr__(self):
    return f'<Device {self.ip_address}>'
