#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .db import db
from . import *
from flask.ext.script import Command, prompt_bool

from fixtures.data import ( user_roles, user_options, list_options, transactions_types,
                            account_states, transaction_states, measures, offer_states,
                            store_states, task_states, taskitem_states, task_types )


class CreateAllDb(Command):
    """
    Creates database tables
    """

    def run(self, **kwargs):
        db.create_all()


class DropAllDb(Command):
    """
    Drops all database tables
    """

    def run(self, **kwargs):
        if prompt_bool("Are you sure ? You will lose all your data !"):
            db.drop_all()

class CreateFixtures(Command):
    """
    Создание тестовых данных
    """

    def run(self, **kwargs):

        # Заполняем справочник пользовательских опций
        useroptions=[]
        for opt in user_options:
            useroptions.append(UserOption(id=opt[0],description=opt[1]))
            print 'UserOption "%s" created successfully.' % opt[1]
        save_models(useroptions)

        # Заполняем справочник опций для списков
        listoptions=[]
        for opt in list_options:
            listoptions.append(ListOption(id=opt[0],description=opt[1]))
            print 'Option "%s" created successfully.' % opt[1]
        save_models(listoptions)

        # Создаем роли
        roles = []
        for role in user_roles:
            roles.append(Role(name=role[0]))
            print 'Role "%s" created successfully.' % role[0]
        save_models(roles)
       