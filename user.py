#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from werkzeug import cached_property

from .db import db
#from mcnmadmin.uploads import uploaded_avatars

from .settings import UserSettings
from .shoplist import ShoppingList
from .offer import Offer
from .store import Store

from base import BaseMixin

from flask.ext.security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

groups_users = db.Table('groups_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))

roles_groups = db.Table('roles_groups',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))

class Role(db.Model, RoleMixin, BaseMixin):
    __tablename__ = 'roles'

    name        = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(1000))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Role id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

class Group(db.Model, BaseMixin):
    __tablename__ = 'groups'

    name        = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(1000))

    roles       = db.relationship('Group', secondary=roles_groups, backref = db.backref('groups_with_this_role'))

    def __str__(self):
        ctx = (str(self.id), self.name)
        return '<Group id=%s, name=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self


class User(db.Model, UserMixin, BaseMixin):
    __tablename__ = 'users'

    username         = db.Column(db.String(255))
    first_name       = db.Column(db.String(255))
    last_name        = db.Column(db.String(255))
    email            = db.Column(db.String(255), nullable=False, unique=True)
    phone            = db.Column(db.String(255))
    password         = db.Column(db.String(255), nullable=False)

    active           = db.Column(db.Boolean, default=False, nullable=False)
    gender           = db.Column(db.Integer(), default=2)
    language         = db.Column(db.String(2), default='ru') #choices=('en','ru','de','es')
    website          = db.Column(db.String(255), default='http://simpla.com')
    birthdate        = db.Column(db.DateTime())
    about_me         = db.Column(db.String(1000))
    avatar           = db.Column(db.String(1000)) # ссылка на фотку пользователя

    country          = db.Column(db.String(255))
    city             = db.Column(db.String(255))

    # настройки пользователя
    settings         = db.relationship('UserSettings', backref=db.backref('user'))

    # список всех ролей данного пользователя
    roles            = db.relationship('Role', secondary=roles_users, backref = db.backref('users_with_this_role', lazy='dynamic'))
    # список всех групп куда входит этот пользователь ролей
    groups           = db.relationship('Group', secondary=groups_users, backref = db.backref('users_in_this_group'))
    # список всех списков покупок у этого пользователя
    lists            = db.relationship('ShoppingList', backref=db.backref('user'))
    # список всех предложения, созданых пользователем
    offers           = db.relationship('Offer', backref=db.backref('who_add'))
    # список всех магазинов, созданых пользователем
    stores           = db.relationship('Store', backref=db.backref('who_add'))
    # список всех corporation, созданых пользователем
    corporations     = db.relationship('Corporation', backref=db.backref('who_add'))

    confirmed_at     = db.Column(db.DateTime())
    last_login_at    = db.Column(db.DateTime)
    last_login_ip    = db.Column(db.String(255))
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(255))
    login_count      = db.Column(db.Integer)

    def get_id(self):
        return str(self.id)

    @property
    def age(self):
        if not self.birth_date: return False
        else:
            today = datetime.date.today()
            # Raised when birth date is February 29 and the current year is not a
            # leap year.
            try:
                birthday = self.birth_date.replace(year=today.year)
            except ValueError:
                day = today.day - 1 if today.day != 1 else today.day + 2
                birthday = self.birth_date.replace(year=today.year, day=day)
            if birthday > today: return today.year - self.birth_date.year - 1
            else: return today.year - self.birth_date.year

    @cached_property
    def avatar_url(self):
        #return uploaded_avatars.url(self.avatar)
        return

    @cached_property
    def natural_roles(self):
        natural_roles = []
        for role in self.roles:
            natural_roles.append(Role.query.get(role.id).name)
        return natural_roles

    def __str__(self):
        ctx = (str(self.id), self.email)
        return '<User id=%s, email=%s>' % ctx

    def __repr__(self):
        return "<%s>" % self

class UserFavouriteStore(db.Model, BaseMixin):
    __tablename__ = 'favourite_stores'
    user_id  = db.Column(db.Integer(), db.ForeignKey('users.id'))  # id пользователя, кто добавил предложение
    store_id = db.Column(db.Integer(), db.ForeignKey('stores.id')) # id магазина

