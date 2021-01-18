from data.park import Park  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
from infrastructure.load_data_from_csv import load_data_from_csv  # pylint: disable = import-error
import os

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
    session.close()
    if park == None:
        return False
    if isinstance(park.id,int):
        return park.id
    else:
        return False

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
        p.name = park[0]
        p.region = park[1]
        session.add(p)
    session.commit()
    session.close()
    return True

def get_parks_in_region(region_id):
    session = db_session.create_session()
    park_list = session.query(Park).filter(Park.region == region_id).all()
    park_dict = {}
    for park in park_list:
        park_dict[park.name] = park.id
    return park_dict

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
