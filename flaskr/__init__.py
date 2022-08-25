from flask import Flask
from flask_cors import CORS
from flaskr.models import db
from config import LocalConfig
from flaskr.controllers.auth import auth_api
from flaskr.controllers.order import order_api
from flaskr.controllers.item import item_api
from flaskr.controllers.user import user_api
from flask_session import Session
import logging
from flaskr.controllers.exceptions import ControllerException, UnauthorizedException
from flaskr.daos.exceptions import DAOCreateFailedError, DAOConfigError, DAODeleteFailedError, DAOUpdateFailedError

def handle_controller_exception(e):
    logging.getLogger("app").error(e)
    return {"errors": e.messages}, 400

def handle_unauthorized_exception(e):
    logging.getLogger("app").error(e)
    return {"errors": e.messages}, 401

def handle_dao_config_error(e):
    logging.getLogger("app").error(e.messages)
    return {"errors": e.messages}, 500


def handle_dao_delete_failed_error(e):
    logging.getLogger("app").error(e)
    return {"errors": "Entity not found"}, 500

def handle_dao_update_failed_error(e):
    logging.getLogger("app").error(e)
    return {"errors": e.messages}, 500


def handle_dao_create_failed_error(e):
    logging.getLogger("app").error(e)
    return {"errors": e.message}, 500

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
    app.register_blueprint(user_api)
    app.logger.info(f"Registered the api routes")

    app.register_error_handler(ControllerException, handle_controller_exception)
    app.register_error_handler(UnauthorizedException, handle_unauthorized_exception)
    app.register_error_handler(DAOCreateFailedError, handle_dao_create_failed_error)
    app.register_error_handler(DAOUpdateFailedError, handle_dao_update_failed_error)
    app.register_error_handler(DAODeleteFailedError, handle_dao_delete_failed_error)
    app.register_error_handler(DAOConfigError, handle_dao_config_error)

    @app.route("/")
    def hello():
        return "Hello"

    return app