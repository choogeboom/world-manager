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


creature_class_spell_map = db.Table(
    'creature_class_spell_map',
    db.Column('spell_id', db.Integer, db.ForeignKey('spell.id')),
    db.Column('creature_class_id', db.Integer,
              db.ForeignKey('creature_class.id')),
    db.PrimaryKeyConstraint('spell_id', 'creature_class_id')
)

damage_type_spell_map = db.Table(
    'damage_type_spell_map',
    db.Column('damage_type_id', db.Integer, db.ForeignKey('damage_type.id')),
    db.Column('spell_id', db.Integer, db.ForeignKey('spell.id')),
    db.PrimaryKeyConstraint('damage_type_id', 'spell_id')
)


damage_type_active_ability_map = db.Table(
    'damage_type_active_ability_map',
    db.Column('damage_type_id', db.Integer, db.ForeignKey('damage_type.id')),
    db.Column('active_ability_id', db.Integer,
              db.ForeignKey('active_ability.id')),
    db.PrimaryKeyConstraint('damage_type_id', 'active_ability_id')
)


class DieType(enum.Enum):
    d4 = 4
    d6 = 6
    d8 = 8
    d10 = 10
    d12 = 12
    d20 = 20
    d100 = 100


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


class DamageType(ResourceMixin, db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(32),
                     nullable=False,
                     unique=True,
                     index=True)


class CoinType(ResourceMixin, db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(32),
                     nullable=False,
                     unique=True,
                     index=True)
    abbreviation = db.Column(db.String(8),
                             nullable=False,
                             unique=True,
                             index=True)
    value = db.Column(db.Integer,
                      nullable=False,
                      index=True)


class ActiveAbility(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String(256), unique=True, index=True,
                            nullable=False)
    name = db.Column(db.String(256))
    description = db.Column(db.String(8196))
    number_of_uses = db.Column(db.Integer)
    replenishes_on_short_rest = db.Column(db.Boolean)
    replenishes_on_long_rest = db.Column(db.Boolean)
    action_type = db.Column(
        db.Enum('Action', 'Bonus Action', 'Reaction', 'Free', 'Other'))
    damage_types = db.relationship('DamageType',
                                   secondary='damage_type_active_ability_map',
                                   backref=db.backref('active_abilities',
                                                      lazy='dynamic'))


class PassiveAbility(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_name = db.Column(db.String(256),
                            unique=True,
                            index=True,
                            nullable=False)
    description = db.Column(db.String(8196))


class Spell(ResourceMixin, db.Model):

    id = db.Column(db.Integer,
                   primary_key=True)
    unique_name = db.Column(db.String(256),
                            nullable=False,
                            unique=True,
                            index=True)
    name = db.Column(db.String(256),
                     nullable=False,
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
    classes = db.relationship('CreatureClass',
                              secondary=creature_class_spell_map,
                              backref=db.backref('spells', lazy='dynamic'))
    damage_types = db.relationship('DamageType',
                                   secondary=damage_type_spell_map,
                                   backref=db.backref('spells', lazy='dynamic'))


class SpellComponent(db.Model):
    __table_args__ = (db.UniqueConstraint('type', 'spell_id'),)

    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column('type', db.Enum('V', 'S', 'M', native_enum=False),
                      nullable=False,
                      index=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.id'),
                         nullable=False,
                         index=True)
    spell = db.relationship('Spell', back_populates='components')


class CreatureClass(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)


background_passive_ability_map = db.Table(
    'background_passive_ability_map',
    db.Column('passive_ability_id', db.Integer,
              db.ForeignKey('passive_ability.id')),
    db.Column('background_id', db.Integer,
              db.ForeignKey('background.id')),
    db.PrimaryKeyConstraint('passive_ability_id', 'background_id')
)


class Background(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String)
    passive_abilities = db.relationship(
        'PassiveAbility',
        secondary=background_passive_ability_map)


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


class StatBlockClass(ResourceMixin, db.Model):
    __table_args__ = (
        db.UniqueConstraint('stat_block_id', 'creature_class_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    stat_block_id = db.Column(db.Integer, db.ForeignKey('stat_block.id'))
    creature_class_id = db.Column(db.Integer,
                                  db.ForeignKey('creature_class.id'))
    level = db.Column(db.Integer, nullable=False, index=True)
    hit_die = db.Column(db.Enum(DieType))
    creature_class = db.relationship('CreatureClass')
    stat_block = db.relationship('StatBlock', back_populates='classes')


class Ability(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),
                     nullable=False,
                     unique=True,
                     index=True)
    abbreviation = db.Column(db.String(8),
                             nullable=False,
                             unique=True,
                             index=True)


class AbilityScore(ResourceMixin, db.Model):
    __table_args__ = (
        db.UniqueConstraint('ability_id', 'stat_block_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    ability_id = db.Column(db.Integer,
                           db.ForeignKey('ability.id'),
                           nullable=False)
    ability = db.relationship('Ability')
    stat_block_id = db.Column(db.Integer,
                              db.ForeignKey('stat_block.id'),
                              nullable=False)
    stat_block = db.relationship('StatBlock', back_populates='abilities')
    base_value = db.Column(db.Integer, default=10)


class SavingThrowProficiency(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ability_score_id = db.Column(db.Integer,
                                 db.ForeignKey('ability_score.id'),
                                 unique=True)
    ability_score = db.relationship('AbilityScore')
    proficiency_multiplier = db.Column(db.Integer, default=0,
                                       nullable=False)


class Skill(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),
                     nullable=False,
                     unique=True)
    default_ability_id = db.Column(db.Integer,
                                   db.ForeignKey('ability.id'),
                                   nullable=False)


class SkillProficiency(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skill = db.relationship('Skill')
    stat_block_id = db.Column(db.Integer, db.ForeignKey('stat_block.id'))
    proficiency_multiplier = db.Column(db.Integer, default=0, nullable=False)


class StatBlock(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, index=True)
    agency_type = db.Column(db.Enum('PC', 'NPC', native_enum=False))
    classes = db.relationship('StatBlockClass')
    background_id = db.Column(db.Integer, db.ForeignKey('background.id'),
                              nullable=True, index=True)
    background = db.relationship('Background')
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'),
                        nullable=False, index=True)
    race = db.relationship('Race')
    alignment = db.Column(db.Enum(Alignment, native_enum=False), index=True)
    experience_points = db.Column(db.Integer, index=True, default=0)

    proficiency_bonus = db.Column(db.Integer)

    ability_scores = db.relationship('AbilityScore',
                                     back_populates='stat_block')

    base_hit_point_max = db.Column(db.Integer)

    walking_speed = db.Column(db.Integer)
    swimming_speed = db.Column(db.Integer)
    climbing_speed = db.Column(db.Integer)
    flying_speed = db.Column(db.Integer)

    personality_traits = db.Column(db.String)
    ideals = db.Column(db.String)
    bonds = db.Column(db.String)
    flaws = db.Column(db.String)
