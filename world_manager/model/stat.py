
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


class_spell_map = db.Table(
    'class_spell_map',
    db.Column('spell_id', db.Integer, db.ForeignKey('spell.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

damage_type_spell_map = db.Table(
    'damage_type_spell_map',
    db.Column('damage_type_id', db.Integer, db.ForeignKey('damage_type.id')),
    db.Column('spell_id', db.Integer, db.ForeignKey('spell.id')))


class DamageType(ResourceMixin, db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(32),
                     nullable=False,
                     unique=True,
                     index=True)


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
    components = db.relationship('SpellComponent', back_populates='spell')
    material_components = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.String(), nullable=True)
    higher_levels = db.Column(db.String())
    classes = db.relationship('Class', secondary=class_spell_map,
                              backref=db.backref('spells', lazy='dynamic'))
    damage_types = db.relationship('DamageType',
                                   secondary=damage_type_spell_map,
                                   backref=db.backref('spells', lazy='dynamic'))


class SpellComponent(db.Model):
    __table_args__ = (db.UniqueConstraint('type', 'spell_id'))

    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column('type', db.Enum(['V', 'S', 'M'], native_enum=False),
                      nullable=False,
                      index=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id'),
                         nullable=False,
                         index=True)
    spell = db.relationship('Spell', back_populates='components')


class Class(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)


class StatBlockClass(ResourceMixin, db.Model):
    __table_args__ = (db.UniqueConstraint('stat_block_id', 'class_id'))

    id = db.Column(db.Integer, primary_key=True)
    stat_block_id = db.Column(db.Integer, db.ForeignKey('stat_block.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    level = db.Column(db.Integer, nullable=False, index=True)
    class_ = db.relationship('Class')


class StatBlock(ResourceMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    classes = db.relationship('StatBlockClass')
