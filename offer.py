#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin, ByMixin
from acl import ACLObjectRef

OFFER_STATE_UNKNOWN = 0
OFFER_STATE_OK      = 1
OFFER_STATE_DELETE  = 2

OFFER_READ  = 'offer_read'
OFFER_WRITE = 'offer_write'

OFFER_PICTURE_READ  = 'offer_picture_read'
OFFER_PICTURE_WRITE = 'offer_picture_write'


class Offer(db.Model, BaseMixin, ByMixin, ACLObjectRef):
    """
    Таблица предложений
    """

    __tablename__ = 'offers'

    name             = db.Column(db.Unicode(100), nullable=False)  # Название предлоджения, пример "Колбаса Охотничья"
    description      = db.Column(db.UnicodeText())  # Описание акции
    store_id         = db.Column(db.Integer, db.ForeignKey('stores.id'))  # id магазина, чье предложение
    price            = db.Column(db.Numeric(10,2))  # стоимость предложения, например "1234.70"

    weight           = db.Column(db.Numeric(10,4)) # вес товара
    weight_type      = db.Column(db.Integer, db.ForeignKey('weight_types.id')) # единицы измерения веса

    volume           = db.Column(db.Numeric(10,4)) # объем товара для жидкостей
    volume_type      = db.Column(db.Integer, db.ForeignKey('volume_types.id')) # единицы измерения объема

    measure_id       = db.Column(db.Integer, db.ForeignKey('measures.id')) # id типа едницы товара
    measure          = db.relationship("Measure")

    type             = db.Column(db.Integer)  # тип предложения 0-обычное, 1-спец предложение
    state_id         = db.Column(db.Integer, db.ForeignKey('offer_states.id'))  # id состояния предложения

    background_color = db.Column(db.String(10))  # цвет фона предложения в интерфейсе (актуально для спец. предложений)
    border_color     = db.Column(db.String(10))  # цвет рамки спец предложения в интерфейсе (актуально для спец. предложений)
    text_color       = db.Column(db.String(10))  # цвет текста предложения в интерфейсе (актуально для спец. предложений)

    logo             = db.Column(db.String(1000))  # ссылка на лого (актуально для спец. предложений)
    oldprice         = db.Column(db.Numeric(10,2))  # стоимость предложения, например "234.70" (актуально для спец. предложений)

    items            = db.relationship('ShoppingListItem', primaryjoin="ShoppingListItem.offer_id==Offer.id", backref=db.backref('offer'))
    datefinish       = db.Column(db.DateTime, nullable=True)  # дата-время окончания действия предложения

    taskitem_id      = db.Column(db.Integer, db.ForeignKey('task_items.id')) # id элемента задачи если это была пакетная загрузка

    pictures         = db.relationship('OfferPicture', primaryjoin="OfferPicture.offer_id==Offer.id", backref=db.backref('offer'))

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
    Таблица-справочник типов единиц товаров
    """

    __tablename__ = 'measures'
    description   = db.Column(db.String(1000))  # Описание

    def __str__(self):
        return self.description

    def __repr__(self):
        return "<%s>" % self


class WeightType(db.Model, BaseMixin):
    """
    Таблица-справочник единиц измерений веса
    """

    __tablename__ = 'weight_types'
    description = db.Column(db.String(1000))  # Описание
    abbr        = db.Column(db.String(1000))  # Сокращение

    def __str__(self):
        return self.abbr

    def __repr__(self):
        return "<%s>" % self


class VolumeType(db.Model, BaseMixin):
    """
    Таблица-справочник единиц измерений объема
    """

    __tablename__ = 'volume_types'
    description = db.Column(db.String(1000))  # Описание
    abbr        = db.Column(db.String(1000))  # Сокращение

    def __str__(self):
        return self.abbr

    def __repr__(self):
        return "<%s>" % self


class OfferPicture(db.Model, BaseMixin, ByMixin, ACLObjectRef):
    """
    Таблица изображений для предложений
    """

    __tablename__ = 'offer_pictures'

    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id')) # id магазина
    url      = db.Column(db.UnicodeText) # Адрес фото



class OfferState(db.Model, BaseMixin):
    """
    Таблица состояний предложения
    """

    __tablename__ = 'offer_states'
    description = db.Column(db.Unicode(1000))  # Описание состояния транзакции

    def __str__(self):
        return self.description

    def __repr__(self):
        return "<%s>" % self
