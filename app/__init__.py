# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Import routes
        from . import routes

        # Register Blueprints or other modules
        # app.register_blueprint(<your_blueprint>)

    return app
