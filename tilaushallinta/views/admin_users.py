#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import DBSession, User
from datetime import datetime

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

err_missing_name = "Käyttäjän nimi puuttuu"
err_missing_email = "Käyttäjän sähköpostiosoite puuttuu"
err_missing_pass = "Käyttäjän salasana puuttuu"

@view_config(route_name='admin_users_new', renderer='../templates/admin_users_new.pt')
def view_admin_users_new(request):
    errors = ""

    post = request.POST
    keys = post.keys()
    if 'data' in keys:
        if not 'name' in keys or len(post['name']) == 0:
            errors += err_missing_name
        if not 'email' in keys or len(post['email']) == 0:
            errors += err_missing_email
        if not 'password' in keys or len(post['password']) == 0:
            errors += err_missing_pass

        if 'admin' in keys:
            admin = True
        else:
            admin = False

        if not errors:
            next_id = 0
            if DBSession.query(User).count() > 0:
                next_id = DBSession.query(User).order_by(User.id.desc()).first().id+1

            user = User(id=next_id, date=datetime.now(),
                        email=post['email'], name=post['name'],
                        admin=admin)
            user.set_password(post['password'])

            DBSession.add(user)

            return HTTPFound(request.route_url('admin_users'))
        else:
            return {'errors': errors}

    return {}


@view_config(route_name='admin_users_edit', renderer='../templates/admin_users_edit.pt')
def view_admin_users_edit(request):
    user = DBSession.query(User).filter_by(id=request.matchdict['id']).order_by(User.date.desc()).first()

    locked = True if user.email == "admin" else False
    return {'user': user, 'locked': locked}