#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .db import db
from base import BaseMixin, ByMixin


STORE_STATE_UNKNOWN = 0
STORE_STATE_OK      = 1
STORE_STATE_DELETE  = 2


#class Corporation(db.Model, BaseMixin, ByMixin):
class Corporation(db.Model, BaseMixin):
    """
    Таблица для ЮЛ магазинов
    """

    __tablename__ = 'corporations'

    name        = db.Column(db.Unicode(), nullable=False) # Название ЮЛ, пример "ОАО Ромашка"
    description = db.Column(db.Unicode(1000))  # Описание ЮЛ
    president   = db.Column(db.Unicode(1000))  # Директор
    INN         = db.Column(db.Unicode(25))  # ИНН
    KPP         = db.Column(db.Unicode(25))  # КПП
    bank        = db.Column(db.Unicode(1000))  # Банк
    account     = db.Column(db.Unicode(20))  # Расчетный счет
    subdomain   = db.Column(db.String(255))  # Поддомен, если задан то личный кабинет парнера доступен по адресу <subdomain>.myconomy.ru

    stores      = db.relationship('Store', backref=db.backref('corporation'))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Corporation id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self


class Store(db.Model, BaseMixin, ByMixin):
    """
    Таблица магазинов
    """

    __tablename__ = 'stores'
    name           = db.Column(db.Unicode(1000), nullable=False) # Название, пример "Перекресток"
    description    = db.Column(db.Unicode(1000)) # Описание магазина
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporations.id')) # id ЮЛ
    city           = db.Column(db.Unicode(1000), nullable=False) # Город, пример "Москва", выбирается из списка известных городов
    region         = db.Column(db.Unicode(1000)) # Район города, пример "ЦАО", , выбирается из списка известных районов/округов
    metro          = db.Column(db.Unicode(1000)) # Ближайшее метро, пример "Арбатская", выбирается из списка известных станций метро
    address        = db.Column(db.Unicode(1000)) # Адрес, пример "ул. Бутырская, д. 20", выбирается из списка известных адресов, типа ФИАС http://fias.nalog.ru/Public/DownloadPage.aspx
    phone          = db.Column(db.Unicode(200)) # Телефон, пример "+7(495)123-34-45"
    open_time      = db.Column(db.String(25))
    close_time     = db.Column(db.String(25))
    lat            = db.Column(db.Float()) # координата: широта
    lng            = db.Column(db.Float()) # координата: долгота

    state_id       = db.Column(db.Integer, db.ForeignKey('store_states.id'))  # id состояния предложения

    delivery       = db.Column(db.Boolean, default=False) # True - есть доставка, False - нет доставки (по умолчанию)
    onlineonly     = db.Column(db.Boolean, default=False) # True - только онлайн, False - обычный розничный магаз (по умолчанию)

    taskitem_id = db.Column(db.Integer, db.ForeignKey('task_items.id')) # id элемента задачи если это была пакетная загрузка

    # список всех предложения этого магазина
    offers         = db.relationship('Offer', backref=db.backref('store'))

    __table_args__ = (
                       db.Index("idx_stores_corporation_id", "corporation_id"),
                       db.Index("idx_stores_state_id", "state_id"),
                       db.Index("idx_stores_taskitem_id", "taskitem_id"),
                     )

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Store id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

groups_stores = db.Table('groups_stores',
    db.Column('store_id', db.Integer(), db.ForeignKey('stores.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('storegroups.id')))


class StoreGroup(db.Model, BaseMixin, ByMixin):
    """
    Таблица групп магазинов
    """

    __tablename__ = 'storegroups'
    name        = db.Column(db.Unicode(), nullable=False, unique=True)
    description = db.Column(db.Unicode(1000))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Store group id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self


class StorePicture(db.Model, BaseMixin, ByMixin):
    """
    Таблица изображений магазинов
    """
    __tablename__ = 'store_pictures'
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # id магазина
    url      = db.Column(db.UnicodeText) # Адрес фото


class StoreState(db.Model, BaseMixin):
    """
    Таблица состояний магазина
    """

    __tablename__ = 'store_states'
    description = db.Column(db.Unicode(1000))  # Описание состояния транзакции
