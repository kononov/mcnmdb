#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import sa as db
from base import BaseMixin, ByMixin


USEROPTION_GPS           = 1
USEROPTION_PUBLISH_OFFER = 2
USEROPTION_PUBLISH_PRICE = 3
USEROPTION_PUBLISH_STORE = 4

LISTOPTION_RADIUS_SEARCH    = 1
LISTOPTION_PRIORITET_SEARCH = 2
LISTOPTION_SORT_BY          = 3

class UserSettings(db.Model, BaseMixin):
    """
    Таблица значений настроек пользователя
    """

    __tablename__ = 'user_settings'
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    option_id   = db.Column(db.Integer, db.ForeignKey('user_options.id'))

    intvalue    = db.Column(db.Integer)        # 
    floatvalue  = db.Column(db.Numeric(10,2))  # 
    stringvalue = db.Column(db.String(1000))   #
    datevalue   = db.Column(db.DateTime)       #
    boolvalue   = db.Column(db.Boolean)        #


class ShoppingListSettings(db.Model, BaseMixin):
    """
    Таблица значений настроек списков
    """

    __tablename__ = 'list_settings'
    list_id     = db.Column(db.Integer, db.ForeignKey('lists.id'))
    option_id   = db.Column(db.Integer, db.ForeignKey('list_options.id'))

    intvalue    = db.Column(db.Integer)        # 
    floatvalue  = db.Column(db.Numeric(10,2))  # 
    stringvalue = db.Column(db.String(1000))   #
    datevalue   = db.Column(db.DateTime)       #
    boolvalue   = db.Column(db.Boolean)        #


class UserOption(db.Model, BaseMixin):
    """
    Таблица-справочник настроек пользователя
    """

    __tablename__ = 'user_options'
    description = db.Column(db.Unicode(1000))

    # настройки пользователя
    settings    = db.relationship('UserSettings', backref=db.backref('option')) 

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Option id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self


class ListOption(db.Model, BaseMixin):
    """
    Таблица-справочник настроек списков
    """

    __tablename__ = 'list_options'
    description = db.Column(db.Unicode(1000))

    # настройки списка
    settings    = db.relationship('ShoppingListSettings', backref=db.backref('option'))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Option id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self
