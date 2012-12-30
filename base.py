#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from colanderalchemy import Column
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_mapper, ColumnProperty
from sqlalchemy.orm.session import object_session
from sqlalchemy.orm.properties import RelationshipProperty as RelProperty

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

    def _get_columns(self):
        """Returns a dictionary-like object containing all the columns of the
        specified `model` class.
        """
        return self._sa_class_manager
		
    def _get_relations(self):
        """Returns a list of relation names of `model` (as a list of strings)."""
        cols = self._get_columns()
        return [k for k in cols if isinstance(cols[k].property, RelProperty)]

    def _to_dict(self, deep=None, exclude=None, include=None,
                 exclude_relations=None, include_relations=None):
        """Returns a dictionary representing the fields of the specified `instance`
        of a SQLAlchemy model.

        `deep` is a dictionary containing a mapping from a relation name (for a
        relation of `instance`) to either a list or a dictionary. This is a
        recursive structure which represents the `deep` argument when calling
        :func:`!_to_dict` on related instances. When an empty list is encountered,
        :func:`!_to_dict` returns a list of the string representations of the
        related instances.

        If either `include` or `exclude` is not ``None``, exactly one of them must
        be specified. If both are not ``None``, then this function will raise a
        :exc:`ValueError`. `exclude` must be a list of strings specifying the
        columns which will *not* be present in the returned dictionary
        representation of the object (in other words, it is a
        blacklist). Similarly, `include` specifies the only columns which will be
        present in the returned dictionary (in other words, it is a whitelist).

        .. note::

           If `include` is an iterable of length zero (like the empty tuple or the
           empty list), then the returned dictionary will be empty. If `include` is
           ``None``, then the returned dictionary will include all columns not
           excluded by `exclude`.

        `include_relations` is a dictionary mapping strings representing relation
        fields on the specified `instance` to a list of strings representing the
        names of fields on the related model which should be included in the
        returned dictionary; `exclude_relations` is similar.

        """
        if (exclude is not None or exclude_relations is not None) and \
                (include is not None or include_relations is not None):
            raise ValueError('Cannot specify both include and exclude.')
        # create the dictionary mapping column name to value
        columns = (p.key for p in object_mapper(self).iterate_properties
                   if isinstance(p, ColumnProperty))
        # filter the columns based on exclude and include values
        if exclude is not None:
            columns = (c for c in columns if c not in exclude)
        elif include is not None:
            columns = (c for c in columns if c in include)
        result = dict((col, getattr(self, col)) for col in columns)
        # Convert datetime and date objects to ISO 8601 format.
        #
        # TODO We can get rid of this when issue #33 is resolved.
        for key, value in result.items():
            if isinstance(value, datetime.date):
                result[key] = value.isoformat()
        # recursively call _to_dict on each of the `deep` relations
        deep = deep or {}
        for relation, rdeep in deep.iteritems():
            # Get the related value so we can see if it is None, a list, a query
            # (as specified by a dynamic relationship loader), or an actual
            # instance of a model.
            relatedvalue = getattr(self, relation)
            if relatedvalue is None:
                result[relation] = None
                continue
            # Determine the included and excluded fields for the related model.
            newexclude = None
            newinclude = None
            if exclude_relations is not None and relation in exclude_relations:
                newexclude = exclude_relations[relation]
            elif (include_relations is not None and
                  relation in include_relations):
                newinclude = include_relations[relation]
            if isinstance(relatedvalue, list):
                result[relation] = [self._to_dict(inst, rdeep, exclude=newexclude,
                                             include=newinclude)
                                    for inst in relatedvalue]
            else:
                result[relation] = self._to_dict(relatedvalue.one(), rdeep,
                                            exclude=newexclude,
                                            include=newinclude)
        return result


    @property
    def serialized(self):
        relations = frozenset(self._get_relations())
        deep = dict((r, {}) for r in relations)
	
        return self._to_dict(deep=deep)

class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), nullable=False, primary_key=True)


def before_signal(session, *args):
    map(lambda o: hasattr(o, 'before_new') and o.before_new(), session.new)
    map(lambda o: hasattr(o, 'before_delete') and o.before_delete(), session.deleted)

event.listen(db.session.__class__, 'before_flush', before_signal)
