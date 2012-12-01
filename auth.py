#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .db import db
from base import BaseMixin


class AuthUser(db.Model, BaseMixin):
    """
    """
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # id пользователя
    social_id = db.Column(db.Unicode(length=256), unique=True, nullable=True)


class VkontakteAuthUser(AuthUser):
    """
    """
    __tablename__ = 'vk_auth_user'


class FacebookAuthUser(AuthUser):
    """
    """
    __tablename__ = 'facebook_auth_user'

    first_name = db.Column(db.String(255))
    last_name  = db.Column(db.String(255))
    email      = db.Column(db.String(255), nullable=False, unique=True)
    token      = db.Column(db.UnicodeText(), nullable=False)


class OdnoklassnikiAuthUser(AuthUser):
    """
    """
    __tablename__ = 'odnkl_auth_user'


class MailRuAuthUser(AuthUser):
    """
    """
    __tablename__ = 'mailru_auth_user'


class TwitterAuthUser(AuthUser):
    """
    """
    __tablename__ = 'twitter_auth_user'

    screen_name = db.Column(db.String(255))
    oauth_token = db.Column(db.UnicodeText(), nullable=False)
    oauth_token_secret = db.Column(db.UnicodeText(), nullable=False)
