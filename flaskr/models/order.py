from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from flaskr.models import Base


class Order(Base):
    __tablename__ = "order"
    id = Column(BigInteger(), primary_key=True)
    order_id = Column(BigInteger)
    user_id = Column(BigInteger, nullable=False)
    item_id = Column(BigInteger, nullable=False)
    status = Column(String)
    created_at = Column(DateTime, default=func.current_timestamp())

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def from_data(data):
        user_schema = OrderSchema(load_instance=False).load(data)
        return Order(**user_schema)

    def update_data(self, data):
        user_schema = OrderSchema(load_instance=False).load(data)
        for k in user_schema.keys():
            setattr(self, k, user_schema[k])

    def get_data(self):
        return OrderSchema().dump(self)


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        unknown = EXCLUDE
        load_instance = True

    order_id = fields.Integer(data_key="orderId")
    user_id = fields.Integer(data_key="userId", required=True)
    item_id = fields.Integer(data_key="itemId", required=True)
    status = fields.String(data_key="status")
    created_at = fields.DateTime(data_key="createdAt")
