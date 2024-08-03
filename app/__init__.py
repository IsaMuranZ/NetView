# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Database configuration
    # this is hardcoded for now and should be changed later to a more graceful solution
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://netview_user:netviewadmin@localhost/netview'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Import parts of our application
        from . import routes

        # Create database tables
        db.create_all()

    return app
