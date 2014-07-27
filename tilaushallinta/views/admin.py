#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.view import view_config

@view_config(route_name='admin', renderer='../templates/admin.pt')
def view_admin(request):
    return {}