import enum

from utils.sql import ResourceMixin
from world_manager.extensions import db
from world_manager.model import account


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


class Item(ResourceMixin, db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(128),
                     nullable=False,
                     unique=True,
                     index=True)
    description = db.Column(db.String)
    weight = db.Column(db.Float(),
                       default=0)
    value = db.Column(db.Integer,
                      index=True)


class CoinType(ResourceMixin, db.Model):
    id = db.Column(db.Integer,
                   db.ForeignKey('item.id'),
                   primary_key=True)
    item = db.relationship('Item')
    abbreviation = db.Column(db.String(8),
                             nullable=False,
                             unique=True,
                             index=True)


class ArmorCategories(enum.Enum):
    Unarmored = 1
    LightArmor = 2
    MediumArmor = 3
    HeavyArmor = 4


class Armor(ResourceMixin, db.Model):
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    item = db.relationship('Item')
    category = db.Column(db.Enum(ArmorCategories, native_enum=False),
                         nullable=False)
    base_armor_class = db.Column(db.Integer, nullable=False, index=True)
    strength_requirement = db.Column(db.Integer, nullable=False, index=True,
                                     default=0)
    stealth_effect = db.Column(db.String, index=True)


class Shield(ResourceMixin, db.Model):
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    item = db.relationship('Item')


class WeaponCategory(enum.Enum):
    Simple = 1
    Martial = 2


class WeaponClass(enum.Enum):
    Melee = 1
    Ranged = 2


weapon_weapon_property_map = db.Table(
    'weapon_weapon_property_map',
    db.Column('weapon_id', db.ForeignKey('weapon.id')),
    db.Column('weapon_property_id', db.ForeignKey('weapon_property.id')),
    db.PrimaryKeyConstraint('weapon_id', 'weapon_property_id'))


class Weapon(ResourceMixin, db.Model):
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    item = db.relationship('Item')
    category = db.Column(db.Enum(WeaponCategory, native_enum=False),
                         nullable=False)
    classification = db.Column(db.Enum(WeaponClass, native_enum=False))
    properties = db.relationship('WeaponProperty',
                                 secondary=weapon_weapon_property_map)


class WeaponProperty(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16),
                     nullable=False,
                     unique=True,
                     index=True)
    description = db.Column(db.String())


class ActionType(enum.Enum):
    Action = 1
    BonusAction = 2
    Reaction = 3
    LegendaryAction = 4
    LairAction = 5


class Attack(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),
                     nullable=False,
                     unique=True,
                     index=True)
    display_name = db.Column(db.String(64),
                             nullable=False)
    required_number_of_hands = db.Column(db.Integer, nullable=False)
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'))
    ability = db.relationship('Ability')
    melee_range = db.Column(db.Integer)
    short_range = db.Column(db.Integer)
    long_range = db.Column(db.Integer)
    uses_proficiency = db.Column(db.Boolean(), default=True)


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
    current_hit_dice = db.Column(db.Integer,
                                 nullable=False,
                                 default=0)


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
    stat_block = db.relationship('StatBlock', back_populates='ability_scores')
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


class SpeedType(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16),
                     unique=True,
                     nullable=False,
                     index=True)


class SpeedScore(ResourceMixin, db.Model):
    __table_args__ = (
        db.UniqueConstraint('speed_type_id', 'stat_block_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    speed_type_id = db.Column(db.Integer, db.ForeignKey('speed_type.id'),
                              nullable=False)
    speed_type = db.relationship('SpeedType')
    stat_block_id = db.Column(db.Integer, db.ForeignKey('stat_block.id'),
                              nullable=False)
    stat_block = db.relationship('StatBlock', back_populates='speed_scores')
    base_value = db.Column(db.Integer, default=0, nullable=False, index=True)


class StatBlock(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=True)
    user = db.relationship(account.User)
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
    current_hit_points = db.Column(db.Integer)
    temporary_hit_points = db.Column(db.Integer)

    speed_scores = db.relationship('SpeedScore', back_populates='stat_block')

    personality_traits = db.Column(db.String)
    ideals = db.Column(db.String)
    bonds = db.Column(db.String)
    flaws = db.Column(db.String)


stat_block_condition_map = db.Table(
    'stat_block_condition_map',
    db.Column('condition_id',
              db.Integer,
              db.ForeignKey('condition.id')),
    db.Column('stat_block_id',
              db.Integer,
              db.ForeignKey('stat_block.id')),
    db.PrimaryKeyConstraint('condition_id', 'stat_block_id')
)


class Condition(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),
                     nullable=False,
                     unique=True,
                     index=True)
    description = db.Column(db.String)


class FeatureCategory(enum.Enum):
    RacialTrait = 1
    ClassFeature = 2
    Feat = 3
    BackgroundFeature = 4
    ItemFeature = 5


class Rest(enum.Enum):
    ShortRest = 1
    LongRest = 2


class Feature(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),
                     nullable=False,
                     unique=True,
                     index=True)
    description = db.Column(db.String(),
                            nullable=False,
                            )
    category = db.Column(db.Enum(FeatureCategory, native_enum=False),
                         nullable=False,
                         index=True)
    maximum_uses = db.Column(db.Integer)
    current_uses = db.Column(db.Integer)
    replenishes_on = db.Column(db.Enum(Rest, native_enum=False))


class Language(ResourceMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    script = db.Column(db.String(32))