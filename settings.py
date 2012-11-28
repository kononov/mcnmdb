#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin


class UserSettings(db.Model, BaseMixin):
    __tablename__ = 'user_settings'

    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    option_id   = db.Column(db.Integer, db.ForeignKey('user_options.id'))

    intvalue    = db.Column(db.Integer)      # 
    floatvalue  = db.Column(db.Float)        # 
    stringvalue = db.Column(db.String(1000)) #
    datevalue   = db.Column(db.DateTime)     #
    boolvalue   = db.Column(db.Boolean)      #


class ShoppingListSettings(db.Model, BaseMixin):
    __tablename__ = 'list_settings'

    list_id     = db.Column(db.Integer, db.ForeignKey('lists.id'))
    option_id   = db.Column(db.Integer, db.ForeignKey('list_options.id'))

    intvalue    = db.Column(db.Integer)      # 
    floatvalue  = db.Column(db.Float)        # 
    stringvalue = db.Column(db.String(1000)) #
    datevalue   = db.Column(db.DateTime)     #
    boolvalue   = db.Column(db.Boolean)      #


class UserOption(db.Model, BaseMixin):
    __tablename__ = 'user_options'
    name        = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(1000))

    # настройки пользователя
    settings    = db.relationship('UserSettings', backref=db.backref('option')) 

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Option id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

class ListOption(db.Model, BaseMixin):
    __tablename__ = 'list_options'
    name        = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(1000))

    # настройки списка
    settings    = db.relationship('ShoppingListSettings', backref=db.backref('option'))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Option id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self
