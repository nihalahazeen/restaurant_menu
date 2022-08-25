from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy import Column, BigInteger, Integer, String
from flaskr.models import Base, is_not_blank


class Item(Base):
    __tablename__ = "item"
    item_id = Column(BigInteger(), primary_key=True)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def from_data(data):
        item_schema = ItemSchema(load_instance=False).load(data)
        return Item(**item_schema)

    def update_data(self, data):
        item_schema = ItemSchema(load_instance=False).load(data)
        for k in item_schema.keys():
            setattr(self, k, item_schema[k])

    def get_data(self):
        return ItemSchema().dump(self)


class ItemSchema(SQLAlchemySchema):
    class Meta:
        model = Item
        unknown = EXCLUDE
        load_instance = True

    item_id = fields.Integer(data_key="itemId")
    name = fields.String(data_key="name", required=True, validate=is_not_blank)
    price = fields.Integer(data_key="price")
