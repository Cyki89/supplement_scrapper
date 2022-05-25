from flask import Flask
from .extentions import mongo, cors
from .views import api

 
def create_app(config_obj='supplements_scraper.settings'):
    app = Flask(__name__)

    app.config.from_object(config_obj)

    cors.init_app(app)
    mongo.init_app(app)
   
    api.init_app(app)

    return app