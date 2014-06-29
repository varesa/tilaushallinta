#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.view import view_config

@view_config(route_name='login', renderer='../templates/login.pt')
def view_login(request):
    return {}

@view_config(route_name='logout', renderer='../templates/login.pt')
def view_logout(request):
    return {}

