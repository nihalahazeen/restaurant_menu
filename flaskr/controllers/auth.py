from flask import Blueprint, jsonify, request, session
from flaskr.controllers.exceptions import ControllerException
from flaskr.models.user import User
from flaskr.daos.user import user_dao


auth_api = Blueprint("auth_api", __name__)

@auth_api.route("/signup", methods=["POST"])
def signup():
    data = request.json
    user = user_dao.find_one(User.username == data["username"])
    if user:
        raise ControllerException(message="username exists")
    if not data["username"]:
        raise ControllerException(message="Enter username")
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