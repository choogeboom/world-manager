from utils.sql import ScopedSession
from world_manager.model.stat import SchoolOfMagic


def test_resource(db):
    school_name = 'Evocation'
    with ScopedSession() as session:
        school = SchoolOfMagic(name=school_name)
        session.add(school)
        session.commit()
        print(school)

    with ScopedSession() as session:
        school = session.query(SchoolOfMagic).filter_by(name=school_name).one()