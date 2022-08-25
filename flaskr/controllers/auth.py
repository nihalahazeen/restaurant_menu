from flask import Blueprint, jsonify, request, session, current_app as app
from flaskr.controllers.exceptions import ControllerException, UnauthorizedException
from flaskr.models.user import User
from flaskr.daos.user import user_dao
from functools import wraps


auth_api = Blueprint("auth_api", __name__)

def is_admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if app.config["TESTING"]:
                return fn(*args, **kwargs)
            if session["isAdmin"] == False:
                raise UnauthorizedException(message="Access denied, admin only")
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@auth_api.route("/signup", methods=["POST"])
@is_admin()
def signup():
    data = request.json
    if not data["username"]:
        raise ControllerException(message="Enter username")
    user = user_dao.find_one(User.username == data["username"])
    if user:
        raise ControllerException(message="username exists")
    password = data["password"]
    confirm_password = data["confirmPassword"]
    if password != confirm_password:
        raise ControllerException(message="Password mismatch")
    data["isAdmin"] = False
    user = user_dao.create(User.from_data(data), commit=True, flush=True)
    return jsonify({"userId": user.id})
    

@auth_api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        raise ControllerException(message="Missing information")
    user = user_dao.find_one(User.username == username)
    session["username"] = username
    session["isAdmin"] = user.is_admin
    return jsonify({"username": user.username, "isAdmin": user.is_admin})


@auth_api.route("/logout", methods=["POST"])
def logout():
    if not session["username"]:
        raise ControllerException(message="Already logged out")
    session["username"] = None
    session["isAdmin"] = None
    return jsonify({"message":"User logged out"})
