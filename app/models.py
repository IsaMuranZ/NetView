# app/models.py
# The purpose of this file is to define the database models for persistent storage
from . import db

class Device(db.Model):
    # TODO: add history or last connected column
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False)
    hostname = db.Column(db.String(255))
    status = db.Column(db.String(50))

    def __repr__(self):
        return f'<Device {self.ip_address}>'
