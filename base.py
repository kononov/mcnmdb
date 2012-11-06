#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm.session import object_session

from .db import db

def save_model(model):
    db.session.add(model)
    db.session.commit()
    return model

def save_models(models):
    db.session.add_all(models)
    db.session.commit()
    return models

class UpdateMixin(object):
    """Provides the 'update' convenience function to allow class
    properties to be written via keyword arguments when the object is
    already initialised.

    .. code-block: python

        class Person(Base, UpdateMixin):
            name = db.Column(String(19))

        >>> person = Person(name='foo')
        >>> person.update(**{'name': 'bar'})

    """

    def update(self, **kw):
        for k in kw:
            if hasattr(self, k):
                setattr(self, k, kw[k])

class IdMixin(object):
    """
    Provides the :attrs:`id` primary key column
    """
    id = db.Column(db.Integer(), primary_key=True) # уникальный идентификатор

class TimestampMixin(object):
    """Adds automatically updated created_at and updated_at timestamp
    columns to a table, that unsurprisingly are updated on record INSERT and
    UPDATE. UTC time is used in both cases.
    """

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # дата-время добавления записи
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow) # дата-время обновления записи

class BaseMixin(IdMixin, UpdateMixin, TimestampMixin):
    """Provieds all benefits of
    providing a deform compatible appstruct property and an easy way to
    query VersionedMeta. It also defines an id column to save on boring
    boilerplate.
    """

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    @property
    def session(self):
        return object_session(self)

    @property
    def _history_class(self):
        """Returns the corresponding history class if the inheriting
        class supports versioning (by checking for the existence of a
        '__history_mapper__' attribute). Otherwise, returns None.
        """
        if hasattr(self, '__history_mapper__'):
            return self.__history_mapper__.class_
        else:
            return None

    @property
    def history(self):
        """Returns an SQLAlchemy query of the object's history (previous
        versions). If the class does not support history/versioning,
        returns None.
        """
        history = self.history_class
        if history:
            return self.session.query(history).filter(history.id == self.id)
        else:
            return None

    def generate_appstruct(self):
        """Returns a Deform compatible appstruct of the object and it's
        properties. Does not recurse into SQLAlchemy relationships.
        An example using the :class:`~drinks.models.User` class (that
        inherits from BaseMixin):

        .. code-block:: python

            >>> user = User(username='mcuserpants', disabled=True)
            >>> user.appstruct
            {'disabled': True, 'username': 'mcuserpants'}

        """
        mapper = object_mapper(self)
        return dict([(p.key, self.__getattribute__(p.key)) for
            p in mapper.iterate_properties if
            not self.__getattribute__(p.key) is None])

    @property
    def appstruct(self):
        return self.generate_appstruct()