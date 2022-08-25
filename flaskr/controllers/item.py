from flask import Blueprint, jsonify, request
from flaskr.models.item import Item
from flaskr.daos.item import item_dao
from flaskr.controllers.auth import is_admin

item_api = Blueprint("item_api", __name__)

@item_api.route("/add_item", methods=["POST"])
@is_admin()
def add_item():
    data = request.json
    item = item_dao.create(Item.from_data(data), commit=True, flush=True)
    return jsonify({"itemId": item.item_id})


@item_api.route("/delete_item", methods=["POST"])
@is_admin()
def delete_item():
    item_id = request.json["itemId"]
    item = item_dao.find_one(Item.item_id == item_id)
    item_dao.delete(item, commit=True, flush=True)
    return jsonify({"itemId": item.item_id})


@item_api.route("/update_item", methods=["POST"])
@is_admin()
def update_item():
    data = request.json
    item_id = request.json["itemId"]
    item = item_dao.find_one(Item.item_id == item_id)
    item.update_data(data)
    item_dao.update(item, commit=True)
    return jsonify({"itemId": item.item_id})


@item_api.route("/get_items", methods=["GET"])
def get_items():
    items = item_dao.list_all()
    item_list = [
        {**Item.get_data(item)}
        for item in items
    ]
    return jsonify({"Result": item_list})
