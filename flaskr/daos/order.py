from flaskr.daos.base import BaseDAO
from flaskr.models.order import Order


class OrderDAO(BaseDAO):
    model_cls = Order


order_dao = OrderDAO()