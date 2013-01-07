#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin, ByMixin
from acl import ACLObjectRef

USEROPTION_GPS           = 1
USEROPTION_PUBLISH_OFFER = 2
USEROPTION_PUBLISH_PRICE = 3
USEROPTION_PUBLISH_STORE = 4

LISTOPTION_RADIUS_SEARCH    = 1
LISTOPTION_PRIORITET_SEARCH = 2
LISTOPTION_SORT_BY          = 3

USER_SETTING_READ  = 'user_setting_read'
USER_SETTING_WRITE = 'user_setting_write'

SHOPPINGLIST_SETTING_READ  = 'shoppinglist_setting_read'
SHOPPINGLIST_SETTING_WRITE = 'shoppinglist_setting_write'

class UserSetting(db.Model, BaseMixin, ACLObjectRef):
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


class ShoppingListSetting(db.Model, BaseMixin, ACLObjectRef):
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
    settings    = db.relationship('UserSetting', primaryjoin="UserSetting.option_id==UserOption.id", backref=db.backref('option'))

    def __str__(self):
        return self.description

    def __repr__(self):
        return "<%s>" % self


class ListOption(db.Model, BaseMixin):
    """
    Таблица-справочник настроек списков
    """

    __tablename__ = 'list_options'
    description = db.Column(db.Unicode(1000))

    # настройки списка
    settings    = db.relationship('ShoppingListSetting', primaryjoin="ShoppingListSetting.option_id==ListOption.id", backref=db.backref('option'))

    def __str__(self):
        return self.description

    def __repr__(self):
        return "<%s>" % self
