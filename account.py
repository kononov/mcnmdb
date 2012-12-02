#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin, ByMixin


TRANSACTION_TYPE_UNKNOWN = 0
TRANSACTION_TYPE_DEBIT   = 1 # увеличение средств
TRANSACTION_TYPE_CREDIT  = 2 # уменьшение средств


ACCOUNT_STATE_UNKNOWN = 0
ACCOUNT_STATE_ACTIVE  = 1
ACCOUNT_STATE_BLOCKED = 2
ACCOUNT_STATE_ClOSED  = 3


TRANSACTION_STATE_UNKNOWN = 0
TRANSACTION_STATE_OK      = 1
TRANSACTION_STATE_DELETE  = 2
TRANSACTION_STATE_STORN   = 11


class Account(db.Model, BaseMixin, ByMixin):
    """
    Таблица счетов для учета средств магазинов
    """

    __tablename__ = 'accounts'
    corporation_id = db.Column(db.Integer, db.ForeignKey('corporations.id')) # id сети
    rest = db.Column(db.Numeric(10,2)) # текущий остаток по счету
    state_id = db.Column(db.Integer, db.ForeignKey('account_states.id'))  # id состояния счета

    __table_args__ = (
                       db.Index("idx_accounts_corporation_id", "corporation_id"),
                       db.Index("idx_accounts_state_id", "state_id"),
                     )


class Transaction(db.Model, BaseMixin, ByMixin):
    """
    Таблица траназакций по счетам
    """

    __tablename__ = 'transactions'
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    type = db.Column(db.Integer, db.ForeignKey('transaction_types.id')) # тип операции: приход, расход
    state_id = db.Column(db.Integer, db.ForeignKey('transaction_states.id'))  # id состояния операции
    summ = db.Column(db.Numeric(10,2)) # сумма операции
    rest = db.Column(db.Numeric(10,2)) # остаток после совершения операции
    comment = db.Column(db.UnicodeText())  # Комменты к транзакции

    __table_args__ = (
                       db.Index("idx_transactions_account_id", "account_id"),
                       db.Index("idx_transactions_state_id", "state_id"),
                     )


class TransactionType(db.Model, BaseMixin):
    """
    Таблица типов транзакций
    """

    __tablename__ = 'transaction_types'
    description = db.Column(db.Unicode(1000))


class AccountState(db.Model, BaseMixin):
    """
    Таблица состояний счета
    """

    __tablename__ = 'account_states'
    description = db.Column(db.Unicode(1000))  # Описание состояния счета


class TransactionState(db.Model, BaseMixin):
    """
    Таблица состояний транзакций
    """

    __tablename__ = 'transaction_states'
    description = db.Column(db.Unicode(1000))  # Описание состояния транзакции

