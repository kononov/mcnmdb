#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from .db import db
from base import BaseMixin

TASK_TYPE_UNKNOWN    = 0
TASK_TYPE_OFFER_LOAD = 1
TASK_TYPE_STORE_LOAD = 2

TASK_STATE_UNKNOWN       = 0
TASK_STATE_INIT          = 1
TASK_STATE_START         = 2
TASK_STATE_EXEC          = 3
TASK_STATE_FINISH_ERR    = 4
TASK_STATE_FINISH_SUCCES = 5

TASK_ITEM_STATE_UNKNOWN  = 0
TASK_ITEM_STATE_OK       = 1
TASK_ITEM_STATE_ERROR    = 2


class TaskState(db.Model, BaseMixin):
    __tablename__ = 'task_states'
    description = db.Column(db.String(1000))  # Описание состояния задачи


class TaskItemState(db.Model, BaseMixin):
    __tablename__ = 'taskitem_states'
    description = db.Column(db.String(1000))  # Описание состояния элемента задачи


class TaskType(db.Model, BaseMixin):
    __tablename__ = 'task_types'
    description = db.Column(db.String(1000))  # Описание типа задачи


class TaskItem(db.Model, BaseMixin):
    __tablename__ = 'task_items'
    row_num = db.Column(db.Integer()) # номер строки в обрабатываемомм файле
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))  # id задачи
    state_id = db.Column(db.Integer, db.ForeignKey('taskitem_states.id'))  # id состояния задачи
    description = db.Column(db.UnicodeText())  # Описание элемента задачи
    error_info = db.Column(db.UnicodeText())  # Описание элемента задачи

class Task(db.Model, BaseMixin):
    __tablename__ = 'tasks'
    state_id = db.Column(db.Integer, db.ForeignKey('task_states.id'))  # id состояния задачи
    type_id = db.Column(db.Integer, db.ForeignKey('task_types.id'))  # id типа задачи
    description = db.Column(db.UnicodeText())  # Описание задачи
    finished_at = db.Column(db.DateTime)  # дата-время завершения обработки задачи
    file_path = db.Column(db.Unicode(length=1000))  # Путь где лежит файл
    file_name = db.Column(db.Unicode(length=256))  # Имя файла

    # список всех элементов в задаче
    items = db.relationship('TaskItem', backref=db.backref('task'))


