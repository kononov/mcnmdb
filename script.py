#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import *
from flask.ext.script import Command, prompt_bool
from fixtures import data, user, f_store, f_offer
from flask.ext.security.utils import encrypt_password
import datetime

class CreateAllCommand(Command):
    """
    Creates database tables
    """

    def __init__(self, db):
        self.db = db

    def run(self, **kwargs):
        self.db.create_all()


class DropAllCommand(Command):
    """
    Drops all database tables
    """

    def __init__(self, db):
        self.db = db

    def run(self, **kwargs):
        if prompt_bool("Are you sure ? You will lose all your data !"):
            self.db.drop_all()


class CreateFixturesCommand(Command):
    """
    Создание тестовых данных
    """

    def __init__(self, db):
        self.db = db

    def run(self, **kwargs):

        self.db.drop_all()
        self.db.create_all()

        # Заполняем справочник пользовательских опций
        useroptions=[]
        for opt in data.user_options:
            useroptions.append(UserOption(id=opt[0],description=opt[1]))
            print 'UserOption "%s" created successfully.' % opt[1]
        save_models(useroptions)

        # Заполняем справочник опций для списков
        listoptions=[]
        for opt in data.list_options:
            listoptions.append(ListOption(id=opt[0],description=opt[1]))
            print 'Option "%s" created successfully.' % opt[1]
        save_models(listoptions)

        # Создаем роли
        roles = []
        for role in data.user_roles:
            roles.append(Role(name=role))
            print 'Role "%s" created successfully.' % role
        save_models(roles)

        # Заполняем справочник типов транзакций
        trn_types = []
        for trn_type in data.transactions_types:
            trn_types.append(TransactionType(id=trn_type[0], description=trn_type[1]))
            print 'Type for transaction "%s" created successfully.' % trn_type[1]
        save_models(trn_types)

        # Заполняем справочник состояний счетов
        accountstates = []
        for account_state in data.account_states:
            accountstates.append(AccountState(id=account_state[0], description=account_state[1]))
            print 'State for account "%s" created successfully.' % account_state[1]
        save_models(accountstates)

        # Заполняем справочник состояний транзакций
        transactionstates = []
        for trn_state in data.transaction_states:
            transactionstates.append(TransactionState(id=trn_state[0], description=trn_state[1]))
            print 'State for transaction "%s" created successfully.' % trn_state[1]
        save_models(transactionstates)

        # Заполняем справочник состояний предложений
        offerstates = []
        for offer_state in data.offer_states:
            offerstates.append(OfferState(id=offer_state[0], description=offer_state[1]))
            print 'State for offer "%s" created successfully.' % offer_state[1]
        save_models(offerstates)

        # Заполняем справочник состояний магазинов
        storestates = []
        for store_state in data.store_states:
            storestates.append(StoreState(id=store_state[0], description=store_state[1]))
            print 'State for store "%s" created successfully.' % store_state[1]
        save_models(storestates)

        # Заполняем справочник состояний заданий
        taskstates = []
        for task_state in data.task_states:
            taskstates.append(TaskState(id=task_state[0], description=task_state[1]))
            print 'State for task "%s" created successfully.' % task_state[1]
        save_models(taskstates)

        # Заполняем справочник состояний элементов заданий
        taskitemstates = []
        for taskitem_state in data.taskitem_states:
            taskitemstates.append(TaskItemState(id=taskitem_state[0], description=taskitem_state[1]))
            print 'State for taskitem "%s" created successfully.' % taskitem_state[1]
        save_models(taskitemstates)

        # Заполняем справочник типов заданий
        tasktypes = []
        for task_type in data.task_types:
            tasktypes.append(TaskType(id=task_type[0], description=task_type[1]))
            print 'Type for task "%s" created successfully.' % task_type[1]
        save_models(tasktypes)

        # Заполняем справочник типов единиц товаров
        f_measures = []
        for measure in data.measures:
            f_measures.append(Measure(id=measure[0], description=measure[1]))
            print 'Measure "%s" created successfully.' % measure[1]
        save_models(f_measures)

        # Создаем пользователей
        f_user = []
        for u in user.users:
            roles = []
            for role in u[2]:
                role = Role.query.filter_by(name=role).first()
                roles.append(role)
            f_user.append(User(email=u[0], password=encrypt_password(u[1]), roles=roles, active=u[3], confirmed_at=datetime.datetime.utcnow()))
            print 'User "%s" created successfully.' % u[0]
        save_models(f_user)


        # Создаем юр. лица
        f_corporations = []
        for corp in f_store.corporations:
            f_corporations.append(Corporation(name=corp[0],description=corp[1]))
            print 'Corporation "%s" created successfully.' % corp[0]
        save_models(f_corporations)

        # Создаем магазины
        f_stores = []
        for store in f_store.stores:
            f_stores.append(Store(name=store[0], open_time=store[1], close_time=store[2], metro=store[3], phone=store[4], city=store[5], address=store[6], corporation_id=1))
            print 'Store "%s" created successfully.' % store[0]
        save_models(f_stores)

        # Создаем предложения
        f_offers = []
        for offer in f_offer.offers:
            f_offers.append(Offer(name=offer[0], description=offer[1], type=offer[2], price=offer[3], measure_id=offer[4], store_id=1, datefinish=datetime.date(2012, 12, 31)))
            print 'Offer "%s" created successfully.' % offer[0]
        save_models(f_offers)