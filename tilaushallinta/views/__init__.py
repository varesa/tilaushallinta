#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

##########################################################
# Split views into different sub-files based on category #
##########################################################

from .common import add_login_status
from .admin_db import view_admin_db, view_admin_db_model, view_admin_db_row
from .home import view_home
from .login_management import view_login, view_logout
from .order_new import view_order_new, view_order_submit
from .order_list_and_details import view_tilaukset_list, view_order_details
from .show_text import view_show_text
from .admin import view_admin
from .admin_users import view_admin_users, view_admin_users_new, view_admin_users_edit
from .admin_assert import view_admin_assertfail
