from marshmallow import fields, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy import Column, BigInteger, String, Boolean
from flaskr.models import Base, is_not_blank


class User(Base):
    __tablename__ = "user"
    id = Column(BigInteger(), primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(String, nullable = False)
    is_admin = Column(Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def from_data(data):
        user_schema = UserSchema(load_instance=False).load(data)
        return User(**user_schema)

    def update_data(self, data):
        user_schema = UserSchema(load_instance=False).load(data)
        for k in user_schema.keys():
            setattr(self, k, user_schema[k])

    def get_data(self):
        return UserSchema().dump(self)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        unknown = EXCLUDE
        load_instance = True

    id = fields.Integer(data_key="id")
    username = fields.String(data_key="username", required=True, validate=is_not_blank)
    password = fields.String(data_key="password", required=True, validate=is_not_blank)
    is_admin = fields.Boolean(data_key="isAdmin")
