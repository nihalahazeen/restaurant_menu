from flaskr.daos.base import BaseDAO
from flaskr.models.user import User


class UserDAO(BaseDAO):
    model_cls = User


user_dao = UserDAO()