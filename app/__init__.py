from flask import Flask
from amadeus import Client
import config
import os

amadeus = Client(
    client_id=config.AMADEUS_API_KEY,
    client_secret=config.AMADEUS_API_SECRET
)

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.static_folder = 'static'

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
