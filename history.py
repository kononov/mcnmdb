#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin, ByMixin

TYPE_SOURCE_UNKNOWN    = 0
TYPE_SOURCE_WEB        = 1
TYPE_SOURCE_ANY_CLIENT = 2
TYPE_SOURCE_IOS        = 3
TYPE_SOURCE_ANDROID    = 4


class SearchHistory(db.Model, BaseMixin, ByMixin):
    """
    Таблица истории поиска пользователя
    """

    __tablename__ = 'search_history'

    query   = db.Column(db.Unicode(), nullable=False)  # строка поиска
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type    = db.Column(db.Integer) # источник поиска


class GeoHistory(db.Model, BaseMixin, ByMixin):
    """
    Таблица истории координат пользователей
    """

    __tablename__ = 'geo_history'

    lat     = db.Column(db.Float()) # координата: широта
    lng     = db.Column(db.Float()) # координата: долгота
    type    = db.Column(db.Integer) # источник поиска
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

