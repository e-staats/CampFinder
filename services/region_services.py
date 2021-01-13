from data.region import Region  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
from infrastructure.load_data_from_csv import load_data_from_csv  # pylint: disable = import-error
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
    filepath = os.path.join('.','park_data','wi_regions.csv')
    region_list = load_data_from_csv(filepath)

    session = db_session.create_session()
    for region_item in region_list:
        r = Region()
        r.name = region_item[0]
        r.id = region_item[1]
        r.external_id = region_item[2]
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

def create_external_region_dict():
    return_dict = {}
    session = db_session.create_session()
    regions = session.query(Region).all()
    for region in regions:
        return_dict[region.external_id] = region.name
    return return_dict

def create_internal_region_dict():
    return_dict = {}
    session = db_session.create_session()
    regions = session.query(Region).all()
    for region in regions:
        return_dict[region.id] = region.name
    return return_dict
