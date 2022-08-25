from flask import Flask
from flask_cors import CORS
from flaskr.models import db
from config import LocalConfig
from flaskr.controllers.auth import auth_api
from flaskr.controllers.order import order_api
from flaskr.controllers.item import item_api
from flask_session import Session


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    if config == "local":
        app.config.from_object(LocalConfig())

    else:
        # load the config if passed in
        app.config.from_object(config)

    app.logger.info(f"Loaded config {config}")
    Session(app)
    db.init_app(app)
    app.register_blueprint(auth_api)
    app.register_blueprint(order_api)
    app.register_blueprint(item_api)
    app.logger.info(f"Registered the api routes")

    @app.route("/")
    def hello():
        return "Hello"

    return app