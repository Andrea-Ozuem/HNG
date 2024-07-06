#!/usr/bin/python3
"""This module defines the Models for the API"""

from passlib.apps import custom_app_context as pwd_context
from api import db

user_org = db.Table('users_organisations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True,
        nullable=False),
    db.Column('organisation_id', db.Integer, db.ForeignKey('organisations.id'), primary_key=True,
        nullable=False)
)

class User(db.Model):
    """This class defines a user by various attributes"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(32))
    user_orgs = db.relationship("Organisation", secondary=user_org, backref='User')

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

                
class Organisation(db.Model):
    """ Organistion class """
    __tablename__ = 'organisations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(128))