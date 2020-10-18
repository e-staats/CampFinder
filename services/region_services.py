from data.region import Region  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import os


def populate_regions():
    region_dict = get_region_dict()

    session = db_session.create_session()
    for name in region_dict.keys():
        r = Region()
        r.id = region_dict[name]
        r.name = name
        session.add(r)
    session.commit()
    return True


def get_region_dict():
    return {
        "Northwest WI": 1,
        "Southwest WI": 2,
        "Northeast WI": 3,
        "Southeast WI": 4,
    }
