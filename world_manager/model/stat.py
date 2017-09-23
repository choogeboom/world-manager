import enum

from utils.sql import ResourceMixin
from world_manager.extensions import db


class SchoolOfMagic(ResourceMixin, db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(64),
                     nullable=False,
                     unique=True,
                     index=True)
    spells = db.relationship('Spell', back_populates='school')


class Spell(ResourceMixin, db.Model):

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(256),
                     nullable=False,
                     unique=True,
                     index=True)
    ritual = db.Column(db.Boolean,
                       nullable=False,
                       index=True)
    level = db.Column(db.Integer,
                      nullable=False,
                      index=True)
    school_id = db.Column(db.Integer,
                          db.ForeignKey('school_of_magic.id'),
                          nullable=False,
                          index=True)
    school = db.relationship('SchoolOfMagic', back_populates='spells')

    casting_time = db.Column(db.Integer,
                             nullable=False,
                             index=True)
    range = db.Column(db.String(64),
                      nullable=False,
                      index=True)
    components = db.Column(db.String(8),
                           nullable=False,
                           index=True)


