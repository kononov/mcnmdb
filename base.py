#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from colanderalchemy import Column
from sqlalchemy import event
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm.session import object_session
from sqlalchemy.orm.properties import RelationshipProperty as RelProperty

from .db import db
from flask.ext.restless.views import _get_relations, _to_dict


def save_model(model):
    db.session.add(model)
    db.session.commit()
    return model

def save_models(models):
    db.session.add_all(models)
    db.session.commit()
    return models

def is_date_field(model, fieldname):
    """Returns ``True`` if and only if the field of `model` with the specified
    name corresponds to either a :class:`datetime.date` object or a
    :class:`datetime.datetime` object.

    """
    prop = getattr(model, fieldname).property
    if isinstance(prop, RelProperty):
        return False
    fieldtype = prop.columns[0].type
    return isinstance(fieldtype, Date) or isinstance(fieldtype, DateTime)

def get_or_create(session, model, **kwargs):
    """Returns the first instance of the specified model filtered by the
    keyword arguments, or creates a new instance of the model and returns that.

    This function returns a two-tuple in which the first element is the created
    or retrieved instance and the second is a boolean value which is ``True``
    if and only if an instance was created.

    The idea for this function is based on Django's ``Model.get_or_create()``
    method.

    `session` is the session in which all database transactions are made (this
    should be :attr:`flask.ext.sqlalchemy.SQLAlchemy.session`).

    `model` is the SQLAlchemy model to get or create (this should be a subclass
    of :class:`~flask.ext.restless.model.Entity`).

    `kwargs` are the keyword arguments which will be passed to the
    :func:`sqlalchemy.orm.query.Query.filter_by` function.

    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance, True


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
    Абстрактная примесь которая добавляет в другие модели id - первичный ключ
    """

    id = Column(db.Integer(), autoincrement=True, primary_key=True, ca_exclude=True)

    @classmethod
    def by_id(cls, id) :
        return db.query(cls).filter_by(id = id).first()



class TimesMixin(object):
    """Абстрактная примесь которая добавляет в другие модели поля:
        created_at - дата создания
        updated_at - дата последнего обновления
    """

    # дата-время добавления записи
    created_at = Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False, ca_exclude=True)
    # дата-время обновления записи
    updated_at = Column(db.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, ca_exclude=True)


class ByMixin(object):
    """Абстрактная примесь которая добавляет в другие модели поля:
        created_by - кто создал
        updated_by - последний кто обновил
    Поля заполняются автоматически. Кто создал и обновил ссылаются на модель User.
    """

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id',
                      onupdate="cascade", ondelete="restrict"))

    @declared_attr
    def updated_by(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id',
                      onupdate="cascade", ondelete="restrict"))


    @declared_attr
    def __table_args__(cls):
        return (
                 db.Index("idx_%s_created_by" % cls.__tablename__.lower(), "created_by"),
                 db.Index("idx_%s_updated_by" % cls.__tablename__.lower(), "updated_by"),
               )


class BaseMixin(IdMixin, UpdateMixin, TimesMixin):
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

    def serialize(self, exclude_columns=None, exclude_relations=None, include_columns=None, include_relations=None):

        relations = frozenset(_get_relations(self))
        # do not follow relations that will not be included in the response
        if include_columns is not None:
            cols = frozenset(include_columns)
            rels = frozenset(include_relations)
            relations &= (cols | rels)
        elif exclude_columns is not None:
            relations -= frozenset(exclude_columns)
        deep = dict((r, {}) for r in relations)

#        result = _to_dict(instance=self, deep=deep, exclude=exclude_columns, include=include_columns, exclude_relations=exclude_relations, include_relations=include_relations)
        result = _to_dict(instance=self, deep=deep, exclude=exclude_columns, exclude_relations=exclude_relations)

        return result


class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), nullable=False, primary_key=True)


def before_signal(session, *args):
    map(lambda o: hasattr(o, 'before_new') and o.before_new(), session.new)
    map(lambda o: hasattr(o, 'before_delete') and o.before_delete(), session.deleted)

event.listen(db.session.__class__, 'before_flush', before_signal)
