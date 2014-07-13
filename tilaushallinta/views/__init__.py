#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

##########################################################
# Split views into different sub-files based on category #
##########################################################

from .common import add_login_status
from .db_viewer import view_db, view_db_model, view_db_model_row
from .home import view_home
from .login_management import view_login, view_logout
from .order import view_tilaus, view_tilaus_submit
from .order_list_and_details import view_tilaukset_list, view_order_details
from .utils import view_show_text
from .admin import view_admin