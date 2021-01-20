from data.park import Park  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
from infrastructure.load_data_from_csv import load_data_from_csv  # pylint: disable = import-error
import services.url_services as url_service
import os
import copy

def get_park_from_id(park_id):
    session = db_session.create_session()
    park = session.query(Park).filter(Park.id == park_id).first()
    session.close()
    if park == None:
        return False
    if isinstance(park.id,int):
        return park
    else:
        return False

def get_id_from_name(name):
    session = db_session.create_session()
    park = session.query(Park).filter(Park.name == name).first()
    if park == None:
        return_val = None
    else:
        return_val = copy.deepcopy(park.id)
    session.close()
    return return_val

def get_name_from_id(park_id):
    session = db_session.create_session()
    park = session.query(Park).filter(Park.id == park_id).first()
    session.close()
    if park == None:
        return False
    if isinstance(park.id,int):
        return park.name
    else:
        return False

def parks_exist():
    session = db_session.create_session()
    park = session.query(Park).first()
    if park==None:
        session.close()
        return False
    session.close()
    return True

def populate_parks(filepath=None):
    filepath = os.path.join(os.path.dirname(__file__),'..','park_data') if filepath == None else filepath
    park_list = load_data_from_csv(os.path.join(filepath, 'wi_parks.csv'))

    session = db_session.create_session()
    for park in park_list:
        p = Park()
        p.external_id = park[0]
        p.name = park[1]
        p.region = park[2]
        session.add(p)
    session.commit()
    session.close()
    return True

def get_parks_in_region(region_id, by_ids=False):
    session = db_session.create_session()
    park_list = session.query(Park).filter(Park.region == region_id).all()
    park_dict = {}
    if by_ids == True:
        for park in park_list:
            park_dict[park.id] = park.name
    else:
        for park in park_list:
            park_dict[park.name] = park.id
    session.close()
    return park_dict

def create_URL_from_id(park_id, start_date, end_date):
    park = get_park_from_id(park_id)
    return url_service.set_up_url(start_date, end_date, None, park.external_id)

def create_link_from_id(park_id, start_date, end_date):
    park = get_park_from_id(park_id)
    url = create_URL_from_id(park, start_date, end_date)
    return f"""<a href="{url}">{park.name}</a>"""


#                                      ,@@@@@#@@@@@@@@.@@*
#                            #@@%                            *&@@@*
#                      .@@@                                        @
#                     &&                                             &*
#                       @                                          @
#           *@,         @                                          @
#      ,@&      /@@@&%@@                                            @@&,
#    @                                                                   .,,,#@@@&(@@.
#    @                 *%%%@@.                                                         @
#   ,&                (#%@@*#@                                                         @
#     @              #@%@#&&@@        .@@#/@  @(@/  Eric's Sweet .@@#(@  @/@, .@       @
#     @                 (@@@@## ,%&   .@ %@@ @@##@* @@  @% @@ &@ .@ &@@ @@##@,.@..    (@
#    .&                   #@#@@@@@@                                                   @
#    .@             /#*@@@#@ @@@@@@              @@ @# & Park,@.(@ @(                @
#      &          .&(((@&@@@@@@*@@@#             @@,  %@@@@  @.@@ (@(@.               &
#      @           (#@@&@@@@,#(#@@                                                   (&
#      *@          &@ %#@@@@@&.@&##(#&     @@@@ @@@@ %@ Services @@  @@@@ @@@@       *&
#       ,(       %@@@#%#(##@@@@@@@@@@@     ,@@@ @@@@ %@@@   @ @  &@ @#    @@@&       @
#       @.      .  &@@@@@@@@,.(@@@@        %&%  %%%% (% ,%  *%*  #%   %&# %%%%      @
#       @       .&#@@@@@@@@@  .@@                        @@(@,                    %/
#       @       (&@@@@&@@@@@@@@.@@@@@#              /@.       ,&                  %,
#        /@        ##@@@@@@@@* &@@@@@@     @@    /  ,    &       .@.               @
#          @    .@@*@@@  @@@ .@@@&&##%@@@,  ,&%  * , *@@@@   &%  ,   (@           &/
#          @        #(&&(@@@@@@@@@@#@&@@     @%%#(  &%##&@@ /,@&#, .     @%       @
#          ,%   .. .&%@@@@@@@@@@@@@@@%@@(/&@@#//##@@%/*,*,/#/((%@@@/  %&*   @   *@
#           @ &@(. &@@@@@@@@@@@@@@@@#&@@@@##%##%&%##&@%(%@@@@@#*,/#&@@@%/,,,., @
#           @#%&&@@@@@@@@@@@@@%@@%.,#&&&( %.,,,,.,/&@#.*@*&%/ .*&@@#,.,*&@&&@@@.
#            @#(/*..,*,.@@@@@*,(@&#,,##&%&@@.**&&,,&(,%#,*%&,.%@/,,*&@(/#####@
#             @%&#&%%&,.@@@@@,...(/@@...&&@@@.*&,,%*.%, /#@@/@(,@&*@&%@.*/(%@
#              @#,  @@@@@@@@@#@@&&@@#@/((/@/@@, /&,..(*,&(@@@@@@@@@@@@@@/@@
#                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(.,(&@@@@@@@%&#%@&&%#@&
#                 .@@@&&@@@@@@@@@&@@@@@@@@@#@@@@@@@@@@@@@@@&&@@@@@&#/*@&
#                   *%@@@@%%@@@@@@@@%@@@@&%%@@@@@&%@%%&#%@@@@@@@%&@@@@@
#                     @%@@@@@#(@@&%%&@@@       (@@@@@@@@@#&%%*&@@&#@@@
#                      .@&%#@@@&,(@   %               %@@%(@/.#@@%%@@
#                       .@&&@@&(#&& .                 &@@@&/@@%&@@@.
#                          @%#/%@@%%                  #./&@&%@@%@,
#                           (@(,*/%@&%%*,*//.  @%#*%@,@@&,%@##@@.
#                            /@@@%(*,.   .,*&%*/(*. (#/&@@&%@.
#                              .@&(#&@@@@@@@@@&/,,,.,##@&&@.
#                                *@@@@@@@@@@@&@@%@@@@@@@@@
#                                  %@(**/(/***//%@@@@@@(
#                                     *@&%%##%&@&%@@,
#                                         ,@@@@@@@
