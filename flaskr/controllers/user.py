from flask import Blueprint, jsonify
from flaskr.daos.user import user_dao

user_api = Blueprint("user_api", __name__)

@user_api.route("/get_users", methods=["GET"])
def get_users():
    users = user_dao.list_all()
    user_list = [
        {"userId": user.id, "username":user.username}
        for user in users
    ]
    return jsonify({"Result": user_list})