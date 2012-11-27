#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin

class ShoppingListItem(db.Model, BaseMixin):
    __tablename__ = 'list_items'

    list_id   = db.Column(db.Integer, db.ForeignKey('lists.id'))
    offer_id  = db.Column(db.Integer, db.ForeignKey('offers.id'))
    purchased = db.Column(db.Boolean, default=False) # True - куплено, False - не куплено
    price     = db.Column(db.Float) # стоимость купленого товара по версии пользователя, например "1234.70"
    confirmed = db.Column(db.Boolean) # True - цена подтверждена, False - цена не подтверждена

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<ListItem id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

class ShoppingList(db.Model, BaseMixin):
    __tablename__ = 'lists'

    name        = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000))
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))

    # список всех позиций в этом списке
    items       = db.relationship('ShoppingListItem',
        backref=db.backref('list', lazy='dynamic'))

    # настройки списка
    settings    = db.relationship('ShoppingListSettings',
        backref=db.backref('list', lazy='dynamic'))

    def __str__(self):
        ctx = (str(self.id), self.name, self.user_id)
        return '<List id=%s, name=%s, user_id=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self
