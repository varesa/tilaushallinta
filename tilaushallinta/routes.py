#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

def configure_routes(config):

    config.add_route('home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('order_list', '/tilaukset')
    config.add_route('order_details', '/tilaukset/{id}')

    config.add_route('show_text', '/texts/{name}')

    config.add_route('tilaus', '/tilaus')
    config.add_route('tilaus_submit', '/tilaus_submit')

    config.add_route('admin', '/admin')
    config.add_route('admin_users', '/admin/users')

    config.add_route('admin_db', '/admin/db')
    config.add_route('admin_db_model', '/admin/db/{name}')
    config.add_route('admin_db_row', '/admin/db/{name}/{id}')

    config.add_route('assertfail', '/assertfail')