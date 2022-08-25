from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from flaskr.daos.exceptions import DAOConfigError, DAOCreateFailedError, DAOUpdateFailedError, DAODeleteFailedError
from flaskr.models import Base, db


class BaseDAO:
    model_cls: Base = None

    @classmethod
    def find_one(cls, base_filter: Any) -> Base:
        """
        Find a model by id
        """
        if cls.model_cls is None:
            raise DAOConfigError()
        return db.session.query(cls.model_cls).filter(base_filter).one_or_none()

    @classmethod
    def find_all(cls, base_filter: Any) -> Base:
        """
        Find a model by id
        """
        if cls.model_cls is None:
            raise DAOConfigError()
        return db.session.query(cls.model_cls).filter(base_filter).all()

    @classmethod
    def create(cls, model: Base, commit: bool = False, flush: bool = False) -> Base:
        """
        Generic for creating models
        :raises: DAOCreateFailedError
        """
        try:
            db.session.add(model)
            if commit:
                db.session.commit()
            if flush:
                db.session.flush()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOCreateFailedError(exception=ex)
        return model

    @classmethod
    def update(cls, model: Base, commit: bool = False) -> Base:
        """
        Generic update a model
        :raises: DAOCreateFailedError
        """
        try:
            db.session.merge(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAOUpdateFailedError(exception=ex)
        return model
    
    @classmethod
    def list_all(cls) -> Base:
        """
        List model
        """
        if cls.model_cls is None:
            raise DAOConfigError()
        return db.session.query(cls.model_cls).all()

    @classmethod
    def delete(cls, model: Base, commit: bool = False, flush: bool = False) -> Base:
        """
        Generic for deleting models
        :raises: DAODeleteFailedError
        """
        try:
            db.session.delete(model)
            if commit:
                db.session.commit()
            if flush:
                db.session.flush()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            raise DAODeleteFailedError(exception=ex)
        return model