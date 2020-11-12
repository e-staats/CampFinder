from data.region import Region  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import os

def get_name_from_id(region_id):
    session = db_session.create_session()
    region = session.query(Region).filter(Region.id == region_id).first()
    session.close()
    if region == None:
        return False
    if isinstance(region.id,int):
        return region.name
    else:
        return False

def populate_regions():
    region_dict = get_region_dict()

    session = db_session.create_session()
    for name in region_dict.keys():
        r = Region()
        r.id = region_dict[name]
        r.name = name
        session.add(r)
    session.commit()
    session.close()
    return True

def regions_exist():
    session = db_session.create_session()
    region = session.query(Region).first()
    if region==None:
        session.close()
        return False
    session.close()
    return True

def get_region_dict():
    return {
        "Northwest WI": 1,
        "Southwest WI": 2,
        "Northeast WI": 3,
        "Southeast WI": 4,
    }
