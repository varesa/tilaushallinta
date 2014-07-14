#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from pyramid.view import view_config
from ..models import DBSession, User

@view_config(route_name='admin_users', renderer='../templates/admin_users.pt')
def view_admin_users(request):
    users = DBSession.query(User).order_by(User.uuid.desc()).all()

    latest = []
    lastid = None

    for user in users:
        if user.id is not lastid:
            latest.append(user)
            lastid = user.id
    latest.reverse()
    return {'users': latest}


@view_config(route_name='admin_users_new', renderer='../templates/admin_users_new.pt')
def view_admin_users_new(request):
    return {}


@view_config(route_name='admin_users_edit', renderer='../templates/admin_users_edit.pt')
def view_admin_users_edit(request):
    return {}