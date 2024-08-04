# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Below two imports are for changes to the database that require migration
from flask_migrate import Migrate
from .models import db


def create_app():
    app = Flask(__name__)

    # Database configuration
    # this is hardcoded for now and should be changed later to a more graceful solution
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://netview_user:netviewadmin@localhost/netview'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    # Initialize Flask-Migrate with the app and db. This is for migrations

    with app.app_context():
        # Import parts of our application
        from . import routes

        # Create database tables
        db.create_all()

    return app
