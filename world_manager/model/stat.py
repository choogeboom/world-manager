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
    hit_die = db.Column(db.Enum(['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']))
    class_ = db.relationship('Class')


class Background(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String)


class Race(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String)
    creature_type_id = db.Column(db.Integer, db.ForeignKey('creature_type.id'))
    creature_type = db.relationship('CreatureType')


class CreatureType(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String)


class Alignment(enum.Enum):
    Neutral = 1
    ChaoticNeutral = 2
    ChaoticGood = 3
    NeutralGood = 4
    LawfulGood = 5
    LawfulNeutral = 6
    LawfulEvil = 7
    NeutralEvil = 8
    ChaoticEvil = 9


class StatBlock(ResourceMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, index=True)
    classes = db.relationship('StatBlockClass')
    background_id = db.Column(db.Integer, db.ForeignKey('background.id'),
                              nullable=True, index=True)
    background = db.relationship('Background')
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'),
                        nullable=False, index=True)
    race = db.relationship('Race')
    alignment = db.Column(db.Enum(Alignment), index=True)
    experience_points = db.Column(db.Integer, index=True, server_default=0)

    proficiency_bonus = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    base_hit_point_max = db.Column(db.Integer)

    walking_speed = db.Column(db.Integer)
    swimming_speed = db.Column(db.Integer)
    climbing_speed = db.Column(db.Integer)
    flying_speed = db.Column(db.Integer)

    strength_save_proficiency = db.Column(db.Boolean, server_default=False)
    athletics_proficiency = db.Column(db.Boolean, server_default=False)

    dexterity_save_proficiency = db.Column(db.Boolean, server_default=False)
    acrobatics_proficiency = db.Column(db.Boolean, server_default=False)
    sleight_of_hand_proficiency = db.Column(db.Boolean, server_default=False)
    stealth_proficiency = db.Column(db.Boolean, server_default=False)

    constitution_save_proficiency = db.Column(db.Boolean,  server_default=False)

    intelligence_save_proficiency = db.Column(db.Boolean, server_default=False)
    arcana_proficiency = db.Column(db.Boolean, server_default=False)
    history_proficiency = db.Column(db.Boolean, server_default=False)
    investigation_proficiency = db.Column(db.Boolean, server_default=False)
    nature_proficiency = db.Column(db.Boolean, server_default=False)
    religion_proficiency = db.Column(db.Boolean, server_default=False)

    wisdom_save_proficiency = db.Column(db.Boolean, server_default=False)
    animal_handling_proficiency = db.Column(db.Boolean, server_default=False)
    insight_proficiency = db.Column(db.Boolean, server_default=False)
    medicine_proficiency = db.Column(db.Boolean, server_default=False)
    perception_proficiency = db.Column(db.Boolean, server_default=False)
    survival_proficiency = db.Column(db.Boolean, server_default=False)

    charisma_save_proficiency = db.Column(db.Boolean, server_default=False)
    deception_proficiency = db.Column(db.Boolean, server_default=False)
    intimidation_proficiency = db.Column(db.Boolean, server_default=False)
    performance_proficiency = db.Column(db.Boolean, server_default=False)
    persuasion_proficiency = db.Column(db.Boolean, server_default=False)

    personality_traits = db.Column(db.String)
    ideals = db.Column(db.String)
    bonds = db.Column(db.String)
    flaws = db.Column(db.String)
