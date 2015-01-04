#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

def configure_routes(config):

    config.add_route('home', '/')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('order_new', '/tilaukset/uusi')
    config.add_route('order_submit', '/tilaukset/submit')

    config.add_route('order_list', '/tilaukset')
    config.add_route('order_details', '/tilaukset/{id}')
    config.add_route('order_summary', '/tilaukset/{id}/yhteenveto')

    config.add_route('update_tilaaja', '/update/tilaaja/{id}')
    config.add_route('update_kohde', '/update/kohde/{id}')

    config.add_route('order_setstate', '/tilaukset/{id}/setstate')

    config.add_route('kohteet_list', '/kohteet')
    config.add_route('kohteet_details', '/kohteet/{id}')

    config.add_route('json_tilaajat', '/json/tilaajat')
    config.add_route('json_kohteet', '/json/kohteet')

    config.add_route('vkk_new', '/vkkt/uusi')
    config.add_route('vkk_submit', '/vkkt/submit')
    config.add_route('vkk_list', '/vkkt')
    config.add_route('vkk_details', '/vkkt/{id}')

    config.add_route('show_text', '/texts/{name}')

    config.add_route('user_profile', '/profiili')

    config.add_route('admin', '/admin')
    config.add_route('admin_hintaluokat', '/admin/hintaluokat')
    config.add_route('admin_users', '/admin/users')
    config.add_route('admin_users_new', '/admin/users/new')
    config.add_route('admin_users_edit', '/admin/users/{id}')

    config.add_route('admin_db', '/admin/db')
    config.add_route('admin_db_model', '/admin/db/{name}')
    config.add_route('admin_db_row', '/admin/db/{name}/{id}')

    config.add_route('admin_assertfail', '/admin/assertfail')
