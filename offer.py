#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin

class Offer(db.Model, BaseMixin):
    __tablename__ = 'offers'

    name          = db.Column(db.String(255), nullable=False)  # Название предлоджения, пример "Колбаса Охотничья"
    description   = db.Column(db.String(1000))  # Описание акции
    store_id      = db.Column(db.Integer, db.ForeignKey('stores.id'))  # id магазина, чье предложение
    price         = db.Column(db.Float)  # стоимость предложения, например "1234.70"

    measure_id    = db.Column(db.Integer, db.ForeignKey('measures.id')) # id типа едницы товара
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'))  # id пользователя, кто добавил предложение
    type          = db.Column(db.Integer)  # тип предложения 0-обычное, 1-спец предложение

    background_color = db.Column(db.String(10))  # цвет фона предложения в интерфейсе (актуально для спец. предложений)
    border_color     = db.Column(db.String(10))  # цвет рамки спец предложения в интерфейсе (актуально для спец. предложений)
    text_color       = db.Column(db.String(10))  # цвет текста предложения в интерфейсе (актуально для спец. предложений)

    logo          = db.Column(db.String(1000))  # ссылка на лого (актуально для спец. предложений)
    oldprice      = db.Column(db.Float)  # стоимость предложения, например "234.70" (актуально для спец. предложений)

    items         = db.relationship('ShoppingListItem', backref=db.backref('offer'))
    datefinish    = db.Column(db.DateTime, nullable=False)  # дата-время окончания действия предложения

    taskitem_id = db.Column(db.Integer, db.ForeignKey('task_items.id')) # id элемента задачи если это была пакетная загрузка

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Offer id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

class Measure(db.Model, BaseMixin):
    __tablename__ = 'measures'
    description   = db.Column(db.String(1000))  # Описание

class OfferPicture(db.Model, BaseMixin):
    __tablename__ = 'offer_pictures'

    offer_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # id магазина
    url      = db.Column(db.UnicodeText) # Адрес фото
