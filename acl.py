#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .db import db
from base import BaseMixin
from sqlalchemy.util import classproperty
from sqlalchemy.orm.session import object_session


class ACLSubject(db.Model, BaseMixin):

    __tablename__ = 'acl_subjects'

    def may(self, verb, obj = None):
        session = object_session(self)
        verb = ACLVerb.get(session, verb)
        obj = ACLObject.get_object(obj)

        value = None

        for rule in session.query(ACLRule).filter_by(subj = self, verb = verb, obj = obj).all():
            if False == rule.value:
                return False
            elif True == rule.value:
                value = True
            else:
		        assert('not reached')

        return value

    def permit(self, verb, obj = None, value = True):
	    session = object_session(self)
	    verb = ACLVerb.get(session, verb)
	    obj = ACLObject.get_object(obj)

	    # check if rule exists, if yes, return
	    if session.query(ACLRule).filter_by(subj = self, verb = verb, obj = obj, value = value).first(): return

	    # create rule
	    r = ACLRule(subj = self, verb = verb, obj = obj, value = value)
	    session.add(r)

class ACLVerb(db.Model, BaseMixin):

    __tablename__ = 'acl_verbs'

    name = db.Column(db.String, unique = True)

    def __init__(self, name):
	    self.name = name

    @staticmethod
    def get_by_name(session, name):
        session.flush()
        verb = session.query(ACLVerb).filter_by(name = name).first()

    	if not verb:
    		verb = ACLVerb(name)
    		session.add(verb)
    		session.flush()
    	return verb

	@staticmethod
	def get(session, name_or_verb):
		if isinstance(name_or_verb, ACLVerb): return name_or_verb
		return ACLVerb.get_by_name(session, name_or_verb)

class ACLObject(db.Model, BaseMixin):

	__tablename__ = 'acl_objects'

	@staticmethod
	def get_object(acl_obj):
		if None == acl_obj: return None
		if isinstance(acl_obj, ACLObjectRef):
			acl_obj.init_acl()
			return acl_obj._acl_object
		return acl_obj

class ACLSubjectRef(object):
	@classproperty
	def _acl_subject_id(cls):
		return db.Column(db.Integer, db.ForeignKey(ACLSubject.id))

	@classproperty
	def _acl_subject(cls):
		return db.relationship(ACLSubject)

	def init_acl(self):
		if None == self._acl_subject:
			self._acl_subject = ACLSubject()

	def may(self, *args, **kwargs):
		self.init_acl()
		return self._acl_subject.may(*args, **kwargs)

	def permit(self, *args, **kwargs):
		self.init_acl()
		return self._acl_subject.permit(*args, **kwargs)

class ACLObjectRef(object):
	@classproperty
	def _acl_object_id(cls):
		return db.Column(db.Integer, db.ForeignKey(ACLObject.id))

	@classproperty
	def _acl_object(cls):
		return db.relationship(ACLObject)

	def init_acl(self):
		if None == self._acl_object:
			self._acl_object = ACLObject()

class ACLRule(db.Model, BaseMixin):
    __tablename__ = 'acl_rules'

    subj_id = db.Column(db.Integer, db.ForeignKey('acl_subjects.id'))
    verb_id = db.Column(db.Integer, db.ForeignKey('acl_verbs.id'))
    obj_id  = db.Column(db.Integer, db.ForeignKey('acl_objects.id'), nullable = True)

    subj    = db.relationship("ACLSubject")
    verb    = db.relationship("ACLVerb")
    obj     = db.relationship("ACLObject")

    value   = db.Column(db.Boolean)
