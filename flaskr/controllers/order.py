from flask import Blueprint, jsonify, request, session
from flaskr.controllers.exceptions import ControllerException
from flaskr.models.user import User
from flaskr.daos.user import user_dao
from flaskr.models.item import Item
from flaskr.daos.item import item_dao
from flaskr.models.order import Order
from flaskr.daos.order import order_dao
from flaskr.controllers.auth import is_admin
import random


order_api = Blueprint("order_api", __name__)

@order_api.route("/add_order", methods=["POST"])
@is_admin()
def add_order():
    user_id = request.json["userId"]
    item_list = request.json["itemList"]
    order_id = random.randint(10000000, 99999999)
    for item in item_list:
        order_dao.create(Order.from_data({"orderId": order_id,"userId": user_id, "itemId": item, "status": "Ordered"}), commit=True, flush=True)
    return jsonify({"orderId": order_id})
    

@order_api.route("/get_orders", methods=["GET"])
@is_admin()
def get_orders():
    orders = order_dao.list_all()
    order_dict = {}
    for order in orders:
        if order.order_id not in order_dict.keys():
            user = user_dao.find_one(User.id == order.user_id)
            item = item_dao.find_one(Item.item_id == order.item_id)
            order_dict[str(order.order_id)] = {
                "orderedAt": order.created_at,
                "status": order.status,
                "customer": user.username,
                "items":[{**Item.get_data(item)}]
            }
        else:
            item = item_dao.find_one(Item.item_id == order.item_id)
            order_dict[str(order.order_id)]["items"].append({**Item.get_data(item)})
    return jsonify(order_dict)


@order_api.route("/update_order", methods=["POST"])
@is_admin()
def update_order():
    data = request.json
    orders = order_dao.find_all(Order.order_id == data["orderId"])
    for order in orders:
        order_data = {**Order.get_data(order)}
        order_data["status"] = data["status"]
        order.update_data(order_data)
        order_dao.update(order, commit=True)
    return jsonify({"orderId": order.order_id})


@order_api.route("/user_orders", methods=["GET"])
def user_orders():
    user_id = request.json.get("userId")
    if not user_id:
        raise ControllerException(message="Missing userId")
    orders = order_dao.find_all(Order.user_id == user_id)
    order_dict = {}
    for order in orders:
        if order.order_id not in order_dict.keys():
            user = user_dao.find_one(User.id == order.user_id)
            item = item_dao.find_one(Item.item_id == order.item_id)
            order_dict[str(order.order_id)] = {
                "orderedAt": order.created_at,
                "status": order.status,
                "customer": user.username,
                "items":[{**Item.get_data(item)}]
            }
        else:
            item = item_dao.find_one(Item.item_id == order.item_id)
            order_dict[str(order.order_id)]["items"].append({**Item.get_data(item)})
    return jsonify(order_dict)
