#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .db import db
from base import BaseMixin


class Corporation(db.Model, BaseMixin):
    __tablename__ = 'corporations'

    name        = db.Column(db.String(255), nullable=False) # Название ЮЛ, пример "ОАО Ромашка"
    description = db.Column(db.String(1000)) # Описание ЮЛ
    president   = db.Column(db.String(255))  # Директор
    INN         = db.Column(db.String(255))  # ИНН
    KPP         = db.Column(db.String(255))  # КПП
    bank        = db.Column(db.String(255))  # Банк
    account     = db.Column(db.String(255))  # Расчетный счет
    subdomain   = db.Column(db.String(255))  # Поддомен, если задан то личный кабинет парнера доступен по адресу <subdomain>.myconomy.ru

    user_id        = db.Column(db.Integer, db.ForeignKey('users.id')) # id пользователя, кто добавил сеть
    stores      = db.relationship('Store',
        backref=db.backref('corporation', lazy='dynamic'))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Corporation id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self


class Store(db.Model, BaseMixin):
    __tablename__ = 'stores'

    name           = db.Column(db.String(255), nullable=False) # Название, пример "Перекресток"
    description    = db.Column(db.String(1000)) # Описание магазина
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporations.id')) # id сети
    city           = db.Column(db.String(255), nullable=False) # Город, пример "Москва", выбирается из списка известных городов
    region         = db.Column(db.String(255)) # Район города, пример "ЦАО", , выбирается из списка известных районов/округов
    metro          = db.Column(db.String(255)) # Ближайшее метро, пример "Арбатская", выбирается из списка известных станций метро
    address        = db.Column(db.String(1000)) # Адрес, пример "ул. Бутырская, д. 20", выбирается из списка известных адресов, типа ФИАС http://fias.nalog.ru/Public/DownloadPage.aspx
    phone          = db.Column(db.String(255)) # Телефон, пример "+7(495)123-34-45"
    lat            = db.Column(db.Float()) # широта
    lng            = db.Column(db.Float()) # долгота
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id')) # id пользователя, кто добавил магазин
    subdomain   = db.Column(db.String(255))  # Поддомен, если задан то личный кабинет парнера доступен по адресу <subdomain>.myconomy.ru

    delivery       = db.Column(db.Boolean, default=False) # True - есть доставка, False - нет доставки (по умолчанию)
    onlineonly     = db.Column(db.Boolean, default=False) # True - только онлайн, False - обычный розничный магаз (по умолчанию)

    # список всех предложения этого магазина
    offers         = db.relationship('Offer',
        backref=db.backref('store', lazy='dynamic'))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Store id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self


class StorePicture(db.Model, BaseMixin):
    __tablename__ = 'store_pictures'

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # id магазина
    url      = db.Column(db.UnicodeText) # Адрес фото
