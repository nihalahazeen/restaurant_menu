from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

Base = declarative_base()


def is_not_blank(val):
    return val is not None and len(val.strip()) != 0