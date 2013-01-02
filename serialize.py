#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from sqlalchemy.orm import object_mapper, ColumnProperty
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.properties import RelationshipProperty as RelProperty
from sqlalchemy.orm.query import Query

def get_columns(model):
    """Returns a dictionary-like object containing all the columns of the
    specified `model` class.

    """
    return model._sa_class_manager


def get_related_model(model, relationname):
    """Gets the class of the model to which `model` is related by the attribute
    whose name is `relationname`.

    """
    return get_columns(model)[relationname].property.mapper.class_


def get_relations(model):
    """Returns a list of relation names of `model` (as a list of strings)."""
    cols = get_columns(model)
    return [k for k in cols if isinstance(cols[k].property, RelProperty)]


def primary_key_name(model_or_instance):
    """Returns the name of the primary key of the specified model or instance
    of a model, as a string.

    If `model_or_instance` specifies multiple primary keys and ``'id'`` is one
    of them, ``'id'`` is returned. If `model_or_instance` specifies multiple
    primary keys and ``'id'`` is not one of them, only the name of the first
    one in the list of primary keys is returned.

    """
    its_a_model = isinstance(model_or_instance, type)
    mapper = class_mapper if its_a_model else object_mapper
    mapped = mapper(model_or_instance)
    primary_key_names = [key.name for key in mapped.primary_key]
    return 'id' if 'id' in primary_key_names else primary_key_names[0]


# This code was adapted from :meth:`elixir.entity.Entity.to_dict` and
# http://stackoverflow.com/q/1958219/108197.
def to_dict(instance, deep=None, exclude=None, include=None,
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
    columns = (p.key for p in object_mapper(instance).iterate_properties
               if isinstance(p, ColumnProperty))
    # filter the columns based on exclude and include values
    if exclude is not None:
        columns = (c for c in columns if c not in exclude)
    elif include is not None:
        columns = (c for c in columns if c in include)
    result = dict((col, getattr(instance, col)) for col in columns)
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
        relatedvalue = getattr(instance, relation)
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
        # Do some black magic on SQLAlchemy to decide if the related instance
        # should be rendered as a list or as a single object.
        uselist = instance._sa_class_manager[relation].property.uselist
        if uselist:
            result[relation] = [to_dict(inst, rdeep, exclude=newexclude,
                                         include=newinclude)
                                for inst in relatedvalue]
            continue
        # If the related value is dynamically loaded, resolve the query to get
        # the single instance.
        if isinstance(relatedvalue, Query):
            relatedvalue = relatedvalue.one()
        result[relation] = to_dict(relatedvalue, rdeep, exclude=newexclude,
                                    include=newinclude)
    return result