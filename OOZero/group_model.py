from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from OOZero.model import db
import OOZero.event_model as event
import OOZero.user_model as user
import hashlib
import secrets
import datetime

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    owner = db.relationship("User", foreign_keys=[owner_id], backref=db.backref("owned_groups", uselist=True), uselist=False)
    name = db.Column(db.String(60), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    picture = db.Column(db.LargeBinary, nullable=True)

class UserInGroup(db.Model):
    __tablename__ = 'user_in_group'
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), primary_key=True, unique=False)
    group = db.relationship("Group", foreign_keys=[group_id], backref=db.backref("members", uselist=True), uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, unique=False)
    user = db.relationship("User", foreign_keys=[user_id], backref=db.backref("groups", uselist=True), uselist=False)
    write = db.Column(db.Boolean, unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False)

class SharedEvent(db.Model):
    __tablename__ = "shared_event"
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), primary_key=True, unique=False)
    event = db.relationship("Event", foreign_keys=[event_id], backref=db.backref("shared_events", uselist=True), uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, unique=False)
    user = db.relationship("User", foreign_keys=[user_id], backref=db.backref("shared_events", uselist=True), uselist=False)
    write = db.Column(db.Boolean, unique=False, nullable=False)
