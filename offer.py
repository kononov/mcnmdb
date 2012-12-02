#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin, ByMixin


OFFER_STATE_UNKNOWN = 0
OFFER_STATE_OK      = 1
OFFER_STATE_DELETE  = 2


class Offer(db.Model, BaseMixin, ByMixin):
    """
    Таблица предложений
    """

    __tablename__ = 'offers'

    name             = db.Column(db.String(255), nullable=False)  # Название предлоджения, пример "Колбаса Охотничья"
    description      = db.Column(db.String(1000))  # Описание акции
    store_id         = db.Column(db.Integer, db.ForeignKey('stores.id'))  # id магазина, чье предложение
    price            = db.Column(db.Numeric(10,2))  # стоимость предложения, например "1234.70"

    measure_id       = db.Column(db.Integer, db.ForeignKey('measures.id')) # id типа едницы товара

    type             = db.Column(db.Integer)  # тип предложения 0-обычное, 1-спец предложение
    state_id         = db.Column(db.Integer, db.ForeignKey('offer_states.id'))  # id состояния предложения

    background_color = db.Column(db.String(10))  # цвет фона предложения в интерфейсе (актуально для спец. предложений)
    border_color     = db.Column(db.String(10))  # цвет рамки спец предложения в интерфейсе (актуально для спец. предложений)
    text_color       = db.Column(db.String(10))  # цвет текста предложения в интерфейсе (актуально для спец. предложений)

    logo             = db.Column(db.String(1000))  # ссылка на лого (актуально для спец. предложений)
    oldprice         = db.Column(db.Numeric(10,2))  # стоимость предложения, например "234.70" (актуально для спец. предложений)

    items            = db.relationship('ShoppingListItem', backref=db.backref('offer'))
    datefinish       = db.Column(db.DateTime, nullable=False)  # дата-время окончания действия предложения

    taskitem_id      = db.Column(db.Integer, db.ForeignKey('task_items.id')) # id элемента задачи если это была пакетная загрузка

    __table_args__ = (
                       db.Index("idx_offers_store_id", "store_id"),
                       db.Index("idx_offers_state_id", "state_id"),
                       db.Index("idx_offers_taskitem_id", "taskitem_id"),
                     )


    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Offer id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

class Measure(db.Model, BaseMixin):
    """
    Таблица типов единиц товаров
    """

    __tablename__ = 'measures'
    description   = db.Column(db.String(1000))  # Описание


class OfferPicture(db.Model, BaseMixin, ByMixin):
    """
    Таблица изображений для предложений
    """

    __tablename__ = 'offer_pictures'

    offer_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # id магазина
    url      = db.Column(db.UnicodeText) # Адрес фото



class OfferState(db.Model, BaseMixin):
    """
    Таблица состояний предложения
    """

    __tablename__ = 'offer_states'
    description = db.Column(db.Unicode(1000))  # Описание состояния транзакции
