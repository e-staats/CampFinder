from data.park import Park  # pylint: disable = import-error
import data.db_session as db_session  # pylint: disable = import-error
import os

def get_park_id_from_name(name):
    session = db_session.create_session()
    park = session.query(Park).filter(Park.name == name).first()
    if isinstance(park.id,int):
        return park.id
    else:
        return False


def populate_parks():
    park_dict = get_park_dict()

    session = db_session.create_session()
    for name in park_dict.keys():
        p = Park()
        p.name = name
        p.region = park_dict[name]
        session.add(p)
    session.commit()
    return True


def get_park_dict():
    return {
        "Amnicon Falls": "1",
        "Aztalan": "4",
        "Big Bay": "1",
        "Big Foot Beach": "4",
        "Black River": "2",
        "Blue Mound": "2",
        "Brule River": "1",
        "Brunet Island": "1",
        "Buckhorn": "2",
        "Cadiz Springs": "2",
        "Chippewa Flowage": "1",
        "Chippewa Moraine": "1",
        "Copper Falls": "1",
        "Council Grounds": "3",
        "Devil": "2",
        "Elroy-Sparta": "2",
        "Flambeau River": "1",
        "Glacial Drumlin": "4",
        "Governor Dodge": "2",
        "Governor Earl Peshtigo River": "3",
        "Governor Knowles": "1",
        "Governor Nelson": "2",
        "Governor Thompson": "3",
        "Harrington Beach": "4",
        "Hartman Creek": "3",
        "High Cliff": "3",
        "Interstate": "1",
        "Kettle Moraine - Lapham Peak Unit": "4",
        "Kettle Moraine - Northern Unit": "4",
        "Kettle Moraine - Pike Lake Unit": "4",
        "Kettle Moraine - Southern Unit": "4",
        "Kohler-Andrae": "4",
        "Lake Kegonsa": "2",
        "Lake Wissota": "1",
        "Lakeshore": "4",
        "Mackenzie Center": "2",
        "Menominee River": "3",
        "Merrick": "2",
        "Mill Bluff": "2",
        "Mirror Lake": "2",
        "Nelson Dewey": "2",
        "New Glarus Woods": "2",
        "Newport": "3",
        "Northern Highland - American Legion": "3",
        "Pattison": "1",
        "Peninsula": "3",
        "Perrot": "2",
        "Point Beach": "3",
        "Potawatomi": "3",
        "Rib Mountain": "3",
        "Richard Bong": "4",
        "Roche-A-Cri": "2",
        "Rock Island": "3",
        "Rocky Arbor": "2",
        "Straight Lake": "1",
        "Tower Hill": "2",
        "Turtle Flambeau": "1",
        "Whitefish Dunes": "3",
        "Wildcat Mountain": "2",
        "Willow Flowage": "3",
        "Willow River": "1",
        "Wyalusing": "2",
        "Yellowstone Lake": "2",
    }


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
