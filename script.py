#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from random import randint

from . import *
from flask.ext.script import Command, prompt_bool
from fixtures import data, user, f_store, f_offer
from flask.ext.security.utils import encrypt_password


class CreateAllCommand(Command):
    """
    Creates database tables
    """

    def __init__(self, db):
        self.db = db

    def run(self, **kwargs):
        self.db.create_all(bind=[None])


class DropAllCommand(Command):
    """
    Drops all database tables
    """

    def __init__(self, db):
        self.db = db

    def run(self, **kwargs):
        if prompt_bool("Are you sure ? You will lose all your data !"):
            self.db.drop_all(bind=[None])


class CreateFixturesCommand(Command):
    """
    Создание тестовых данных
    """

    def __init__(self, db):
        self.db = db

    def run(self, **kwargs):

        self.db.drop_all(bind=[None])
        self.db.create_all(bind=[None])

        print '---------------------START-------------------------'

        # Заполняем справочник пользовательских опций
        useroptions=[]
        for opt in data.user_options:
            useroptions.append(UserOption(id=opt[0],description=opt[1]))
            print 'OK! - UserOption "%s" created successfully.' % opt[1]
        save_models(useroptions)
        print '---------------------------------------------------'

        # Заполняем справочник опций для списков
        listoptions=[]
        for opt in data.list_options:
            listoptions.append(ListOption(id=opt[0],description=opt[1]))
            print 'OK! - Option "%s" created successfully.' % opt[1]
        save_models(listoptions)
        print '---------------------------------------------------'

        # Создаем роли
        roles = []
        for role in data.user_roles:
            roles.append(Role(name=role))
            print 'OK! - Role "%s" created successfully.' % role
        save_models(roles)
        print '---------------------------------------------------'

        # Заполняем справочник типов транзакций
        trn_types = []
        for trn_type in data.transactions_types:
            trn_types.append(TransactionType(id=trn_type[0], description=trn_type[1]))
            print 'OK! - Type for transaction "%s" created successfully.' % trn_type[1]
        save_models(trn_types)
        print '---------------------------------------------------'

        # Заполняем справочник состояний счетов
        accountstates = []
        for account_state in data.account_states:
            accountstates.append(AccountState(id=account_state[0], description=account_state[1]))
            print 'OK! - State for account "%s" created successfully.' % account_state[1]
        save_models(accountstates)
        print '---------------------------------------------------'

        # Заполняем справочник состояний транзакций
        transactionstates = []
        for trn_state in data.transaction_states:
            transactionstates.append(TransactionState(id=trn_state[0], description=trn_state[1]))
            print 'OK! - State for transaction "%s" created successfully.' % trn_state[1]
        save_models(transactionstates)
        print '---------------------------------------------------'

        # Заполняем справочник состояний предложений
        offerstates = []
        for offer_state in data.offer_states:
            offerstates.append(OfferState(id=offer_state[0], description=offer_state[1]))
            print 'OK! - State for offer "%s" created successfully.' % offer_state[1]
        save_models(offerstates)
        print '---------------------------------------------------'

        # Заполняем справочник состояний магазинов
        storestates = []
        for store_state in data.store_states:
            storestates.append(StoreState(id=store_state[0], description=store_state[1]))
            print 'OK! - State for store "%s" created successfully.' % store_state[1]
        save_models(storestates)
        print '---------------------------------------------------'

        # Заполняем справочник состояний заданий
        taskstates = []
        for task_state in data.task_states:
            taskstates.append(TaskState(id=task_state[0], description=task_state[1]))
            print 'OK! - State for task "%s" created successfully.' % task_state[1]
        save_models(taskstates)
        print '---------------------------------------------------'

        # Заполняем справочник состояний элементов заданий
        taskitemstates = []
        for taskitem_state in data.taskitem_states:
            taskitemstates.append(TaskItemState(id=taskitem_state[0], description=taskitem_state[1]))
            print 'OK! - State for taskitem "%s" created successfully.' % taskitem_state[1]
        save_models(taskitemstates)
        print '---------------------------------------------------'

        # Заполняем справочник типов заданий
        tasktypes = []
        for task_type in data.task_types:
            tasktypes.append(TaskType(id=task_type[0], description=task_type[1]))
            print 'OK! - Type for task "%s" created successfully.' % task_type[1]
        save_models(tasktypes)
        print '---------------------------------------------------'

        # Заполняем справочник типов единиц товаров
        f_measures = []
        for measure in data.measures:
            f_measures.append(Measure(id=measure[0], description=measure[1]))
            print 'OK! - Measure "%s" created successfully.' % measure[1]
        save_models(f_measures)
        print '---------------------------------------------------'

        # Создаем юр. лица
        f_corporations = []
        for corp in f_store.corporations:
            f_corporations.append(Corporation(name=corp[0],description=corp[1]))
            print 'OK! - Corporation "%s" created successfully.' % corp[0]
        save_models(f_corporations)
        print '---------------------------------------------------'



        # Создаем пользователей
        f_user = []
        for u in user.users:
            roles = []
            for role in u[2]:
                role = Role.query.filter_by(name=role).first()
                roles.append(role)
            corporation = Corporation.query.filter_by(name=u[4]).first()
            if corporation:
                f_user.append(User(email=u[0], password=encrypt_password(u[1]), roles=roles, active=u[3], confirmed_at=datetime.datetime.utcnow(), corporation=corporation))
            else:
                f_user.append(User(email=u[0], password=encrypt_password(u[1]), roles=roles, active=u[3], confirmed_at=datetime.datetime.utcnow()))
            print 'OK! - User "%s" created successfully.' % u[0]
        save_models(f_user)
        print '---------------------------------------------------'

        # Создаем магазины и рандомно привязываем их к ЮЛ
        f_stores = []
        for store in f_store.stores:
            f_stores.append(Store(name=store[0], open_time=store[1], close_time=store[2], metro=store[3], phone=store[4], city=store[5], address=store[6], corporation_id=randint(1,len(f_corporations)) ))
            print 'OK! - Store "%s" created successfully.' % store[0]
        save_models(f_stores)
        print '---------------------------------------------------'


        # Создаем группы магазинов
        # Рандомно заполняем группы половину всех магазинов. Чтобы магазы не в группах тоже остались.
        f_storegroups = []
        for group in f_store.groups:
            corporation = Corporation.query.filter_by(name=group[2]).first()
            if corporation:
                if group[0]==u"Магазины в Москве":
                    x_stores = filter(lambda store: store.city==u"Москва" and store.corporation.name==group[2], f_stores[len(f_stores)/2:])
                    f_storegroups.append(StoreGroup(name=group[0],description=group[1], corporation_id=corporation.id, stores_in_this_group=x_stores))
                    print 'OK! - StoreGroup "%s" created successfully.' % group[0]
                elif group[0]==u"Магазины в Замкадье":
                    x_stores = filter(lambda store: store.city!=u"Москва" and store.corporation.name==group[2], f_stores[len(f_stores)/2:])
                    f_storegroups.append(StoreGroup(name=group[0],description=group[1], corporation_id=corporation.id, stores_in_this_group=x_stores))
                    print 'OK! - StoreGroup "%s" created successfully.' % group[0]
            else:
                print u'ERROR! - Проверить фикстуры для группы "%s". Невозможно определить ЮрЛицо по названию "%s"!' % (group[0], group[2])
        save_models(f_storegroups)
        print '---------------------------------------------------'


        # Рандомно добавляем покупателям избранные магазины, по 20 штук
        f_favstores = []
        for u in filter(lambda u: "customer" in u[2], user.users):
            for i in range(20):
                usr = User.query.filter_by(email=u[0]).first()
                f_favstores.append(UserFavouriteStore(user_id=usr.id, store_id=randint(1,len(f_stores))))
                print "OK! - Store successfully added to user's (%s) favorites." % u[0]
        save_models(f_favstores)
        print '---------------------------------------------------'


        # Создаем предложения
        f_offers = []
        for offer in f_offer.offers:
            f_offers.append(Offer(name=offer[0], description=offer[1], type=offer[2], price=offer[3], measure_id=offer[4], store_id=1, datefinish=datetime.date(2012, 12, 31)))
            print 'OK! - Offer "%s" created successfully.' % offer[0]
        save_models(f_offers)
        print '------------------FINISH------------------------'