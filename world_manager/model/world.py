from utils.sql import ResourceMixin, AwareDateTime
from world_manager.extensions import db


class Event(ResourceMixin, db.Model):

    id = db.Column(db.BigInteger,
                   primary_key=True)

    name = db.Column(db.String(255),
                     nullable=False,
                     unique=True,
                     index=True)

    description = db.Column(db.String(4096))

    parent_event_id = db.Column(db.BigInteger,
                                db.ForeignKey('event.id'),
                                index=True)

    children = db.relationship('Event',
                               backref=db.backref('parent', remote_side=[id]))

    start_date = db.Column(AwareDateTime(),
                           index=True)

    end_date = db.Column(AwareDateTime(),
                         index=True)




