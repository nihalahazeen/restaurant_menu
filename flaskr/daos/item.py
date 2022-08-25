from flaskr.daos.base import BaseDAO
from flaskr.models.item import Item


class ItemDAO(BaseDAO):
    model_cls = Item


item_dao = ItemDAO()